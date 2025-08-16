import unittest
from unittest.mock import patch
import datetime

# Assume accounts.py is in the same directory and contains the classes and functions to be tested.
# To run this file standalone for verification, you would need to have accounts.py present.
from accounts import (
    Account,
    get_share_price,
    InsufficientFundsError,
    InsufficientSharesError,
    InvalidSymbolError
)


class TestHelperFunctions(unittest.TestCase):
    """Tests for helper functions like get_share_price."""

    def test_get_share_price_valid(self):
        """Test retrieving price for a valid, uppercase symbol."""
        self.assertEqual(get_share_price('AAPL'), 150.00)
        self.assertEqual(get_share_price('GOOGL'), 2500.00)

    def test_get_share_price_case_insensitive(self):
        """Test that symbol lookup is case-insensitive."""
        self.assertEqual(get_share_price('tsla'), 700.00)

    def test_get_share_price_invalid(self):
        """Test that an invalid symbol raises InvalidSymbolError."""
        with self.assertRaises(InvalidSymbolError):
            get_share_price('INVALID')


class TestAccount(unittest.TestCase):
    """Test suite for the Account class."""

    def setUp(self):
        """Set up a new Account instance before each test."""
        self.account = Account(user_id='testuser123')

    def test_initialization(self):
        """Test the initial state of a new account."""
        self.assertEqual(self.account._user_id, 'testuser123')
        self.assertEqual(self.account.get_cash_balance(), 0.0)
        self.assertEqual(self.account._total_deposits, 0.0)
        self.assertEqual(self.account.get_holdings(), {})
        self.assertEqual(self.account.get_transaction_history(), [])

    def test_deposit_positive_amount(self):
        """Test a successful deposit."""
        self.account.deposit(5000.50)
        self.assertEqual(self.account.get_cash_balance(), 5000.50)
        self.assertEqual(self.account._total_deposits, 5000.50)
        transactions = self.account.get_transaction_history()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['type'], 'DEPOSIT')
        self.assertEqual(transactions[0]['total_value'], 5000.50)

    def test_deposit_invalid_amount(self):
        """Test depositing a zero or negative amount."""
        with self.assertRaisesRegex(ValueError, "Deposit amount must be a positive number."):
            self.account.deposit(0)
        with self.assertRaisesRegex(ValueError, "Deposit amount must be a positive number."):
            self.account.deposit(-100)
        self.assertEqual(self.account.get_cash_balance(), 0.0)

    def test_withdraw_successful(self):
        """Test a successful withdrawal."""
        self.account.deposit(1000)
        self.account.withdraw(250)
        self.assertEqual(self.account.get_cash_balance(), 750)
        self.assertEqual(self.account._total_deposits, 1000)  # Should not change on withdrawal
        transactions = self.account.get_transaction_history()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[1]['type'], 'WITHDRAW')
        self.assertEqual(transactions[1]['total_value'], 250)

    def test_withdraw_insufficient_funds(self):
        """Test withdrawing more than the available balance."""
        self.account.deposit(100)
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(100.01)
        self.assertEqual(self.account.get_cash_balance(), 100)  # Balance should be unchanged

    def test_withdraw_invalid_amount(self):
        """Test withdrawing a zero or negative amount."""
        self.account.deposit(100)
        with self.assertRaisesRegex(ValueError, "Withdrawal amount must be a positive number."):
            self.account.withdraw(0)
        with self.assertRaisesRegex(ValueError, "Withdrawal amount must be a positive number."):
            self.account.withdraw(-50)
        self.assertEqual(self.account.get_cash_balance(), 100)  # Balance should be unchanged

    @patch('accounts.get_share_price', return_value=150.00)
    def test_buy_shares_successful(self, mock_get_price):
        """Test a successful share purchase."""
        self.account.deposit(1000)
        self.account.buy_shares('AAPL', 5)

        mock_get_price.assert_called_once_with('AAPL')
        self.assertEqual(self.account.get_cash_balance(), 1000 - (150 * 5))
        self.assertEqual(self.account.get_holdings(), {'AAPL': 5})

        transactions = self.account.get_transaction_history()
        self.assertEqual(len(transactions), 2)
        buy_tx = transactions[1]
        self.assertEqual(buy_tx['type'], 'BUY')
        self.assertEqual(buy_tx['symbol'], 'AAPL')
        self.assertEqual(buy_tx['quantity'], 5)
        self.assertEqual(buy_tx['price_per_share'], 150.00)
        self.assertEqual(buy_tx['total_value'], 750.00)

    @patch('accounts.get_share_price', return_value=700.00)
    def test_buy_shares_insufficient_funds(self, mock_get_price):
        """Test buying shares with insufficient cash."""
        self.account.deposit(1000)
        with self.assertRaises(InsufficientFundsError):
            self.account.buy_shares('TSLA', 2)  # Cost = 1400

        self.assertEqual(self.account.get_cash_balance(), 1000)  # Unchanged
        self.assertEqual(self.account.get_holdings(), {})  # Unchanged

    def test_buy_shares_invalid_quantity(self):
        """Test buying with zero, negative, or non-integer quantity."""
        self.account.deposit(1000)
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.buy_shares('AAPL', 0)
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.buy_shares('AAPL', -1)
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.buy_shares('AAPL', 1.5)

    def test_buy_shares_invalid_symbol(self):
        """Test buying shares of an invalid symbol."""
        self.account.deposit(1000)
        with self.assertRaises(InvalidSymbolError):
            self.account.buy_shares('FAKE', 10)

    @patch('accounts.get_share_price', return_value=150.00)
    def test_sell_shares_successful(self, mock_get_price):
        """Test a successful share sale."""
        # Setup: Manually add holdings and set cash for isolated test
        self.account._cash_balance = 100.0
        self.account._holdings = {'AAPL': 10}

        self.account.sell_shares('aapl', 4)  # Test case-insensitivity
        mock_get_price.assert_called_once_with('AAPL')
        self.assertEqual(self.account.get_cash_balance(), 100 + (150 * 4))
        self.assertEqual(self.account.get_holdings(), {'AAPL': 6})

        transactions = self.account.get_transaction_history()
        self.assertEqual(len(transactions), 1)
        sell_tx = transactions[0]
        self.assertEqual(sell_tx['type'], 'SELL')
        self.assertEqual(sell_tx['symbol'], 'AAPL')
        self.assertEqual(sell_tx['quantity'], 4)
        self.assertEqual(sell_tx['price_per_share'], 150.00)
        self.assertEqual(sell_tx['total_value'], 600.00)

    @patch('accounts.get_share_price', return_value=150.00)
    def test_sell_all_shares(self, mock_get_price):
        """Test that selling all shares of a stock removes it from holdings."""
        self.account._holdings = {'AAPL': 5, 'GOOGL': 2}
        self.account._cash_balance = 0

        self.account.sell_shares('AAPL', 5)
        self.assertEqual(self.account.get_cash_balance(), 750)
        self.assertEqual(self.account.get_holdings(), {'GOOGL': 2})  # AAPL should be gone

    def test_sell_shares_insufficient_shares(self):
        """Test selling more shares than owned."""
        self.account._holdings = {'TSLA': 5}
        with self.assertRaises(InsufficientSharesError):
            self.account.sell_shares('TSLA', 6)
        with self.assertRaises(InsufficientSharesError):
            self.account.sell_shares('AAPL', 1)  # Don't own any
        self.assertEqual(self.account.get_holdings(), {'TSLA': 5})  # Unchanged

    def test_sell_shares_invalid_quantity(self):
        """Test selling with zero, negative, or non-integer quantity."""
        self.account._holdings = {'TSLA': 5}
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.sell_shares('TSLA', 0)
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.sell_shares('TSLA', -1)
        with self.assertRaisesRegex(ValueError, "Quantity must be a positive integer."):
            self.account.sell_shares('TSLA', 1.5)

    def test_getters_return_copies(self):
        """Test that getter methods for collections return copies, not references."""
        self.account.deposit(100)
        self.account._holdings = {'AAPL': 10}

        # Test get_holdings()
        holdings_copy = self.account.get_holdings()
        holdings_copy['NEW'] = 99
        self.assertNotEqual(holdings_copy, self.account.get_holdings())
        self.assertNotIn('NEW', self.account.get_holdings())

        # Test get_transaction_history()
        transactions_copy = self.account.get_transaction_history()
        transactions_copy.append({'new': 'transaction'})
        self.assertNotEqual(transactions_copy, self.account.get_transaction_history())
        self.assertEqual(len(self.account.get_transaction_history()), 1)

    @patch('accounts.get_share_price')
    def test_get_portfolio_value(self, mock_get_price):
        """Test the calculation of total portfolio value."""
        # Mock prices for multiple stocks
        mock_get_price.side_effect = lambda symbol: {'AAPL': 150.0, 'TSLA': 700.0}[symbol]

        self.account.deposit(1000)
        self.account._holdings = {'AAPL': 10, 'TSLA': 2}
        # cash + (10 * 150) + (2 * 700) = 1000 + 1500 + 1400 = 3900
        expected_value = 1000.0 + (10 * 150.0) + (2 * 700.0)
        self.assertEqual(self.account.get_portfolio_value(), expected_value)

    @patch('accounts.get_share_price')
    def test_get_profit_loss(self, mock_get_price):
        """Test the calculation of profit and loss."""
        # Mock prices
        mock_get_price.side_effect = lambda symbol: {'AAPL': 150.0}[symbol]

        self.account.deposit(2000)
        # At this point, portfolio value is 2000, deposits are 2000. P/L = 0
        self.assertEqual(self.account.get_profit_loss(), 0.0)

        # Manually set up state after a hypothetical buy to simplify test
        self.account._cash_balance = 500  # 2000 deposit - 1500 cost
        self.account._holdings = {'AAPL': 10}
        self.account._total_deposits = 2000 # Total deposits remains the same

        # Portfolio value = 500 cash + (10 * 150) = 2000. P/L = 2000 - 2000 = 0
        self.assertEqual(self.account.get_profit_loss(), 0.0)

        # Now, let's say the price of AAPL goes up
        mock_get_price.side_effect = lambda symbol: {'AAPL': 160.0}[symbol]
        # Portfolio value = 500 cash + (10 * 160) = 2100. P/L = 2100 - 2000 = 100
        self.assertEqual(self.account.get_profit_loss(), 100.0)

        # Now, let's say the price of AAPL goes down
        mock_get_price.side_effect = lambda symbol: {'AAPL': 145.0}[symbol]
        # Portfolio value = 500 cash + (10 * 145) = 1950. P/L = 1950 - 2000 = -50
        self.assertEqual(self.account.get_profit_loss(), -50.0)


if __name__ == '__main__':
    unittest.main()