
pot:
	intltool-extract --type="gettext/ini" gtkalsasetup.desktop.in
	intltool-extract --type="gettext/ini" gtkalsasetup-kde.desktop.in
	xgettext --from-code=utf-8 \
		-x po/EXCLUDE \
		-L Glade \
		-o po/gtkalsasetup.pot \
		gtkalsasetup.ui
	xgettext --from-code=utf-8 \
		-j \
		-L Python \
		-o po/gtkalsasetup.pot \
		gtkalsasetup
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkalsasetup.pot gtkalsasetup.desktop.in.h
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkalsasetup.pot gtkalsasetup-kde.desktop.in.h
	rm gtkalsasetup.desktop.in.h gtkalsasetup-kde.desktop.in.h

update-po:
	for i in `ls po/*.po`; do \
		msgmerge -U $$i po/gtkalsasetup.pot ;\
	done
	rm -f po/*~

.PHONY: pot update-po
