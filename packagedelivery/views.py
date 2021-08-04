from django.shortcuts import render, HttpResponse
from .forms import loginForm
def home(request):
    context = {}
    form = loginForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, 'home.html', context)