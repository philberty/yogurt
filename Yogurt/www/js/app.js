require.config({
    paths: {
        jquery: [
	    'https://code.jquery.com/jquery-2.1.1.min',
	    '/js/lib/jquery/dist/jquery'],

        spin: [
	    '/js/lib/spin.js/spin'],

        bootstrap: [
	    '//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/bootstrap.min',
	    '/js/lib/bootstrap/dist/js/bootstrap'],

	bootstrapAutoHiding: [
	    '/js/lib/bootstrap-autohidingnavbar/dist/jquery.bootstrap-autohidingnavbar'],

        angular: [
	    '//cdnjs.cloudflare.com/ajax/libs/angular.js/1.2.20/angular.min',
	    '/js/lib/angular/angular'],

        angularRoute: [
	    '//cdnjs.cloudflare.com/ajax/libs/angular.js/1.2.20/angular-route.min',
	    '/js/lib/angular-route/angular-route'],

	angularScroll: [
	    '/js/lib/angular-scroll/angular-scroll'],

        angularBootstrap: [
	    '//cdnjs.cloudflare.com/ajax/libs/angular-ui-bootstrap/0.10.0/ui-bootstrap-tpls.min',
	    '/js/lib/angular-bootstrap/ui-bootstrap-tpls'],

        angularSpinner: [
	    '/js/lib/angular-spinner/angular-spinner']
    },
    shim: {
	'bootstrapAutoHiding': {
	    deps: ['bootstrap'],
	    exports: 'bootstrapAutoHiding'
	},
	'bootstrap': {
	    deps: ['jquery'],
	    exports: 'bootstrap'
	},
	'angularScroll': {
	    deps: ['angular'],
	    exports: 'angularScroll'
	},
        'angularSpinner': {
            deps: ['angular', 'spin'],
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

define('app', ["jquery", "angular", "angularBootstrap", "angularRoute", "angularScroll",
	       "angularSpinner", "bootstrap", "bootstrapAutoHiding"],
       function($, angular)
       {
	   var app = angular.module("FringeApp", ['ngRoute', 'ui.bootstrap', 'duScroll', 'angularSpinner']);

	   app.directive('dynamic', function ($compile) {
	       return {
		   restrict: 'A',
		   replace: true,
		   link: function (scope, ele, attrs) {
		       scope.$watch(attrs.dynamic, function(html) {
			   ele.html(html);
			   $compile(ele.contents())(scope);
		       });
		   }
	       };
	   });

	   app.controller("sidebar", function($scope, $location) {
               $scope.$on('$locationChangeSuccess', function(event) {
		   var context = $location.path()
		   if (context.substring(1, 7) == "videos" || context.substring(1, 7) == "league") {
                       $scope.tab = "vods"
		   } else {
                       $scope.tab = context
		   }
               })
	   })

	   app.config(
               ['$routeProvider',
		function($routeProvider) {
                    $routeProvider
			.when('/about', {
                            templateUrl: 'about.html',
                            controller: 'about'
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
			.when('/', {
                            redirectTo: "/about"
			})
			.otherwise({
                            redirectTo: '/'
			})
		}
               ]
	   )

	   app.controller('about', function($scope, $http, usSpinnerService) {
	       $http.get('/api/live').success(function(data) {
		   $scope.live = false
		   if (data.length > 0) {
		       var eindex = Math.floor(Math.random() * data.length)
		       $scope.event = data.live_events[eindex]
		       if (typeof($scope.event.stream) == 'object') {
			   $scope.html = $scope.event.stream.embed
			   $scope.live = true
		       }
		   }
	       })
	   })

	   app.controller('upcoming', function($scope, $http, usSpinnerService) {
               $http.get('/api/upcoming').success(function(data) {
		   $scope.data = data['events']
		   $scope.data[0]['first'] = true
		   for (i in $scope.data) {
		       if (typeof($scope.data[i].stream) == 'object') {
			   if ($scope.data[i].stream == null) {
			       $scope.data[i].stream = 'Stream is unavailable'
			   } else {
			       $scope.data[i].stream = $scope.data[i].stream.stream
			   }
		       }
		   }
		   $scope.valid = true
		   usSpinnerService.stop('loader')
               })
               $scope.name = 'Upcoming Events'
               $scope.oneAtATime = true;
	   })

	   app.controller('live', function($scope, $http, usSpinnerService) {
               $http.get('/api/live').success(function(data) {
		   $scope.data = data['live_events']
		   $scope.valid = ($scope.data.length > 0) ? true : false
		   if ($scope.valid) {
                       $scope.data[0]['first'] = true
		   }
		   for (i in $scope.data) {
                       if (typeof($scope.data[i].stream) == 'object') {
			   if ($scope.data[i].stream == null) {
			       $scope.data[i].stream = 'Stream is unavailable'
			   } else {
			       $scope.data[i].stream = $scope.data[i].stream.stream
			   }
                       }
		   }
		   usSpinnerService.stop('loader')
               })
               $scope.name = 'Live Events'
               $scope.oneAtATime = true
               $scope.valid = false
	   })

	   app.controller('ModalInstanceCtrl', function ($scope, $modalInstance, video) {
	       $scope.video = video
	       $scope.cancel = function () {
		   $modalInstance.dismiss('cancel');
	       };
	   });

	   app.controller('streams', function($scope, $http, $document, $modal, usSpinnerService) {
               $http.get('/api/streams').success(function(data) {
		   $scope.data = data['starcraft2']
		   $scope.data[0]['first'] = true
		   for (i in $scope.data) {
                       if ($scope.data[i].logo == null) {
			   $scope.data[i].logo = "http://s.jtvnw.net/jtv_user_pictures/hosted_images/GlitchIcon_purple.png"
                       }
		   }
		   $scope.valid = true
		   usSpinnerService.stop('loader')
               })
               $scope.valid = false

	       $scope.errorPopover = function(video) {
		   var modalInstance = $modal.open({
		       templateUrl: 'streamError.html',
		       controller: 'ModalInstanceCtrl',
		       resolve: {
			   video: function () {
			       return video;
			   }
		       }
		   });
		   
		   modalInstance.result.then(function (selectedItem) {
		       $scope.selected = selectedItem;
		   });
	       };

	       $scope.watchVideo = function(video) {
		   if (typeof(video.embed) == "undefined") {
		       $scope.errorPopover(video)
		       return
		   }
		   usSpinnerService.spin('loader')
		   $scope.title = video.name
		   $scope.html = video.embed
		   $scope.isEmbed = true
		   $document.scrollTopAnimated(0)
		   usSpinnerService.stop('loader')
	       }

	       $scope.clearVideo = function() {
		   $scope.isEmbed = false
	       }
	   })

	   app.controller('league', function($scope, $routeParams, $http) {
               $http.get('/api/league/' + $routeParams.param + '/events').success(function(data) {
		   $scope.events = data
		   $scope.name = $routeParams.param
               })
	   })

	   app.controller('videos', function($scope, $routeParams, $http, $document, usSpinnerService) {
               var league = $routeParams['league']
               var path = $routeParams['resourceUrl'].split('/')

               var basePath = '#/videos/' + league
               $scope.breadcrumb = []
               for (var i in path) {
		   var elem = path[i]
		   basePath += '/' + elem
		   $scope.breadcrumb.push({
                       'key': elem,
                       'href': basePath
		   })
               }
               $scope.league = league
               $scope.event = path[0]
               $scope.basePath = basePath
               $scope.backToLeagues = "#/league/" + league

               $http.get('/api/league/' + league + '/event/' + $scope.event).success(function(data) {
		   $scope.data = data

		   for (var i in path) {
                       var elem = path[i]
                       $scope.data = $scope.data[elem]
		   }

		   $scope.isEmbed = false
		   $scope.isList = false
		   $scope.isDir = false
		   $scope.listKeys = $scope.data['_keys']
		   if ($scope.data['_type'] == 'list') {
                       $scope.isList = true
		   } else {
                       $scope.isDir = true
		   }
		   usSpinnerService.stop('loader')
               })

	       $scope.watchVideo = function(video) {
		   usSpinnerService.spin('loader')
		   $scope.title = video.title
		   $scope.html = video.embed
		   $scope.isEmbed = true
		   $document.scrollTopAnimated(0)
		   usSpinnerService.stop('loader')
	       }
	       $scope.clearVideo = function() {
		   $scope.isEmbed = false
	       }
	   })

	   app.controller('vods', function($scope, $http) {
               $http.get('/api/leagues').success(function(data) {
		   var leagues = $scope.leagues = []

		   $scope.addLeague = function(name) {
                       $http.get('/api/league/' + name).success(function(channel) {
			   channel['_name'] = name
			   leagues.push(channel);
                       })
		   };

		   for (var i in data['leagues']) {
                       $scope.addLeague(data['leagues'][i])
		   }
               })
	   })

	   angular.bootstrap(document, ['FringeApp']);
	   $("div.navbar-fixed-top").autoHidingNavbar();
	   
	   return app;
       });
