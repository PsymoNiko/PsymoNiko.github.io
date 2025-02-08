from django.contrib import admin

# Register your models here.
from .models import User, Account, Transaction

admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Account)
