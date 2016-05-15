(function () {
	'use strict';

	angular
		.module('stock_simulator.portfolios.controllers')
		.controller('PortfolioDetailController', ['$scope', '$routeParams', 'Portfolios', 'Transactions',
			function ($scope, $routeParams, Portfolios, Transactions) {

				$scope.userID = $routeParams.userID;

				// Load page with portfolio
				initialize($routeParams.userID, $routeParams.portfolioID);

				function initialize(username, portfolioID) {
					// get the portfolio
					Portfolios.getOnePortfolio(username, portfolioID)
						.then(getOnePortfolioSuccessFn, getOnePortfolioErrorFn);
					// get the portfolio's transactions
					Transactions.getTransactions(portfolioID)
						.then(getTransactionsSuccessFn);
				}

				function getOnePortfolioSuccessFn(response) {
					$scope.portfolio = response.data;
				}
				function getOnePortfolioErrorFn(response) {
					$scope.errorMessage = response.data;
				}
				function getTransactionsSuccessFn(response) {
					$scope.transactions = response.data;
				}
			}
		]);
})();