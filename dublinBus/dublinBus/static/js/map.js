function initMap() {
    /*Build the map, currently no transit layer*/
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: { lat: 53.349804, lng: -6.260310 },
        /*Disable the default map ui*/
        disableDefaultUI: true,
        /*restrict the boundary of map*/
        restriction: {
            latLngBounds: {
                north: 54,
                south: 53,
                west: -6.4,
                east: -6.2,
            },
            strictBounds: false
        },
        /*Change the map into Nightmode*/
        styles: [
            {elementType: "geometry", stylers: [{ color: "#242f3e" }]},
            {elementType: "labels.text.stroke",stylers: [{ color: "#242f3e" }]},
            {elementType: "labels.text.fill",stylers: [{ color: "#746855" }]},
            {featureType: "administrative.locality",elementType: "labels.text.fill",stylers: [{ color: "#d59563" }]},
            {featureType: "poi",elementType: "labels.text.fill",stylers: [{ color: "#d59563" }]},
            {featureType: "poi.park",elementType: "geometry",stylers: [{ color: "#263c3f" }]},
            {featureType: "poi.park",elementType: "labels.text.fill",stylers: [{ color: "#6b9a76" }]},
            {featureType: "road",elementType: "geometry",stylers: [{ color: "#38414e" }]},
            {featureType: "road",elementType: "geometry.stroke",stylers: [{ color: "#212a37" }]},
            {featureType: "road",elementType: "labels.text.fill",stylers: [{ color: "#9ca5b3" }]},
            {featureType: "road.highway",elementType: "geometry",stylers: [{ color: "#746855" }]},
            {featureType: "road.highway",elementType: "geometry.stroke",stylers: [{ color: "#1f2835" }]},
            {featureType: "road.highway",elementType: "labels.text.fill",stylers: [{ color: "#f3d19c" }]},
            {featureType: "transit",elementType: "geometry",stylers: [{ color: "#2f3948" }]},
            {featureType: "transit.station",elementType: "labels.text.fill",stylers: [{ color: "#d59563" }]},
            {featureType: "water",elementType: "geometry",stylers: [{ color: "#17263c" }]},
            {featureType: "water",elementType: "labels.text.fill",stylers: [{ color: "#515c6d" }]},
            {featureType: "water",elementType: "labels.text.stroke",stylers: [{ color: "#17263c" }]},
        ]   
    });
    console.log(map)
    

    /*Build the move to current location function with Geolocation*/
    const locationWindow = new google.maps.InfoWindow();
    const locationButton = document.createElement("button");
    locationButton.textContent = "Current Location";
    locationButton.classList.add("custom-map-control-button");
    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(
                locationButton
            );
    locationButton.addEventListener("click", () => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const pos = {
                            lat: position.coords.latitude,
                            lng: position.coords.longitude,
                        };
                    //Due to the area of the map is restricted, there needs to check if the user is near the staions
                    if (position.coords.latitude>53.365||position.coords.latitude<53.325||position.coords.longitude>-6.2307||position.coords.longitude<-6.3101){
                            handleLocationError("type1", locationWindow, map.getCenter());
                    }else{
                            locationWindow.setPosition(pos);
                            locationWindow.setContent("Location found.");
                            locationWindow.open(map);
                    }
                },() => {
                    handleLocationError("type2", locationWindow, map.getCenter());
                        });
            } else {
                // Browser doesn't support Geolocation
                handleLocationError("type3", locationWindow, map.getCenter());
            }
        });
        
    /*handle Location Error*/
    function handleLocationError(browserProblem, locationWindow, pos) {
        locationWindow.setPosition(pos);
        if (browserProblem=="type1"){
                var problem="Error: Currently there is no station near your position"
        }else{
                if (browserProblem=="type2"){
                    var problem="Error: The Geolocation service failed."
                }else{
                    var problem="Error: Your browser doesn't support geolocation."
                }
        };
        locationWindow.setContent(problem);
        locationWindow.open(map);
    };
    
    
    
    // /*Direction from two selected stop position*/
    // const directionsRenderer = new google.maps.DirectionsRenderer();
    // const directionsService = new google.maps.DirectionsService();
    // directionsRenderer.setMap(map);
    
    // const onChangeHandler = function () {
    //     calculateAndDisplayRoute(directionsService, directionsRenderer);
    // };
    
    // document.getElementById("start").addEventListener("change", onChangeHandler);
    // document.getElementById("end").addEventListener("change", onChangeHandler);
    

    //function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    //     directionsService.route({
    //         origin: {query: document.getElementById("start").value,},
    //         destination: {query: document.getElementById("end").value,},
    //         travelMode: google.maps.TravelMode.TRANSIT,
    //         transitOptions: {
    //             departureTime: new Date(getElementById("userUnixDate")),
    //             modes: ['BUS'],
    //             routingPreference: 'FEWER_TRANSFERS'
    //         },
    //     },(response, status) => {
    //         if (status === "OK") {
    //             directionsRenderer.setDirections(response);
    //         } else {
    //             window.alert("Directions request failed due to " + status);
    //         }
    //     });
    // }

    /*Search for a stop with Geocoder, this function needs to be merged into Routes part*/ 
    const geocoder = new google.maps.Geocoder();
    const searchwindow = new google.maps.InfoWindow();
    // document.getElementById("submit").addEventListener("click", () => {
    //     searchwindow.close();
    //     geocodeLatLng(geocoder, map, searchwindow);
    // });

    function geocodeLatLng(geocoder, map, searchwindow) {
        var searchInput=document.getElementById("search_datalist").value;
        console.log("aa");
        if(!searchInput) return;
        console.log("aa");
        var position= document.querySelector("#station_datalist"+" option[value='"+searchInput+"']").dataset.value;
        const latlngStr = position.split(",", 2);
        const latlng = {
            lat: parseFloat(latlngStr[0]),
            lng: parseFloat(latlngStr[1]),
        };
        geocoder.geocode({ location: latlng }, (results, status) => {
            if (status === "OK") {
                if (results[0]) {
                    map.setZoom(14);
                    const marker = new google.maps.Marker({
                        position: latlng,
                        map: map,
                        });
                    searchwindow.setContent(results[0].formatted_address);
                    searchwindow.open(map, marker);
                    marker.setMap(null);
                } else {
                    window.alert("No results found");
                }
            } else {
                window.alert("Geocoder failed due to: " + status);
            }
        });
    }
    getRoute(map);
}





