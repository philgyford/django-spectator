/**
 * For displaying the map on the VenueDetail page.
 *
 * Expects there to be two variables declared:
 *  spectator_map_latitude
 *  spectator_map_longitude
 *
 * And for there to be a div, sized appropriately, with a class of
 * 'js-venue-map-container'.
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

  var container = document.getElementsByClassName('js-venue-map-container')[0];
  container.innerHTML = '<div class="js-venue-map venue-map"></div>';

  var position = {lat: parseFloat(lat), lng: parseFloat(lon)};

  var mapEl = document.getElementsByClassName('js-venue-map')[0];

  var map = new google.maps.Map(mapEl, {
    zoom: 12,
    center: position
  });

  var marker = new google.maps.Marker({
    map: map,
    position: position
  });
};

