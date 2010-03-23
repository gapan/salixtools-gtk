#!/bin/sh

xgettext --from-code=utf-8 \
	-x EXCLUDE \
	-L Glade \
	-o gtklocalesetup.pot \
	../gtklocalesetup.glade
