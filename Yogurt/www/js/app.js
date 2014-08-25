require.config({
    paths: {
	jquery: '/js/lib/jquery/dist/jquery',
	bootstrap: '/js/lib/bootstrap/dist/js/bootstrap.min.js',

	angular: '/js/lib/angular/angular',
	angularRoute: '/js/lib/angular-route/angular-route',
	angularTree: '/js/lib/angular-ui-tree/dist/angular-ui-tree',
	angularBootstrap: '/js/lib/angular-bootstrap/ui-bootstrap-tpls'
    },
    shim: {
	'angularTree': {
	    deps: ['angular'],
	    exports: 'angular'
	},
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

define('app', ["jquery", "angular", "angularBootstrap", "angularTree", "angularRoute"], function($, angular) {
    var app = angular.module("FringeApp", ['ngRoute', 'ui.bootstrap', 'ui.tree']);

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
		 .when('/league/:param', {
		     templateUrl: 'league.html',
		     controller: 'league'
		 })
		 .when('/videos/:league/:event', {
		     templateUrl: 'breadcrumb.html',
		     controller: 'videos'
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

    app.controller ('league', function ($scope, $routeParams, $http) {
	$http.get ('/api/league/' + $routeParams.param + '/events').success(function(data) {
	    $scope.events = data
	    $scope.name = $routeParams.param
	})
    })

    app.controller ('videos', function ($scope, $routeParams, $http) {
	var eventPath = '/api/league/' + $routeParams.league + '/event/' + $routeParams.event;
	$http.get (eventPath).success(function(data) {
	    $scope.league = $routeParams.league
	    $scope.event = $routeParams.event

	    var videos = {}
	    var exclude = ["__yogurt_timestamp", "status"]
	    for (var i in data) {
		var found = false;
		for (var y in exclude) {
		    if (i == exclude[y]) {
			found = true
			break
		    }
		}
		if (!found) {
		    videos[i] = data[i]
		}
	    }
	    $scope.videos = videos


	    $scope.list = [{
      "id": 1,
      "title": "1. dragon-breath",
      "items": []
    }, {
      "id": 2,
      "title": "2. moiré-vision",
      "items": [{
        "id": 21,
        "title": "2.1. tofu-animation",
        "items": [{
          "id": 211,
          "title": "2.1.1. spooky-giraffe",
          "items": []
        }, {
          "id": 212,
          "title": "2.1.2. bubble-burst",
          "items": []
        }],
      }, {
        "id": 22,
        "title": "2.2. barehand-atomsplitting",
        "items": []
      }],
    }, {
      "id": 3,
      "title": "3. unicorn-zapper",
      "items": []
    }, {
      "id": 4,
      "title": "4. romantic-transclusion",
      "items": []
    }];

	})
    })

    app.controller ('vods', function ($scope, $http) {
	$http.get ('/api/leagues').success(function(data) {
	    var leagues = $scope.leagues = []

	    $scope.addLeague = function(name) {
		$http.get ('/api/league/'+name).success(function(channel) {
		    channel['_name'] = name
		    leagues.push(channel);
		})	
	    };

	    for (var i in data ['leagues']) {
		$scope.addLeague (data['leagues'][i])
	    }
	})
    })
    
    angular.bootstrap(document, ['FringeApp']);
    return app;
});
