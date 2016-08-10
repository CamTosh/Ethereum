<!DOCTYPE html>
<html>
<head>
	<title>EthPanel</title>
	<link rel="stylesheet" type="text/css" href="css/reset.css">
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/semantic-ui/2.2.2/semantic.min.css">
</head>
<body>
<div class="ui info message">
	<div class="header">Thanks for use this dashboard !</div>
	<p>There is still in development but you can contribute : <a href="https://github.com/CamTosh/Ethereum/" target="_blank">Github</a></p>
</div>
<center>
	<table class="ui orange table collapsing celled">
		<tfoot class="full-width">
			<tr>
				<th>
					Dashboard
				</th>
				<th>
					<a href="list.php"><div class="ui right floated small labeled icon blue basic button"><i class="list layout icon"></i>List</div></a>
				</th>
				<th>
					<a href="dashboard.php"><div class="ui right floated small labeled icon blue basic button"><i class="grid  layout icon"></i> Grid</div></a>
				</th>
			</tr>
	  </tfoot>
	</table>
	<table class="ui green table collapsing selectable celled"">
	<?php
			
			$file = file_get_contents("config.json");
			$f = json_decode($file);

			$miner = $f->master;
			$i = 0;

			foreach ($miner as $m) {
				?>
		<thead>
			<tr>
				<th>Master <?= $i ?></th>
				<th>Link</th>
				<th>Status</th>
			</tr>
		</thead>
		<tbody>
		<?php
				$r = 0;
				foreach ((array) $m as $k) {

				?>
		<tr>
			<td><a href="http://<?= $k ?>" target="_blank"><?= $k ?></a></td>
			<td>
			<a href="single.php?group=<?= $i ?>&rig=<?= $r ?>" target="_blank">Single page</a>
			</td>
			<td class="positive">At work</td>
		</tr>
		<?php
				$r++;
			}
			$i++;
				?>
		</tbody>
	<?php
		}
		?>

	</table>
	<table class="ui grey table collapsing selectable celled"">
	<?php
			
			$file = file_get_contents("config.json");
			$f = json_decode($file);

			$miner = $f->worker;
			$i = 0;

			foreach ($miner as $m) {
				?>
		<thead>
			<tr>
				<th>Baie <?= $i ?></th>
				<th>Link</th>
				<th>Status</th>
			</tr>
		</thead>
		<tbody>
		<?php
				$r = 0;
				foreach ((array) $m as $k) {

				?>
		<tr>
			<td><a href="http://<?= $k ?>" target="_blank"><?= $k ?></a></td>
			<td>
			<a href="single.php?group=<?= $i ?>&rig=<?= $r ?>" target="_blank">Single page</a>
			</td>
			<td class="positive">At work</td>
		</tr>
		<?php
				$r++;
			}
			$i++;
				?>
		</tbody>
	<?php
		}
		?>
	</table>
</center>
</body>
</html>