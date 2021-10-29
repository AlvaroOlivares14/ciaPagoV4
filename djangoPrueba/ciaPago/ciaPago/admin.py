from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ciaPago.basePrueba import Comunero, Cuotassociales, Derechopozo, PagoPozo, Pagos, Pozoasociado

class Prueba1(admin.ModelAdmin):
	list_display = ('rut', 'password')

#admin.site.register(Comunero, UserAdmin)

admin.site.register(Comunero)
admin.site.register(Cuotassociales)
admin.site.register(Derechopozo)
admin.site.register(PagoPozo)
admin.site.register(Pagos)
admin.site.register(Pozoasociado)