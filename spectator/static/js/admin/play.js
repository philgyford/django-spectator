/**
 * Used on the PlayAdmin change form.
 * Adds the ID of the play to the 'Add new event' link in PlayProductionInline
 * that links to the PlayProduction add form, so that our JS on that page can
 * use it.
 *
 * Ideally these arguments would be added to the URL in PlayProductionInline,
 * but I can't work out how to access the PlayProduction's parent model (i.e.
 * the Play) from there.
 *
 * So this is a bit of a likely-to-break hack.
 *
 * We pass ?play_id=123 in the URL.
 */
;(function($) {

  function addToLink() {
    var $link = $('.js-add-event-link').first();
    if ( ! $link) {
      return;
    };

    var url = window.location.href;
    var regex = new RegExp(".*/play/([0-9]+)/change/?");
    var results = regex.exec(url);
    if (results && results.length > 1) {
      var play_id = results[1];
      var add_link = $link.prop('href');
      $link.prop('href', add_link + '?play_id=' + play_id);
    };
  };

  $(document).ready(function(){
    addToLink();
  });

})(django.jQuery);
