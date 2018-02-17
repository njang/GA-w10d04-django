from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Treasure
from .forms import TreasureForm

def index(request):
    treasures = Treasure.objects.all()
    form = TreasureForm()
    return render(request, 'index.html', {'treasures': treasures, 'form':form})

def show(request, treasure_id):
    treasure = Treasure.objects.get(id=treasure_id)
    return render(request, 'show.html', {'treasure': treasure}) 

def post_treasure(request):
    form = TreasureForm(request.POST)
    if form.is_valid():
        form.save(commit = True)
    return HttpResponseRedirect('/')
