from django.shortcuts import render
from django.http import HttpResponse
from .models import Treasure

def index(request):
	treasures = Treasure.objects.all()
	return render(request, 'index.html', {'treasures': treasures})

def show(request, treasure_id):
	treasure = Treasure.objects.get(id=treasure_id)
	return render(request, 'show.html', {'treasure': treasure}) 

# class Treasure:
#     def __init__(self, name, value, material, location):
#         self.name = name
#         self.value = value
#         self.material = material
#         self.location = location

# treasures = [
#     Treasure('Gold Nugget', 500.00, 'gold', "Curly's Creed, NM"),
#     Treasure("Fool's Gold", 0, 'pyrite', "Fool's Falls, CO"),
#     Treasure('Coffee Can', 20.00, 'tin', "Acme, CA")
# ]