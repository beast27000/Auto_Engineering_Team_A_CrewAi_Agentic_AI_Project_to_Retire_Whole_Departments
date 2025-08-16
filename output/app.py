import gradio as gr
from accounts import Account, TradingError

# --- 1. Global State Setup ---
# Initialize a single account instance for the demo user.
# This object will persist for the lifetime of the Gradio app.
account = Account(user_id="demo_user")

# Pre-fund the account for a better demonstration experience.
try:
    if account.get_cash_balance() == 0:
        account.deposit(10000)
except TradingError:
    # This will not be hit with a hardcoded positive value
    pass


# --- 2. Data Formatting Helpers ---
# These functions prepare data from the backend for display in Gradio components.

def format_holdings_for_df():
    """Formats the holdings dictionary into a list for a Gradio DataFrame."""
    holdings = account.get_holdings()
    if not holdings:
        return []
    # Convert {'AAPL': 10, 'TSLA': 5} to [['AAPL', 10], ['TSLA', 5]]
    return [[symbol, quantity] for symbol, quantity in holdings.items()]

def format_transactions_for_df():
    """Formats the transaction list into a list of lists for a Gradio DataFrame."""
    history = account.get_transaction_history()
    formatted_history = []
    # Reverse the list to show the most recent transactions first
    for t in reversed(history):
        formatted_history.append([
            t['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            t['type'],
            t.get('symbol', 'N/A'),
            t.get('quantity', 'N/A'),
            f"${t['price_per_share']:.2f}" if t.get('price_per_share') is not None else "N/A",
            f"${t['total_value']:.2f}"
        ])
    return formatted_history

def get_all_report_updates():
    """
    A single function to fetch all dynamic data points from the account.
    Returns a tuple in a specific order to update multiple Gradio components at once.
    """
    return (
        account.get_cash_balance(),
        account.get_portfolio_value(),
        account.get_profit_loss(),
        format_holdings_for_df(),
        format_transactions_for_df()
    )


# --- 3. UI Action Handlers ---
# These wrapper functions connect Gradio inputs to the backend account methods.
# They handle exceptions gracefully and return all necessary updates for the UI.

def handle_deposit(amount):
    """Wrapper for the deposit action."""
    try:
        if amount is None or amount <= 0:
            raise ValueError("Deposit amount must be a positive number.")
        account.deposit(float(amount))
        message = f"Successfully deposited ${amount:,.2f}."
    except (TradingError, ValueError) as e:
        message = f"Error: {e}"
    
    updates = get_all_report_updates()
    return (message,) + updates

def handle_withdraw(amount):
    """Wrapper for the withdraw action."""
    try:
        if amount is None or amount <= 0:
            raise ValueError("Withdrawal amount must be a positive number.")
        account.withdraw(float(amount))
        message = f"Successfully withdrew ${amount:,.2f}."
    except (TradingError, ValueError) as e:
        message = f"Error: {e}"

    updates = get_all_report_updates()
    return (message,) + updates

def handle_buy(symbol, quantity):
    """Wrapper for the buy_shares action."""
    try:
        if not all([symbol, quantity]):
            raise ValueError("Symbol and quantity must be provided.")
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        account.buy_shares(symbol, int(quantity))
        message = f"Successfully bought {int(quantity)} share(s) of {symbol}."
    except (TradingError, ValueError, TypeError) as e:
        message = f"Error: {e}"
        
    updates = get_all_report_updates()
    return (message,) + updates

def handle_sell(symbol, quantity):
    """Wrapper for the sell_shares action."""
    try:
        if not all([symbol, quantity]):
            raise ValueError("Symbol and quantity must be provided.")
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        account.sell_shares(symbol, int(quantity))
        message = f"Successfully sold {int(quantity)} share(s) of {symbol}."
    except (TradingError, ValueError, TypeError) as e:
        message = f"Error: {e}"

    updates = get_all_report_updates()
    return (message,) + updates

# --- 4. Gradio UI Definition ---

with gr.Blocks(title="Trading Account Demo", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Trading Account Simulator")
    gr.Markdown("A simple UI to demonstrate a backend trading account module.")

    # --- Define Shared Components ---
    # These components display data that is updated by actions across all tabs.
    # They are defined outside the tabs to be easily accessible.
    with gr.Row():
        cash_balance_display = gr.Number(
            label="Cash Balance ($)", interactive=False
        )
        portfolio_value_display = gr.Number(
            label="Total Portfolio Value ($)", interactive=False
        )
        pnl_display = gr.Number(
            label="Profit / Loss ($)", interactive=False
        )

    # This status box will be used by multiple tabs to show action results.
    status_box = gr.Textbox(label="Status", interactive=False, lines=2)
    
    # List of all components that need to be updated after an action.
    # The order must match the tuple returned by the handler functions.
    shared_outputs = [
        status_box,
        cash_balance_display,
        portfolio_value_display,
        pnl_display,
        # The DataFrame components are defined below but referenced here.
    ]

    with gr.Tabs():
        # --- Tab 1: Account Management ---
        with gr.TabItem("Account Management"):
            gr.Markdown("## Manage Your Cash Balance")
            with gr.Row():
                with gr.Column():
                    deposit_amount = gr.Number(label="Deposit Amount")
                    deposit_button = gr.Button("Deposit", variant="primary")
                with gr.Column():
                    withdraw_amount = gr.Number(label="Withdraw Amount")
                    withdraw_button = gr.Button("Withdraw")

        # --- Tab 2: Trading ---
        with gr.TabItem("Trading"):
            gr.Markdown("## Buy and Sell Shares")
            # Stock symbols are hardcoded based on the backend's `get_share_price` function.
            trade_symbol = gr.Dropdown(
                ['AAPL', 'GOOGL', 'TSLA'], label="Stock Symbol"
            )
            trade_quantity = gr.Number(label="Quantity", minimum=1, step=1)
            with gr.Row():
                buy_button = gr.Button("Buy", variant="primary")
                sell_button = gr.Button("Sell")

        # --- Tab 3: Reports ---
        with gr.TabItem("Reports"):
            gr.Markdown("## View Your Portfolio and History")
            refresh_button = gr.Button("Refresh Reports")

            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### Current Holdings")
                    holdings_df = gr.DataFrame(
                        headers=["Symbol", "Quantity"],
                        datatype=["str", "number"],
                        row_count=(5, "dynamic"),
                        col_count=(2, "fixed"),
                    )
                with gr.Column(scale=3):
                    gr.Markdown("### Transaction History")
                    transactions_df = gr.DataFrame(
                        headers=["Timestamp", "Type", "Symbol", "Qty", "Price/Share", "Total Value"],
                        datatype=["str", "str", "str", "number", "str", "str"],
                        row_count=(10, "dynamic"),
                        col_count=(6, "fixed"),
                    )
    
    # --- 5. Connect Components and Handlers ---

    # Append the report DataFrames to the list of shared outputs.
    # This must be done after they are defined.
    shared_outputs.extend([holdings_df, transactions_df])

    # Connect buttons from the "Account Management" tab.
    deposit_button.click(
        fn=handle_deposit,
        inputs=[deposit_amount],
        outputs=shared_outputs
    )
    withdraw_button.click(
        fn=handle_withdraw,
        inputs=[withdraw_amount],
        outputs=shared_outputs
    )

    # Connect buttons from the "Trading" tab.
    buy_button.click(
        fn=handle_buy,
        inputs=[trade_symbol, trade_quantity],
        outputs=shared_outputs
    )
    sell_button.click(
        fn=handle_sell,
        inputs=[trade_symbol, trade_quantity],
        outputs=shared_outputs
    )

    # The refresh button on the "Reports" tab updates everything without a status message.
    # We create a simple wrapper to match the output component list structure.
    def refresh_wrapper():
        message = f"Reports updated at {gr.time('now')}."
        updates = get_all_report_updates()
        return (message,) + updates

    refresh_button.click(
        fn=refresh_wrapper,
        inputs=None,
        outputs=shared_outputs
    )

    # Use demo.load to populate the UI with initial data when the app starts.
    # This provides a better user experience than starting with an empty interface.
    def initial_load_wrapper():
        # On initial load, there's no action, so the status message is neutral.
        message = "Welcome! Account data loaded successfully."
        updates = get_all_report_updates()
        return (message,) + updates
        
    demo.load(
        fn=initial_load_wrapper,
        inputs=None,
        outputs=shared_outputs
    )

# --- 6. Launch the Application ---
if __name__ == "__main__":
    demo.launch()
