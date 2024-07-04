from django.shortcuts import render

# Create your views here.
def index(req):
    return render(req, "index.html")
# myapp/views.py
from django.shortcuts import render
from .models import Restaurant
from .utils import haversine

def restaurant_list(request):
    if request.method == 'POST':
        user_lat = request.POST.get('latitude')
        user_lng = request.POST.get('longitude')
        radius = request.POST.get('radius',2) #By default it displays the restuarants Upto 5Km. when the user Enters The Kilomenter then it will considered

        # # Debug: Print the received values
        # print('Received Latitude:', user_lat)
        # print('Received Longitude:', user_lng)
        # print('Received Radius:', radius)

        if user_lat and user_lng and radius:
            user_lat = float(user_lat)
            user_lng = float(user_lng)
            radius = float(radius)
            
            # # Debug: Print converted values
            # print('Converted Latitude:', user_lat)
            # print('Converted Longitude:', user_lng)
            # print('Converted Radius:', radius)

            # Get all restaurants and filter them based on the distance
            restaurants = Restaurant.objects.all()
            filtered_restaurants = [
                restaurant for restaurant in restaurants
                if haversine(user_lat, user_lng, restaurant.latitude, restaurant.longitude) <= radius
            ]
        else:
            filtered_restaurants = Restaurant.objects.all()

        return render(request, 'index.html', {'restaurants': filtered_restaurants })

    return render(request, 'index.html', {'restaurants': []})



from django.shortcuts import render, get_object_or_404

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'restaurant_details.html', {'restaurant': restaurant})