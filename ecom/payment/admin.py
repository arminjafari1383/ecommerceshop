from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

#Register the model on the admin section thing
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# create an OrderItem Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
#Extend our order model 
class OrderAdmin(admin.ModelAdmin):
    model = Order
    # readonly_fields = ["date_ordered"]
    inlines = [OrderItemInline]


#unregister order model
admin.site.unregister(Order)


# RE-register our order and orderitems
admin.site.register(Order,OrderAdmin)