(function () {
	'use strict';

	angular
		.module('stock_simulator.portfolios.directives')
		.directive('portfolioSnapshot', function () {
			var directive = {
				restrict: 'E',
				scope: {
					portfolio: '=',
					userID: '=',
					isPageOwner: '=',
					deletePortfolio: '&'
				},
				controller: function ($scope, $window, $http, Transactions) {
					// Function to delete portfolio using parent scope's deletePortfolio function
					$scope.delete = function (id) {
						var deleteConfirmation = $window.confirm("Are you sure you want to delete this?");
						if (deleteConfirmation) {
							$scope.deletePortfolio()(id);
						}
					};
					// Populate $scope.portfolio's overallReturn and marketValue variables
					$scope.portfolio.marketValue = $scope.portfolio.cash;
					var tickers = [];
					angular.forEach($scope.portfolio.stocks, function (stock) {
						tickers.push(stock.ticker);
					});
					tickers = tickers.join();
					if (tickers) {
						$http.get('/api/quote/' + tickers).then(getQuoteSuccessFn, getQuoteErrorFn);
					} else {
						$scope.portfolio.overallReturn =
							(($scope.portfolio.marketValue/100000 - 1) * 100).toFixed(2);
					}

					function getQuoteSuccessFn (response) {
						// Add market value of each stock to portfolio's market value
						angular.forEach($scope.portfolio.stocks, function (stock) {
							stock.price = response.data[stock.ticker].price;
							$scope.portfolio.marketValue += stock.price * stock.quantity;
						});
						$scope.portfolio.overallReturn =
							(($scope.portfolio.marketValue/100000 - 1) * 100).toFixed(2);
					}

					function getQuoteErrorFn (response) {
						//TODO: Show error message on index view when /api/quote fails
					}
				},
				templateUrl: '/static/templates/portfolios/portfolio-snapshot.html'
			};
			return directive;
		});
})();