#!/bin/sh
# build a source package by including all files specified in filelist.txt
# into a tar ball named as package-version.tar.gz

VERSION=`date "+%Y%m%d"`
PACKAGE=maxent
FILELIST="`dirname $0`/filelist.txt"
FILEPERM="`dirname $0`/fileperm.sh"

tmp_dir=$PACKAGE-$VERSION
rm -rf $tmp_dir
mkdir $tmp_dir

#copying file
for f in `cat ${FILELIST}`; do
    dest_file="$tmp_dir/$f"
    dest_dir="$tmp_dir/`dirname $f`"
    if [ ! -d $dest_dir ]; then
        mkdir -p $dest_dir
    fi
    echo "copying $f to $dest_file"
    cp -H $f $dest_file
    chmod 0644 $dest_file
done

#set special file permission
cd $tmp_dir
. ../$FILEPERM
cd ..

tar cf $tmp_dir.tar $tmp_dir
gzip -f -9 $tmp_dir.tar
rm -rf $tmp_dir
