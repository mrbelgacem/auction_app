from typing import List
from random import choice, randint

from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from algosdk import account, mnemonic

from auction_app.dto.operations.accounts.generate.account import Account, ListAccount
from auction_app.resources.utils.operations.contracts.pendingTxnResponse import PendingTxnResponse
from auction_app.resources.utils.operations.contracts.transactionUtil import TransactionUtil
from auction_app.tests.resources.utils.auction.setup import Setup

import logging

class AccountUtils():
        
    def payAccount(self,
        client: AlgodClient, sender: Account, to: str, amount: int
    ) -> PendingTxnResponse:
        txn = transaction.PaymentTxn(
            sender=sender.getPublicAddress(),
            receiver=to,
            amt=amount,
            sp=client.suggested_params(),
        )
        signedTxn = txn.sign(sender.getPrivateKey())
    
        client.send_transaction(signedTxn)
        return TransactionUtil.waitForTransaction(client, signedTxn.get_txid())
    
    
    FUNDING_AMOUNT = 100_000_000
    
    
    def fundAccount(self, client: AlgodClient, address: str, amount: int = FUNDING_AMOUNT, **kwargs
    ) -> PendingTxnResponse:
        fundingAccount = choice(Setup.getGenesisAccounts(**kwargs))
        return self.payAccount(client, fundingAccount, address, amount)
    
    
    accountList: ListAccount = []
    
    
    def createNewWalletAndGenerateAccount(**kwargs) -> Account:
    
        private_key, address = account.generate_account()
        acc = Account(private_key, **kwargs)     
    
        return acc
        
        
    def getTemporaryAccount(self, client: AlgodClient, **kwargs) -> Account:
        global accountList
    
        if len(self.accountList) == 0:
            sks = [account.generate_account()[0] for i in range(16)]
            self.accountList = [Account(sk) for sk in sks]
            ## kwargs['KMD_TOKEN'], kwargs['KMD_ADDRESS'], kwargs['KMD_WALLET_NAME'], kwargs['KMD_WALLET_PASSWORD']
            genesisAccounts = Setup.getGenesisAccounts(**kwargs)
            suggestedParams = client.suggested_params()
    
            txns: List[transaction.Transaction] = []
            for i, a in enumerate(self.accountList):
                fundingAccount = genesisAccounts[i % len(genesisAccounts)]
                txns.append(
                    transaction.PaymentTxn(
                        sender=fundingAccount.getPublicAddress(),
                        receiver=a.getPublicAddress(),
                        amt=self.FUNDING_AMOUNT,
                        sp=suggestedParams,
                    )
                )
    
            txns = transaction.assign_group_id(txns)
            signedTxns = [
                txn.sign(genesisAccounts[i % len(genesisAccounts)].getPrivateKey())
                for i, txn in enumerate(txns)
            ]
    
            client.send_transactions(signedTxns)
    
            TransactionUtil.waitForTransaction(client, signedTxns[0].get_txid())
    
        return self.accountList.pop()
    
    
    def optInToAsset(self,
        client: AlgodClient, assetID: int, account: Account
    ) -> PendingTxnResponse:
        txn = transaction.AssetOptInTxn(
            sender=account.getPublicAddress(),
            index=assetID,
            sp=client.suggested_params(),
        )
        signedTxn = txn.sign(account.getPrivateKey())
    
        client.send_transaction(signedTxn)
        return TransactionUtil.waitForTransaction(client, signedTxn.get_txid())
    
    
    def createDummyAsset(self, client: AlgodClient, total: int, account: Account = None, **kwargs) -> int:
        if account is None:
            account = self.getTemporaryAccount(client, **kwargs)
    
        randomNumber = randint(0, 999)
        # this random note reduces the likelihood of this transaction looking like a duplicate
        randomNote = bytes(randint(0, 255) for _ in range(20))
    
        txn = transaction.AssetCreateTxn(
            sender=account.getPublicAddress(),
            total=total,
            decimals=0,
            default_frozen=False,
            manager=account.getPublicAddress(),
            reserve=account.getPublicAddress(),
            freeze=account.getPublicAddress(),
            clawback=account.getPublicAddress(),
            unit_name=f"D{randomNumber}",
            asset_name=f"Dummy {randomNumber}",
            url=f"https://dummy.asset/{randomNumber}",
            note=randomNote,
            sp=client.suggested_params(),
        )
        signedTxn = txn.sign(account.getPrivateKey())
    
        client.send_transaction(signedTxn)
    
        response = TransactionUtil.waitForTransaction(client, signedTxn.get_txid())
        assert response.assetIndex is not None and response.assetIndex > 0
        return response.assetIndex
