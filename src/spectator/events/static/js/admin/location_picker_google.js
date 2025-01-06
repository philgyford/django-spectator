/**
 * Create a Google map with a marker.
 * Creating or dragging the marker sets values in the form's input fields.
 * This is a slight variation on the location_picker_mapbox.js version.
 *
 * This assumes we have four fields on our model:
 *
 *  Latitude -  e.g. DecimalField(max_digits=9, decimal_places=6,
 *  Longitude - e.g. DecimalField(max_digits=9, decimal_places=6,
 *  Address - CharField
 *  Country - Charfield, expecting a two-letter code like US, FR or GB.
 *
 * See spectator.models.events.Venue.
 *
 * Also requires:
 *
 *  Including the Google Maps JavaScript API.
 *  Using CSS to give div.setloc-map a width and height.
 */
(function ($) {
  // We'll insert the map after this element:
  var prev_el_selector = ".form-row.field-country";

  // The input elements we'll put lat/lon into and use
  // to set the map's initial lat/lon.
  var lat_input_selector = "#id_latitude",
    lon_input_selector = "#id_longitude";

  // The input elements we'll put the address string and country code into.
  var address_input_selector = "#id_address",
    country_input_selector = "#id_country";

  // If we don't have a lat/lon in the input fields,
  // this is where the map will be centered initially.
  var initial_lat = 51.516448,
    initial_lon = -0.130463;

  // Initial zoom level for the map.
  var initial_zoom = 6;

  // Initial zoom level if input fields have a location.
  var initial_with_loc_zoom = 12;

  // Global variables. Nice.
  var mapConfig, geocoder, map, marker, $lat, $lon, $address, $country;

  /**
   * Create HTML elements, display map, set up event listenerss.
   */
  function initMap() {
    mapConfig =
      typeof spectator_map_config !== "undefined"
        ? spectator_map_config
        : false;

    if (mapConfig === false) {
      console.error("The spectator_map_config variable is not set");
      return;
    }

    var $prevEl = $(prev_el_selector);

    if ($prevEl.length === 0) {
      // Can't find where to put the map.
      console.error("Can't find where to insert the map element");
      return;
    }

    $lat = $(lat_input_selector);
    $lon = $(lon_input_selector);
    $address = $(address_input_selector);
    $country = $(country_input_selector);

    var has_initial_loc = $lat.val() && $lon.val();

    if (has_initial_loc) {
      // There is lat/lon in the fields, so centre the map on that.
      initial_lat = parseFloat($lat.val());
      initial_lon = parseFloat($lon.val());
      initial_zoom = initial_with_loc_zoom;
    }

    $prevEl.after($('<div class="js-setloc-map setloc-map"></div>'));

    var mapEl = document.getElementsByClassName("js-setloc-map")[0];

    var tileStyle = mapConfig.tile_style ? mapConfig.tile_style : "roadmap";

    map = new google.maps.Map(mapEl, {
      zoom: initial_zoom,
      center: { lat: initial_lat, lng: initial_lon },
      mapTypeId: tileStyle,
    });

    geocoder = new google.maps.Geocoder();

    // Create but don't position the marker:
    marker = new google.maps.Marker({
      map: map,
      draggable: true,
    });

    if (has_initial_loc) {
      // There is lat/lon in the fields, so centre the marker on that.
      setMarkerPosition(initial_lat, initial_lon);
    }

    google.maps.event.addListener(map, "click", function (ev) {
      setMarkerPosition(ev.latLng.lat(), ev.latLng.lng());
      setInputValues(ev.latLng.lat(), ev.latLng.lng());
    });

    google.maps.event.addListener(marker, "dragend", function () {
      setInputValues(marker.getPosition().lat(), marker.getPosition().lng());
    });
  }

  /**
   * Re-position marker.
   */
  function setMarkerPosition(lat, lon) {
    marker.setPosition({ lat: lat, lng: lon });
  }

  /**
   * Set the values of all the input fields, including getting the
   * geocoded data for address and country, based on lat and lon.
   */
  function setInputValues(lat, lon) {
    setLatLonInputValue($lat, lat);
    setLatLonInputValue($lon, lon);

    geoCode(lat, lon, function (geocoded) {
      if (geocoded["address"]) {
        $address.val(geocoded["address"]);
      }
      if (geocoded["country"]) {
        $country.val(geocoded["country"]);
      }
    });
  }

  /**
   * Set the value of $input to val, with the correct decimal places.
   * We work out decimal places using the <input>'s step value, if any.
   */
  function setLatLonInputValue($input, val) {
    // step should be like "0.000001".
    var step = $input.prop("step");
    var dec_places = 0;

    if (step) {
      if (step.split(".").length == 2) {
        dec_places = step.split(".")[1].length;
      }

      val = val.toFixed(dec_places);
    }

    $input.val(val);
  }

  /**
   * Get an address and a country code for the given lat and lon.
   * callback is the function to call with the data once ready.
   * Returns an object with 'address' and 'country' elements, like:
   *
   * {address: "Colchester, Essex, England", country: "GB"}
   * {address: "Houston, Harris County, Texas", country: "US"}
   */
  function geoCode(lat, lon, callback) {
    var geocoded = { address: "", country: "" };

    geocoder.geocode(
      { location: { lat: lat, lng: lon } },
      function (results, status) {
        if (status === "OK") {
          if (results[0]) {
            var components = results[0].address_components;
            var address_parts = [];
            // The elements we want to get from the components:
            var wanted = [
              "postal_town",
              "locality",
              "administrative_area_level_2",
              "administrative_area_level_1",
            ];

            for (var n = 0; n < components.length; n++) {
              var name = components[n].long_name;
              var type = components[n].types[0];
              if (
                $.inArray(type, wanted) >= 0 &&
                $.inArray(name, address_parts) == -1
              ) {
                address_parts.push(name);
              }
              if (type == "country") {
                geocoded["country"] = components[n].short_name;
              }
            }

            geocoded["address"] = address_parts.join(", ");
          } else {
            alert("No geocoding results found");
          }
        } else {
          alert("Geocoding failed due to: " + status);
        }
        callback(geocoded);
      },
    );
  }

  $(document).ready(function () {
    initMap();
  });
})(django.jQuery);
