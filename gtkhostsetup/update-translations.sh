#!/bin/sh

intltool-extract --type="gettext/ini" gtkhostsetup.desktop.in
intltool-extract --type="gettext/ini" gtkhostsetup-kde.desktop.in

xgettext --from-code=utf-8 \
	-x po/EXCLUDE \
	-L Glade \
	-o po/gtkhostsetup.pot \
	gtkhostsetup.glade

xgettext --from-code=utf-8 \
	-j \
	-L Python \
	-o po/gtkhostsetup.pot \
	gtkhostsetup
xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkhostsetup.pot gtkhostsetup.desktop.in.h
xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkhostsetup.pot gtkhostsetup-kde.desktop.in.h

rm gtkhostsetup.desktop.in.h gtkhostsetup-kde.desktop.in.h

cd po
for i in `ls *.po`; do
	msgmerge -U $i gtkhostsetup.pot
done
rm -f ./*~

