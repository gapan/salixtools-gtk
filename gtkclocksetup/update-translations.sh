#!/bin/sh

intltool-extract --type="gettext/ini" gtkclocksetup.desktop.in
intltool-extract --type="gettext/ini" gtkclocksetup-kde.desktop.in

xgettext --from-code=utf-8 \
	-x po/EXCLUDE \
	-L Glade \
	-o po/gtkclocksetup.pot \
	gtkclocksetup.glade

xgettext --from-code=utf-8 \
	-j \
	-L Python \
	-o po/gtkclocksetup.pot \
	gtkclocksetup

xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkclocksetup.pot gtkclocksetup.desktop.in.h
xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkclocksetup.pot gtkclocksetup-kde.desktop.in.h

rm gtkclocksetup.desktop.in.h gtkclocksetup-kde.desktop.in.h

cd po
for i in `ls *.po`; do
	msgmerge -U $i gtkclocksetup.pot
done
rm -f ./*~

