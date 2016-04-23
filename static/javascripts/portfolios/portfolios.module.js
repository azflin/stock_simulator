(function () {
	'use strict';

	angular
		.module('stock_simulator.portfolios', [
			'stock_simulator.portfolios.controllers',
			'stock_simulator.portfolios.services',
			'stock_simulator.portfolios.directives'
		]);

	angular
		.module('stock_simulator.portfolios.controllers', []);

	angular
		.module('stock_simulator.portfolios.services', []);

	angular
		.module('stock_simulator.portfolios.directives', []);
})();