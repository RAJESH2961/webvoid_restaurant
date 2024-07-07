           // Function to fetch user location
            // Call getLocation when the page loads
            window.onload = fetchUserLocation;
           
            function fetchUserLocation() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(showPosition, showError, {
                        enableHighAccuracy: true,
                        timeout: 10000,
                        maximumAge: 0
                    });
                } else {
                    alert("Geolocation is not supported by this browser.");
                }
            }
            
            // Success callback function for fetching location
            function showPosition(position) {
                var latitude = position.coords.latitude;
                var longitude = position.coords.longitude;

                
            
                console.log(latitude)
                console.log(longitude)
             
            
             
                        // Set the values of hidden fields
                        document.getElementById('latitudeDisplay').value = latitude;
                        document.getElementById('longitudeDisplay').value = longitude;
            
                // Call the function to get the city name
                getCityName(latitude, longitude);
            }
            
            // Error callback function for fetching location
            function showError(error) {
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        alert("User denied the request for Geolocation.");
                        break;
                    case error.POSITION_UNAVAILABLE:
                        alert("Location information is unavailable.");
                        break;
                    case error.TIMEOUT:
                        alert("The request to get user location timed out.");
                        break;
                    case error.UNKNOWN_ERROR:
                        alert("An unknown error occurred.");
                        break;
                }
            }
            // Add event listener to the button
            document.querySelector('.search-nearby-btn').addEventListener('click', function(event) {
                event.preventDefault();
                fetchUserLocation();
            });
            
            
            // Getting City name using nominatim Open street API
            async function getCityName(latitude, longitude) {
                        const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&addressdetails=1`;
                        try {
                            const response = await fetch(url);
                            const data = await response.json();
                            const city = data.address.city || data.address.town || data.address.village || "City not found";
            
                            document.getElementById("city").textContent = city;
                            // document.getElementById("city1").textContent = `Displaying Restaurants in ${city}`;
                            document.getElementById("city1").textContent = `Your Location : ${city}`;
                        } catch (error) {
                            console.error("Error fetching city name:", error);
                        }
                    }
               