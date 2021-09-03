from django.shortcuts import render	# notice the import!

def index(request):
    return render(request, "Dash/index.html")

def maps_sm(request):
    return render(request, "Dash/mapsSm.html")