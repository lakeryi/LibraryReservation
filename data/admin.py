from django.contrib import admin


from .models import Students, Rent, Chairs
# Register your models here.
admin.site.register(Students)
admin.site.register(Rent)
admin.site.register(Chairs)
