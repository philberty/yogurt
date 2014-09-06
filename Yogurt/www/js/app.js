require.config({
    paths: {
	jquery: '/js/lib/jquery/dist/jquery',
	bootstrap: '/js/lib/bootstrap/dist/js/bootstrap.min.js',

	socialite: '/js/lib/socialite-js/socialite',

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

define('app', ["jquery", "angular", "angularBootstrap", "angularRoute", "socialite"], function($, angular) {
    var app = angular.module("FringeApp", ['ngRoute', 'ui.bootstrap']);

    app.controller("sidebar", function($scope, $location) {
	$scope.$on('$locationChangeSuccess', function(event) {
	    $scope.tab = $location.path()
	})
    })

    app.config(
	['$routeProvider', function($routeProvider) {
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
		.when('/videos/:league/:resourceUrl*', {
		    templateUrl: 'breadcrumb.html',
		    controller: 'videos'
		})
		.when('/twitch/:title/:id', {
		    templateUrl: 'twitch.html',
		    controller: 'twitch'
		})
		.when('/', {
		    redirectTo: "/about"
		})
		.otherwise({
		    redirectTo: '/'
		})
	}]
    )
    
    app.controller ('upcoming', function ($scope, $http) {
	$http.get ('/api/upcoming').success(function(data) {
	    $scope.data = data ['events']
	    $scope.data[0]['first'] = true
	})
	$scope.name = 'Upcoming Events'
	$scope.oneAtATime = true;
    })

    app.controller ('live', function ($scope, $http) {
	$http.get ('/api/live').success(function(data) {
	    $scope.data = data ['live_events']
	    $scope.data[0]['first'] = true
	})
	$scope.name = 'Live Events'
	$scope.oneAtATime = true;
    })

     app.controller ('streams', function ($scope, $http) {
	$http.get ('/api/streams').success(function(data) {
	    $scope.data = data ['starcraft2']
	    $scope.data[0]['first'] = true
	})
	$scope.oneAtATime = true;
    })

    app.controller ('league', function ($scope, $routeParams, $http) {
	$http.get ('/api/league/' + $routeParams.param + '/events').success(function(data) {
	    $scope.events = data
	    $scope.name = $routeParams.param
	})
    })

    app.controller ('twitch', function ($scope, $routeParams) {
	$scope.title = $routeParams.title
	$scope.video = "archive_id=" + $routeParams.id
    })

    app.controller ('videos', function ($scope, $routeParams, $http) {
	var league = $routeParams['league']
	var path = $routeParams['resourceUrl'].split('/')

	var basePath = '#/videos/'+league
	$scope.breadcrumb = []
	for (var i in path) {
	    var elem = path[i]
	    basePath += '/' + elem
	    $scope.breadcrumb.push({'key': elem, 'href':basePath})
	}
	$scope.league = league
	$scope.event = path[0]
	$scope.basePath = basePath
	$scope.backToLeagues = "#/league/" + league

	$http.get ('/api/league/'+league+'/event/'+$scope.event).success(function(data) {
	    $scope.data = data

	    for (var i in path) {
		var elem = path[i]
		$scope.data = $scope.data[elem]
	    }

	    $scope.isList = false
	    $scope.isDir = false
	    $scope.listKeys = $scope.data['_keys']
	    if ($scope.data['_type'] == 'list') {
		$scope.isList = true
	    } else {
		$scope.isDir = true
	    }
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
    Socialite.load();

    return app;
});
