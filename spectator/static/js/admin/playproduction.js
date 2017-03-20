/**
 * So that we can provide the ID of a Play from the Play change form and
 * have it filled in the correct field on the PlayProduction change form.
 *
 * We can pass ?play_id=123 in the URL.
 */
;(function($) {

  function populatePlayId() {
    var $input = $('#id_play').first();
    if ( ! $input) {
      return;
    } else if ($input.val() != '') {
      // Already something in the field.
      return;
    };

    var play_id = getParamByName('play_id');
    if (play_id) {
      $input.val(play_id);
    };
  };

  function getParamByName(name) {
    var url = window.location.href;
    var regex = new RegExp("[?&]"+name+"(=([^&#]*)|&|#|$)");
    var results = regex.exec(url);
    if (!results) {
      return null;
    };
    if (!results[2]) {
      return '';
    };
    return decodeURIComponent(results[2].replace(/\+/g, " "));
  };

  $(document).ready(function(){
    populatePlayId();
  });

})(django.jQuery);

