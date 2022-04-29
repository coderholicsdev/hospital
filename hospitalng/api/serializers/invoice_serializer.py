'''
Serializer for invoices
'''
from rest_framework import serializers

# import models
from api.models import (
    InvoiceItem,
    Invoice
)

# Invoicing
class InvoiceItemSerializer(serializers.ModelSerializer):
    total_for_item = serializers.SerializerMethodField('total_price')

    class Meta:
        model = InvoiceItem
        fields = ['description', 'unit_price', 'quantity', 'total_for_item']

    def total_price(self, obj):
        total_price = obj.unit_price * obj.quantity
        return total_price

class InvoicesSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Invoice
        fields = ['invoice_id', 'invoice_status', 'issued_date', 'items']
    
class UpdateInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['invoice_status']

class AdminInvoicesSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    user = serializers.CharField(source='user.email')
    class Meta:
        model = Invoice
        fields = ['user', 'invoice_id', 'invoice_status', 'issued_date', 'items']
