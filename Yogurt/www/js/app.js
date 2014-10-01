require.config({
    paths: {
        jquery: '/js/lib/jquery/dist/jquery',
        bootstrap: '/js/lib/bootstrap/dist/js/bootstrap.min.js',
        spin: '/js/lib/spin.js/spin',
        socialite: '/js/lib/socialite-js/socialite',

        angular: '/js/lib/angular/angular',
        angularRoute: '/js/lib/angular-route/angular-route',
        angularBootstrap: '/js/lib/angular-bootstrap/ui-bootstrap-tpls',
        angularSpinner: '/js/lib/angular-spinner/angular-spinner'
    },
    shim: {
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

define('app', ["jquery", "angular", "angularBootstrap", "angularRoute", "angularSpinner", "socialite"], function($, angular) {
    var app = angular.module("FringeApp", ['ngRoute', 'ui.bootstrap', 'angularSpinner']);

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
                    .when('/twitch/:channel/:title/:id', {
                        templateUrl: 'twitch.html',
                        controller: 'twitch'
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

    app.controller('upcoming', function($scope, $http, usSpinnerService) {
        $http.get('/api/upcoming').success(function(data) {
            $scope.data = data['events']
            $scope.data[0]['first'] = true
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
                    $scope.data[i].stream = $scope.data[i].stream.stream
                }
            }
            usSpinnerService.stop('loader')
        })
        $scope.name = 'Live Events'
        $scope.oneAtATime = true
        $scope.valid = false
    })

    app.controller('streams', function($scope, $http, usSpinnerService) {
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
        $scope.oneAtATime = true
        $scope.valid = false
    })

    app.controller('league', function($scope, $routeParams, $http) {
        $http.get('/api/league/' + $routeParams.param + '/events').success(function(data) {
            $scope.events = data
            $scope.name = $routeParams.param
        })
    })

    app.controller('twitch', function($scope, $routeParams) {
        $scope.channel = $routeParams.channel
        $scope.title = $routeParams.title
        $scope.id = $routeParams.id
    })

    app.controller('videos', function($scope, $routeParams, $http, usSpinnerService) {
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
    Socialite.load();

    return app;
});