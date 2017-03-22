/**
 * For displaying the map on the VenueDetail page.
 *
 * Expects there to be two variables declared:
 *  spectator_map_latitude
 *  spectator_map_longitude
 *
 * And for there to be a div, sized appropriately, with an ID of 'venue-map'.
 *
 * Include the Google Maps Javascript API file like:
 * https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=spectatorInitMap
 */
function spectatorInitMap() {
  var lat = typeof spectator_map_latitude !== 'undefined' ? spectator_map_latitude : '';
  var lon = typeof spectator_map_longitude !== 'undefined' ? spectator_map_longitude : '';

  if ( ! lat || ! lon) {
    return;
  };

  var position = {lat: parseFloat(lat), lng: parseFloat(lon)};

  var map = new google.maps.Map(document.getElementById('venue-map'), {
    zoom: 12,
    center: position
  });

  var marker = new google.maps.Marker({
    map: map,
    position: position
  });
};

