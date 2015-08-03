from django.shortcuts import render
from django.apps import apps


Page = apps.get_model('dumpling.Page')

def index(request):                                                  
    return render(request, 'dumpling/index.html', {                   
        'roots': Page.objects.filter(parent=None),                    
    })       
