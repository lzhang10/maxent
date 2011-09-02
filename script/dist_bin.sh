#!/bin/sh
# make a binary only distribution

OS=`uname -s` 
package=maxent
COMPRESS=touch # do nothing by default
if [ -x /usr/bin/upx ]; then
    COMPRESS=/usr/bin/upx
fi

if [ -x /usr/local/bin/upx ]; then
    COMPRESS=/usr/local/bin/upx
fi

if [ `echo $CC | grep mingw` ]; then
    OS=XMINGW32
    if [ -x /usr/local/mingw32/bin/upx.exe ]; then
        COMPRESS="wine -- /usr/local/mingw32/bin/upx.exe"
    fi
fi

build_unix() {
    platform=$1
    ./configure --enable-static
    make
    tmp_dir=`mktemp -d /tmp/tmp_build.XXXXXX`
    cd src/opt
    strip maxent
    $COMPRESS maxent
    cd -
    cp README LICENSE src/opt/maxent $tmp_dir
    cd $tmp_dir
    tar cf ${package}-${platform}-static.tar README LICENSE maxent
    gzip ${package}-${platform}-static.tar
    cd -
    mv $tmp_dir/${package}-${platform}-static.tar.gz .
    rm -rf $tmp_dir
    echo "Done!"
}

build_cygwin() {
    ./configure --enable-static
    make
    tmp_dir=`mktemp -d /tmp/tmp_build.XXXXXX`
    cd src/opt
    strip maxent.exe
    cd -
    cp README LICENSE src/opt/maxent.exe $tmp_dir
    cp /usr/bin/cygwin1.dll $tmp_dir
    cd $tmp_dir
    zip -j ${package}-cygwin-static.zip README LICENSE maxent.exe cygwin1.dll
    cd -
    mv $tmp_dir/${package}-cygwin-static.zip .
    rm -rf $tmp_dir
    echo "Done!"
}

build_mingw() {
    ./configure --enable-static
    make
    tmp_dir='tmp_build'
    rm -rf $tmp_dir
    mkdir $tmp_dir
    cd src/opt
    strip maxent.exe
    $COMPRESS maxent.exe
    cd -
    cp README LICENSE src/opt/maxent.exe $tmp_dir
    cd $tmp_dir
    tar zcf ${package}-mingw32-static.tar.gz README LICENSE maxent.exe
    mv ${package}-mingw32-static.tar.gz ..
    cd -
    rm -rf $tmp_dir
    echo "Done!"
}

build_cross_mingw() {
    STRIP=/usr/local/bin/mingw32-strip
    ./configure --prefix=/usr/local/mingw32/ --host=i386-pc-mingw32 --enable-static
    make
    tmp_dir=`mktemp -d /tmp/tmp_build.XXXXXX`
    cd src/opt
    $STRIP maxent.exe
    $COMPRESS maxent.exe
    cd -
    cp README LICENSE src/opt/maxent.exe $tmp_dir
    cd $tmp_dir
    zip -j ${package}-mingw32-static.zip README LICENSE maxent.exe
    mv ${package}-mingw32-static.zip ..
    cd -
    rm -rf $tmp_dir
    echo "Done! See /tmp for result file."
}

case $OS in
    FreeBSD)
    echo "Building FreeBSD binaries"
    build_unix freebsd
    ;;
    Linux)
    echo "Building Linux binaries"
    build_unix linux
    ;;
    CYGWIN*)
    echo "Building Cygwin binaries"
    build_cygwin
    ;;
    MINGW32*)
    echo "Building MingW32 binaries"
    build_mingw
    ;;
    XMINGW32*)
    echo "Building Cross MingW32 binaries"
    build_cross_mingw
    ;;
    *)
    echo "Sorry your OS is not supported yet"
    ;;
esac

