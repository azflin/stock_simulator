(function () {
	'use strict';

	angular
		.module('stock_simulator.authentication.controllers')
		.controller('LogoutController', ['$scope', 'Authentication',
			function ($scope, Authentication) {
				$scope.logout = Authentication.logout;
		}])
})();