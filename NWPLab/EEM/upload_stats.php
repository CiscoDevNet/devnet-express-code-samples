<?php

header("Content-Type: text/plain");

if (!isset($_GET['ostats']) || !isset($_GET['istats'])) {
    die("ERROR: The arguments 'ostats' and 'istats' must be specified!");
}

$fd = fopen("/var/www/ostats.dat", "a");

fwrite($fd, $_GET['ostats']);

@fclose($fd);

$fd = fopen("/var/www/istats.dat", "a");

fwrite($fd, $_GET['istats']);

@fclose($fd);

?>
SUCCESS