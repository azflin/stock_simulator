(function () {
	'use strict;'

	angular
		.module('stock_simulator.authentication.controllers')
		.controller('UsersListController', ['$scope', '$http',
			function($scope, $http) {
				$http.get('/api/users/').then(function (response) {
					$scope.users = [];
					angular.forEach(response.data, function (value) {
						this.push({"id": value.id, "username": value.username})
					}, $scope.users);
				});
			}]);
})();