<?php

$contents = trim(file_get_contents("/var/www/istats.dat"));

$ilines = explode("\n", $contents);

$contents = trim(file_get_contents("/var/www/ostats.dat"));

$olines = explode("\n", $contents);

$points = array();

for ($i = 0; $i < count($ilines); $i++) {
    array_push($points, "[$i, {$ilines[$i]}, {$olines[$i]}]");
}

?>

<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<div id="chart_div"></div>

<script language="JavaScript">
google.load('visualization', '1', {packages: ['corechart', 'line']});
google.setOnLoadCallback(drawChart);

function drawChart() {
      var data = new google.visualization.DataTable();
      data.addColumn('number', 'X');
      data.addColumn('number', 'Input');
      data.addColumn('number', 'Output');
      
      data.addRows([<?=implode(",", $points)?>]);
      
      var options = {
          hAxis: {
              title: 'Time'
          },
          vAxis: {
              title: 'Bytes'
          },
      };
      
      var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
      chart.draw(data, options);
}
</script>
        