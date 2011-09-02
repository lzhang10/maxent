find . -type d -exec chmod 0755 {} \;
find . -type f -exec chmod 0644 {} \;
chmod 0755 configure
chmod 0755 script/pkg_build.sh
chmod 0755 script/fileperm.sh
chmod 0755 script/dist_bin.sh
chmod 0755 script/boostheaders.py
chmod 0755 tools/build_jam.sh
