(function () {
	'use strict';

	angular
		.module('stock_simulator.transactions.directives')
		.directive('newTransactionModal', function () {
			var directive = {
				restrict: 'E',
				templateUrl: '/static/templates/transactions/new_transaction_modal.html'
			};
			return directive;
		});
})();