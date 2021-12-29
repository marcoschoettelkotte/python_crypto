from web3 import Web3
import json
import time
import config
import abi

web3 = Web3(Web3.HTTPProvider(config.bsc))

print(web3.isConnected())

balance = web3.eth.get_balance(config.sender_address)
humanReadable = web3.fromWei(balance, 'ether')

contract = web3.eth.contract(address=config.panRouterContractAddress, abi=abi.panabi)

tokenToBuy = web3.toChecksumAddress(config.buyAddress) # buyed address
spend = web3.toChecksumAddress(config.wbnb) # WBNB address

nonce = web3.eth.get_transaction_count(config.sender_address)
print(nonce)
start = time.time()

amount = 1
restAmount = amount * 0.95
taxAmount = amount - restAmount

#tax pancake
tx_tax = {
    'nonce': nonce,
    'to': config.taxesAddress,
    'value': web3.toWei(taxAmount, 'ether'),
    'gas': 250000,
    'gasPrice': web3.toWei('10', 'gwei'),
}

# buy pancake
pancakeswap2_txn = contract.functions.swapExactETHForTokens(
    0,
    [spend, tokenToBuy],
    config.sender_address,
    (int(time.time()) + 10000)   
).buildTransaction({
    'from': config.sender_address,
    'value': web3.toWei(restAmount, 'ether'),
    'gas': 250000,
    'gasPrice': web3.toWei('10', 'gwei'),
    'nonce': nonce + 1,
})

signed_txn_tax = web3.eth.account.sign_transaction(tx_tax, private_key=config.private_key)
tx_token_tax = web3.eth.send_raw_transaction(signed_txn_tax.rawTransaction)

signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config.private_key)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

# print address
print("TaxAddress: https://testnet.bscscan.com/tx/"+web3.toHex(tx_token_tax))
print("BuyAddress: https://testnet.bscscan.com/tx/"+web3.toHex(tx_token))