from algosdk import account, mnemonic
import json

from django.db import models


'''Data Transfer Objects'''

class NotImplemented(models.Model):
    """test not implemented"""

    comment = models.CharField(max_length=400)

    def __init__(self, comm) -> None: 
        self.comment = comm if (comm) else 'not implemented'    
        
    @property
    def getComment(self) -> str:
        return self.comment    
 
class ComplexEncoder(json.JSONEncoder):
    
    def default(self, o):
        return o.__dict__
    