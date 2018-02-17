from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return render(request, 'index.html', {'treasures': treasures})

class Treasure:
    def __init__(self, name, value, material, location):
        self.name = name
        self.value = value
        self.material = material
        self.location = location

treasures = [
    Treasure('Gold Nugget', 500.00, 'gold', "Curly's Creed, NM"),
    Treasure("Fool's Gold", 0, 'pyrite', "Fool's Falls, CO"),
    Treasure('Coffee Can', 20.00, 'tin', "Acme, CA")
]