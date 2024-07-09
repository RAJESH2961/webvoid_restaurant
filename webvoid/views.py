from django.shortcuts import render

# Create your views here.
def index(req):
    return render(req, "index.html")
# myapp/views.py
from django.shortcuts import render
from .models import Restaurant,Menu, RestaurantReview, MenuReview
from .utils import haversine

def restaurant_list(request):
    if request.method == 'POST':
        user_lat = request.POST.get('latitude')
        user_lng = request.POST.get('longitude')
        radius = request.POST.get('radius') #By default it displays the restuarants Upto 5Km. when the user Enters The Kilomenter then it will considered

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

        return render(request, 'restaurants.html', {'restaurants': filtered_restaurants })

    return render(request, 'restaurants.html', {'restaurants': []})



from django.shortcuts import render, get_object_or_404

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    # fetching menus from the particular restaurant
    menus = Menu.objects.filter(restaurant=restaurant)
    # getting reviews from the database
    # Fetch approved reviews for the restaurant
    reviews = RestaurantReview.objects.filter(restaurant=restaurant, is_approved=True)
        # up to here we fetched the data from the database

    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id')
        user_name = request.POST.get('user_name')
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')

        try:
            # Retrieve the restaurant object or raise 404 if not found
            restaurant = get_object_or_404(Restaurant, id=restaurant_id)
            
            # Create a new review object
            review = RestaurantReview.objects.create(
                restaurant=restaurant,
                user_name=user_name,
                review_text=review_text,
                rating=rating
            )
            # again here we are fetching the same data which we fetched above because bacause here we are writing the if condition(inside the block) it indicates the local memory scope
            # and also we are handling the form request in the same page so when we refresh the data old data will be erased so in order to display the data we pass the same data again 
            restaurant = get_object_or_404(Restaurant, pk=pk)
            # fetching menus from the particular restaurant
            menus = Menu.objects.filter(restaurant=restaurant)
            # getting reviews from the database
            reviews = RestaurantReview.objects.filter(restaurant=restaurant, is_approved=True)

            # Prepare the alert message to display in the same template
            return render(request, 'restaurant_details.html',
                           {'alert_message': 'Review submitted successfully!',
                            'restaurant': restaurant ,
                            'menus': menus, 
                            'reviews': reviews})
        except ValueError:
            return render(request, 'restaurant_details.html', {'alert_message': 'Invalid data format.'})


    return render(request, 'restaurant_details.html', {'restaurant': restaurant ,
                                                        'menus': menus, 
                                                        'reviews': reviews})


from django.shortcuts import render, get_object_or_404
from .models import Menu, MenuReview

def menu_detail(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    menureviews = MenuReview.objects.filter(menu=menu, is_approved=True)

    if request.method == "POST":
        user_name = request.POST.get('user_name')
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')

        # Ensure to fetch the restaurant associated with the menu
        restaurant_id = menu.restaurant_id  # Adjust this according to your model structure

        # Validate and save the review if all required fields are present
        if user_name and review_text and rating:
            review = MenuReview.objects.create(
                menu=menu,
                restaurant_id=restaurant_id,
                user_name=user_name,
                review_text=review_text,
                rating=rating,
                is_approved=False  # Optionally set approval status based on your workflow
            )
            # Optionally, redirect to a success page or reload the page to show the new review
            menureviews = MenuReview.objects.filter(menu=menu, is_approved=True)

    return render(request, 'menu_detail.html', {'menu': menu, 'menureviews': menureviews})
