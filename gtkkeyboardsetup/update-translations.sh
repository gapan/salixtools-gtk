#!/bin/sh

intltool-extract --type="gettext/ini" gtkkeyboardsetup.desktop.in
intltool-extract --type="gettext/ini" gtkkeyboardsetup-kde.desktop.in

xgettext --from-code=utf-8 \
	-x po/EXCLUDE \
	-L Glade \
	-o po/gtkkeyboardsetup.pot \
	gtkkeyboardsetup.glade

xgettext --from-code=utf-8 \
	-j \
	-L Python \
	-o po/gtkkeyboardsetup.pot \
	gtkkeyboardsetup
xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkkeyboardsetup.pot gtkkeyboardsetup.desktop.in.h
xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkkeyboardsetup.pot gtkkeyboardsetup-kde.desktop.in.h

rm gtkkeyboardsetup.desktop.in.h gtkkeyboardsetup-kde.desktop.in.h

cd po
for i in `ls *.po`; do
	msgmerge -U $i gtkkeyboardsetup.pot
done
rm -f ./*~

