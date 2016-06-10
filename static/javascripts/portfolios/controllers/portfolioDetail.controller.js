(function () {
	'use strict';

	angular
		.module('stock_simulator.portfolios.controllers')
		.controller('PortfolioDetailController',
			['$scope', '$routeParams', 'Portfolios', 'Transactions', 'Authentication',
				function ($scope, $routeParams, Portfolios, Transactions, Authentication) {

					$scope.userID = $routeParams.userID;
					//$scope.isPageOwner triggers ng-show for new transaction button
					if (Authentication.getAuthenticatedAccount().username == $scope.userID) {
						$scope.isPageOwner = true;
					}

					$scope.initialize = function () {
						// get the portfolio
						Portfolios.getOnePortfolio($scope.userID, $routeParams.portfolioID)
							.then(getOnePortfolioSuccessFn, getOnePortfolioErrorFn);
						// get the portfolio's transactions
						Transactions.getTransactions($routeParams.portfolioID)
							.then(getTransactionsSuccessFn);
					};

					// Load page with portfolio
					$scope.initialize($routeParams.userID, $routeParams.portfolioID);

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