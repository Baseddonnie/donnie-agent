from web3 import Web3
import os

class BankrWallet:
    def __init__(self):
        self.address = "0x5721c2c3146d7b121b0454031926d4b3dfd0ddf3"
        self.api_key = os.getenv("BANKR_API_KEY")
        self.w3 = Web3(Web3.HTTPProvider("https://rpc.bankr.network"))
    
    def balance(self, token):
        """Get token balance"""
        # ERC20 balanceOf implementation
        pass
    
    def buy_donnie(self, amount_eth):
        """Buy DONNIE$ tokens"""
        # call Bankr swap
        pass
    
    def tip(self, to, amount):
        """Tip DONNIE$ to another address"""
        # transfer DONNIE$
        pass
