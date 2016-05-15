(function () {
	'use strict';

	angular
		.module('stock_simulator.transactions.services')
		.factory('Transactions', ['$http', function ($http) {
			var Transactions = {
				getTransactions: getTransactions
			};

			return Transactions;

			function getTransactions(portfolioID) {
				return $http.get('/api/portfolios/' + portfolioID + '/transactions/');
			}
		}])
})();