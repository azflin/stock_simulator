(function () {
	'use strict';

	angular
		.module('stock_simulator.portfolios.services')
		.factory('Portfolios', ['$http', 'Authentication', function ($http, Authentication) {
			var Portfolios = {
				getAllPortfolios: getAllPortfolios,
				createPortfolio: createPortfolio,
				deletePortfolio: deletePortfolio
			};

			return Portfolios;

			function getAllPortfolios(username) {
				return $http.get('/api/portfolios/?username=' + username);
			}

			function createPortfolio(name) {
				return $http.post('/api/portfolios/', {
					name: name
				});
			}

			function deletePortfolio(portfolio_id) {
				return $http.delete('/api/portfolios/' + portfolio_id +
					'/?username=' + Authentication.getAuthenticatedAccount().username);
			}
		}]);
})();