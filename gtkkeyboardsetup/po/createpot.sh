#!/bin/sh

xgettext --from-code=utf-8 \
	-x EXCLUDE \
	-L Glade \
	-o gtkkeyboardsetup.pot \
	../gtkkeyboardsetup.ui

xgettext --from-code=utf-8 \
	-j \
	-L Python \
	-o gtkkeyboardsetup.pot \
	../gtkkeyboardsetup.py
