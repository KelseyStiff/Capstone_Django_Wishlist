from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.

def place_list(request):

    if request.method == 'POST':
        #create new place object
        form = NewPlaceForm(request.POST)
        place = form.save() #creating model object from form
        if form.is_valid(): #validating against db constraints
            place.save() #saves place to db
            return redirect('place_list') #reloads homepage

    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', { 'places': places, 'new_place_form': new_place_form })

def about(request):
    author = 'Kelsey'
    about = 'A website to create list of palces to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about })


def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = place.object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()
    return redirect('place_list')


