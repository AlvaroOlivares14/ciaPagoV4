from django.http import HttpResponse
from django.template import RequestContext

import requests
import random

import transbank

# import intento Z
from tbk.services import WebpayService
from tbk.commerce import Commerce
from tbk import INTEGRACION
from django.conf import settings

def vista(x):

	texto = 'hola mundo: ' + str(x)
	return texto


def crearTransWebpay(return_url, amount, buy_order):
	#buy_order = str(random.randrange(1000000, 99999999))
	session_id = str(random.randrange(1000000, 99999999))
	#amount = random.randrange(10000, 1000000)

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


	commerce = Commerce(settings.WEBPAY_COMMERCE_CODE, key_data, cert_data, tbk_cert_data, INTEGRACION)
	webpay = WebpayService(commerce)
	transaction = webpay.init_transaction(amount, buy_order, return_url, settings.WEBPAY_URL_FINAL)
	
	return transaction