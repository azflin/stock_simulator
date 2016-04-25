(function () {
	'use strict';

	angular
		.module('stock_simulator.portfolios.controllers')
		.controller('PortfolioDetailController', ['$scope', '$routeParams', 'Portfolios',
			function ($scope, $routeParams, Portfolios) {

				// Load page with portfolio
				initialize($routeParams.userID, $routeParams.portfolioID);

				function initialize(username, portfolioID) {
					Portfolios.getOnePortfolio(username, portfolioID)
						.then(initializeSuccessFn, initializeErrorFn);
				}

				function initializeSuccessFn(response) {
					console.log(response.data);
				}

				function initializeErrorFn(response) {
					console.log(response.data);
				}
			}
		]);
})();