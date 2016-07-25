<!DOCTYPE html>
<html>
<head>
	<title>EthPanel</title>
	<link rel="stylesheet" type="text/css" href="css/list.css">
</head>
<body class="standard">
	<table>
	<?php
			
			$file = file_get_contents("config.json");
			$f = json_decode($file);

			$miner = $f->worker[0];
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
				foreach ($m as $k) {

				?>
		<tr>
			<td><a href="http://<?= $k ?>" target="_blank"><?= $k ?></a></td>
			<td>
			<a href="single.php?group=<?= $i ?>&rig=<?= $r ?>" target="_blank">Single page</a>
			</td>
			<td>At work</td>
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
</body>
</html>