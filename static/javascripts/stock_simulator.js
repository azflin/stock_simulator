(function () {
  'use strict';

  angular
		.module('stock_simulator', [
			'stock_simulator.routes',
			'stock_simulator.portfolios',
			'stock_simulator.authentication',
			'stock_simulator.transactions'
		])

		// Provide CSRF Token for Django's unsafe methods
		.run(function ($http) {
			$http.defaults.xsrfHeaderName = 'X-CSRFToken';
  		$http.defaults.xsrfCookieName = 'csrftoken';
		});
})();