
from django.http import JsonResponse
import json

from django.conf import settings
import logging

from auction_app.dto.operations.accounts.generate.account import Account, ComplexEncoder
from auction_app.apps.abstractMethods.abstractHttpMethod import AbstractHttpMethod
from auction_app.tests.resources.utils.auction.setup import Setup
from auction_app.tests.resources.utils.account.generateNewAccount import GenerateNewAccount


class generateAccount(AbstractHttpMethod):
    
    def get(self, request):
        logger = logging.getLogger('auction_app')
        
        path = getattr(settings, 'DIR', None)
        
        # Algod parameter
        algodAddress = getattr(settings, 'ALGOD_ADDRESS', None)
        algodToken = getattr(settings, 'ALGOD_TOKEN', None)
        # Key Management Daemon parameter
        kmdToken = getattr(settings, 'KMD_TOKEN', None)
        kmdAddress = getattr(settings, 'KMD_ADDRESS', None)
        kmdWalletName = getattr(settings, 'KMD_WALLET_NAME', None)
        kmdWalletPassword = getattr(settings, 'KMD_WALLET_PASSWORD', None)  
               
        acc:Account = None
                
        try:
            # Create an algod client (only for testing)
            client = Setup.getAlgodClient(self, ALGOD_TOKEN=algodToken, ALGOD_ADDRESS=algodAddress)
            
            status = client.status()
            logging.info(f'Check node status : \n {json.dumps(status, indent=4)}')

            params = client.suggested_params()
            logging.info(f'Check suggested transaction parameters : \n {json.dumps(vars(params), indent=4)}')        
        
            acc:Account = GenerateNewAccount.generateForTest(self)
        
        except Exception as err:
            logging.error(f"Error generating account: {err=}, {type(err)=}")
            raise        
        logger.info('Generating account OK...')

        return JsonResponse(acc, encoder=ComplexEncoder, safe=False)
        

    
    
    def post(self, request):

        return ({'method':'post not implemented'})
    
    
    def patch(self, request, itemId):
        
        return ({'method':'patch not implemented'})

    
    def put(self, request, itemId):
        
        return ({'method':'put not implemented'})
    

    def delete(self, request, itemId):
        
        return ({'method':'delete not implemented'})