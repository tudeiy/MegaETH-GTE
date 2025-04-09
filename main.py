import time
import random
from web3 import Web3
from eth_account import Account
from core.config import RPC_URL, ROUTER_ADDRESS, ROUTER_ABI, BASE_TOKEN, GTE_TOKENS
from core.utils.utils import print_header, get_private_key, show_balances, get_token_balance
from core.swap.swap import swap

def main():
    print_header()
    private_key = get_private_key()
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    account = Account.from_key(private_key)
    router = web3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI)
    show_balances(web3, account)

    try:
        rounds = int(input("🔁 Berapa kali mau swap bolak-balik? "))
        percent = float(input("💸 Berapa persen dari saldo yang mau diswap tiap kali (contoh: 30)? "))
    except ValueError:
        print("❌ Input tidak valid. Harus angka.")
        return

    if not 0 < percent <= 100:
        print("❌ Persen harus antara 0-100.")
        return

    swap_fraction = percent / 100
    tokens = [k for k in GTE_TOKENS if k != BASE_TOKEN]

    for i in range(rounds):
        print(f"\n🔁 SWAP PUTARAN KE-{i+1}")
        show_balances(web3, account)

        for token in tokens:
            amt = get_token_balance(web3, account, BASE_TOKEN)
            if amt > 0:
                swap(web3, account, router, BASE_TOKEN, token, amt * swap_fraction)
                time.sleep(random.uniform(3, 8))

        for token in tokens:
            amt = get_token_balance(web3, account, token)
            if amt > 0:
                swap(web3, account, router, token, BASE_TOKEN, amt)
                time.sleep(random.uniform(3, 8))

    print(f"\n✅ SEMUA SWAP PUTARAN {rounds} SELESAI.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⛔ Dibatalkan oleh user.")
