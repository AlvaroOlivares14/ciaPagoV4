from django.http import HttpResponse
from django.template import Template, context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.template import RequestContext
from ciaPago.basePrueba import Cuotassociales, PagoPozo, Pagos
from ciaPago.action import vista, crearTransWebpay
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_exempt
import tbk
from tbk import INTEGRACION
from django.conf import settings
from datetime import date

#import os

with open(
	settings.WEBPAY_OUR_PRIVATE_KEY, "r"
) as file:
	key_data = file.read()
with open(
	settings.WEBPAY_OUR_PUBLIC_CERT, "r"
) as file:
	cert_data = file.read()
with open(
	settings.WEBPAY_CERT, "r"
) as file:
	tbk_cert_data = file.read()

"""normal_commerce = tbk.commerce.Commerce(
    commerce_code=settings.WEBPAY_COMMERCE_CODE,
    key_data=key_data,
    cert_data=cert_data,
    tbk_cert_data=tbk_cert_data,
    environment=tbk.environments.DEVELOPMENT,
)
webpay_service = tbk.services.WebpayService(normal_commerce)"""
commerce = tbk.commerce.Commerce(settings.WEBPAY_COMMERCE_CODE, key_data, cert_data, tbk_cert_data, INTEGRACION)
webpay_service = tbk.services.WebpayService(commerce)


def index(request):
	pagina = get_template('index.html')
	p2 = pagina.render()
	return HttpResponse(p2)


@login_required(login_url='/index/login/')
def perfil(request):
	
	#username = request.user.username
	cuotas = Cuotassociales.objects.all().filter(fk_rut=request.user.username)
	data = {
		'cuotas': cuotas
	}

	if (request.POST.get('mybtn')):
		if (str(request.POST.get('mybtn')).find(',') >= 0):
			aux = str(request.POST.get('mybtn'))
			listaID = aux.split(',')
			total = 0

			for x in listaID:
				aux2 = Cuotassociales.objects.all().filter(idcuota=str(x)).values_list('valor')
				aux3 = int(''.join(str(aux2[0][0])))
				total = total + aux3

			aux3 = total

		else:
			aux = str(request.POST.get('mybtn'))
			aux2 = Cuotassociales.objects.all().filter(idcuota=str(aux)).values_list('valor')
			aux3 = ''.join(str(aux2[0][0]))
		
		aux4 = str("{:,}".format(int(aux3)))
		#domain = Site.objects.get_current().domain

		transactionAux = crearTransWebpay('http://127.0.0.1:8000/' + 'accounts/profile/webpay/trans/', int(aux3), aux)
		#transactionAux = crearTransWebpay('http://' + domain+'accounts/profile/webpay/trans/')
		transaction = {
			'token': transactionAux['token'],
			'url': transactionAux['url'],
			'value': aux4,
		}
		
		return render(request, 'webpay/init.html', transaction)

	return render(request, 'perfil.html', data)

#@login_required(login_url='/index/login/')
@csrf_exempt
def transComp(request):
	token = str(request.POST.get('token_ws'))
	transaction = webpay_service.get_transaction_result(token)
	transaction_detail = transaction["detailOutput"][0]
	webpay_service.acknowledge_transaction(token)

	# datos respuesta (ejemplo)
	"""OrderedDict([
	 ('sharesAmount', None),
	 ('sharesNumber', 0), 
	 ('amount', Decimal('512225')), 
	 ('commerceCode', '597020000541'), 
	 ('buyOrder', '66470238'), 
	 ('authorizationCode', '1213'), 
	 ('paymentTypeCode', 'VN'), 
	 ('responseCode', 0)])"""

	today = date.today()

	# dd/mm/YY
	fecha = today.strftime("%d/%m/%Y")

	transactionToken ={
		'token': token,
		'fecha': fecha,
		'amount': transaction_detail['amount'],
		'responseCode': int(transaction_detail['responseCode'])
	}

	if (transaction_detail['responseCode'] == 0):

		# guardar pago en tabla
		idPago = str(transactionToken['token'])

		pago = Pagos(idtransaccion=idPago, fecha=str(fecha), valor=int(transaction_detail['amount']))
		pago.save()

		pago = Pagos.objects.get(idtransaccion=idPago)


		# en caso de una cuota
		if ( str(transaction_detail['buyOrder']).find(',') == -1 ):

			# modificar cuota
			idCuota = str(transaction_detail['buyOrder'])

			cuota = Cuotassociales.objects.get(idcuota = idCuota)
			cuota.estadocuota = 1
			cuota.fk_idtransaccion = pago
			cuota.save()

			# generar relacion pago-pozo
			cuota = Cuotassociales.objects.get(idcuota = idCuota)
			pago_pozo = PagoPozo(fk_idtransaccion2= pago, fk_idcasub2= cuota.fk_idcasub3)
			pago_pozo.save()
			

		# en caso de multiples cuotas
		else:
			listadoCoutas = str(transaction_detail['buyOrder']).split(',')
			for idCuota in listadoCoutas:
				# modificar cuota
				cuota = Cuotassociales.objects.get(idcuota = idCuota)
				cuota.estadocuota = 1
				cuota.fk_idtransaccion = pago
				cuota.save()

				# generar relacion pago-pozo
				if ( not PagoPozo.objects.filter(fk_idtransaccion2=pago).filter(fk_idcasub2=cuota.fk_idcasub3).exists() ):
					pago_pozo = PagoPozo(fk_idtransaccion2= pago, fk_idcasub2= cuota.fk_idcasub3)
					pago_pozo.save()
			
		
		return render(request, 'webpay/success.html', transactionToken)
	else:
		return render(request, 'webpay/success.html', transactionToken)
	

@csrf_exempt
def transCancel(request):
	return render(request, 'webpay/success.html')