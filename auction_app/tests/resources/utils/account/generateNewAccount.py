
from time import time, sleep
from datetime import datetime
import logging
import configparser
import json
import argparse

from django.conf import settings

from algosdk import account, encoding, mnemonic
from algosdk.logic import get_application_address

from auction_app.tests.resources.utils.auction.accountUtils import AccountUtils
from auction_app.dto.operations.accounts.generate.account import Account


class GenerateNewAccount:
    
    def generateForTest(self, **kwargs) -> Account:
        accName = kwargs['name'] if ('name' in kwargs) else None  
        accComment = kwargs['comment'] if ('comment' in kwargs) else None
                
        return AccountUtils.createNewWalletAndGenerateAccount(name= accName, comment= accComment)
        
        
        