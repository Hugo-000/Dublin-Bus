const center = { lat: 53.3498, lng: -6.2603 };
// Create a bounding box with sides ~10km away from the center point
const defaultBounds = {
    north: center.lat + 0.28949,
    south: center.lat - 0.218991,
    east: center.lng + 0.256544,
    west: center.lng - 0.390267,
};

const options = {
    bounds: defaultBounds,
    componentRestrictions: { country: "ie" },
    fields: ["address_components", "geometry", "icon", "name"],
    strictBounds: false,
};
try {
    new google.maps.places.Autocomplete(document.getElementById("id_origin_location"), options);
    new google.maps.places.Autocomplete(document.getElementById("id_destination_location"), options);
}
catch (error) {

}

try{
    new google.maps.places.Autocomplete(document.getElementById("id_address"), options);
} catch (error) {

}