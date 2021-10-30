from django.http import HttpResponse
from django.template import Template, context
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.template import RequestContext
from ciaPago.basePrueba import Cuotassociales
#import os

#pagina = 

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
	return render(request, 'perfil.html', data)

	#pagina = get_template('perfil.html')
	#p2 = pagina.render()
	#return HttpResponse(p2)

"""def login(request):
	#pagina = get_template('index.html')
	#p1 = pagina.render()
	#return HttpResponse(p1)
"""
#def test1 (request):
	#mypath = os.getcwd()
	#maindir = os.path.dirname(os.path.dirname(mypath))
	#indexdir = maindir + '\\SistemaWebElectivo5\\index.html'
	#os.chdir(indexdir)
	#os.getcwd()
	#return HttpResponse()