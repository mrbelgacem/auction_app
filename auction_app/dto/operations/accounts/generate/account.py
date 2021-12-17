from algosdk import account, mnemonic
import json
from typing import List

from django.db import models
from django.core import serializers
from django.forms.models import model_to_dict

'''Data Transfer Objects'''

class Account(models.Model):
    """Represents a private key and address for an Algorand account"""


    foncId = models.BigIntegerField()
    name = models.CharField(max_length=200)
    comment = models.CharField(max_length=400)
    publicAddress = models.CharField(max_length=400)
    privateKey = models.CharField(max_length=400)
    mnemonic = models.CharField(max_length=400) 
    
    
    def __init__(self, privateKey: str, **kwargs) -> None:
        self.foncId = kwargs['foncId'] if ('foncId' in kwargs) else None
        self.name = kwargs['name'] if ('name' in kwargs) else None  
        self.comment = kwargs['comment'] if ('comment' in kwargs) else None
        self.publicAddress = account.address_from_private_key(privateKey)
        self.privateKey = privateKey
        self.mnemonic = mnemonic.from_private_key(self.privateKey)
        
        
    @property
    def getFoncId(self) -> str:
        return self.foncId        

    @property
    def getName(self) -> str:
        return self.name
    
    @property
    def getComment(self) -> str:
        return self.comment    
    
    @property
    def getPublicAddress(self) -> str:
        return self.publicAddress

    @property
    def getPrivateKey(self) -> str:
        return self.privateKey
    
    @property
    def getMnemonic(self) -> str:
        return mnemonic.from_private_key(self.privateKey)

    @classmethod
    def FromMnemonic(cls, m: str) -> "Account":
        return cls(mnemonic.to_private_key(m))

#    @classmethod
#    def reprJSON(self):
#        # Serialization
#        return dict(foncId=self.getFoncId, name=self.getName, comment=self.getComment, publicAddr=self.getPublicAddress, privateKey=self.getPrivateKey, mnemonic=self.getMnemonic) 

#    @classmethod
#    def toJSON(self):
#        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class ListAccount:
    
    def __init__(self, accounts: List[Account]) -> None:
        self.accounts = accounts
        
    @property
    def getAccList(self) -> List[Account]:
        return self.accounts
 
#    @classmethod
#    def reprJSON(self): 
#        # Serialization
#        return dict(accounts=self.getAccList)
    
#    @classmethod
#    def toJSON(self):
#        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)    


class ComplexEncoder(json.JSONEncoder):
    
    def default(self, o):
        #return serializers.serialize('json', [ o, ])
        #return model_to_dict( o )
        return o.__dict__
    
#    def default(self, obj):
#        if hasattr(obj,'reprJSON'):
#            return obj.reprJSON()
#        else:
#            return json.JSONEncoder.default(self, obj)