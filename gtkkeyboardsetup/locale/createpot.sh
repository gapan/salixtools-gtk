#!/bin/sh

xgettext --from-code=utf-8 \
	-x EXCLUDE \
	-L Glade \
	-o gtkkeyboardsetup.pot \
	../gtkkeyboardsetup.glade

xgettext --from-code=utf-8 \
	-j \
	-L Python \
	-o gtkkeyboardsetup.pot \
	../gtkkeyboardsetup
