#!/bin/sh

xgettext --from-code=utf-8 \
	-x EXCLUDE \
	-L Glade \
	-o gtkusersetup.pot \
	../gtkusersetup.glade

xgettext --from-code=utf-8 \
	-j \
	-L Python \
	-o gtkusersetup.pot \
	../gtkusersetup
