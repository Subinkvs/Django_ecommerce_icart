from django.contrib import admin
from .models import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from django.http import HttpResponse
from django.db.models.functions import TruncDay
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
import json

class MenClothingAdmin(admin.ModelAdmin):
    # ... (your existing admin configurations)

    def get_chart_data(self):
        labels = []
        data = []

        queryset = MenClothing.objects.order_by('quantity')
        for product in queryset:
            labels.append(product.name)
            data.append(product.quantity)

        return {'labels': labels, 'data': data}

    def changelist_view(self, request, extra_context=None):
        # Use the collected data in the changelist_view
        extra_context = extra_context or {}
        extra_context['chart_data'] = json.dumps(self.get_chart_data())

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
        

# admin side report generator as PDF
def download_pdf(self, request, queryset):
    '''admin side report generator as PDF'''
    model_name = self.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={model_name}.pdf'
    
    
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle('PDF Report')
    
    ordered_queryset = queryset.order_by('-id')
    headers = [self.model._meta.get_field(field).verbose_name for field in self.list_display]
    data = [headers] 


    
    for obj in ordered_queryset:
        data_row = [str(getattr(obj, field)) for field in self.list_display]
        data.append(data_row)
        
    table = Table(data)
    table.setStyle(TableStyle(
        [
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]
        ))
    
    canvas_width = 400
    canvas_height = 400
    
    table.wrapOn(pdf, canvas_width, canvas_height)
    table.drawOn(pdf, 40, canvas_height - len(data))
    
    pdf.save()
    return response
    
download_pdf.short_description = "Dowload selected items as PDF"
    
# Register your models here.
'''Menclothing model in admin interface'''
class MenClothingAdmin(admin.ModelAdmin):
    list_display = ('category', 'brand', 'size', 'color', 'price')
    list_filter = ('category', 'size', 'color')
    search_fields = ('brand', 'description')
    actions = [download_pdf]
   
    
'''Coupon model in admin interface'''
class CouponAdmin(admin.ModelAdmin):
      list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
      list_filter = ['active', 'valid_from', 'valid_to']
      search_fields = ['code']
      actions = [download_pdf]

   


admin.site.register(MenClothing, MenClothingAdmin)
admin.site.register(BannerImage)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Profile)
admin.site.register(Coupon, CouponAdmin)