function getRoute(map) {
    // If Django adds error list class (i.e. the form is invalid)
    // don't attempt to get the route
    if (document.querySelector('.errorlist')) return;

    try {
        const directionsService = new google.maps.DirectionsService();
        const directionsDisplay = new google.maps.DirectionsRenderer();

        const origin = document.querySelector('#id_origin_location').value;
        const destination = document.querySelector('#id_destination_location').value;

        var userUnixDate = document.getElementById("userUnixDate").textContent;
        console.log(document.getElementById("userUnixDate").textContent)
        console.log(userUnixDate)
        console.log(new Date(1626081706 * 1000))
        const request = {
            origin,
            destination,
            travelMode: google.maps.DirectionsTravelMode.TRANSIT,
            transitOptions: {
                departureTime: new Date(userUnixDate  * 1000),
                modes: ['BUS'],
                routingPreference: 'FEWER_TRANSFERS'
            },
        };

        

        directionsDisplay.setMap(map);
        directionsDisplay.setPanel(document.getElementById('panel'));

        directionsService.route(request, function(response, status) {
            if (status == google.maps.DirectionsStatus.OK) {
                // Setup loading screen
                // Give the server the details
                // .then(do the stuff)

                directionsDisplay.setDirections(response);

                console.log(response)
                response.routes.forEach(r => {
                    r.legs.forEach(l => {
                        l.steps.forEach(s => {
                            if (s.transit) {
                                console.log("s", s)
                                console.log('arrival_stop', s.transit)

                            }

                        })

                    })
                });
            }
        });


        
        console.log(directionsService)
    } catch(e) {
        console.log('e', e);
    }

}