<!DOCTYPE html>
<html ng-app="app">
<head>
	<meta charset="utf-8">
	<title>GPU Info</title>
	<link rel="stylesheet" type="text/css" href="css/reset.css">
	<link rel="stylesheet" type="text/css" href="css/design.css">
	<link type="text/css" rel="stylesheet" href="css/graph.css">
	<link type="text/css" rel="stylesheet" href="css/line.css">
</head>
<body>
<script src="js/d3.v3.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.min.js"></script>
<script src="js/rickshaw.js"></script>
<script src="js/smothie.js"></script>

<script src="js/angular.min.js"></script>

<script type="text/javascript">
	var app = angular.module('app', []);
	console.log(<?= $rig ?>)
</script>

	<main>
		<div class="container">
		<?php
		// C'est crade mais fonctionnel
		$rig = $_GET['rig'];

		$json_file = file_get_contents('config.json');
		$f = json_decode($json_file);

		$data = $f->worker;

		foreach ($data[$rig] as $d) {
			?>
			<section class="serv" ng-controller="gpu">
			<header class="serv__head">
				<div>
					<span class="serv__status serv__status--up">
						&#9679;
					</span>
					<h3 class="serv__name" id="serv_name">{{ infos.Name }}</h3>
				</div>
				<div class="serv__ip" id="serv_ip">{{ infos.Ip }}</div>
			</header>
			<article class="serv__gpu" ng-repeat="g in infos.gpu">
				<div class="serv__grid-3">
					<div class="serv__mod">
						<div class="serv__modLabel serv__modLabel--red">
							Load
						</div>
						<div class="serv__modNumber" id="serv_load">
							 {{ g.Load }}
							<label class="serv__modUnit">%</label>
						</div>
					</div>
					<div class="serv__mod">
						<div class="serv__modLabel serv__modLabel--green">
							Heat
						</div>
						<div class="serv__modNumber" id="serv_heat">
							 {{ g.Heat }}
							<label class="serv__modUnit">&deg;C</label>
						</div>
					</div>
					<div class="serv__mod">
						<div class="serv__modLabel serv__modLabel--yellow">
							Fan
						</div>
						<div class="serv__modNumber" id="serv_fan">
							 {{ g.FanSpeed }}
							<label class="serv__modUnit">%</label>
						</div>
					</div>
					<div class="serv__mod">
						<div class="serv__modLabel serv__modLabel--red">
							Clock
							<div class="serv__modSublabel">Max</div>
						</div>
						<div class="serv__modNumber">
							{{ (g.CurrentClock / g.MaxClock * 100).toFixed(2) }}
							<label class="serv__modUnit">%</label>
							<div class="serv__modSubnumbler">
								{{ g.MaxClock }}mHz
							</div>
						</div>
					</div>
					<div class="serv__mod">
						<div class="serv__modLabel serv__modLabel--red">
							Mem
							<div class="serv__modSublabel">Max</div>
						</div>
						<div class="serv__modNumber">
							{{ (g.CurrentMem / g.MaxMem * 100).toFixed(2) }}
							<span id="serv_mem"></span>
							<label class="serv__modUnit">%</label>
							<div class="serv__modSubnumbler">
								<span id="serv_maxmem"></span>{{ g.MaxMem }}mHz
							</div>
						</div>
					</div>
				</div>
			</article>
		</section>

		<script type="text/javascript">

			app.controller("gpu", function($scope, $http) {
				var gpu = function gpuInfos() {
				$http.get("http://<?= $d ?>").then(function (response) {
					$scope.infos = response.data.data;
				});}
				setInterval(gpu, 1000);
			});

		</script>

		<?php
		}
		?>
		</div>
	</main>
</body>
</html>