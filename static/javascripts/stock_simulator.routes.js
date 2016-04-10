(function () {
  'use strict';

  angular
    .module('stock_simulator.routes', ['ngRoute'])
    .config(['$routeProvider', function($routeProvider){
			$routeProvider.when('/', {
				controller: 'PortfoliosIndexController',
				templateUrl: '/static/templates/portfolios/index.html',
				authenticate: true
			}).when('/home', {
				templateUrl: '/static/templates/home.html',
				authenticate: false
			}).when('/register', {
				controller: 'RegisterController',
				templateUrl: '/static/templates/authentication/register.html',
				authenticate: false
			}).when('/login', {
				controller: 'LoginController',
				templateUrl: '/static/templates/authentication/login.html',
				authenticate: false
			}).otherwise('/');
		}]);

})();