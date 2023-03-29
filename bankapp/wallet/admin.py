from django.contrib import admin

from .models import (Expenses, Income, Wallet, 
                     Goals, Customer, Transfer, 
                     Account)


admin.site.register(Expenses)
admin.site.register(Income)
admin.site.register(Wallet)
admin.site.register(Goals)
admin.site.register(Customer)
admin.site.register(Transfer)
admin.site.register(Account)
