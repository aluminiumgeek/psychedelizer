/*
* psychedelizer.0x80.ru
* app.js (c) Mikhail Mezyakov <mihail265@gmail.com>
* 
* Angular init and routes config
*/

var app = angular.module('Psychedelizer', ['angularFileUpload', 'ngRoute']);

app.config(function ($routeProvider, $locationProvider) {
    $routeProvider.
        when('/', {
            templateUrl: '/partials/home.html',
            controller: 'HomeCtrl'
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
