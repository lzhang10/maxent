#!/bin/sh
echo "Building jam executable ..."
tar xf jam-2.5.tar

cd jam-2.5

OS=`uname -s`
case $OS in
    MINGW32*)
    echo "apply patch for MINGW32 environment"
    patch -p1 < ../mingw.diff
    ;;
    *) ;;
esac 

make

find . -name "jam" -exec cp {} ../jam \;
find . -name "jam.exe" -exec cp {} ../jam.exe \;

if [ ! -x ../jam -a ! -x ../jam.exe ]; then 
    # fail to build jam, fallback to jam0
    find . -name "jam0" -exec cp {} ../jam \;
    find . -name "jam0.exe" -exec cp {} ../jam.exe \;
fi

cd ..
rm -rf jam-2.5
echo "Done!"
