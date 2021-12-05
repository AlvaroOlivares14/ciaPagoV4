from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ciaPago.models import Comunero, Cuotassociales, Derechopozo, PagoPozo, Pagos, Pozoasociado
from datetime import datetime
from django.contrib.admin import DateFieldListFilter
from django.contrib.admin import SimpleListFilter
from django.utils.html import format_html

"""-----------------------------------------------
Filtros
--------------------------------------------------
"""
class FiltrarMes(SimpleListFilter):
	title = "mes"  # a label for our filter
	parameter_name = "mes"  # you can put anything here

	def lookups(self, request, model_admin):
		# This is where you create filter options
		return [
			("enero", "Enero"),
			("febrero", "Febrero"),
			("marzo", "Marzo"),
			("abril", "Abril"),
			("mayo", "Mayo"),
			("junio", "Junio"),
			("julio", "Julio"),
			("agosto", "Agosto"),
			("septiembre", "Septiembre"),
			("octubre", "Octubre"),
			("noviembre", "Noviembre"),
			("diciembre", "Diciembre"),
        ]

	def queryset(self, request, queryset):
		# This is where you process parameters selected by use via filter options:
		if self.value() == "enero":
			return queryset.filter(fecha__contains='/01/')

		if self.value() == "febrero":
			return queryset.filter(fecha__contains='/02/')

		if self.value() == "marzo":
			return queryset.filter(fecha__contains='/03/')

		if self.value() == "abril":
			return queryset.filter(fecha__contains='/04/')

		if self.value() == "mayo":
			return queryset.filter(fecha__contains='/05/')

		if self.value() == "junio":
			return queryset.filter(fecha__contains='/06/')

		if self.value() == "julio":
			return queryset.filter(fecha__contains='/07/')

		if self.value() == "agosto":
			return queryset.filter(fecha__contains='/08/')

		if self.value() == "septiembre":
			return queryset.filter(fecha__contains='/09/')

		if self.value() == "octubre":
			return queryset.filter(fecha__contains='/10/')

		if self.value() == "noviembre":
			return queryset.filter(fecha__contains='/11/')

		if self.value() == "diciembre":
			return queryset.filter(fecha__contains='/12/')

		if self.value():
			return queryset.all()

class FiltrarAno(SimpleListFilter):
	title = "año"  # a label for our filter
	parameter_name = "año"  # you can put anything here

	def lookups(self, request, model_admin):
		# This is where you create filter options
		return [
			("0", "Este año"),
			("1", "Hace un año"),
			("2", "Hace dos años"),
        ]

	def queryset(self, request, queryset):
		# This is where you process parameters selected by use via filter options:
		if self.value() == "0":
			temp = datetime.now()
			now = temp.year
			year = '/' + str(now)
			return queryset.filter(fecha__contains=year)

		if self.value() == "1":
			temp = datetime.now()
			now = temp.year - 1
			year = '/' + str(now)
			return queryset.filter(fecha__contains=year)

		if self.value() == "2":
			temp = datetime.now()
			now = temp.year - 2
			year = '/' + str(now)
			return queryset.filter(fecha__contains=year)

		if self.value():
			return queryset.all()

class FiltrarEstado(SimpleListFilter):
	title = "estado"  # a label for our filter
	parameter_name = "estado"  # you can put anything here

	def lookups(self, request, model_admin):
		# This is where you create filter options
		return [
			("0", "No pagado"),
			("1", "Pagado"),
        ]

	def queryset(self, request, queryset):
		# This is where you process parameters selected by use via filter options:
		if self.value() == "0":
			return queryset.filter(estadocuota=0)

		if self.value() == "1":
			return queryset.filter(estadocuota=1)

		if self.value():
			return queryset.all()

"""--------------------------------------------------------------
Admin models
-----------------------------------------------------------------
"""
class PagosAdmin(admin.ModelAdmin):
	list_display = ('display_id', 'display_fecha', 'valor')

	def display_id(self, obj) :
		return obj.idtransaccion
	display_id.short_description = 'ID'
	
	def display_fecha(self, obj) :
		fechaLista = datetime.strptime(obj.fecha, '%d/%m/%Y').strftime('%d/%m/%Y')
		return fechaLista
	display_fecha.short_description = 'Fecha'

	list_filter = ('valor', FiltrarMes, FiltrarAno)
	search_fields = ['idtransaccion', 'fecha', 'valor']

class ComuneroAdmin(admin.ModelAdmin):
	list_display = ('rut', 'display_telefono', 'display_cuotas')

	def display_telefono(self, obj) :
		return obj.telefonocelular1
	display_telefono.short_description = 'Telefono'

	def display_cuotas(self, obj) :
		#url = reverse('admin:myapp_style_change', args=(obj.style_id,))
		url = 'http://127.0.0.1:8000/admin/ciaPago/cuotassociales/?q=' + obj.rut
		return format_html("<a href='{}'>{} cuota/s</a>", url, obj.cuotassociales_set.count())
		
	display_cuotas.short_description = 'Cuotas'

	search_fields = ['rut']

class CuotaAdmin(admin.ModelAdmin):
	list_display = ('display_id', 'valor', 'display_fEmi', 'display_fVen', 'display_estado')

	def display_id(self, obj) :
		return obj.idcuota
	display_id.short_description = 'ID'

	def display_fEmi(self, obj) :
		return obj.fechaemicion
	display_fEmi.short_description = 'Fecha de emisión'

	def display_fVen(self, obj) :
		return obj.fechavencimiento
	display_fVen.short_description = 'Fecha de emisión'

	def display_estado(self, obj) :
		if obj.estadocuota == 0:
			return 'No pagado'
		else:
			from django.utils.html import escape
			return format_html('<p><img src="{}" width="{}" height={}/> Pagado</p>', 
			"https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Flat_tick_icon.svg/1200px-Flat_tick_icon.svg.png",
			'15px',
			'15px'
			)
			#return 'Pagado'
	display_estado.short_description = 'Estado'

	list_filter = (FiltrarEstado,)
	search_fields = ['idcuota', 'valor', 'estadocuota', 'fechaemicion', 'fechavencimiento', 'fk_rut__rut']

class PozoAdmin(admin.ModelAdmin):
	list_display = ('display_id', 'caudal')

	def display_id(self, obj) :
		return obj.idcasub
	display_id.short_description = 'ID'

	search_fields = ['idcasub', 'caudal']

admin.site.register(Comunero, ComuneroAdmin)
admin.site.register(Cuotassociales, CuotaAdmin)
admin.site.register(Derechopozo)
admin.site.register(PagoPozo)
admin.site.register(Pagos, PagosAdmin)
admin.site.register(Pozoasociado, PozoAdmin)