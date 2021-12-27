

import json
import logging
from algosdk.error import AlgodHTTPError


class CheckBalance:
    
    def checkBalance(client, **kwargs) -> json:
        
        logger = logging.getLogger('auction_app')
        
        account_info_list = {'accountInfo' : [], 'errors' : []}
        for pk in kwargs['accPubKey']:   
            if pk :
                try:
                    account_info_list['accountInfo'].append(client.account_info(pk))
                except AlgodHTTPError as err:
                    pkError = {'address' : pk, 'error' : err.args}
                    account_info_list['errors'].append(pkError)
                    #account_info_list['errors'].append(json.dumps(pkError))
                    logger.error(json.dumps(pkError, indent=4))
                    pass                
            
        return account_info_list