#!/bin/bash

# Copyright (C) 2015 Craig Phillips.  All rights reserved.

bashcat_test 8 3 5 2 66.7 <<SCRIPT
case "some_text" in
(some_text)
    true # Covered
    ;;
(different_text)
    true # Not covered
    ;;
esac
SCRIPT

bashcat_test 6 4 2 2 50.0 <<SCRIPT
case "some_text" in
(some_text)
    true ;; # Covered 
(different_text)
    true ;; # Not covered 
esac
SCRIPT

bashcat_test 7 4 3 2 50.0 <<SCRIPT
case "some_text" 
    in
(some_text)
    true ;; # Covered 
(different_text)
    true ;; # Not covered 
esac
SCRIPT

bashcat_test 21 7 14 2 28.6 <<SCRIPT
case "$1" in
        start)
            start
            ;;
         
        stop)
            stop
            ;;
         
        status)
            status 
            ;;
        restart)
            stop
            start
            ;;
         
        *)
            echo 
 
esac
SCRIPT

bashcat_test 12 4 8 2 50.0 <<SCRIPT
case "yno" in

        [yY] | [yY][Ee][Ss] )
                echo 
                ;;

        [nN] | [n|N][O|o] )
                echo 
                ;;
        *) echo 
            ;;
esac
SCRIPT
bashcat_test 8 3 5 2 66.7 <<SCRIPT
case blah
in
blah) true ;;
blah) ;;
blah)
    true
    ;;
esac
SCRIPT

bashcat_test 8 3 5 2 66.7 <<SCRIPT
case blah
in
blah\)) ;;
blah) true ;;
blah)
    true
    ;;
esac
SCRIPT

bashcat_test 8 3 5 2 66.7 <<SCRIPT
case blah
in
blah\)) ;;
blah\)) true ;;
blah)
    true
    ;;
esac
SCRIPT

bashcat_test 8 3 5 2 66.7 <<SCRIPT
case blah
in
blah\)) ;;
blah) true ;;
blah\))
    true
    ;;
esac
SCRIPT
