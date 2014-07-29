require.config({
    paths: {
	jquery: '/js/lib/jquery/jquery',
	angular: '/js/lib/angular/angular',
	feeds: '/js/feeds'
    }
});

define(['jquery', 'angular', 'feeds'], function ($, Angular, Feeds) {
    console.log ('Loaded this dependancies!')
    Feeds.upcoming ()
});
