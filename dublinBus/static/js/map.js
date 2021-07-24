function initMap() {
    // Initializes the map on the page //
    
    // Creates the map //
    const map = createMap();

    // If there is no map created then do nothing
    if (!map) return;

    // prints the information pertaining to the map in the console //
    console.log(map);

    // calls a function to add controlability to the map //
    addControls(map);

    // calls funcntion to get a route for the map //
    getRoute(map);
}


function addControls(map) {

    // function to add controls to the map for current location //

    // create the location information window and a button // 
    const locationWindow = new google.maps.InfoWindow();
    const locationButton = document.createElement("button");

    // assign the attributes to the button //
    locationButton.textContent = "Current Location";
    locationButton.classList.add("custom-map-control-button");

    // set the location of the button //
    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(locationButton);

    // Enable the button to listen to a click and onclick move to current location //
    locationButton.addEventListener("click", () => {
        // if Browser doesn't support Geolocation return error //
        if (!navigator.geolocation) return handleLocationError("type3", locationWindow, map.getCenter());

        // else assume browser has geoloction enabled
        navigator.geolocation.getCurrentPosition(
            // set the latitude and longitude of the map restrictions
            ({ coords: { latitude, longitude } }) => {
            //Due to the area of the map is restricted, there needs to check if the user is near the staions
            if (latitude > 53.365 || latitude < 53.325 || longitude > -6.2307 || longitude < -6.3101) {
                // if user not within the coordinates fro restriction produce an error
                handleLocationError("type1", locationWindow, map.getCenter());

            } else {
                // if user is within the restricted area set the position
                locationWindow.setPosition({
                    lat: latitude,
                    lng: longitude,
                });
                // show the current location on the map
                locationWindow.setContent("Location found.");
                locationWindow.open(map);
            }
        // if the geo location functionality fails produce an error
        }, () => handleLocationError("type2", locationWindow, map.getCenter()));
    });
}
function createMap() {
    const element = document.getElementById("map");

    if (!element) return;
    
    // build a map in night time mode
    // assign the map to the element identified as map
    return new google.maps.Map(element, {
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
}


function handleLocationError(browserProblem, locationWindow, pos) {
    // convert the error types into human understandable error codes 
    locationWindow.setPosition(pos); // why do we need this?????
    if (browserProblem=="type1"){
            var problem="Error: Currently there is no station near your position"
    }else{
            if (browserProblem=="type2"){
                var problem="Error: The Geolocation service failed."
            } else {
                var problem="Error: Your browser doesn't support geolocation."
            }
    };
    locationWindow.setContent(problem);
    locationWindow.open(map);
}; 


function getRoute(map) {
    // 

    // If Django adds error list class (i.e. the form is invalid)
    // don't attempt to get the route
    if (document.querySelector('.errorlist')) return;

    const origin = document.querySelector('#id_origin_location').value;
    const destination = document.querySelector('#id_destination_location').value;

    // If there is no value for origin or desitnation return
    if (!origin || !destination) return;

    try {
        const directionsService = new google.maps.DirectionsService();
        const directionsDisplay = new google.maps.DirectionsRenderer();

        var userUnixDate = document.getElementById("userUnixDate").textContent;
        console.log(document.getElementById("userUnixDate").textContent)
        console.log(userUnixDate)
        console.log(new Date(1626081706 * 1000))
        const requestOpts = {
            origin,
            destination,
            travelMode: google.maps.DirectionsTravelMode.TRANSIT,
            transitOptions: {
                departureTime: new Date(userUnixDate  * 1000),
                modes: ['BUS'],
                routingPreference: 'FEWER_TRANSFERS'    //LESS_WALKING is the alternative
            },
            //provideRouteAlternatives: false,            //When True provides alternative routes
        };

        directionsDisplay.setMap(map);
        directionsDisplay.setPanel(document.getElementById('panel'));

        console.log('directions', directionsDisplay)

        const directionsResult = directionsService.route(requestOpts);
        console.log('Results', directionsResult)

        // directionsResult.then(response => {
        //     let legs = [];
            
        //     response.routes.forEach(route => {
        //         legs = legs.concat(route.legs);
        //     });

        //     let steps = legs[0]['steps'];
        //     let travel_modes = [];

        //     steps.forEach(element => travel_modes.concat(element['travel_mode']))

        //     // for (let step = 0; step < length(); step++) {
        //     //     console.log('Walking east one step');
        //     // }

        //     console.log('legs', legs[0]);
        //     console.log('======');
        //     console.log('steps', steps);
        //     console.log('======');
            

        //     const l = response.routes.reduce((accumulator, route) => [...accumulator, ...route.legs], []);
        //     console.log('Legs', l);
        // })  

        directionsService.route(requestOpts, (...args) => handleRouteResponse(directionsDisplay, ...args));
    } catch(e) {
        console.log('e', e);
    }
}

function handleRouteResponse(directionsDisplay, response, status) {
    if (status == google.maps.DirectionsStatus.OK) {

        // response.then(result => {           
            const s = response.routes
                .reduce((accumulator, route) => [...accumulator, ...route.legs], [])
                .reduce((accumulator, leg) => [...accumulator, ...leg.steps], []);

            console.log('steps Jen', s);

            const l = response.routes
                .reduce((accumulator, route) => [...accumulator, ...route.legs], [])
                .reduce((accumulator, leg) => [...accumulator, ...leg.steps], [])
                .map(step => ({ distance: step.distance, duration: step.duration, instructions: step.instructions, transit: step.transit, travel_mode: step.travel_mode }));
            console.log('steps Jen', l);

        fetch('/dublinBusHybrid/journeyPlanner/', {
            method: 'POST',
            credentials: 'include',     
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json; charset=UTF-8',
                'X-CSRFToken': getCSRFToken()
            },

            body: JSON.stringify({
                'travel_date': document.querySelector('#id_travel_date').value,
                'travel_time': document.querySelector('#id_travel_time').value + ':00',
                'Steps': l,
            })
        }).then(r => console.log('r', r));

        directionsDisplay.setDirections(response);


        // Setup loading screen
        // Give the server the details
        // .then(do the stuff)

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
}

// get a csrf token from the page by selecting the input element and
// returning the value
function getCSRFToken() {
    return document.querySelector('[name="csrfmiddlewaretoken"]').value;
}