require.config({
    paths: {
	jquery: '/js/lib/jquery/dist/jquery',
	angular: '/js/lib/angular/angular',
	bootstrap: '/js/lib/bootstrap/dist/js/bootstrap'
    },
    shim: {
	'angular': {
	    exports: 'angular'
        }
    }
});

define("app", ["angular"], function(angular) {
    var app = angular.module("FringeApp", []);
    
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

    return app;
});
