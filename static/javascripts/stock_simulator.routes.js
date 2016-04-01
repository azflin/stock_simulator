(function () {
  'use strict';

  angular
    .module('stock_simulator.routes', ['ngRoute'])
    .config(['$routeProvider', function($routeProvider){
			$routeProvider.when('/register', {
				controller: 'RegisterController',
				templateUrl: '/static/templates/authentication/register.html'
			}).when('/login', {
				controller: 'LoginController',
				templateUrl: '/static/templates/authentication/login.html'
			}).otherwise('/');
		}]);

})();