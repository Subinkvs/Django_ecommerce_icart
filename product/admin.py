from django.contrib import admin
from .models import *

# Register your models here.
'''Menclothing model in admin interface'''
class MenClothingAdmin(admin.ModelAdmin):
    list_display = ('category', 'brand', 'size', 'color', 'price')
    list_filter = ('category', 'size', 'color')
    search_fields = ('brand', 'description')

'''Coupon model in admin interface'''
class CouponAdmin(admin.ModelAdmin):
      list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
      list_filter = ['active', 'valid_from', 'valid_to']
      search_fields = ['code']


admin.site.register(MenClothing, MenClothingAdmin)
admin.site.register(BannerImage)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)
admin.site.register(Coupon, CouponAdmin)
