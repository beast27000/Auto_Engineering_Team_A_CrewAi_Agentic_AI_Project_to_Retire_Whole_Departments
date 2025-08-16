# Design Document: Trading Simulation Account Management System

**To:** Backend Developer
**From:** Engineering Lead
**Date:** 2023-10-27
**Subject:** Design for `accounts.py` module

Here is the detailed design for the `accounts.py` module. This module will be a self-contained system for managing a user's trading simulation account. Please adhere to the function signatures, class structure, and logic described below.

The entire system should be implemented within a single Python file named `accounts.py`.

---

## 1. Module Overview (`accounts.py`)

This module provides the `Account` class, which encapsulates all the necessary data and operations for a single user account in a trading simulation. It handles cash deposits/withdrawals, share trading, and reporting. The module is designed to be self-contained and includes custom exceptions for clear error handling and a mock pricing function for immediate testing.

### 1.1. Module Dependencies

The module will use the following standard Python libraries:
- `datetime`: To timestamp transactions.
- `typing`: For type hints (`Dict`, `List`, `Union`).

No external packages are required.

## 2. Custom Exceptions

To provide clear, catchable errors to the calling code (e.g., a UI or an API layer), we will define a set of custom exceptions.

```python
# accounts.py

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
```

## 3. Helper Functions

### `get_share_price(symbol)`

This function simulates an external market data feed. For this implementation, it will return a fixed price for a few predefined stock symbols. If a symbol is not recognized, it should raise an `InvalidSymbolError`.

**Function Signature:**

```python
# accounts.py

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
    # Implementation details:
    # Use a dictionary to store the fixed prices.
    # e.g., {'AAPL': 150.00, 'GOOGL': 2500.00, 'TSLA': 700.00}
    # Look up the symbol (case-insensitive) and return the price.
    # If not found, raise InvalidSymbolError.
```

## 4. Main Class: `Account`

This class represents a single user's account and contains all the logic for managing funds, holdings, and transactions.

**Class Definition:**

```python
# accounts.py

class Account:
    """
    Manages a user's trading account, including cash, holdings, and transactions.
    """
```

### 4.1. Constructor: `__init__`

The constructor initializes a new account. An account starts with a zero balance, no holdings, and an empty transaction history.

**Method Signature:**

```python
    def __init__(self, user_id: str):
        """
        Initializes a new trading account.

        Args:
            user_id: A unique identifier for the account holder.
        """
        # Internal Attributes:
        # self._user_id: str = user_id
        # self._cash_balance: float = 0.0
        # self._total_deposits: float = 0.0
        # self._holdings: Dict[str, int] = {}  # e.g., {'AAPL': 50}
        # self._transactions: List[Dict] = []
```

### 4.2. Cash Management Methods

#### `deposit(amount)`

Adds funds to the account's cash balance.

**Method Signature:**

```python
    def deposit(self, amount: float) -> None:
        """
        Deposits a specified amount of cash into the account.

        Args:
            amount: The amount of cash to deposit. Must be a positive number.

        Raises:
            ValueError: If the amount is not a positive number.
        """
        # Logic:
        # 1. Validate that `amount` is > 0.
        # 2. Add `amount` to `self._cash_balance`.
        # 3. Add `amount` to `self._total_deposits`.
        # 4. Record a 'DEPOSIT' transaction using a helper method.
```

#### `withdraw(amount)`

Removes funds from the account's cash balance.

**Method Signature:**

```python
    def withdraw(self, amount: float) -> None:
        """
        Withdraws a specified amount of cash from the account.

        Args:
            amount: The amount of cash to withdraw. Must be a positive number.

        Raises:
            ValueError: If the amount is not a positive number.
            InsufficientFundsError: If withdrawal amount exceeds cash balance.
        """
        # Logic:
        # 1. Validate that `amount` is > 0.
        # 2. Check if `amount` <= `self._cash_balance`. If not, raise InsufficientFundsError.
        # 3. Subtract `amount` from `self._cash_balance`.
        # 4. Record a 'WITHDRAW' transaction.
```

### 4.3. Trading Methods

#### `buy_shares(symbol, quantity)`

Purchases a specified quantity of shares, deducting the cost from the cash balance.

**Method Signature:**

