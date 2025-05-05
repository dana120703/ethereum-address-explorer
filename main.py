from requests import get
from matplotlib import pyplot as plt
from datetime import datetime

api_key = "API_KEY_HERE"	
base_url = "https://api.etherscan.io/api"
ether_value = 10 ** 18

def make_api_url(module, action, address, **kwargs):
    url = base_url + f"?module={module}&action={action}&address={address}&apikey={api_key}"
    for key, value in kwargs.items():
        url += f"&{key}={value}"
    return url

def get_account_balance(address):
    get_cash_url = make_api_url("account", "balance", address, tag="latest")
    response = get(get_cash_url)
    data = response.json()
    value = int(data["result"]) / ether_value
    return value

def get_transactions(address):
    get_transaction_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
    response = get(get_transaction_url)
    data = response.json()
    return data["result"]

def print_transactions(transactions):
    for tx in transactions:
        timestamp = datetime.fromtimestamp(int(tx['timeStamp']))
        value_eth = int(tx['value']) / ether_value
        print(f"Dato: {timestamp}, Fra: {tx['from']}, Til: {tx['to']}, Verdi: {value_eth:.4f} ETH")

def main():
    address = input("Skriv inn Ethereum-adressen du vil søke opp: ")
    
    balance = get_account_balance(address)
    print(f"\nDagens balanse for {address}: {balance:.4f} ETH")
    
    transactions = get_transactions(address)
    print(f"\nFant {len(transactions)} transaksjoner for denne adressen:")
    print_transactions(transactions)

if __name__ == "__main__":
    main()

