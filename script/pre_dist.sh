#!/bin/sh
# various patches for making a final dist tar ball
version=`date "+%Y%m%d"`

update_version_string() {
    old=$1
    new=$1.new
    sed "s/version-devel/${version}/g" < $old > $new
    rm $old
    mv $new $old
}

update_version_string config.h 
update_version_string configure
update_version_string python/setup.py.in
update_version_string python/setup.py

. script/fileperm.sh
