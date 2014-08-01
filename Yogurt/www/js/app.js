require.config({
    paths: {
	jquery: '/js/lib/jquery/dist/jquery',
	angular: '/js/lib/angular/angular',
	domReady: '/js/lib/requirejs-domready/domReady'
    },
    shim: {
	'angular': {
	    exports: 'angular'
        }
    }
});

define("app", ["angular"], function(angular) {
    var app = angular.module("phonecatApp", []);
    
    app.controller('PhoneListCtrl', function ($scope) {
	$scope.phones = [
	    {'name': 'Nexus S',
	     'snippet': 'Fast just got faster with Nexus S.'},
	    {'name': 'Motorola XOOM™ with Wi-Fi',
	     'snippet': 'The Next, Next Generation tablet.'},
	    {'name': 'MOTOROLA XOOM™',
	     'snippet': 'The Next, Next Generation tablet.'}
	];
    });

    return app;
});
