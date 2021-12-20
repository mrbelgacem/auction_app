
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
from auction_app.apps.abstractMethods.abstractHttpMethod import AbstractHttpMethod
from auction_app.tests.resources.utils.auction.setup import Setup
from auction_app.tests.resources.utils.account.generateNewAccount import GenerateNewAccount
from auction_app.tests.dto.notImplemented import NotImplemented


class accountEndPoint(View):

    @api_view(['POST'])
    def account_generate(request):
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
               
        acc:Account = None
                
        try:
            # Create an algod client (only for testing)
            client = Setup.getAlgodClient(ALGOD_TOKEN=algodToken, ALGOD_ADDRESS=algodAddress)
            
            status = client.status()
            logging.info(f'Check node status : \n {json.dumps(status, indent=4)}')

            params = client.suggested_params()
            logging.info(f'Check suggested transaction parameters : \n {json.dumps(vars(params), indent=4)}')    
            
            infoAccount = {}
            
            if request.data :
                # if body not empty
                infoAccount = request.data
                
            
            accName = infoAccount.get('name') if ('name' in infoAccount) else None  
            accComment = infoAccount.get('comment') if ('comment' in infoAccount) else None            
        
            #acc = Account.objects.get(name=accName)
            #serializer = AccountSerializer(instance=Account, data=request.data)        
        
            acc:Account = GenerateNewAccount.generateForTest(name=accName, comment=accComment)
        
            serializer = AccountSerializer(acc, many=False)
        except Exception as err:
            logging.error(f"Error generating account: {err=}, {type(err)=}")
            raise  
        
        logger.info('Generating account OK...')
        return Response(serializer.data)
        

#    def post(self, request):
        
#        return JsonResponse(NotImplemented('Method not implemented'), encoder=ComplexEncoder, safe=False)
    
    
#    def patch(self, request):
        
#        return JsonResponse(NotImplemented('Method not implemented'), encoder=ComplexEncoder, safe=False)

#    def put(self, request):
        
 #       return JsonResponse(NotImplemented('Method not implemented'), encoder=ComplexEncoder, safe=False)
    
#    def put(self, request, itemId):    
#        return JsonResponse(NotImplemented('Method not implemented'), encoder=ComplexEncoder, safe=False)
    

#    def delete(self, request):
        
#        return JsonResponse(NotImplemented('Method not implemented'), encoder=ComplexEncoder, safe=False)