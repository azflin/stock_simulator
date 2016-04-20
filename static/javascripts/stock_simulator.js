(function () {
  'use strict';

  angular
		.module('stock_simulator', [
			'stock_simulator.routes',
			'stock_simulator.portfolios',
			'stock_simulator.authentication'
		])

		// Provide CSRF Token for Django's unsafe methods
		.run(function ($http) {
			$http.defaults.xsrfHeaderName = 'X-CSRFToken';
  		$http.defaults.xsrfCookieName = 'csrftoken';
		});
})();