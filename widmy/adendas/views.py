from django.shortcuts import render
from .logic import adendas_logic as al
from django.http import Http404, HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def adendas_view(request):
    if request.method == 'GET':
        identificador = request.GET.get("identificador", None)
        if identificador:
            adenda = al.get_adenda(identificador)
            adenda_dto = serializers.serialize('json', [adenda,])
            return HttpResponse(adenda_dto, 'application/json')
        else:
            adendas = al.get_adendas()
            adendas_dto = serializers.serialize('json', adendas)
            return HttpResponse(adendas_dto, 'application/json')
        
    if request.method == 'POST':
        adenda = al.create_adenda(request)
        adenda_dto = serializers.serialize('json', [adenda])
        return HttpResponse(adenda_dto, 'application/json')
    
@csrf_exempt
def adenda_view(request, identificador):
    if request.method == 'GET':
        adenda = al.get_adenda(identificador)
        adenda_dto = serializers.serialize('json', [adenda])
        return HttpResponse(adenda_dto, 'application/json')
    
    if request.method == 'PUT':
        adenda = al.update_adenda(identificador, request)
        adenda_dto = serializers.serialize('json', [adenda])
        return HttpResponse(adenda_dto, 'application/json')
    
from django.db import connections
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from .models import Palabra

@csrf_exempt
def buscar_palabra(request):
    if request.method == 'POST':
        palabra = request.POST.get('palabra')
        # Utilizamos la conexión con la base de datos 'palabras'
        with connections['palabras'].cursor() as cursor:
            # Ejecutamos la consulta para buscar la palabra en la tabla de la base de datos 'palabras'
            cursor.execute("SELECT * FROM adendas_palabra WHERE nombre = %s", [palabra])
            resultado = cursor.fetchone()
        if resultado is None:
            raise Http404("La palabra no existe")
        # Creamos un objeto Palabra a partir del resultado de la consulta
        resultado = Palabra(*resultado)
        frases = [resultado.frase1, resultado.frase2, resultado.frase3]
        return render(request, 'buscar_palabra.html', {'frases': frases})
    return render(request, 'buscar_palabra.html')
