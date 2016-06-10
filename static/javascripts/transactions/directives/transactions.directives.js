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
				controller: function ($scope, Transactions) {
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
						$scope.alertMessage = response.data[0];
					}
				},
				templateUrl: '/static/templates/transactions/new_transaction_modal.html'
			};
			return directive;
		});
})();