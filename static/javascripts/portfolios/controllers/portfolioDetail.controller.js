(function () {
	'use strict';

	angular
		.module('stock_simulator.portfolios.controllers')
		.controller('PortfolioDetailController',
			['$scope', '$routeParams', '$http', 'Portfolios', 'Transactions', 'Authentication',
				function ($scope, $routeParams, $http, Portfolios, Transactions, Authentication) {

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
						var tickers = [];
						angular.forEach(response.data.stocks, function (stock) {
							tickers.push(stock.ticker);
						});
						tickers = tickers.join();
						$http.get('/api/quote/' + tickers).then(
							function (response) {
								$scope.portfolio.marketValue = $scope.portfolio.cash;
								angular.forEach($scope.portfolio.stocks, function (stock) {
									stock.price = response.data[stock.ticker].price;
									$scope.portfolio.marketValue += stock.price * stock.quantity;
								});
								$scope.portfolio.overallReturn =
									(($scope.portfolio.marketValue/100000 - 1) * 100).toFixed(2);
								$scope.portfolio.style = {};
								// Set color of overall return
								if ($scope.portfolio.overallReturn >= 0) {
									$scope.portfolio.style.color = "green";
								} else {
									$scope.portfolio.style.color = "red";
								}
							}
						);
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