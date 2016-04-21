(function () {
	'use strict';

	angular
		.module('stock_simulator.portfolios.services', [])
		.factory('Portfolios', ['$http', 'Authentication', function ($http, Authentication) {
			var Portfolios = {
				all: all,
				create: create,
				deletePortfolio: deletePortfolio
			};

			return Portfolios;

			function all (username) {
				return $http.get('/api/portfolios/?username=' + username);
			}

			function create (name) {
				return $http.post('/api/portfolios/', {
					name: name
				});
			}

			function deletePortfolio (portfolio_id) {
				return $http.delete('/api/portfolios/' + portfolio_id +
					'/?username=' + Authentication.getAuthenticatedAccount().username);
			}
		}]);
})();