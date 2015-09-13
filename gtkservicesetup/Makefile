
pot:
	intltool-extract --type="gettext/ini" gtkservicesetup.desktop.in
	intltool-extract --type="gettext/ini" gtkservicesetup-kde.desktop.in
	xgettext --from-code=utf-8 \
		-x po/EXCLUDE \
		-L Glade \
		-o po/gtkservicesetup.pot \
		gtkservicesetup.glade
	xgettext --from-code=utf-8 \
		-j \
		-L Python \
		-o po/gtkservicesetup.pot \
		gtkservicesetup
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkservicesetup.pot gtkservicesetup.desktop.in.h
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkservicesetup.pot gtkservicesetup-kde.desktop.in.h
	rm gtkservicesetup.desktop.in.h gtkservicesetup-kde.desktop.in.h

update-po:
	for i in `ls po/*.po`; do \
		msgmerge -U $$i po/gtkservicesetup.pot ;\
	done
	rm -f po/*~

.PHONY: pot update-po
