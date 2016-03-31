// Authenticate module containing all services and controllers related to authentication

(function () {
	'use strict';

	angular.module('authentication', [])

		//Login Controller
		.controller('LoginController', ['$scope', 'login', function($scope, login) {
			$scope.login = login;
		}])
		//Login Service
		.factory('login', ['$http', function($http) {

			//Helper login success/error functions
			function loginSuccessFn(response){
				window.location = '/';
			}
			function loginErrorFn(response){
				console.error('Incorrect username/password combination.');
			}

			//Function to login through POST /api/login/
			return function(username, password) {
				return $http.post('/api/login/', {
					username: username,
					password: password
				}).then(loginSuccessFn, loginErrorFn);
			};
		}])

		//Logout Controller
		.controller('LogoutController', ['$scope', 'logout', function($scope, logout) {
			$scope.logout = logout;
		}])
		//Logout Service
		.factory('logout', ['$http', function($http) {

			//Helper logout success/error functions
			function logoutSuccessFn(response){
				window.location ='/';
			}
			function logoutErrorFn(response){
				console.error("Logout failed.");
			}

			//Function to logout through POST /api/logout/
			return function(){
				$http.post('/api/logout/')
					.then(logoutSuccessFn, logoutErrorFn);
			};
		}])
})();