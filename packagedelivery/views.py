from django.shortcuts import render
from .forms import loginForm, maps
from django.conf import settings


def home(request):
    context = {}
    loginform = loginForm(request.POST or None, request.FILES or None)
    # if form.is_valid():
    #     form.save()
    context['loginform'] = loginform
    return render(request, 'home.html', context)

def map(request):
    context = {}
    # context['google_map_key'] = settings.GOOGLE_API_KEY
    context['tomtom_map_key'] = settings.TOMTOM_API_KEY
    kg_Select = maps(request.POST or None, request.FILES or None)
    loginform = loginForm(request.POST or None, request.FILES or None)
    context['loginform'] = loginform
    # if kg_Select.is_valid():
    #     kg_Select.save() 
    context['formkg'] = kg_Select
    if request.GET:
        price = request.GET.get('price', None)
        context['price'] = price
        print(price)
        return render(request, 'home.html', context)
    else: 
        print('hi')
        return render(request, 'map.html', context)

def aboutus(request):
    return render(request,"aboutus.html")

def contactus(request):
    return render(request,"contactus.html")