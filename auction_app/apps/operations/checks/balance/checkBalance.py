

import json
import logging


class CheckBalance:
    
    def checkBalance(client, **kwargs) -> json:
        
        logger = logging.getLogger('auction_app')
        
        #logger.info(f"Check balance account public key : {kwargs['accPubKey']}")
        
#        for pk in my_list:
#            print(pk)
        account_info = None
        if kwargs['accPubKey'] :
            account_info = client.account_info(kwargs['accPubKey'])
            #logging.debug(f"Account info \n {json.dumps(account_info, indent=4)}")
            
        return account_info