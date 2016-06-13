var app = angular.module('gpu', []);
app.controller('ctrl', function($scope, $http) {
	$http.get("http://ipServer:6969/") .then(function (response) {
		$scope.names = response.data.data;
	});
});