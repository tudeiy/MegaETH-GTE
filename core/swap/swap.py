import time
import random
from web3 import Web3
from ..config import GTE_TOKENS, BASE_TOKEN, ROUTER_ADDRESS, ERC20_ABI, ROUTER_ABI, SLIPPAGE, GAS_MULTIPLIER

def approve(web3, account, token_address, amount):
    contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
    tx = contract.functions.approve(ROUTER_ADDRESS, amount).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 100000,
        'gasPrice': int(web3.eth.gas_price * GAS_MULTIPLIER)
    })
    signed = account.sign_transaction(tx)
    tx_hash = web3.eth.send_raw_transaction(signed.raw_transaction)
    web3.eth.wait_for_transaction_receipt(tx_hash)

def swap(web3, account, router, token_in, token_out, amount_decimal):
    token_in_data = GTE_TOKENS[token_in]
    token_out_data = GTE_TOKENS[token_out]
    deadline = int(time.time()) + 1800
    amount_in = int(amount_decimal * (10 ** token_in_data["decimals"]))
    amount_out_min = int(amount_in * (1 - SLIPPAGE))
    
    max_retries = 3
    retry_count = 0
    while retry_count < max_retries:
        try:
            nonce = web3.eth.get_transaction_count(account.address, 'pending')
            if retry_count > 0:
                nonce += 1

            if token_in == BASE_TOKEN:
                path = [Web3.to_checksum_address(token_out_data["address"])]
                tx = router.functions.swapExactETHForTokens(
                    amount_out_min,
                    path,
                    account.address,
                    deadline
                ).build_transaction({
                    'from': account.address,
                    'value': amount_in,
                    'gas': 300000,
                    'gasPrice': int(web3.eth.gas_price * GAS_MULTIPLIER),
                    'nonce': nonce
                })
            elif token_out == BASE_TOKEN:
                approve(web3, account, token_in_data["address"], amount_in)
                path = [Web3.to_checksum_address(token_in_data["address"])]
                tx = router.functions.swapExactTokensForETH(
                    amount_in,
                    amount_out_min,
                    path,
                    account.address,
                    deadline
                ).build_transaction({
                    'from': account.address,
                    'gas': 300000,
                    'gasPrice': int(web3.eth.gas_price * GAS_MULTIPLIER),
                    'nonce': nonce
                })
            else:
                approve(web3, account, token_in_data["address"], amount_in)
                path = [
                    Web3.to_checksum_address(token_in_data["address"]),
                    Web3.to_checksum_address(token_out_data["address"])
                ]
                tx = router.functions.swapExactTokensForTokens(
                    amount_in,
                    amount_out_min,
                    path,
                    account.address,
                    deadline
                ).build_transaction({
                    'from': account.address,
                    'gas': 300000,
                    'gasPrice': int(web3.eth.gas_price * GAS_MULTIPLIER),
                    'nonce': nonce
                })

            signed = account.sign_transaction(tx)
            tx_hash = web3.eth.send_raw_transaction(signed.raw_transaction)
            print(f"[→] SWAP {token_in} → {token_out} = {amount_decimal:.6f} {token_in}")
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            return receipt
        except Exception as e:
            if "nonce too low" in str(e).lower() or "already known" in str(e).lower():
                print(f"[⚠️] Nonce terlalu rendah, mencoba ulang dengan nonce yang lebih tinggi (percobaan ke-{retry_count + 1})")
                retry_count += 1
                time.sleep(2)
                continue
            raise e
    
    raise Exception("Gagal melakukan swap setelah beberapa kali percobaan")
