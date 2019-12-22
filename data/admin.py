from django.contrib import admin

from .models import Students, Rent, Chairs, Friends, Rooms
# Register your models here.
admin.site.register(Students)
admin.site.register(Rent)
admin.site.register(Chairs)
admin.site.register(Friends)
admin.site.register(Rooms)
