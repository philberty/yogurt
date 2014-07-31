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

define(['jquery', 'angular'], function ($, angular) {
    var phonecatApp = angular.module('phonecatApp', []);	
    console.log (phonecatApp.controller)
});
