from django.contrib import admin
from .models import ShippingAddress , Order ,OrderItem


admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)



class OrderitemInline(admin.StackedInline):
    model = OrderItem
    extra = 0 #  yee Order model ke andar extra info add nahi karta

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    fields = ['user','full_name','email','shipping_address','amount_paid','date_ordered','shipped','date_shipped']
    inlines = [OrderitemInline]
    



admin.site.unregister(Order)
admin.site.register(Order,OrderAdmin)