from django.db import models

class Restaurant(models.Model):
    STYLE_CHOICES = [
        ('Indian', 'Indian'),
        ('North Indian', 'North Indian'),
        ('South Indian', 'South Indian'),
        ('Chinese', 'Chinese'),
        ('Indian, North Indian, Chinese', 'Indian, North Indian, Chinese'),
        ('Asian', 'Asian'),
        ('Italian', 'Italian'),
        ('French', 'French'),
        ('American', 'American'),
        ('Mexican', 'Mexican'),
        ('Japanese', 'Japanese'),
        ('Chinese', 'Chinese'),
        ('Thai', 'Thai'),
        ('Mediterranean', 'Mediterranean'),
        ('Middle Eastern', 'Middle Eastern'),
        ('Greek', 'Greek'),
        ('Spanish', 'Spanish'),
        ('Korean', 'Korean'),
        ('Vietnamese', 'Vietnamese'),
        ('German', 'German'),
        ('Caribbean', 'Caribbean'),
        ('African', 'African'),
        ('Seafood', 'Seafood'),
        ('Vegetarian', 'Vegetarian'),
        ('Vegan', 'Vegan'),
    ]


    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    website_link = models.URLField(blank=True, null=True)
    google_map_link = models.URLField(blank=True, null=True)
    opening_hours = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=11, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    restaurant_style = models.CharField(max_length=50, choices=STYLE_CHOICES)

    def __str__(self):
        return self.name

class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_images/')

    def __str__(self):
        return f"Image for {self.restaurant.name}"
