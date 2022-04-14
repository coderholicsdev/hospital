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
    class Meta:
        model = InvoiceItem
        fields = ['description', 'unit_price']

class InvoicesSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    class Meta:
        model = Invoice
        fields = ['invoice_id', 'invoice_status', 'issued_date', 'items']

