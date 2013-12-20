from django.contrib import admin
from webescrow.models import Transaction
from suit.admin import SortableTabularInline, SortableModelAdmin
from mptt.admin import MPTTModelAdmin


class TransactionAdmin(admin.ModelAdmin):
    #list_display = ('Transaction',)
    fields = ('user', 'sender', 
        'buyer', 'expires', 'amount', 
        'condition_description', 'condition_document',  
        'terms_agreed', 'is_complete'
        )
    search_fields = ['sender']
admin.site.register(Transaction, TransactionAdmin)