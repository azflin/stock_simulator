(function () {
	'use strict';

	angular
		.module('stock_simulator.transactions.directives')
		.directive('newTransactionModal', function () {
			var directive = {
				restrict: 'E',
				scope: {
					portfolioId : '@',
					initialize: '&'
				},
				controller: function ($scope, $http, Transactions) {
					// call postTransaction on New Transaction submit.
					$scope.postTransaction = function (transaction) {
						$scope.status = 'pending';
						Transactions.postTransaction(
							$scope.portfolioId,
							transaction.ticker,
							transaction.side,
							transaction.quantity
						).then(postTransactionSuccessFn, postTransactionErrorFn);
					};

					function postTransactionSuccessFn(response) {
						$scope.initialize();
						$scope.status = 'success';
						if (response.data.transaction_type == 'Buy') {
							var side_verb = 'Bought ';
						} else if (response.data.transaction_type == 'Sell') {
							var side_verb = 'Sold ';
						}
						$scope.alertMessage = side_verb + response.data.quantity + " units of " +
							response.data.ticker + " @ $" + response.data.price.toFixed(2) + ", totalling $" +
							(response.data.quantity * response.data.price).toFixed(2);
					}

					function postTransactionErrorFn(response) {
						$scope.status = 'failure';
						$scope.alertMessage = response.data;
					}

					// Call getQuote on key press of ticker input box.
					$scope.getQuote = function (ticker) {
						// To account for empty ticker input. Clear scope's quote.
						if (!ticker) {
							$scope.quote = null;
						} else {
							$http.get('/api/quote/' + ticker).then(
								function success(response) {
									return getQuoteSuccessFn(response, ticker)
								}, getQuoteErrorFn
							);
						}
					};

					function getQuoteSuccessFn (response, ticker) {
						// If an empty object is returned, it means invalid yahoo finance ticker.
						if (Object.keys(response.data).length == 0) {
							$scope.quote = { invalidTickerMessage: "Invalid ticker." };
						} else {
							$scope.quote = response.data[ticker.toUpperCase()];
							//$scope.quoteStyle will be passed into ng-style for certain tags
							$scope.quoteStyle = {};
							// Make positive price changes green and negative changes red
							if ($scope.quote.change >= 0) {
								$scope.quoteStyle.color = "green";
							} else if ($scope.quote.change < 0) {
								$scope.quoteStyle.color = "red";
							}
						}
					}

					function getQuoteErrorFn (response) {
						$scope.status = 'failure';
						$scope.alertMessage = "Could not get stock quote data." +
							"This must mean there is an issue with the Yahoo Finance webservice."
					}
				},
				templateUrl: '/static/templates/transactions/new-transaction-modal.html'
			};
			return directive;
		});
})();