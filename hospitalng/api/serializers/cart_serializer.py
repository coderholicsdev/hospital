'''
Serializer to handle products that come from the cart
'''
from rest_framework import serializers

class CartSerializer(serializers.Serializer):
    cart_items = serializers.JSONField()

    class Meta:
        fields = ['cart_items']
