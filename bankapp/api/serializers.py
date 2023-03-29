from rest_framework import serializers
from wallet.models import *
from .services import calc_balance
from django.shortcuts import get_object_or_404


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('id', 'fname', 'lname',)
        read_only_fields = ('id', )

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super(CustomerSerializer, self).create(validated_data)
    

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'name', 'balance',)
        # balance is read only, because i don't want someone create account
        # with money
        # read_only_fields = ('id', 'name', 'balance',)
    
    # def get(self, validated_data):



class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ('id', 'name', 'sum', 'pub_date')


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ('id', 'name', 'sum', 'pub_date')


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ('id', 'name', 'sum', 'pub_date')


class GoalsSerializer(serializers.ModelSerializer):
    date_goal = serializers.DateField(
        format='%d.%m.%Y',
        input_formats=['%d.%m.%Y']
    )
    class Meta:
        model = Goals
        fields = ('id', 'name', 'sum_goal', 'date_goal', 'pub_date')


class TransferSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(TransferSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['from_account'].queryset = self.fields['from_account']\
                .queryset.filter(user=self.context['view'].request.user)

    to_account = serializers.CharField()

    def validate(self, data):
        try:
            data['to_account'] = Account.objects.get(pk=data['to_account'])
        except Exception as e:
            print(e)
            raise serializers.ValidationError(
                "No such account from serializer")
        return data

    class Meta:
        model = Transfer
        fields = ('id', 'from_account', 'to_account', 'amount')
        read_only_fields = ('id', )