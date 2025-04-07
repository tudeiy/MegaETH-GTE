from colorama import Fore, init
from web3 import Web3
from ..config import GTE_TOKENS, BASE_TOKEN, ERC20_ABI

init(autoreset=True)

def print_header():
    banner = """
    ██╗    ██╗ ██╗ ███╗   ██╗ ███████╗ ███╗   ██╗ ██╗ ██████╗  
    ██║    ██║ ██║ ████╗  ██║ ██╔════╝ ████╗  ██║ ██║ ██╔══██╗ 
    ██║ █╗ ██║ ██║ ██╔██╗ ██║ ███████╗ ██╔██╗ ██║ ██║ ██████╔╝ 
    ██║███╗██║ ██║ ██║╚██╗██║ ╚════██║ ██║╚██╗██║ ██║ ██╔═══╝  
    ╚███╔███╔╝ ██║ ██║ ╚████║ ███████║ ██║ ╚████║ ██║ ██║      
     ╚══╝╚══╝  ╚═╝ ╚═╝  ╚═══╝ ╚══════╝ ╚═╝  ╚═══╝ ╚═╝ ╚═╝      
    """
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    lines = banner.split('\n')
    for i, line in enumerate(lines):
        if line.strip():
            print(colors[i % len(colors)] + line)
    print(Fore.WHITE + "\n" + "=" * 50)
    print(Fore.CYAN + "🚀  MegaETH-GTE AUTO SWAP - WINSNIP")
    print(Fore.YELLOW + "🔥 Join Telegram: " + Fore.CYAN + "@winsnip")
    print(Fore.WHITE + "=" * 50 + "\n")

def get_private_key():
    while True:
        pk = input("🔑 Masukkan Private Key (tanpa '0x'): ").strip()
        if len(pk) != 64:
            print("❌ Private Key harus 64 karakter!")
            continue
        try:
            int(pk, 16)
            return pk
        except ValueError:
            print("❌ Format Private Key tidak valid!")

def get_token_balance(web3, account, symbol):
    data = GTE_TOKENS[symbol]
    if symbol == BASE_TOKEN:
        balance = web3.eth.get_balance(account.address)
    else:
        contract = web3.eth.contract(address=Web3.to_checksum_address(data["address"]), abi=ERC20_ABI)
        balance = contract.functions.balanceOf(account.address).call()
    return balance / (10 ** data["decimals"])

def show_balances(web3, account):
    print(f"\n📊 SALDO WALLET: {account.address}")
    for token in GTE_TOKENS:
        amount = get_token_balance(web3, account, token)
        print(f"{token.ljust(12)}: {amount:.6f}")
    print()