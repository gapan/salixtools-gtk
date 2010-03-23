#!/bin/sh

intltool-extract --type="gettext/ini" gtkusersetup.desktop.in
intltool-extract --type="gettext/ini" gtkusersetup-kde.desktop.in

xgettext --from-code=utf-8 \
	-x po/EXCLUDE \
	-L Glade \
	-o po/gtkusersetup.pot \
	gtkusersetup.glade

xgettext --from-code=utf-8 \
	-j \
	-L Python \
	-o po/gtkusersetup.pot \
	gtkusersetup
xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkusersetup.pot gtkusersetup.desktop.in.h
xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkusersetup.pot gtkusersetup-kde.desktop.in.h

rm gtkusersetup.desktop.in.h gtkusersetup-kde.desktop.in.h

cd po
for i in `ls *.po`; do
	msgmerge -U $i gtkusersetup.pot
done
rm -f ./*~

