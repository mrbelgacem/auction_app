import json
from typing import List, Tuple, Dict, Any, Optional, Union
from base64 import b64decode

from algosdk.v2client.algod import AlgodClient
from algosdk import encoding

from pyteal import compileTeal, Mode, Expr
from auction_app.resources.utils.operations.contracts.pendingTxnResponse import PendingTxnResponse

class TransactionUtil():
     
    def waitForTransaction(self,
        client: AlgodClient, txID: str, timeout: int = 10
    ) -> PendingTxnResponse:
        lastStatus = client.status()
        lastRound = lastStatus["last-round"]
        startRound = lastRound
    
        while lastRound < startRound + timeout:
            pending_txn = client.pending_transaction_info(txID)
    
            if pending_txn.get("confirmed-round", 0) > 0:
                return PendingTxnResponse(pending_txn)
    
            if pending_txn["pool-error"]:
                raise Exception("Pool error: {}".format(pending_txn["pool-error"]))
    
            lastStatus = client.status_after_block(lastRound + 1)
    
            lastRound += 1
    
        raise Exception(
            "Transaction {} not confirmed after {} rounds".format(txID, timeout)
        )
    
    
    def fullyCompileContract(client: AlgodClient, contract: Expr) -> bytes:
        teal = compileTeal(contract, mode=Mode.Application, version=5)
        response = client.compile(teal)
        return b64decode(response["result"])
    
    
    def decodeState(self, stateArray: List[Any]) -> Dict[bytes, Union[int, bytes]]:
        state: Dict[bytes, Union[int, bytes]] = dict()
    
        for pair in stateArray:
            key = b64decode(pair["key"])
    
            value = pair["value"]
            valueType = value["type"]
    
            if valueType == 2:
                # value is uint64
                value = value.get("uint", 0)
            elif valueType == 1:
                # value is byte array
                value = b64decode(value.get("bytes", ""))
            else:
                raise Exception(f"Unexpected state type: {valueType}")
    
            state[key] = value
    
        return state
    
    
    def getAppGlobalState(self,
        client: AlgodClient, appID: int
    ) -> Dict[bytes, Union[int, bytes]]:
        appInfo = client.application_info(appID)
        return self.decodeState(appInfo["params"]["global-state"])
    
    
    def getBalances(self, client: AlgodClient, account: str) -> Dict[int, int]:
        balances: Dict[int, int] = dict()
    
        accountInfo = client.account_info(account)
    
        # set key 0 to Algo balance
        balances[0] = accountInfo["amount"]
    
        assets: List[Dict[str, Any]] = accountInfo.get("assets", [])
        for assetHolding in assets:
            assetID = assetHolding["asset-id"]
            amount = assetHolding["amount"]
            balances[assetID] = amount
    
        return balances
    
    
    def getLastBlockTimestamp(self, client: AlgodClient) -> Tuple[int, int]:
        status = client.status()
        lastRound = status["last-round"]
        block = client.block_info(lastRound)
        timestamp = block["block"]["ts"]
    
        return block, timestamp
    
    

    # utility for waiting on a transaction confirmation
    def wait_for_confirmation(client:AlgodClient, transaction_id, timeout):
        """
        Wait until the transaction is confirmed or rejected, or until 'timeout'
        number of rounds have passed.
        Args:
            transaction_id (str): the transaction to wait for
            timeout (int): maximum number of rounds to wait    
        Returns:
            dict: pending transaction information, or throws an error if the transaction
                is not confirmed or rejected in the next timeout rounds
        """
        start_round = client.status()["last-round"] + 1;
        current_round = start_round

        while current_round < start_round + timeout:
            try:
                pending_txn = client.pending_transaction_info(transaction_id)
            except Exception:
                return 
            if pending_txn.get("confirmed-round", 0) > 0:
                return pending_txn
            elif pending_txn["pool-error"]:  
                raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
            client.status_after_block(current_round)                   
            current_round += 1
        raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))

    #   Utility function used to print created asset for account and assetid
    def print_created_asset(algodclient, account, assetid):
        # note: if you have an indexer instance available it is easier to just use this
        # response = myindexer.accounts(asset_id = assetid)
        # then use 'account_info['created-assets'][0] to get info on the created asset
        account_info = algodclient.account_info(account)
        idx = 0;
        for my_account_info in account_info['created-assets']:
            scrutinized_asset = account_info['created-assets'][idx]
            idx = idx + 1       
            if (scrutinized_asset['index'] == assetid):
                print("Asset ID: {}".format(scrutinized_asset['index']))
                print(json.dumps(my_account_info['params'], indent=4))
                break

    #   Utility function used to print asset holding for account and assetid
    def print_asset_holding(algodclient, account, assetid):
        # note: if you have an indexer instance available it is easier to just use this
        # response = myindexer.accounts(asset_id = assetid)
        # then loop thru the accounts returned and match the account you are looking for
        account_info = algodclient.account_info(account)
        idx = 0
        for my_account_info in account_info['assets']:
            scrutinized_asset = account_info['assets'][idx]
            idx = idx + 1        
            if (scrutinized_asset['asset-id'] == assetid):
                print("Asset ID: {}".format(scrutinized_asset['asset-id']))
                print(json.dumps(scrutinized_asset, indent=4))
                break