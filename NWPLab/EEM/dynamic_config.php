<?php

$hostname = $_GET['hostname'];
if (!isset($hostname)) {
        die("Hostname parameter has not been set.");
}

$len = strlen($hostname);
$hf = str_repeat('-', ($len * 2));
$padded = preg_replace("/(.)/", "\\1 ", strtoupper($hostname));

$result = array();
$result['EXEC'] = array();
$result['CONFIG'] = array();

$banner = array();
$b = array();
$b['type'] = 'login';

$btext = $hf . "\n";
$btext .= $padded . "\n";
$btext .= $hf . "\n";
$btext .= "This router is part of the Network Programmability and Automation Lab.\n";
$btext .= "UNAUTHORIZED USE IS STRICTLY FORBIDDEN.\n";

$b['text'] = $btext;

array_push($banner, $b);
$result['CONFIG']['banner'] = $banner;

echo json_encode($result);

?>
