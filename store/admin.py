from django.contrib import admin

from django.contrib.auth.models import User

from . models import Product , Category , Customer , Order ,Profile



class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','category']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','phone']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['product','customer','quantity']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','city','zipcode']



class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username','first_name','last_name','email']
    inlines = [ProfileInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Profile, ProfileAdmin)



admin.site.unregister(User)

admin.site.register(User,UserAdmin)