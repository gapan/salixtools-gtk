#!/bin/sh

xgettext --from-code=utf-8 \
	-x exclude.po \
	-L Glade \
	-o gtklocalesetup.pot \
	../gtklocalesetup.glade
