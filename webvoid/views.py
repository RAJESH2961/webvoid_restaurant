from django.shortcuts import render, redirect

# Create your views here.
from django.core.mail import send_mail
from django.conf import settings

def index(req):
    if req.method == 'POST':
        if 'latitude' in req.POST and 'longitude' in req.POST:
            # Handle location data
            latitude = req.POST.get('latitude')
            longitude = req.POST.get('longitude')
            
            # Store location data in the session
            req.session['latitude'] = latitude
            req.session['longitude'] = longitude
        
        elif 'name' in req.POST and 'message' in req.POST:
            # Handle contact form submission
            name = req.POST.get('name')
            email = req.POST.get('email')
            message = req.POST.get('message')
            
            # Send email to admin
            send_mail(
                    subject=f'Contact Us Message from {name}',
                    message=f"""
                        Name : {name}
                        Email : {email}
                        Message : {message}
                    """,
                    #From email is congigured in settings.py grajesh2907@gmail.com
                    #https://myaccount.google.com/u/1/apppasswords?rapt=AEjHL4Pl93YfXxYImlyf4JGj0pd-4ReC3qWD8qTkc6Z_AB2rqqnLKxvMMM6q6iZCWJBHda3ZKXhY-th4Wcv9JbHGsLJ51zuNQZ9yieWYPl3cBIG-_AhfFos
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    # CC
                    recipient_list=[settings.ADMIN_EMAIL, 'grajesh2906@gmail.com'],
                    fail_silently=False,
                )
            # Render a specific HTML template upon successful form submission
            return render(req, "contact/contact_success.html")
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
from .models import Menu, Restaurant, RestaurantReview

def restaurant_detail(request, pk):
    # Fetch restaurant, menus, and reviews
    restaurant = get_object_or_404(Restaurant, pk=pk)
    menus = Menu.objects.filter(restaurant=restaurant).order_by('amount')
    reviews = RestaurantReview.objects.filter(restaurant=restaurant, is_approved=True)

    # Get the max_amount filter parameter
    max_amount = request.GET.get('max_amount', 1000)

    try:
        # Convert max_amount to an integer
        max_amount = int(max_amount)
    except ValueError:
        # Handle the case where max_amount is not a valid integer
        max_amount = 1000  # Default value

    # Apply the filter to the menus queryset
    menus = menus.filter(amount__lte=max_amount)

    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id')
        user_name = request.POST.get('user_name')
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')

        try:
            # Create a new review object
            restaurant = get_object_or_404(Restaurant, id=restaurant_id)
            review = RestaurantReview.objects.create(
                restaurant=restaurant,
                user_name=user_name,
                review_text=review_text,
                rating=rating
            )
            # Fetch updated data
            reviews = RestaurantReview.objects.filter(restaurant=restaurant, is_approved=True)

            # Return with success message
            return render(request, 'restaurant_details.html', {
                'alert_message': 'Review submitted successfully!',
                'restaurant': restaurant,
                'menus': menus,
                'reviews': reviews,
                'max_amount': max_amount,  # Pass the max_amount to the template
            })
        except ValueError:
            return render(request, 'restaurant_details.html', {
                'alert_message': 'Invalid data format.',
                'restaurant': restaurant,
                'menus': menus,
                'reviews': reviews,
                'max_amount': max_amount,  # Pass the max_amount to the template
            })

    return render(request, 'restaurant_details.html', {
        'restaurant': restaurant,
        'menus': menus,
        'reviews': reviews,
        'max_amount': max_amount,  # Pass the max_amount to the template
    })

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



#Raise a complaint 
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Complaint

def submit_complaint(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        restaurant_name = request.POST.get('restaurant_name')
        issue_description = request.POST.get('issue_description')
        raised_to = request.POST.get('raised_to')
        photo = request.FILES.get('photo')

        # Create and save the Complaint object
        complaint = Complaint(
            name=name,
            email=email,
            contact_number=contact_number,
            restaurant_name=restaurant_name,
            issue_description=issue_description,
            raised_to=raised_to,
            photo=photo
        )
        complaint.save()

        # Store details in session for displaying on the success page
        request.session['complaint_name'] = name
        request.session['complaint_email'] = email
        request.session['complaint_contact_number'] = contact_number
        request.session['complaint_restaurant_name'] = restaurant_name
        request.session['complaint_issue_description'] = issue_description
        request.session['complaint_raised_to'] = raised_to

        messages.success(request, 'Your complaint has been submitted successfully.')
        return redirect('complaint_submitted')  # Redirect to the success page
    
    return render(request, 'contact/complaint_form.html')

def complaint_submitted(request):
    # Assuming you pass the complaint details from the submit_complaint view using messages or context
    context = {
        'name': request.session.get('complaint_name'),
        'email': request.session.get('complaint_email'),
        'contact_number': request.session.get('complaint_contact_number'),
        'restaurant_name': request.session.get('complaint_restaurant_name'),
        'issue_description': request.session.get('complaint_issue_description'),
        'raised_to': request.session.get('complaint_raised_to')
    }
    return render(request, 'contact/complaintSubmitted.html', context)

