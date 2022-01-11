import json
import hashlib
import logging
import base64
from datetime import datetime
from algosdk import mnemonic, transaction, encoding
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

    # PureStake Algod parameter
    algodAddress = getattr(settings, 'PURESTAKE_ENDPOINT_ADDR', None)
    algodToken = getattr(settings, 'PURESTAKE_KEY', None)
    algodHeader = getattr(settings, 'PURESTAKE_HEADER', None)
    
    try:
      # Create the algod Client with a PureStake Key
      algodClient = algod.AlgodClient(algodToken, algodAddress, headers=algodHeader)
    
      logger.info("Creating Asset...")
      # CREATE ASSET
      # Get network params for transactions before every transaction.
      params = algodClient.suggested_params()
      
      # comment these two lines if you want to use suggested params
      # params.fee = 1000
      # params.flat_fee = True
      genHash = params.gh
      firstValidRound = params.first
      # maximum validity of 1000 blocks (1000 blocks in the future)
      lastValidRound = params.last
      txFee = params.min_fee
      
      logger.info(f"Network params : {firstValidRound=}, {lastValidRound=}, {txFee=}")
    
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
          asset_name="Ocean's of " + str(datetime.now().strftime("%a %-d %b %y %-H:%M")),
          manager=accountPubAddr,
          reserve=accountPubAddr,
          freeze=accountPubAddr,
          clawback=accountPubAddr,
          url="https://path/to/my/asset/details", 
          metadata_hash=json_metadata_hash,
          decimals=0)
       
      #tx = transaction.PaymentTxn(sender, fee, first, last, gh, receiver, amt)
      #signTx = tx.sign(private_key)
      
      # Transaction bytes string encoded in base64
      #tx_b64 = encoding.msgpack_encode(txn)
      
    
      # Sign with secret key of creator
      logger.info("Send trx to signature ...")
      stxn = txn.sign(account['secretKey'])
      #stxn = algodClient.send_transaction(txn, headers={'content-type': 'application/x-binary'})
    
      # Send the transaction to the network and retrieve the txid.
      logger.info("Send trx to network ...")
      txid_b64 = algodClient.send_transaction(stxn, headers={'content-type': 'application/x-binary'})
      
      #txid = encoding.msgpack_decode(txid_b64)
      
      #logger.info(f"Transaction Signature : {txid_b64}")
      logger.info(f"Asset Creation Transaction ID : {txid_b64}")
    
      # Wait for the transaction to be confirmed
      TransactionUtil.wait_for_confirmation(algodClient,txid_b64,4)
    
      try:
          # Pull account info for the creator
          # account_info = algod_client.account_info(accounts[1]['publicAddress'])
          # get asset_id from tx
          # Get the new asset's information from the creator account
          ptx = algodClient.pending_transaction_info(txid_b64)
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
