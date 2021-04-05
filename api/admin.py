from django.contrib import admin
from api import models

# Register your models here.
admin.site.register(models.Wallet)
admin.site.register(models.Transaction)
admin.site.register(models.UserProfile)