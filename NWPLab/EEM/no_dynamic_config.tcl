::cisco::eem::description "This policy fetches dynamic configuration from an HTTP server based on the hostname of the requesting device"
::cisco::eem::event_register_none maxrun 60

namespace import ::cisco::eem::*
namespace import ::cisco::lib::*
# This next line imports the built-in HTTP 1.0 client library module.
namespace import ::http::*

# Import our tcllib JSON library and its requirement
source "dict.tcl"
source "json.tcl"

# This procedure will take the decoded JSON result and parse it
# to determine what needs to be done.
proc parseData { dataDict } {
    set execCmds [dict get $dataDict EXEC]
    set cfgCmds [dict get $dataDict CONFIG]
    
    if { [llength $execCmds] } {
        processExec $execCmds
    }
    
    if { [llength $cfgCmds] } {
        processCfg $cfgCmds
    }
}

proc processExec { cmds } {
    global errorInfo

    if { [catch {cli_open} result] } {
	    error "Failed to open CLI session: '$result'" $errorInfo
    }
    
    array set cli $result
    
    if { [catch {cli_exec $cli(fd) "enable"} result] } {
	    error "Failed to enter enable mode: '$result'" $errorInfo
    }
    
    foreach cmd $cmds {
        if { [catch {cli_exec $cli(fd) $cmd} result] } {
	        error "Failed to execute the command '$cmd': '$result'" $errorInfo
        }
    }
    
    catch {cli_close $cli(fd) $cli(tty_id)}
}

proc processCfg { cmdArr } {
    global errorInfo
    
    if { [catch {cli_open} result] } {
	    error "Failed to open CLI session: '$result'" $errorInfo
    }
    
    array set cli $result
    
    if { [catch {cli_exec $cli(fd) "enable"} result] } {
	    error "Failed to enter enable mode: '$result'" $errorInfo
    }
    
    if { [catch {cli_exec $cli(fd) "config t"} result] } {
	    error "Failed to enter configure mode: '$result'" $errorInfo
    }
    
    foreach ss [dict keys $cmdArr] {
        if { $ss == {banner} } {
            foreach b [dict get $cmdArr $ss] {
                configureBanner $cli(fd) $b
            }
        } else {
            foreach cmd [split [dict get $cmdArr $ss] "\n"] {
                if { [catch {cli_exec $cli(fd) $cmd} result] } {
	                error "Failed to execute the command '$cmd': '$result'" $errorInfo
                }
            }
        }
    }
    
    if { [catch {cli_exec $cli(fd) "end"} result] } {
	    error "Failed to leave configure mode: '$result'" $errorInfo
    }
    
    catch {cli_close $cli(fd) $cli(tty_id)}
}
    

# This procedure calls the built-in CLI library
# and then configures the banner based on the dynamic
# data we read from the HTTP server.
proc configureBanner { cli banner } {
    global errorInfo
    
    if { [catch {cli_write $cli "banner [dict get $banner type] |"} result] } {
	    error "Failed to being banner config: '$result'" $errorInfo
    }

    if { [catch {cli_read_pattern $cli "End with the character"} result] } {
	    error "Failed to configure banner: '$result'" $errorInfo
    }

    foreach line [dict get $banner text] {
	    if { [catch {cli_write $cli $line} result] } {
	        error "Failed to configure banner: '$result'" $errorInfo
	    }

	    after 1000
    }

    if { [catch {cli_write $cli "|"} result] } {
	    error "Failed to end banner configuration: '$result'" $errorInfo
    }

    if { [catch {cli_read_pattern $cli "#"} result] } {
	    error "Failed to read prompt: '$result'" $errorInfo
    }
}

# Set out HTTP user agent to something clever.
::http::config -useragent "EASy_HTTP/1.0"

# Open an HTTP connection to our web server.  We will pass an
# HTTP GET argument to the server.  That argument, hostname, will
# contain the hostname of our router.
set tok [::http::geturl "http://10.0.0.6/dynamic_config.php?hostname=[info hostname]"]
if { [::http::error $tok] != "" } {
    puts "ERROR: Failed to get banner config: '[::http::error $tok]'"
    exit 1
}

# The output from the HTTP server will be passed to the tcllib json
# library.  The resulting overall "dictionary" object will be passed
# to our user-defined parseData procedure.
parseData [json::json2dict [::http::data $tok]]