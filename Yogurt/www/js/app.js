require.config({
    paths: {
	jquery: '/js/lib/jquery/dist/jquery',
	bootstrap: '/js/lib/bootstrap/dist/js/bootstrap.min.js',

	angular: '/js/lib/angular/angular',
	angularRoute: '/js/lib/angular-route/angular-route',
	angularBootstrap: '/js/lib/angular-bootstrap/ui-bootstrap-tpls'
    },
    shim: {
	'angularBootstrap': {
	    deps: ['angular'],
	    exports: 'angular'
	},
	'angularRoute': {
	    deps: ['angular'],
	    exports: 'angular'
	},
	'angular': {
	    deps: ['jquery'],
	    exports: 'angular'
        }
    },
    deps: ['app']
});

define('app', ["jquery", "angular", "angularBootstrap", "angularRoute"], function($, angular) {
    var app = angular.module("FringeApp", ['ngRoute', 'ui.bootstrap']);

    app.controller("sidebar", function($scope, $location) {
	$scope.$on('$locationChangeSuccess', function(event) {
	    $scope.tab = $location.path()
	})
    })

    app.config(
	['$routeProvider', function($routeProvider)
	 {
	     $routeProvider
		 .when('/about', {
		     templateUrl: 'about.html',
		     controller: ''
		 })
		 .when('/upcoming', {
		     templateUrl: 'listview.html',
		     controller: 'upcoming'
		 })
		 .when('/live', {
		     templateUrl: 'listview.html',
		     controller: 'live'
		 })
		 .when('/streams', {
		     templateUrl: 'streams.html',
		     controller: 'streams'
		 })
		 .when('/vods', {
		     templateUrl: 'vods.html',
		     controller: 'vods'
		 })
		 .when('/', {
		     redirectTo: "/about"
		 })
	 }
	]
    )
    
    app.controller ('upcoming', function ($scope, $http) {
	$http.get ('/api/upcoming').success(function(data) {
	    $scope.data = data ['events']
	})
	$scope.name = 'Upcoming Events'
	$scope.oneAtATime = true;
    })

    app.controller ('live', function ($scope, $http) {
	$http.get ('/api/live').success(function(data) {
	    $scope.data = data ['live_events']
	})
	$scope.name = 'Live Events'
	$scope.oneAtATime = true;
    })

     app.controller ('streams', function ($scope, $http) {
	$http.get ('/api/streams').success(function(data) {
	    $scope.data = data ['starcraft2']
	})
	$scope.oneAtATime = true;
    })
    
    angular.bootstrap(document, ['FringeApp']);
    return app;
});
