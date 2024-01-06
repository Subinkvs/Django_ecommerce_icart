from django.contrib import admin
from accounts.models import User
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from django.http import HttpResponse

#admin side report generator as PDF
def download_pdf(self, request, queryset):
    '''admin side report generator as PDF'''
    model_name = self.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={model_name}.pdf'
    
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle('PDF Report')
    
    headers = [self.model._meta.get_field(field).verbose_name for field in self.list_display]
    data = [headers] 
    
    for obj in queryset:
        data_row = [str(getattr(obj, field)) for field in self.list_display]
        data.append(data_row)
    
    table = Table(data)
    table.setStyle(TableStyle(
        [
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]
        ))
    
    canvas_width = 600
    canvas_height = 600
    
    table.wrapOn(pdf, canvas_width, canvas_height)
    table.drawOn(pdf, 40, canvas_height - len(data))
    
    pdf.save()
    return response
    
download_pdf.short_description = "Dowload selected items as PDF"

# Register your models here.
'''User model in admin interface'''
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active','phonenumber')
    readonly_fields = ('username', 'email', 'phonenumber','first_name','last_name') 
    
    actions = [download_pdf]

admin.site.register(User, UserAdmin)
