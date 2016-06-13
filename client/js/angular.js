var app = angular.module('gpu', []);

app.controller('ctrl', function($scope, $http) {
	var gpu = function gpuInfos() {
	$http.get("http://ipServer:6969") .then(function (response) {
		$scope.infos = response.data.data;
		console.log("toast");
	});}
	setInterval(gpu, 1000);
});


