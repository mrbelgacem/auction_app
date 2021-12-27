
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import logging

from django.views.decorators.csrf import csrf_exempt
from django.views import View

from auction_app.dto.operations.accounts.generate.account import Account, ComplexEncoder
from auction_app.dto.operations.accounts.generate.serializers import AccountSerializer

from auction_app.apps.operations.checks.balance.checkBalance import CheckBalance

from auction_app.tests.resources.utils.auction.setup import Setup
from auction_app.tests.dto.notImplemented import NotImplemented


class checkEndPoint(View):

    @api_view(['GET', 'POST'])
    def account_check(request):
        logger = logging.getLogger('auction_app')
        
        #path = getattr(settings, 'DIR', None)
        
        # Algod parameter
        algodAddress = getattr(settings, 'ALGOD_ADDRESS', None)
        algodToken = getattr(settings, 'ALGOD_TOKEN', None)
        # Key Management Daemon parameter
        kmdToken = getattr(settings, 'KMD_TOKEN', None)
        kmdAddress = getattr(settings, 'KMD_ADDRESS', None)
        kmdWalletName = getattr(settings, 'KMD_WALLET_NAME', None)
        kmdWalletPassword = getattr(settings, 'KMD_WALLET_PASSWORD', None)  

        balance = None
        
        infoAccount = {}
        pubKeyList = None        
                
        try:
            # Create an algod client (only for testing)
            client = Setup.getAlgodClient(ALGOD_TOKEN=algodToken, ALGOD_ADDRESS=algodAddress)
            
            #status = client.status()
            #logger.info(f'Check node status : \n {json.dumps(status, indent=4)}')

            #params = client.suggested_params()
            #logger.info(f'Check suggested transaction parameters : \n {json.dumps(vars(params), indent=4)}')    
            
            if (request.method == 'POST' and request.data):
                # if body not empty
                infoAccount = request.data
            else :
                logger.info(f'Type of param ... {type(request.GET.get("publicAddress"))}')
                # request.query_params.get('publicAddress', None)
                if isinstance(request.GET.get('publicAddress'), list):
                    # Checking if param has type list
                    pubKeyList = request.GET.get('publicAddress')
                else :
                    # param has type string
                    pubKeyList = [request.GET.get('publicAddress')]
                                       
            accPubKey = infoAccount.get('publicAddress') if ('publicAddress' in infoAccount) else pubKeyList           
           
            balance = CheckBalance.checkBalance(client, accPubKey=accPubKey)
        
        except Exception as err:
            logger.error(f"Error generating account: {err=}, {type(err)=}")
            raise  
        
        logger.info(f'Balance check account OK... {type(balance)}')
        
        return Response(balance)
 