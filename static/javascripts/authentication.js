// Authenticate module containing all services and controllers related to authentication

(function () {
	'use strict';

	angular.module('authentication', [])

		//Register Controller
		.controller('RegisterController', ['$scope', 'register', function ($scope, register) {
			$scope.register = function(){
				if ($scope.password == $scope.confirm_password) {
					register(
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
			function registerSuccessFn (response) {
				window.location = '/';
			}
			function registerErrorFn (response) {
				$scope.error_messages = response.data;
			}
		}])
		//Register service
		.factory('register', ['$http', function ($http) {
			return function(username, email, password) {
				return $http.post('/api/register/', {
					username: username,
					email: email,
					password: password
				});
			};
		}])

		//Login Controller
		.controller('LoginController', ['$scope', 'login', function ($scope, login) {
			$scope.login = function() {
				login($scope.username, $scope.password)
					.then(loginSuccessFn, loginErrorFn);
			};

			//Helper login success/error functions
			function loginSuccessFn(response){
				window.location = '/';
			}
			function loginErrorFn(response){
				$scope.login_error = 'Incorrect username/password combination.';
			}
		}])
		//Login Service
		.factory('login', ['$http', function ($http) {
			return function(username, password) {
				return $http.post('/api/login/', {
					username: username,
					password: password
				});
			};
		}])

		//Logout Controller
		.controller('LogoutController', ['$scope', 'logout', function ($scope, logout) {
			$scope.logout = logout;
		}])
		//Logout Service
		.factory('logout', ['$http', function ($http) {

			//Helper logout success/error functions
			function logoutSuccessFn(response){
				window.location ='/#/home';
				window.location.reload();
			}

			return function () {
				$http.post('/api/logout/')
					.then(logoutSuccessFn);
			};
		}])
})();