/*
* psychedelizer.0x80.ru
* app.js (c) Mikhail Mezyakov <mihail265@gmail.com>
* 
* Angular init and routes config
*/

var app = angular.module('Psychedelizer', ['angularFileUpload', 'ngRoute']);

app.config(function($routeProvider, $locationProvider) {
    $routeProvider.
        when('/', {
            templateUrl: '/partials/home.html',
            controller: 'HomeCtrl',
        }).
        when('/image/:unixtime', {
            templateUrl: '/partials/image.html',
            controller: 'ImageCtrl'
        })
        .otherwise({
            redirectTo: '/'
        });
        
    if (window.history && window.history.pushState) {
        $locationProvider.html5Mode(true);
    }
});

app.run(function($rootScope) {
    $rootScope.$on('$routeChangeSuccess', function(event, current, previous) {
        if (current.$$route.controller != 'HomeCtrl' && previous !== undefined) {
            clearInterval(previous.locals.$scope.get_latest_descriptor);
        }
        else if (current.$$route.controller == 'HomeCtrl') {
            $rootScope.$watch('current.locals.$scope', function() {
                current.locals.$scope.init_ajaxupdater();
                
                if ($rootScope.sort_by == 'best') {
                    current.locals.$scope.show_likes = true;
                }
            })
        }
    });
    
});
