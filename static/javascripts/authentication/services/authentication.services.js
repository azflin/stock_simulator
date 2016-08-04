/**
 * Authentication
 * @namespace stock_simulator.authentication.services
 */
(function () {
	'use strict';

	angular
		.module('stock_simulator.authentication.services')
		.factory('Authentication', ['$http', '$cookies', function($http, $cookies) {
			var Authentication = {
				register: register,
				login: login,
				logout: logout,
				setAuthenticatedAccount: setAuthenticatedAccount,
				unauthenticate: unauthenticate,
				getAuthenticatedAccount: getAuthenticatedAccount
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
					unauthenticate();
					window.location ='/#/';
					window.location.reload();
				}
			}

			function setAuthenticatedAccount(account) {
				$cookies.authenticatedAccount = JSON.stringify(account);
			}

			function unauthenticate() {
				delete $cookies.authenticatedAccount;
			}

			function getAuthenticatedAccount() {
				if ($cookies.authenticatedAccount) {
					return JSON.parse($cookies.authenticatedAccount);
				} else {
					return '';
				}
			}
		}]);
})();