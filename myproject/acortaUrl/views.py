#!/usr/bin/python3

"""
Daniel Suarez Muñoz
Grado en Ing. en Sistemas de Telecomunicaciones
Ejercicio: Práctica 2
"""

from django.shortcuts import render
from .models import urls
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib



def redirect(request,p):
  try:
    i = urls.objects.get(short_url=p)
    resp = '<head><meta http-equiv="Refresh" content="2;url='+ i.large_url +'"></head>'" Redirigiendo........... " 
    	
  except urls.DoesNotExist:
    	p = 'http://127.0.0.1:8000/' + str(p)
    	i = urls.objects.get(short_url=p)
    	resp = '<head><meta http-equiv="Refresh" content="2;url='+ i.large_url +'"></head>'" Redirigiendo........... " 
  return HttpResponse(resp)



@csrf_exempt
def muestra(request):
	if request.method == "GET":
		resp ='<form action="" method="POST">'\
				+'<title>Pagina acorta-URLs</title>'\
				+'<head><h1>Bienvenido a la pagina para acortar URLs</h1></head>'\
				+'Por favor, indique la direccion url a acortar y haga clic en Submit:<br>'\
				+'<input type="text" name="url" value=""><br>'\
				+ '<h1><input type="submit" value="Submit"></h1>'\
			    + '</form>'
	
		lista = urls.objects.all()
		for i in lista:
			resp += '<li>URL LARGA: <a href="' + str(i.large_url) + '">' + str(i.large_url) + '</a>\t'
			resp += '->\t'
			resp += 'URL CORTA: <a href="' + str(i.short_url) + '">' + str(i.short_url) + '</a>'

	elif request.method == "POST":
		newurl = request.body.decode('utf-8')
		newurl= newurl.split("=")[1]
		newurl =  urllib.parse.unquote(newurl, encoding='utf-8') 
		inicio = newurl.split("://")[0]
        
		if (inicio != 'http') and (inicio != 'https'):
			newurl = 'https://' + str(newurl)

		try:     
			lista = urls.objects.all()                                          
			urlcorta = urls.objects.get(large_url=newurl)
			resp = "Ya se ha acortado esa URL,por favor intentalo con otra: <a href="+ newurl + " </a></br>"+newurl+ '<a href="'+ urlcorta.short_url +'"</a></br>'+ urlcorta.short_url +"</br>" \
			+ "<a href=""> Volver a la pagina principal</br>"

		except urls.DoesNotExist:                           
			lista = urls.objects.all()
			cont = 0     
			for i in lista:
				cont = cont + 1
			newshorturl = 'http://127.0.0.1:8000/' + str(cont)
			page = urls(short_url=newshorturl, large_url=newurl)
			page.save()
			i = urls.objects.get(short_url=newshorturl)
			resp = "URL acortada correctamente.</br>"\
			+'<a href="'+ str(i.large_url) +'">' + str(i.large_url) + ' </a></br>'\
			+ '<a href="'+ str(i.short_url) +'">'+ str(i.short_url) + ' </a></br>'\
			+ "<a href=""> Volver a la pagina principal</br>"
	else:
		resp=('Metodo no Permitido')

	return HttpResponse(resp)



