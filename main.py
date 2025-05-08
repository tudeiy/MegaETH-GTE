import time
import random
import os
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
from core.config import RPC_URL, ROUTER_ADDRESS, ROUTER_ABI, BASE_TOKEN, GTE_TOKENS
from core.utils.utils import print_header, show_balances, get_token_balance
from core.swap.swap import swap

# Load .env file
load_dotenv()
pk_list = os.getenv("PK_LIST")
if not pk_list:
    print("❌ PK_LIST tidak ditemukan di file .env")
    exit()

private_keys = [pk.strip() for pk in pk_list.split(",") if pk.strip()]

def run_for_account(private_key):
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    account = Account.from_key(private_key)
    router = web3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI)

    print(f"\n====================")
    print(f"👤 Akun: {account.address}")
    print("====================")

    show_balances(web3, account)

    rounds = 1
    percent = random.uniform(10, 30)
    swap_fraction = percent / 100

    print(f"🔁 Swap bolak-balik {rounds}x | Persen swap: {percent:.2f}%")

    tokens = [k for k in GTE_TOKENS if k != BASE_TOKEN]

    for i in range(rounds):
        print(f"\n🔁 SWAP PUTARAN KE-{i+1} untuk {account.address}")
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

    print(f"\n✅ Semua swap selesai untuk {account.address}")

def main():
    print_header()
    for pk in private_keys:
        try:
            run_for_account(pk)
            print("⏳ Delay sebelum akun berikutnya...\n")
            time.sleep(random.uniform(5, 10))
        except Exception as e:
            print(f"❌ Error pada akun dengan PK {pk[:6]}...: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⛔ Dibatalkan oleh user.")
