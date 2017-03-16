/**
 * Create a map with a marker.
 * Creating or dragging the marker sets the latitude and longitude values
 * in the input fields.
 */
;(function($) {

  // We'll insert the map after this element:
  var prev_el_selector = '.field-longitude';

  // The elements we'll put lat/lon into and use
  // to set the map's initial lat/lon.
  var lat_input_selector = '#id_latitude',
      lon_input_selector = '#id_longitude';

  // If we don't have a lat/lon in the input fields,
  // this is where the map will be centered initially.
  var initial_lat = 51.516448,
      initial_lon = -0.130463;

  // Initial zoom level for the map.
  var initial_zoom = 6;

  // Initial zoom level if input fields have a location.
  var initial_with_loc_zoom = 12;

  // Global variables. Nice.
  var map, marker, $lat, $lon;

  /**
   * Create HTML elements, display map, set up event listenerss.
   */
  function initMap() {
    $prevEl = $(prev_el_selector);
    if ($prevEl.length == 0) {
      // Can't find where to put the map.
      return;
    };

    $lat = $(lat_input_selector);
    $lon = $(lon_input_selector);

    var has_initial_loc = ($lat.val() && $lon.val());

    if (has_initial_loc) {
      // There is lat/lon in the fields, so centre the map on that.
      initial_lat = parseFloat($lat.val());
      initial_lon = parseFloat($lon.val());
      initial_zoom = initial_with_loc_zoom;
    };

    $prevEl.after( $('<div id="setloc-map"></div>') );

    map = new google.maps.Map(document.getElementById('setloc-map'), {
      zoom: initial_zoom,
      center: {lat: initial_lat, lng: initial_lon}
    });

    // Create but don't position the marker:
    marker = new google.maps.Marker({
      map: map,
      draggable: true,
    });

    if (has_initial_loc) {
      // There is lat/lon in the fields, so centre the marker on that.
      setMarkerPosition(initial_lat, initial_lon);
    };

    google.maps.event.addListener(map, 'click', function(ev) {
      setMarkerPosition(ev.latLng.lat(), ev.latLng.lng());
    });

    google.maps.event.addListener(marker, 'dragend', function() {
      setInputValues(marker.getPosition().lat(), marker.getPosition().lng());
    });
  };

  /**
   * Re-position marker and set input values.
   */
  function setMarkerPosition(lat, lon) {
    marker.setPosition({lat: lat, lng: lon});
    setInputValues(lat, lon);
  };

  /**
   * Set both lat and lon input values.
   */
  function setInputValues(lat, lon) {
    setInputValue($lat, lat);
    setInputValue($lon, lon);
  };

  /**
   * Set the value of $input to val, with the correct decimal places.
   * We work out decimal places using the <input>'s step value, if any.
   */
  function setInputValue($input, val) {
    // step should be like "0.000001".
    var step = $input.prop('step');
    var dec_places = 0;

    if (step) {
      if (step.split('.').length == 2) {
        dec_places = step.split('.')[1].length;
      };

      val = val.toFixed(dec_places);
    };

    $input.val(val);
  };

  $(document).ready(function(){
    initMap();
  });

})(django.jQuery);

