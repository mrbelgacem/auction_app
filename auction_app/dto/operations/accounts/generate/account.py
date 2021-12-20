from algosdk import account, mnemonic
import json
from typing import List

from django.db import models

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
    
    
    class Meta:
        verbose_name_plural = 'accounts'
    
    def __str__(self):
        return self.publicAddress

class ListAccount:
    
    def __init__(self, accounts: List[Account]) -> None:
        self.accounts = accounts
        
    @property
    def getAccList(self) -> List[Account]:
        return self.accounts
 

class ComplexEncoder(json.JSONEncoder):
    
    def default(self, o):
        return o.__dict__
    