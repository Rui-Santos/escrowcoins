from django.contrib import admin
from webescrow.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    #list_display = ('Transaction',)
    exclude=('terms_agreed_date', )
    readonly_fields = ('user', 'sender', 'buyer', 'terms_agreed')
    title = ('decade born'),
    fields = ('user', 'sender', 
    	'buyer', 'expires', 'amount', 
        'condition_description', 'condition_document',
        )
    search_fields = ['sender']
admin.site.register(Transaction, TransactionAdmin)