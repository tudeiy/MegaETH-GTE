import time
from web3 import Web3

RPC_URL = "https://carrot.megaeth.com/rpc"
SLIPPAGE = 0.01
GAS_MULTIPLIER = 1.2
BASE_TOKEN = "MegaETH"

ROUTER_ADDRESS = Web3.to_checksum_address("0x96f1b874dd7a3a36acbd92a9df21f0aa8e899eac")

GTE_TOKENS = {
    "WETH": {"address": "0x776401b9BC8aAe31A685731B7147D4445fD9FB19", "decimals": 18},
    "GTE": {"address": "0x9629684df53db9E4484697D0a50C442B2BFa80A8", "decimals": 18},
    "USDC": {"address": "0x8D635C4702bA38B1f1735E8e784C7265dcc0B623", "decimals": 6},
    "tkUSDC": {"address": "0xfAf334E157175fF676911aDcF0964D7f54F2c424", "decimals": 6},
    "MegaETH": {"address": None, "decimals": 18},
    "Kimchizuki": {"address": "0xA626F15D10F2b30AF1fb0d017F20a579500B5029", "decimals": 18},
    "five": {"address": "0xF512886BC6877B0740E8Ca0B3c12bb4cA602B530", "decimals": 18},
    "gte pepe": {"address": "0xBBA08CF5ECE0cC21e1DEB5168746c001B123A756", "decimals": 18},
}

ERC20_ABI = '[{"constant":true,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"amount","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"type":"function"}]'
ROUTER_ABI = '[{"name":"swapExactETHForTokens","type":"function","inputs":[{"name":"amountOutMin","type":"uint256"},{"name":"path","type":"address[]"},{"name":"to","type":"address"},{"name":"deadline","type":"uint256"}],"outputs":[{"name":"amounts","type":"uint256[]"}],"stateMutability":"payable"},{"name":"swapExactTokensForETH","type":"function","inputs":[{"name":"amountIn","type":"uint256"},{"name":"amountOutMin","type":"uint256"},{"name":"path","type":"address[]"},{"name":"to","type":"address"},{"name":"deadline","type":"uint256"}],"outputs":[{"name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable"},{"name":"swapExactTokensForTokens","type":"function","inputs":[{"name":"amountIn","type":"uint256"},{"name":"amountOutMin","type":"uint256"},{"name":"path","type":"address[]"},{"name":"to","type":"address"},{"name":"deadline","type":"uint256"}],"outputs":[{"name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable"}]'