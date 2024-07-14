from fetchers import fetch_transactions

# Function to get latest transactions
def get_transactions():
    transactions = fetch_transactions()
    if transactions:
        transactions_message = "\n\n".join(
            [f"Transaction ID: {txn['txnId']}\nType: {txn['type']}\nAmount: {txn['amount0']} at ${txn['priceUsd']} each" for txn in transactions[:5]]
        )  # Show top 5 transactions
        return transactions_message
    else:
        return "Failed to fetch transactions."
