// Routes for the angularJS app
(function () {
  'use strict';

  angular
    .module('stock_simulator.routes', ['ngRoute'])
    .config(['$routeProvider', function($routeProvider){
			$routeProvider.when('/users/:userID', {
				controller: 'PortfolioIndexController',
				templateUrl: '/static/templates/portfolios/index.html',
			}).when('/users/:userID/:portfolioID', {
				controller: 'PortfolioDetailController',
				templateUrl: '/static/templates/portfolios/detail.html',
			}).when('/home', {
				templateUrl: '/static/templates/home.html',
			}).when('/register', {
				controller: 'RegisterController',
				templateUrl: '/static/templates/authentication/register.html',
			}).when('/login', {
				controller: 'LoginController',
				templateUrl: '/static/templates/authentication/login.html',
			})
		}]);
})();