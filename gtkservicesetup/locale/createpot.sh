#!/bin/sh

xgettext --from-code=utf-8 \
	-x exclude.po \
	-L Glade \
	-o gtkservicesetup.pot \
	../gtkservicesetup.glade

xgettext --from-code=utf-8 \
	-j \
	-L Python \
	-o gtkservicesetup.pot \
	../gtkservicesetup
