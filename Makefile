# This is the surprisingly simple Makefile.
# I don't like the way gmake and automake work, they tend to cause 
# more problems. Therefore I use Jam instead.
#
# This file does the following things:
# First, it builds jam executable in tools/jam if it is not availiable on the
# system. 
# Then it forwards all building requests to Jam
# Jam is the building tool of the well known Boost C++ lib:
# http://www.boost.org

all: tools/jam build_all

build_all:
	@tools/jam -d0

install: tools/jam
	@tools/jam install

uninstall: tools/jam
	@tools/jam uninstall

clean: tools/jam
	@BUILD_TEST=yes tools/jam clean

unittest: tools/jam
	@BUILD_TEST=yes tools/jam -d0

tools/jam:
	@cd tools && sh build_jam.sh

# END OF FILE
