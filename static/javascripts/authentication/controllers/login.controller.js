(function () {
	'use strict';

	angular
		.module('stock_simulator.authentication.controllers')
		.controller('LoginController', ['$scope', 'Authentication',
			function($scope, Authentication) {
				$scope.login = function () {
					Authentication.login($scope.username, $scope.password)
						.then(loginSuccessFn, loginErrorFn);
				};
				//Helper login success/error functions
				function loginSuccessFn(response){
					console.log(response.data);
					window.location = '/#/';
				}
				function loginErrorFn(response){
					$scope.login_error = 'Incorrect username/password combination.';
				}
		}])
})();