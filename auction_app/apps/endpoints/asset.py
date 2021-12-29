import json
import hashlib
import logging
from algosdk import mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import AssetConfigTxn
from algosdk.error import AlgodHTTPError

from django.conf import settings
from django.views import View

from rest_framework.decorators import api_view
from rest_framework.response import Response

from auction_app.resources.utils.operations.contracts.transactionUtil import TransactionUtil

from auction_app.tests.resources.utils.auction.setup import Setup



class assetEndPoint(View):
  
  @api_view(['GET', 'POST'])
  def create_asset(request):
    
    logger = logging.getLogger('auction_app')
  
    # accounts = dictionary holding public key, secret key of accounts.
    # Using Rand Labs Developer API
    # see https://github.com/algorand/py-algorand-sdk/issues/169
    # Change algod_token and algod_address to connect to a different client

    # Algod parameter
    algodAddress = getattr(settings, 'ALGOD_ADDRESS', None)
    algodToken = getattr(settings, 'ALGOD_TOKEN', None)
    
    try:
      # Create an algod client (only for testing)
      algodClient = Setup.getAlgodClient(ALGOD_TOKEN=algodToken, ALGOD_ADDRESS=algodAddress)
    
      logger.info("Creating Asset...")
      # CREATE ASSET
      # Get network params for transactions before every transaction.
      params = algodClient.suggested_params()
      # comment these two lines if you want to use suggested params
      # params.fee = 1000
      # params.flat_fee = True
    
      # JSON file
      f = open ('auction_app/tests/resources/assets/assetMetaData.json', "r")
      
      # Reading from file
      metadataJSON = json.loads(f.read())
      metadataStr = json.dumps(metadataJSON)
    
      hash = hashlib.new("sha512_256")
      hash.update(b"arc0003/amj")
      hash.update(metadataStr.encode("utf-8"))
      json_metadata_hash = hash.digest()
      
      account = None
      if (request.method == 'POST' and request.data):
          # if body not empty
          account = request.data
      else :
        pass
    
      # Account 1 creates an asset called OceanOI and
      # sets Account 1 as the manager, reserve, freeze, and clawback address.
      # Asset Creation transaction
      accountPubAddr = account['publicAddress']
      
      txn = AssetConfigTxn(
          sender=accountPubAddr,
          sp=params,
          total=1000,
          default_frozen=False,
          unit_name="OceanOI",
          asset_name="Ocean's Artwork Coins@arc3",
          manager=accountPubAddr,
          reserve=accountPubAddr,
          freeze=accountPubAddr,
          clawback=accountPubAddr,
          url="https://path/to/my/asset/details", 
          metadata_hash=json_metadata_hash,
          decimals=0)
    
      # Sign with secret key of creator
      stxn = txn.sign(account['secretKey'])
    
      # Send the transaction to the network and retrieve the txid.
      txid = algodClient.send_transaction(stxn)
      logger.info(f"Asset Creation Transaction ID: {txid}")
    
      # Wait for the transaction to be confirmed
      TransactionUtil.wait_for_confirmation(algodClient,txid,4)
    
      try:
          # Pull account info for the creator
          # account_info = algod_client.account_info(accounts[1]['publicAddress'])
          # get asset_id from tx
          # Get the new asset's information from the creator account
          ptx = algodClient.pending_transaction_info(txid)
          asset_id = ptx["asset-index"]
          TransactionUtil.print_created_asset(algodClient, accountPubAddr, asset_id)
          TransactionUtil.print_asset_holding(algodClient, accountPubAddr, asset_id)
      except Exception as e:
          raise

    except AlgodHTTPError as algodErr:
      logger.error(f"Error asset transaction: {algodErr}")
      raise
    except Exception as err:
      logger.error(f"Error generating asset: {err=}, {type(err)=}")
      
      account_info_list = {'accountInfo' : [], 'errors' : []}
      trxError = {'address' : accountPubAddr, 'error' : err.args}
      account_info_list['errors'].append(trxError)
      return Response(account_info_list)
   
    return Response(ptx)
