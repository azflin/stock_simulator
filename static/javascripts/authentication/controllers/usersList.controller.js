(function () {
	'use strict;'

	angular
		.module('stock_simulator.authentication.controllers')
		.controller('UsersListController', ['$scope', '$http',
			function($scope, $http) {
				$http.get('/api/users/').then(function (response) {
					console.log(response.data);
				});
			}]);
})();