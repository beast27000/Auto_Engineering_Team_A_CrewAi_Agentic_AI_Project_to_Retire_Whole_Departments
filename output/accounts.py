import datetime
from typing import Dict, List, Union, Optional

# --- Custom Exceptions ---

class TradingError(Exception):
    """Base exception for all trading-related errors in this module."""
    pass

class InsufficientFundsError(TradingError):
    """Raised when an operation cannot be completed due to insufficient cash."""
    pass

class InsufficientSharesError(TradingError):
    """Raised when a user tries to sell more shares than they own."""
    pass

class InvalidSymbolError(TradingError):
    """Raised when a stock symbol is not recognized by the pricing service."""
    pass

# --- Helper Functions ---

def get_share_price(symbol: str) -> float:
    """
    Retrieves the current market price for a given stock symbol.

    This is a mock implementation for testing purposes.

    Args:
        symbol: The stock symbol (e.g., 'AAPL').

    Returns:
        The current price of the share as a float.

    Raises:
        InvalidSymbolError: If the symbol is not in the predefined list.
    """
    prices = {'AAPL': 150.00, 'GOOGL': 2500.00, 'TSLA': 700.00}
    normalized_symbol = symbol.upper()
    if normalized_symbol not in prices:
        raise InvalidSymbolError(f"Symbol '{symbol}' is not a valid trading symbol.")
    return prices[normalized_symbol]

# --- Main Class ---

class Account:
    """
    Manages a user's trading account, including cash, holdings, and transactions.
    """

    def __init__(self, user_id: str):
        """
        Initializes a new trading account.

        Args:
            user_id: A unique identifier for the account holder.
        """
        self._user_id: str = user_id
        self._cash_balance: float = 0.0
        self._total_deposits: float = 0.0
        self._holdings: Dict[str, int] = {}  # e.g., {'AAPL': 50}
        self._transactions: List[Dict] = []

    def _record_transaction(self,
                            trans_type: str,
                            total_value: float,
                            symbol: Optional[str] = None,
                            quantity: Optional[int] = None,
                            price_per_share: Optional[float] = None) -> None:
        """
        Internal helper to create and log a transaction record.
        """
        transaction = {
            'timestamp': datetime.datetime.now(),
            'type': trans_type,
            'symbol': symbol,
            'quantity': quantity,
            'price_per_share': price_per_share,
            'total_value': total_value
        }
        self._transactions.append(transaction)

    def deposit(self, amount: float) -> None:
        """
        Deposits a specified amount of cash into the account.

        Args:
            amount: The amount of cash to deposit. Must be a positive number.

        Raises:
            ValueError: If the amount is not a positive number.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be a positive number.")
        self._cash_balance += amount
        self._total_deposits += amount
        self._record_transaction('DEPOSIT', total_value=amount)

    def withdraw(self, amount: float) -> None:
        """
        Withdraws a specified amount of cash from the account.

        Args:
            amount: The amount of cash to withdraw. Must be a positive number.

        Raises:
            ValueError: If the amount is not a positive number.
            InsufficientFundsError: If withdrawal amount exceeds cash balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be a positive number.")
        if amount > self._cash_balance:
            raise InsufficientFundsError(f"Cannot withdraw ${amount:.2f}: current balance is ${self._cash_balance:.2f}.")
        self._cash_balance -= amount
        self._record_transaction('WITHDRAW', total_value=amount)

    def buy_shares(self, symbol: str, quantity: int) -> None:
        """
        Buys a quantity of shares for a given symbol.

        Args:
            symbol: The stock symbol to buy.
            quantity: The number of shares to buy. Must be a positive integer.

        Raises:
            ValueError: If quantity is not a positive integer.
            InvalidSymbolError: If the symbol is not valid.
            InsufficientFundsError: If the total cost exceeds the cash balance.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        normalized_symbol = symbol.upper()
        price = get_share_price(normalized_symbol)
        total_cost = price * quantity

        if total_cost > self._cash_balance:
            raise InsufficientFundsError(f"Cannot buy {quantity} of {normalized_symbol}. Cost ${total_cost:.2f} exceeds cash balance of ${self._cash_balance:.2f}.")

        self._cash_balance -= total_cost
        self._holdings[normalized_symbol] = self._holdings.get(normalized_symbol, 0) + quantity
        self._record_transaction('BUY',
                                 symbol=normalized_symbol,
                                 quantity=quantity,
                                 price_per_share=price,
                                 total_value=total_cost)

    def sell_shares(self, symbol: str, quantity: int) -> None:
        """
        Sells a quantity of owned shares for a given symbol.

        Args:
            symbol: The stock symbol to sell.
            quantity: The number of shares to sell. Must be a positive integer.

        Raises:
            ValueError: If quantity is not a positive integer.
            InvalidSymbolError: If the symbol is not valid.
            InsufficientSharesError: If trying to sell more shares than owned.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        normalized_symbol = symbol.upper()
        current_shares = self._holdings.get(normalized_symbol, 0)

        if current_shares < quantity:
            raise InsufficientSharesError(f"Cannot sell {quantity} shares of {normalized_symbol}. You only own {current_shares}.")

        price = get_share_price(normalized_symbol)
        total_proceeds = price * quantity

        self._cash_balance += total_proceeds
        self._holdings[normalized_symbol] -= quantity
        if self._holdings[normalized_symbol] == 0:
            del self._holdings[normalized_symbol]

        self._record_transaction('SELL',
                                 symbol=normalized_symbol,
                                 quantity=quantity,
                                 price_per_share=price,
                                 total_value=total_proceeds)

    def get_portfolio_value(self) -> float:
        """
        Calculates the total value of the portfolio (cash + value of all shares).

        Returns:
            The total portfolio value.
        """
        holdings_value = 0.0
        for symbol, quantity in self._holdings.items():
            try:
                price = get_share_price(symbol)
                holdings_value += price * quantity
            except InvalidSymbolError:
                # In a real system, you'd handle delisted stocks. Here we can ignore.
                pass
        return self._cash_balance + holdings_value

    def get_profit_loss(self) -> float:
        """
        Calculates the net profit or loss of the account.

        This is calculated as (current portfolio value - total cash deposited).

        Returns:
            The profit (positive float) or loss (negative float).
        """
        portfolio_value = self.get_portfolio_value()
        return portfolio_value - self._total_deposits

    def get_transaction_history(self) -> List[Dict]:
        """
        Returns a copy of the list of all transactions for the account.

        Returns:
            A list of dictionaries, where each dictionary represents a transaction.
        """
        return self._transactions.copy()

    def get_holdings(self) -> Dict[str, int]:
        """
        Returns a copy of the user's current share holdings.

        Returns:
            A dictionary mapping symbols to quantities.
        """
        return self._holdings.copy()

    def get_cash_balance(self) -> float:
        """
        Returns the current cash balance.

        Returns:
            The amount of cash in the account.
        """
        return self._cash_balance