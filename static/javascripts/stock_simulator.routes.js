(function () {
  'use strict';

  angular
    .module('stock_simulator.routes', ['ngRoute'])
    .config(['$routeProvider', function($routeProvider){
			$routeProvider.when('/login', {
				controller: 'LoginController',
				templateUrl: '/static/templates/authentication/login.html'
			}).otherwise('/');
		}]);

})();