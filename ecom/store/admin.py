from django.contrib import admin
from .models import *


admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name','subject','phone']