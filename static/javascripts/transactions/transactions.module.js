(function () {
	'use strict';

	angular
		.module('stock_simulator.transactions', [
			'stock_simulator.transactions.services',
			'stock_simulator.transactions.directives'
		]);

	angular
		.module('stock_simulator.transactions.services', []);
	angular
		.module('stock_simulator.transactions.directives', []);
})();