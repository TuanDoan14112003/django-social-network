var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    onBeforePageLoad: function () {
      $('.loader-bars').show();
    },
    onAfterPageLoad: function ($items) {
      $('.loader-bars').hide();
    }
  });