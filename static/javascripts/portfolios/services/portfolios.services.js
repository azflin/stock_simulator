(function () {
	'use strict';

	angular
		.module('stock_simulator.portfolios.services')
		.factory('Portfolios', ['$http', 'Authentication', function ($http, Authentication) {
			var Portfolios = {
				getAllPortfolios: getAllPortfolios,
				getOnePortfolio: getOnePortfolio,
				createPortfolio: createPortfolio,
				deletePortfolio: deletePortfolio
			};

			return Portfolios;

			function getAllPortfolios(username) {
				return $http.get('/api/portfolios/?username=' + username);
			}

			function getOnePortfolio(portfolioID) {
				return $http.get('/api/portfolios/' + portfolioID);
			}

			function createPortfolio(name) {
				return $http.post('/api/portfolios/', {
					name: name
				});
			}

			function deletePortfolio(portfolio_id) {
				return $http.delete('/api/portfolios/' + portfolio_id);
			}
		}]);
})();