from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from customer.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    debt = serializers.CharField(source="get_debt")
    draw = serializers.IntegerField(default=1)
    recordsTotal = serializers.IntegerField(default=1000)
    recordsFiltered = serializers.IntegerField(default=1000)

    class Meta:
        model = Customer

        fields = ['id', 'firstname', 'lastname', 'address', 'phone',
                  'date_joined', 'enterprise', 'debt'
                  ]


class DataTableCustomerSerializer(serializers.ModelSerializer):
    data = CustomerSerializer(many=True, read_only=True)
    draw = serializers.IntegerField(default=1)
    recordsTotal = serializers.IntegerField(default=1000)
    recordsFiltered = serializers.IntegerField(default=1000)

