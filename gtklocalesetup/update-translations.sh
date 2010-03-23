#!/bin/sh

intltool-extract --type="gettext/ini" gtklocalesetup.desktop.in
intltool-extract --type="gettext/ini" gtklocalesetup-kde.desktop.in

xgettext --from-code=utf-8 \
	-x po/EXCLUDE \
	-L Glade \
	-o po/gtklocalesetup.pot \
	gtklocalesetup.glade

xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtklocalesetup.pot gtklocalesetup.desktop.in.h
xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtklocalesetup.pot gtklocalesetup-kde.desktop.in.h

rm gtklocalesetup.desktop.in.h gtklocalesetup-kde.desktop.in.h

cd po
for i in `ls *.po`; do
	msgmerge -U $i gtklocalesetup.pot
done
rm -f ./*~

