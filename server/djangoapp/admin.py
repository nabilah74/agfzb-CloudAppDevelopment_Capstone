from django.contrib import admin
from .models import CarMake, CarModel

# Register your models here.
# CarModelInline class
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 0
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    pass
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)






# Register models here
