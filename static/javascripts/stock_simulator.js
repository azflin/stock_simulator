(function(){
  'use strict';

  var app = angular.module('stock_simulator', []);
  app.controller('TestController', ['$scope', function($scope){
    $scope.message = "fuck boy";
		$scope.click_alert = function(){
			window.alert("niggas!");
		}
  }]);

})();