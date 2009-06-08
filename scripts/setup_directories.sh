#!/bin/bash

echo "creating necessary folders for deployment..."
for dir in {{ site_folders }}
do
    if [[ -d $dir ]]; then
        echo $dir "already exists."
    else
        mkdir $dir
        echo "created" $dir
    fi
done

echo "creating necessary log files for deployment..."
for logfile in {{ log_files }}
do
    if [[ -d $logfile ]]; then
        echo $logfile "already exists."
    else
        touch $logfile
        echo "created" $logfile
    fi
done

echo "setting permissions where necessary..."
exit
