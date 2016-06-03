(function () {
	'use strict';

	angular
		.module('stock_simulator.transactions.directives')
		.directive('newTransactionModal', function () {
			var directive = {
				restrict: 'E',
				scope: {
					action: '&'
				},
				controller: function ($scope) {
					$scope.alertBar = function () {
						var text = 'pussy';
						$scope.action()(text);
					};
				},
				templateUrl: '/static/templates/transactions/new_transaction_modal.html'
			};
			return directive;
		});
})();