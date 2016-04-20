(function () {
	'use strict';

	angular
		.module('stock_simulator.authentication', [
			'stock_simulator.authentication.controllers',
			'stock_simulator.authentication.services',
		]);

	angular
		.module('stock_simulator.authentication.controllers', []);

	angular
		.module('stock_simulator.authentication.services', ['ngCookies']);
})();