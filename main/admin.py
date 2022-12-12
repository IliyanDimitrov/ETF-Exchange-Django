from django.contrib import admin
from .models import  Address, ETF, Transaction, User_Account

# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
    list_display = ('house_number', 'street','city','postcode','country')
    fields = [ ('house_number', 'street'),( 'postcode', 'city'), 'country']
    
@admin.register(ETF)
class ETFAdmin(admin.ModelAdmin):
    pass

    # readonly_fields = (
    #     'tag',
    #     'name',
    #     'description',
    #     'quantity',
    #     'price'
    # )

    list_display = (
        'tag',
        'name',
        'description',
        'quantity',
        'price'
    )
    fields = [ 'tag', 'name',( 'quantity', 'price'), 'description']
    

    
    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
    
    #disabled fields' edition
    # readonly_fields = ('buyer',
        # 'etf_id',
        # 'quantity',
        # 'unit_cost',
        # 'fee',
        # 'purchase_date'
        # )
    
    list_filter = ('purchase_date', 'quantity')
    
    list_display = (
        'buyer',
        'etf_id',
        'quantity',
        'unit_cost',
        'fee',
        'purchase_date'
    )
    
    fieldsets = (
        ('Transaction', {
            "fields": (
                ('buyer', 'etf_id')
            ),
        }), ('Price',{
            'fields': (
                ('unit_cost', 'quantity','purchase_date'), ('fee'))
        })
    )

class TransactionInline(admin.TabularInline):
    readonly_fields= ('buyer',
        'etf_id',
        'quantity',
        'unit_cost',
        'fee',
        'purchase_date')
    model = Transaction

@admin.register(User_Account)
class User_AccountAdmin(admin.ModelAdmin):
    pass

    # readonly_fields= ('balance')

    list_display = (
        'user_id',
        'balance',
        'birth_date',
        'phone_number'
    )
    fields = [ 'user_id', 'balance','address','phone_number', 'birth_date']
    
    
    inlines = [TransactionInline]
# admin.site.register(Address)
# admin.site.register(ETF)
# admin.site.register(Transaction)
# admin.site.register(User_Account)