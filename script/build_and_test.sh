#!/usr/bin/env bash

set -e
set -o pipefail
set -u

script_dir=$(dirname $(readlink -f $0))

cd "$script_dir/.."
mkdir build
cd build
cmake ..
make -j8
cd test
ctest
