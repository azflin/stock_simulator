(function () {
	'use strict';

	angular
		.module('stock_simulator.portfolios.directives', [])
		.directive('portfolioSnapshot', function () {
			var directive = {
				restrict: 'E',
				//scope: {
				//	portfolio: '='
				//},
				templateUrl: '/static/templates/portfolios/portfolio_snapshot.html'
			};
			return directive;
		});
})();