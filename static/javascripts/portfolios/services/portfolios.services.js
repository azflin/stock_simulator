(function () {
	'use strict';

	angular
		.module('stock_simulator.portfolios.services', [])
		.factory('Portfolios', ['$http', function ($http) {
			var Portfolios = {
				all: all,
				create: create,
				deletePortfolio: deletePortfolio
			};

			return Portfolios;

			function all () {
				return $http.get('/api/portfolios/');
			}

			function create (name) {
				return $http.post('/api/portfolios/', {
					name: name
				});
			}

			function deletePortfolio (portfolio_id) {
				return $http.delete('/api/portfolios/' + portfolio_id);
			}
		}]);
})();