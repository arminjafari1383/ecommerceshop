from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name','subject','phone']

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile

#Extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username","first_name","last_name","email"]
    inlines = [ProfileInline]


#Unregistred the old way
admin.site.Unregister(User)

#Re-register the new way
admin.site.register(User,UserAdmin)