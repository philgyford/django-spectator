/**
 * For the Admin Event Change form.
 *
 * This shows/hides the Movie, Play, Classical Works and Dance Pieces
 * fields depending on what Event Kind is chosen in the select field.
 *
 * Because those fields take up a lot of space, which is annoying if
 * most/all of them aren't relevant.
 */
;(function($) {

  /**
   * Set up initial state.
   */
  function initEventAdmin() {
    setUpFromSelect();

    $('#id_kind').change(function() {
      setUpFromSelect();
    });
  };

  /**
   * Look at the event kind in the select field and initialise the showing/
   * hiding of fields based on that.
   */
  function setUpFromSelect() {
    var event_kind = $('#id_kind').val();

    if (event_kind) {
      setForEventKind(event_kind);
    };
  };

  /**
   * Translate from the event_kind used as the value in the select field
   * to the name of the field, if any, that we want to show.
   */
  function setForEventKind(event_kind) {
    if (event_kind == 'movie') {
      setVisibility('movie');
    } else if (event_kind == 'play') {
      setVisibility('play');
    } else if (event_kind == 'concert') {
      setVisibility('classicalworks');
    } else if (event_kind == 'dance') {
      setVisibility('dancepieces');
    } else {
      // Comedy, Gig, etc don't have field to show:
      setVisibility(false);
    };
  };

  /**
   * Show/hide the relevant field.
   * Even if we're going to hide a field, because it's not relevant to the
   * event kind, we'll show it if it has errors, so the user can correct
   * them.
   */
  function setVisibility(fieldToShow) {
    var fields = ['movie', 'play', 'classicalworks', 'dancepieces'];

    $.each(fields, function(n, field) {
      var $el = $('.form-row.field-'+field);

      if (field == fieldToShow) {
        $el.slideDown();
      } else if ($el.hasClass('errors')) {
        $el.slideDown();
      } else {
        $el.slideUp();
      };
    });
  };

  $(document).ready(function(){
    initEventAdmin();
  });

})(django.jQuery);
