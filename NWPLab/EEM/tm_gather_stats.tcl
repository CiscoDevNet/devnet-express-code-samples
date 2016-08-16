::cisco::eem::event_register_timer watchdog time 10

namespace import ::cisco::eem::*
namespace import ::cisco::lib::*

namespace import ::http::*

if { [catch {cli_open} result] } {
    error $result $errorInfo
}

array set cli $result

if { [catch {context_retrieve STATSCTXT prev_stats} result] } {
    array set prev_stats [list]
    set prev_stats(ibytes) 0
    set prev_stats(obytes) 0
} else {
    array set prev_stats $result
}

if { [catch {cli_exec $cli(fd) "enable"} result] } {
    error $result $errorInfo
}

if { [catch {cli_exec $cli(fd) "show interface gi0/1 | inc bytes"} result] } {
    error $result $errorInfo
}

foreach line [split $result "\n"] {
    regexp {packets input, (\d+) bytes} $line -> ibytes
    regexp {packets output, (\d+) bytes} $line -> obytes
}

set istats [expr $ibytes - $prev_stats(ibytes)]
set ostats [expr $obytes - $prev_stats(obytes)]

set prev_stats(ibytes) $ibytes
set prev_stats(obytes) $obytes

catch {context_save STATSCTXT prev_stats}

catch {cli_close $cli(fd) $cli(tty_id)}

## HTTP CODE HERE
::http::config -useragent "tm_gather_stats.tcl/1.0"
set tok [::http::geturl "http://10.0.0.6/upload_stats.php?ostats=$ostats&istats=$istats"]
if { [::http::error $tok] != "" } {
    puts "ERROR: Failed to upload stats: '[::http::error $tok]'"
    exit 1
}
foreach line [split [::http::data $tok] "\n"] {
    if { [regexp {SUCCESS} $line] } {
        break
    }
    if { [regexp {ERROR} $line] } {
        puts "ERROR: Failed to upload stats: '$line'"
        exit 1
    }
}
## END HTTP CODE