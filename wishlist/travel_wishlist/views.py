from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages 

# Create your views here.


@login_required
def place_list(request):

    if request.method == 'POST':
        #create new place object
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False) #creating model object from form (get data but dont save yet)
        place.user = request.user
        if form.is_valid(): #validating against db constraints
            place.save() #saves place to db
            return redirect('place_list') #reloads homepage

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()

    return render(request, 'travel_wishlist/wishlist.html', { 'places': places, 'new_place_form': new_place_form })

@login_required
def about(request):
    author = 'Kelsey'
    about = 'A website to create list of palces to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about })

@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()
    return redirect('place_list')

@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    # DOES THIS PLACE BELONG TO CURRENT USER
    if place.user != request.user:
        return HttpResponseForbidden
    #GET(SHOW DATA) OR POST(UPDATE PLACE OBJECT) REQUEST?
    #if POST request, validate form data and update
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid(): #checking if all the fields filled in w/right data 
            form.save()
            messages.info(request, 'Trip information updated!') #sends a temp message to user
        else:
            messages.error(request, form.errors) #temp, refine error msg later
        return redirect('place_details', place_pk=place_pk)
    else:
        #if GET request, show Place info and form
        #if place is visited, show form, if place is not visited, no form
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()


