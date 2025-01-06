/**
 * For displaying the map on the VenueDetail page.
 *
 * Expects there to be three variables declared:
 *  spectator_map_latitude
 *  spectator_map_longitude
 *  spectator_map_config
 *
 * And for there to be a div, sized appropriately, with a class of
 * 'js-venue-map-container'.
 *
 * spectator_map_config should be set for one of the supported map libraries,
 * and the releveant CSS, and JS for the library should have been included in
 * the page. See the Django Spectator docs for more details.
 *
 * 1. Google
 *  {
 *    "library": "google"
 *  }
 *
 * 2. Mabox
 *  {
 *    "library": "mapbox",
 *    "tile_style": "mapbox://styles/mapbox/light-v10"
 *  }
 */
function spectatorInitMap() {
  var lat =
    typeof spectator_map_latitude !== "undefined" ? spectator_map_latitude : "";
  var lon =
    typeof spectator_map_longitude !== "undefined"
      ? spectator_map_longitude
      : "";
  var mapConfig =
    typeof spectator_map_config !== "undefined" ? spectator_map_config : false;

  if (!lat || !lon || !mapConfig) {
    return;
  }

  // Create the map element.
  var container = document.getElementsByClassName("js-venue-map-container")[0];
  container.innerHTML = '<div class="js-venue-map venue-map"></div>';

  var mapEl = document.getElementsByClassName("js-venue-map")[0];

  var map;

  // Create the map and marker depending on which library we're using...

  if (mapConfig.library === "google") {
    var position = { lat: parseFloat(lat), lng: parseFloat(lon) };

    var tileStyle = mapConfig.tile_style ? mapConfig.tile_style : "roadmap";

    map = new google.maps.Map(mapEl, {
      zoom: 12,
      center: position,
      mapTypeId: tileStyle,
    });

    new google.maps.Marker({
      map: map,
      position: position,
    });
  } else if (mapConfig.library == "mapbox") {
    var position = [parseFloat(lon), parseFloat(lat)];

    var tilesStyle = "mapbox://styles/mapbox/streets-v11";
    if (mapConfig.tile_style) {
      tileStyle = mapConfig.tile_style;
    }

    map = new mapboxgl.Map({
      container: mapEl,
      center: position,
      style: tileStyle,
      zoom: 11,
    });

    map.addControl(new mapboxgl.NavigationControl());

    // Create and add marker
    var el = document.createElement("div");
    el.className = "spectator-marker"; // The CSS classname
    new mapboxgl.Marker(el, { anchor: "bottom" })
      .setLngLat(position)
      .addTo(map);
  }
}
