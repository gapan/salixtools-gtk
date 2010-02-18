#!/bin/sh

xgettext --from-code=utf-8 \
	-x exclude.po \
	-L Glade \
	-o gtkclocksetup.pot \
	../gtkclocksetup.glade

xgettext --from-code=utf-8 \
	-j \
	-L Python \
	-o gtkclocksetup.pot \
	../gtkclocksetup
