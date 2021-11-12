from django.http import HttpResponse
from django.template import Template, context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.template import RequestContext
from ciaPago.basePrueba import Cuotassociales
from ciaPago.action import vista, crearTransWebpay
from django.contrib.sites.models import Site
#from ciaPago.api import WebpayNormalAPI
from django.views.decorators.csrf import csrf_exempt

#import os 

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
		aux = str(request.POST.get('mybtn'))
		aux2 = Cuotassociales.objects.all().filter(idcuota=str(aux)).values_list('valor')
		aux3 = ''.join(str(aux2[0][0]))
		#domain = Site.objects.get_current().domain

		transactionAux = crearTransWebpay('http://127.0.0.1:8000/' + 'accounts/profile/webpay/trans/')
		#transactionAux = crearTransWebpay('http://' + domain+'accounts/profile/webpay/trans/')
		transaction = {
			'token': transactionAux['token'],
			'url': transactionAux['url']
		}
		
		return render(request, 'webpay/init.html', transaction)

	return render(request, 'perfil.html', data)

#@login_required(login_url='/index/login/')
@csrf_exempt
def transComp(request):
	pagina = get_template('index.html')
	p2 = pagina.render()
	return render(request, 'webpay/init.html')