```python
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
        # Logic:
        # 1. Sanitize symbol (e.g., uppercase).
        # 2. Validate that `quantity` is > 0.
        # 3. Get the share price using `get_share_price(symbol)`.
        # 4. Calculate total cost = price * quantity.
        # 5. Check if `total_cost` <= `self._cash_balance`. If not, raise InsufficientFundsError.
        # 6. Subtract `total_cost` from `self._cash_balance`.
        # 7. Update `self._holdings`. Add `quantity` to the existing count for the symbol.
        # 8. Record a 'BUY' transaction with symbol, quantity, and price per share.
```

#### `sell_shares(symbol, quantity)`

Sells a specified quantity of shares, adding the proceeds to the cash balance.

**Method Signature:**

```python
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
        # Logic:
        # 1. Sanitize symbol (e.g., uppercase).
        # 2. Validate that `quantity` is > 0.
        # 3. Check if `symbol` is in `self._holdings` and if `self._holdings[symbol] >= quantity`. If not, raise InsufficientSharesError.
        # 4. Get the share price using `get_share_price(symbol)`.
        # 5. Calculate total proceeds = price * quantity.
        # 6. Add `total_proceeds` to `self._cash_balance`.
        # 7. Update `self._holdings`. Subtract `quantity` from the count. If the count becomes 0, remove the symbol from the dictionary.
        # 8. Record a 'SELL' transaction.
```

### 4.4. Reporting Methods

These methods provide read-only access to the account's state. They should return copies of mutable objects (like dicts and lists) to prevent external modification of the internal state.

#### `get_portfolio_value()`

Calculates the total current value of the account (cash + value of all holdings).

**Method Signature:**

```python
    def get_portfolio_value(self) -> float:
        """
        Calculates the total value of the portfolio (cash + value of all shares).

        Returns:
            The total portfolio value.
        """
        # Logic:
        # 1. Start with `total_value = self._cash_balance`.
        # 2. Iterate through `self._holdings`.
        # 3. For each symbol and quantity, get the current price and add (price * quantity) to `total_value`.
        # 4. Return `total_value`.
```

#### `get_profit_loss()`

Calculates the total profit or loss relative to the total amount of cash deposited.

**Method Signature:**

```python
    def get_profit_loss(self) -> float:
        """
        Calculates the net profit or loss of the account.

        This is calculated as (current portfolio value - total cash deposited).

        Returns:
            The profit (positive float) or loss (negative float).
        """
        # Logic:
        # 1. Calculate current portfolio value by calling `self.get_portfolio_value()`.
        # 2. Return `portfolio_value - self._total_deposits`.
```

#### `get_transaction_history()`

Returns a list of all transactions performed on the account.

**Method Signature:**

```python
    def get_transaction_history(self) -> List[Dict]:
        """
        Returns a copy of the list of all transactions for the account.

        Returns:
            A list of dictionaries, where each dictionary represents a transaction.
        """
        # Logic:
        # Return a copy of `self._transactions` (e.g., `self._transactions.copy()`).
```

#### `get_holdings()`

Returns a dictionary of all shares currently held.

**Method Signature:**

```python
    def get_holdings(self) -> Dict[str, int]:
        """
        Returns a copy of the user's current share holdings.

        Returns:
            A dictionary mapping symbols to quantities.
        """
        # Logic:
        # Return a copy of `self._holdings` (e.g., `self._holdings.copy()`).
```

#### `get_cash_balance()`

Returns the current cash balance.

**Method Signature:**

```python
    def get_cash_balance(self) -> float:
        """
        Returns the current cash balance.

        Returns:
            The amount of cash in the account.
        """
        # Logic:
        # Return `self._cash_balance`.
```

### 4.5. Internal Helper Methods

Consider creating a private helper method to standardize transaction logging.

#### `_record_transaction(...)`

This private method will be called by `deposit`, `withdraw`, `buy_shares`, and `sell_shares` to create a consistent transaction record.

**Example Transaction Record Format (Dictionary):**
```python
{
    'timestamp': datetime.datetime.now(),
    'type': 'BUY',  # 'SELL', 'DEPOSIT', 'WITHDRAW'
    'symbol': 'AAPL',  # (or None for cash transactions)
    'quantity': 10,    # (or None for cash transactions)
    'price_per_share': 150.00, # (or None for cash transactions)
    'total_value': 1500.00 # For buy/sell, this is cost/proceeds. For cash, this is the amount.
}
```