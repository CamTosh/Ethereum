<!DOCTYPE html>
<html ng-app="app">
<head>
	<meta charset="utf-8">
	<title>GPU Info</title>
	<link rel="stylesheet" type="text/css" href="css/list.css">
</head>
<script src="js/angular.min.js"></script>
<script type="text/javascript">
	var app = angular.module('app', []);
</script>
<body>
<div id="demo">
	<div class="table-responsive-vertical shadow-z-1">
	<table id="table" class="table table-hover table-mc-light-blue">
	<?php
		// C'est crade mais fonctionnel
		$json_file = file_get_contents('config.json');
		$f = json_decode($json_file);

		$dataH = $f->master;
		$s = 0;
		foreach ($dataH as $d) {
			?>
		<thead ng-controller="ctrl_master<?= $s ?>">
		<tr ng-repeat="i in infos">
		  <th>{{ i.Ip }}</th>
		  <th>{{ i.Balance /1000000000000000000 }} eth</th>
		  <th>{{ i.Euro }} €</th>
		  <th>{{ (i.Hash / 1000000).toFixed(2) }} mH/s</th>
			<script type="text/javascript">
			app.controller('ctrl_master<?= $s ?>', function($scope, $http) {
			var master = function gpuInfos() {
			$http.get("http://<?= $d->ip ?>") .then(function (response) {
				$scope.infos = response.data.data;
			});}
			setInterval(master, 1000);
		});
		</script>
		</tr>
	  	</thead>

		<?php
			$s++;
		}
		?>
	  	</tbody>
		</table>
	  	</div>
	  	<div class="table-responsive-vertical shadow-z-1">
	  <table id="table" class="table table-hover table-mc-light-blue">
      <thead>
        <tr>
          <th>Name</th>
          <th>Ip</th>
          <th>Load</th>
          <th>Heat</th>
          <th>FanSpeed</th>
          <th>CurrentClock</th>
          <th>CurrentMem</th>
        </tr>
      </thead>
	  
	  	<?php

		$data = $f->worker;

		$i = 0;

		foreach ($data as $d) {
			?>
		<tbody ng-controller="gpu<?= $i ?>">
		<tr ng-repeat="g in infos.gpu">
		  <td data-title="Name">{{ infos.Name }}</td>
		  <td data-title="Ip">{{ infos.Ip }}</td>
		  <td data-title="Load">{{ g.Load }}%</td>
		  <td data-title="Heat">{{ g.Heat }}°c</td>
		  <td data-title="FanSpeed"> {{ g.FanSpeed }}%</td>
		  <td data-title="CurrentClock">{{ (g.CurrentClock / g.MaxClock * 100).toFixed(2) }}%</td>
		  <td data-title="CurrentMem">{{ (g.CurrentMem / g.MaxMem * 100).toFixed(2) }}%</td>

		<script type="text/javascript">

			app.controller("gpu<?= $i ?>", function($scope, $http) {
				var gpu = function gpuInfos() {
				$http.get("http://<?= $d->ip ?>").then(function (response) {
					$scope.infos = response.data.data;
				});}
				setInterval(gpu, 1000);
			});

		</script>
		</tr>
		</tbody>
		<?php
			$i++;
		}
		?>
	</table>
  </div>
</body>
</html>