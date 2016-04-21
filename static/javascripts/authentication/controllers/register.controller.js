(function () {
	'use strict';

	angular
		.module('stock_simulator.authentication.controllers')
		.controller('RegisterController', ['$scope', 'Authentication',
			function($scope, Authentication) {
				$scope.register = function () {
					if ($scope.password == $scope.confirm_password) {
						Authentication.register(
							$scope.username,
							$scope.email,
							$scope.password
						).then(registerSuccessFn, registerErrorFn);
					} else {
						$scope.error_messages = {
							"Password Confirmation": ["Passwords do not match."]
						};
					}
				};

				//Helper register success/error functions
				function registerSuccessFn() {
					Authentication.login($scope.username, $scope.password)
						.then(function (response) {
							Authentication.setAuthenticatedAccount(response.data);
							window.location = '/#/users/' + response.data.username;
							window.location.reload();
						});
				}
				function registerErrorFn(response) {
					$scope.error_messages = response.data;
				}
			}]);
})();