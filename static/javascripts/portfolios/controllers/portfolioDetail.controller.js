(function () {
	'use strict';

	angular
		.module('stock_simulator.portfolios.controllers')
		.controller('PortfolioDetailController', ['$scope', '$routeParams', 'Portfolios',
			function ($scope, $routeParams, Portfolios) {

				$scope.userID = $routeParams.userID;

				// Load page with portfolio
				initialize($routeParams.userID, $routeParams.portfolioID);

				function initialize(username, portfolioID) {
					Portfolios.getOnePortfolio(username, portfolioID)
						.then(initializeSuccessFn, initializeErrorFn);
				}

				function initializeSuccessFn(response) {
					$scope.portfolio = response.data;
					console.log(response.data);
				}

				function initializeErrorFn(response) {
					$scope.errorMessage = response.data;
					console.log(response.data);
				}
			}
		]);
})();