from typing import Optional, List

from algosdk.v2client.algod import AlgodClient
from algosdk.kmd import KMDClient

from auction_app.dto.operations.accounts.generate.account import Account


class Setup():

    def getAlgodClient(**kwargs) -> AlgodClient:
        """Connect Your Client"""
        return AlgodClient(kwargs['ALGOD_TOKEN'], kwargs['ALGOD_ADDRESS'])

    def getKmdClient(self,**kwargs) -> KMDClient:
        """Key Management Daemon"""
        return KMDClient(kwargs['KMD_TOKEN'], kwargs['KMD_ADDRESS'])

    kmdAccounts: Optional[List[Account]] = None
        
    def getGenesisAccounts(self,**kwargs) -> List[Account]:
        global kmdAccounts
    
        if self.kmdAccounts is None:
            kmd = self.getKmdClient(**kwargs)
    
            wallets = kmd.list_wallets()
            walletID = None
            for wallet in wallets:
                if wallet["name"] == kwargs['KMD_WALLET_NAME']:
                    walletID = wallet["id"]
                    break
    
            if walletID is None:
                raise Exception("Wallet not found: {}".format(kwargs['KMD_WALLET_NAME']))
    
            walletHandle = kmd.init_wallet_handle(walletID, kwargs['KMD_WALLET_PASSWORD'])
    
            try:
                addresses = kmd.list_keys(walletHandle)
                privateKeys = [
                    kmd.export_key(walletHandle, kwargs['KMD_WALLET_PASSWORD'], addr)
                    for addr in addresses
                ]
                self.kmdAccounts = [Account(sk) for sk in privateKeys]
            finally:
                kmd.release_wallet_handle(walletHandle)
    
        return self.kmdAccounts
