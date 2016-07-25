<!DOCTYPE html>
<html ng-app="app">
<head>
	<meta charset="utf-8">
	<title>GPU Info</title>
	<link rel="stylesheet" type="text/css" href="css/reset.css">
	<link rel="stylesheet" type="text/css" href="css/design.css">
</head>
<body>
<script src="js/angular.min.js"></script>
<script src="js/jquery-2.2.4.min.js"></script>
<script type="text/javascript">
	var app = angular.module('app', []);
</script>
		<?php
		// C'est crade mais fonctionnel
		$json_file = file_get_contents('config.json');
		$f = json_decode($json_file);

		$dataH = $f->master;
		$s = 0;
		foreach ($dataH as $d) {
			?>
		<header class="header" ng-controller="ctrl_master<?= $s ?>">
			<div class="container" ng-repeat="i in infos">
				<div class="header__serv">
					<h1 class="header__servName"></h1>
					<div class="header__servIp">{{ i.Ip }}</div>
				</div>
				<div class="header__stat">
					<h2 class="header__statName">Gain</h2>
					<div>
						<div>
							<span class="header__statNumber">{{ i.Balance /1000000000000000000 }}</span>
							<span class="header__statUnit"> eth</span>
						</div>
						<div>
							<span class="header__statNumber">{{ i.Euro }}</span>
							<span class="header__statUnit"> &euro;</span>
						</div>
					</div>
				</div>
				<div class="header__stat">
					<h2 class="header__statName">Hash</h2>
					<div>
						<span class="header__statNumber">{{ (i.Hash / 1000000).toFixed(2) }}</span>
						<span class="header__statUnit">Mh/s</span>
					</div>
				</div>
			</div>
			<script type="text/javascript">
			app.controller('ctrl_master<?= $s ?>', function($scope, $http) {
			var master = function gpuInfos() {
			$http.get("http://<?= $d->ip ?>") .then(function (response) {
				$scope.infos = response.data.data;
			});}
			setInterval(master, 1000);
		});
		</script>
		</header>
		
		<?php
			$s++;
		}
		?>


	<main>
		<div class="container">
		<?php

		$data = $f->worker[0];

		$i = 0;

		foreach ($data as $d) {
			foreach ($d as $m) {
			?>
			<section class="serv" ng-controller="gpu<?= $i ?>">
			<header class="serv__head">
				<div>
					<span ng-class="isUp()">
						&#9679;
					</span>
					<h3 class="serv__name" id="serv_name">
					<a href="single.php?rig=<?= $i ?>" target="_blank">{{ infos.Name }}</a>  	
					</h3>
				</div>
				<div class="serv__ip">Baie : <?= $i ?> | <span id="serv_ip"> {{ infos.Ip }} </span></div>
			</header>
			<article class="serv__gpu" ng-repeat="g in infos.gpu">
				<div class="serv__grid-3">
					<div class="serv__mod">
						<div ng-class="load()">
							Load
						</div>
						<div class="serv__modNumber">
							<span id="load">{{ g.Load }}</span>
							<label class="serv__modUnit">%</label>
						</div>
					</div>
					<div class="serv__mod">
						<div ng-class="heat()">
							Heat
						</div>
						<div class="serv__modNumber">
							<span id="heat">{{ g.Heat }}</span>
							<label class="serv__modUnit">&deg;C</label>
						</div>
					</div>
					<div class="serv__mod">
						<div ng-class="fan()">
							Fan
						</div>
						<div class="serv__modNumber">
							<span id="fan">{{ g.FanSpeed }}</span>
							<label class="serv__modUnit">%</label>
						</div>
					</div>
					<div class="serv__mod">
						<div class="serv__modLabel serv__modLabel--red">
							Clock
							<div class="serv__modSublabel">Max</div>
						</div>
						<div class="serv__modNumber" id="serv_clock">
							{{ (g.CurrentClock / g.MaxClock * 100).toFixed(2) }}
							<label class="serv__modUnit">%</label>
							<div class="serv__modSubnumbler" id="serv_maxclock">
								{{ g.MaxClock }}mHz
							</div>
						</div>
					</div>
					<div class="serv__mod">
						<div class="serv__modLabel serv__modLabel--red">
							Mem
							<div class="serv__modSublabel">Max</div>
						</div>
						<div class="serv__modNumber" id="serv_mem">
							{{ (g.CurrentMem / g.MaxMem * 100).toFixed(2) }}
							<span id="serv_mem"></span>
							<label class="serv__modUnit">%</label>
							<div class="serv__modSubnumbler" id="serv_maxmem">
								{{ g.MaxMem }}mHz
							</div>
						</div>
					</div>
				</div>
			</article>
		
		<script type="text/javascript">

			app.controller("gpu<?= $i ?>", function($scope, $http) {
			var gpu = function gpuInfos() {
				$http.get("http://<?= $m ?>").then(function(response) {
							$scope.infos = response.data.data;
							$scope.isUp = function() {
								if (response.data.data.Ip) {
									return "serv__status serv__status--up";
								}
							}
				
							$scope.isUp = function() {
								if (response.data.data.Ip) {
									return "serv__status serv__status--up";
								}
							}
				
							$scope.load = function() {
								v = $("#load").text().match(/\d+/)[0];
								if (v <= 50) {
									return ("serv__modLabel serv__modLabel--green");
								} else if (v <= 80 && v > 50) {
									return ("serv__modLabel serv__modLabel--yellow");
								} else if (v >= 80) {
									return ("serv__modLabel serv__modLabel--red");
								}	
							}
				
							$scope.heat = function() {
								v = $("#heat").text().match(/\d+/)[0];
								if (v <= 50) {
									return ("serv__modLabel serv__modLabel--green");
								} else if (v <= 80 && v > 50) {
									return ("serv__modLabel serv__modLabel--yellow");
								} else if (v >= 80) {
									return ("serv__modLabel serv__modLabel--red");
								}	
							}
				
							$scope.fan = function() {
								v = $("#fan").text().match(/\d+/)[0];
								if (v <= 50) {
									return ("serv__modLabel serv__modLabel--green");
								} else if (v <= 80 && v > 50) {
									return ("serv__modLabel serv__modLabel--yellow");
								} else if (v >= 80) {
									return ("serv__modLabel serv__modLabel--red");
								}	
							}
						});
					}
				setInterval(gpu, 1000);
			});

		</script>
		</section>
		<?php
			}
			$i++;
		}
		?>
		</div>
	</main>
</body>
</html>