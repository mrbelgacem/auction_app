from rest_framework import serializers
from auction_app.dto.operations.accounts.generate.account import Account

class AccountSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Account
        fields='__all__'