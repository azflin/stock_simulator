(function () {
	'use strict';

	angular
		.module('stock_simulator.authentication.services')
		.factory('Authentication', ['$http', '$cookies', function($http, $cookies) {
			var Authentication = {
				register: register,
				login: login,
				logout: logout
			};

			return Authentication;

			function register(username, email, password) {
				return $http.post('/api/register/', {
					username: username,
					email: email,
					password: password
				});
			}

			function login(username, password) {
				return $http.post('/api/login/', {
					username: username,
					password: password
				});
			}

			function logout() {
				return $http.post('/api/logout/')
					.then(logoutSuccessFn);

				function logoutSuccessFn(response){
					window.location ='/#/home';
					window.location.reload();
				}
			}
		}]);
})();