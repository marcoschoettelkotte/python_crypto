from web3 import Web3
import json
import time
import config
import abi


web3 = Web3(Web3.HTTPProvider(config.bsc))

print(web3.isConnected())

spend = web3.toChecksumAddress(config.wbnb)  #WBNB Address testnet
 
contract_id = web3.toChecksumAddress(config.sellAddress) # address to sell
 
contract = web3.eth.contract(address=config.panRouterContractAddress, abi=abi.panabi)


sellTokenContract = web3.eth.contract(contract_id, abi=abi.sellAbi)

balance = sellTokenContract.functions.balanceOf(config.sender_address).call()
symbol = sellTokenContract.functions.symbol().call()
readable = web3.fromWei(balance,'ether')
print("Balance: " + str(web3.fromWei(readable, 'ether')) + " " + symbol)


selltoken_amount = 140.876
tokenValue = web3.toWei(selltoken_amount, 'ether')
tokenValue2 = web3.fromWei(tokenValue, 'ether')
start = time.time()

approve = sellTokenContract.functions.approve(config.panRouterContractAddress, balance).buildTransaction({
            'from': config.sender_address,
            'gasPrice': web3.toWei('10','gwei'),
            'nonce': web3.eth.get_transaction_count(config.sender_address),
            })

signed_txn = web3.eth.account.sign_transaction(approve, private_key=config.private_key)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Approved: " + web3.toHex(tx_token))

#Wait after approve 10 seconds before sending transaction
time.sleep(10)
print(f"Swapping {tokenValue2} {symbol} for BNB")
#Swaping exact Token for ETH 

pancakeswap2_txn = contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            tokenValue ,0, 
            [contract_id, spend],
            config.sender_address,
            (int(time.time()) + 1000000)

            ).buildTransaction({
            'from': config.sender_address,
            'gasPrice': web3.toWei('10','gwei'),
            'nonce': web3.eth.get_transaction_count(config.sender_address),
            })
signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=config.private_key)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(f"Sold {symbol}: " + web3.toHex(tx_token))