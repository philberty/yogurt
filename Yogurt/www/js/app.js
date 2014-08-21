require.config({
    paths: {
	jquery: '/js/lib/jquery/dist/jquery',
	angularRoute: '/js/lib/angular-route/angular-route',
	angular: '/js/lib/angular/angular',
	bootstrap: '/js/lib/bootstrap/dist/js/bootstrap.min.js'
    },
    shim: {
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

define('app', ["jquery", "angular", "angularRoute"], function($, angular) {
    var app = angular.module("FringeApp", ['ngRoute']);

    app.controller("sidebar", function($scope, $location) {
	$scope.$on('$locationChangeSuccess', function(event) {
	    $scope.tab = $location.path()
	})
    })

    app.controller ('live', ['$scope', '$http',
				 function($scope, $http) {
				     $http.get ('/api/live').success(function(data) {
					 $scope.data = data ['live_events']
				     })
				 }])

    app.controller ('upcoming', ['$scope', '$http',
				 function ($scope, $http) {
				     $http.get ('/api/upcoming').success(function(data) {
					 $scope.data = data ['events']
				     })
				 }])

    app.controller ('streams', ['$scope', '$http',
				 function ($scope, $http) {
				     $http.get ('/api/streams').success(function(data) {
					 $scope.data = data ['starcraft2']
				     })
				 }])

    app.controller ('leagues', ['$scope', '$http',
				function ($scope, $http) {
				    $http.get ('/api/leagues').success(function(data) {
					$scope.data = []
					var offs = 0
					for (i in data ['leagues']) {
					    $http.get ('/api/league/' + data ['leagues'][i]).success(
						function(league) {
						    $scope.data [offs++] = league
						}
					    )
					}
				    })
				}])

    app.config(['$routeProvider',
		function($routeProvider) {
		    $routeProvider
			.when('/about', {
			    templateUrl: 'about.html',
			    controller: ''
			})
			.when('/upcoming', {
			    templateUrl: 'upcoming.html',
			    controller: ''
			})
			.otherwise({
			    redirectTo: "/about"
			})
		}])

    angular.bootstrap(document, ['FringeApp']);
    return app;
});
