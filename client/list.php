<!DOCTYPE html>
<html ng-app="app">
<head>
	<meta charset="utf-8">
	<title>GPU Info</title>
	<link rel="stylesheet" type="text/css" href="css/reset.css">
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/semantic-ui/2.2.2/semantic.min.css">
</head>
<body>
<script src="js/angular.min.js"></script>
<script src="js/jquery-2.2.4.min.js"></script>
<script type="text/javascript">
	var app = angular.module('app', []);
</script>

	<?php
		// C'est crade mais (enfin) fonctionnel
		$json_file = file_get_contents('config.json');
		$f = json_decode($json_file);

		$dataH = $f->master;
		$s = 0;
		foreach ($dataH as $d) {
	?>
	<table class="ui celled table grey" ng-controller="ctrl_master<?= $s ?>">
		<thead>
			<tr>
				<th class="center aligned">{{ master.Ip }}</th>
				<th class="center aligned">{{ master.Balance /1000000000000000000 }}</th>
				<th class="center aligned">{{ master.Euro }}</th>
				<th class="center aligned">{{ (master.Hash / 1000000).toFixed(2) }}</th>
			</tr>
		</thead>
		<script type="text/javascript">
			app.controller('ctrl_master<?= $s ?>', function($scope, $http) {
			var master = function gpuInfos() {
			$http.get("http://<?= $d->ip ?>") .then(function (response) {
				$scope.master = response.data;
			});}
			setInterval(master, 1000);
		});
		</script>
	</table>
	<?php
			$s++;
		}
	?>
	<table class="ui striped grey selectable celled table very compact ">
		<p class="right aligned">{{ infos.Name }}<p>
		<p class="left aligned">{{ infos.Ip }}<p>
		<thead>
			<tr class="center aligned">
				<th>Nom</th>
				<th>Ip</th>
				<th>Load</th>
				<th>Heat</th>
				<th>FanSpeed</th>
				<th>Clock</th>
				<th>Mem</</th>
				<th>Max clock</th>
				<th>Max mem</th>
			</tr>
		</thead>
		<?php

		$data = $f->worker;

		$i = 0;
		$x = 0;
		$group = 0;

		foreach ($data as $d) {
			?>	
		<tbody ng-controller="gpu<?= $i ?>">
		<?php

			foreach ((array) $d as $m) {
			?>
			<tr>
				<td class="center aligned">{{ infos.Name }}</td>
				<td class="center aligned">{{ infos.Ip }}</td>
				<tr ng-repeat="g in gpu">
					<td></td>
					<td></td>
					<td ng-class="load()" class="center aligned">
						<span id="load"> {{ g.Load }} </span>%
					</td>
					<td ng-class="heat()" class="center aligned">
						<span id="heat"> {{ g.Heat }} </span>°c
					</td>
					<td ng-class="fan()" class="center aligned">
						<span id="fan"> {{ g.FanSpeed }} </span>%
					</td>
					<td ng-class="clock()" class="center aligned">
						<span id="clock"> {{ (g.CurrentClock / g.MaxClock * 100).toFixed(2) }} </span>%
					</td>
					<td class="center aligned">
						<span id="maxClock"> {{ g.MaxClock }} </span>MhZ
					</td>
					<td ng-class="mem()" class="center aligned">
						<span id="mem"> {{ (g.CurrentMem / g.MaxMem * 100).toFixed(2) }} </span>%
					</td>
					<td class="center aligned">
						<span id="maxMem"> {{ g.MaxMem }} </span>MhZ
					</td>
				</tr>
			</tr>


			<script type="text/javascript">

				app.controller("gpu<?= $i ?>", function($scope, $http) {
				var gpu = function gpuInfos() {
					$http.get("http://<?= $m ?>").then(function (response) {
						$scope.infos = response.data.data;
						$scope.gpu = response.data.data.gpu;
			
								$scope.isUp = function() {
									if (response.data.data.Ip) {
										return "serv__status serv__status--up";
									}
								}
								/*
								$scope.load = function() {
									v = $("#load").text().match(/\d+/)[0];
									if (v <= 50) {
										return ("ui green horizontal label");
									} else if (v <= 80 && v > 50) {
										return ("ui yellow horizontal label");
									} else if (v >= 80) {
										return ("ui red horizontal label");
									}	
								}
					
								$scope.heat = function() {
									v = $("#heat").text().match(/\d+/)[0];
									if (v <= 50) {
										return ("positive");
									} else if (v <= 80 && v > 50) {
										return ("error");
									} else if (v >= 80) {
										return ("warning");
									}
								}
					
								$scope.fan = function() {
									v = $("#fan").text().match(/\d+/)[0];
									if (v <= 50) {
										return ("positive");
									} else if (v <= 80 && v > 50) {
										return ("error");
									} else if (v >= 80) {
										return ("warning");
									}
								}

								$scope.clock = function() {
									v = $("#clock").text().match(/\d+/)[0];
									
									if (v <= 50) {
										return ("positive");
									} else if (v <= 80 && v > 50) {
										return ("error");
									} else if (v >= 80) {
										return ("warning");
									}
								}

								$scope.mem = function() {
									v = $("#mem").text().match(/\d+/)[0];
									
									if (v <= 50) {
										return ("positive");
									} else if (v <= 80 && v > 50) {
										return ("error");
									} else if (v >= 80) {
										return ("warning");
									}
								}
								
								*/
							});
						}
					setInterval(gpu, 1000);
				});
			</script>
		</tbody>
		<?php
			$i++;
		
		}
			$x++;
			$group++;		
		}
		$i = 0;
		?>		
	</table>
</body>
</html>