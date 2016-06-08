// stock_simulator.transactions.services
// provides 'Transactions' service
(function () {
	'use strict';

	angular
		.module('stock_simulator.transactions.services')
		.factory('Transactions', ['$http', function ($http) {
			var Transactions = {
				getTransactions: getTransactions,
				postTransaction: postTransaction
			};

			return Transactions;

			// Get transactions attached to the portfolio ID
			// Endpoint: /api/portfolios/:portfolioID/transactions/
			function getTransactions(portfolioID) {
				return $http.get('/api/portfolios/' + portfolioID + '/transactions/');
			}

			// Post a transaction to the portfolio
			// Endpoint: /api/portfolios/:portfolioID/transactions/
			function postTransaction(portfolioID, ticker, transactionType, quantity) {
				return $http.post(
					'/api/portfolios/' + portfolioID + '/transactions/',
					{
						ticker: ticker,
						transaction_type: transactionType,
						quantity: quantity
					}
				);
			}
		}])
})();