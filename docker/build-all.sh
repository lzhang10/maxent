#!/usr/bin/env bash
# build and run unit tests in supported docker containers
set -e
set -o pipefail

mkdir -p "${TMP:-/tmp}"
tmp=$(mktemp -d "${TMP:-/tmp}/XXXXX")
trap "trap - SIGTERM && kill 0" SIGINT SIGTERM # kill all children processes on exit
trap "rm -rf $tmp" EXIT                        # clean up on exit

script_dir=$(dirname $(readlink -f $0))

for os in debian9 debian10 debian11 ubuntu16.04 ubuntu18.04 ubuntu20.04; do
    echo -n "Building on $os ... "
    if ! docker build -t lzhang10/maxent:$os -f Dockerfile.$os "$script_dir"/.. > $tmp/$os.log 2>&1; then
        echo "FAILED"
        cat $tmp/$os.log
    fi
    echo "OK"
done
