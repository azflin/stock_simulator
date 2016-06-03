(function () {
	'use strict';

	angular
		.module('stock_simulator.portfolios.controllers')
		.controller('PortfolioDetailController', ['$scope', '$routeParams', 'Portfolios', 'Transactions', 'Authentication',
			function ($scope, $routeParams, Portfolios, Transactions, Authentication) {

				$scope.userID = $routeParams.userID;
				//$scope.isPageOwner triggers ng-show for new transaction button
				if (Authentication.getAuthenticatedAccount().username == $scope.userID) {
					$scope.isPageOwner = true;
				}

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

				$scope.alertText = function (text) {
					alert(text);
				};
			}
		]);
})();