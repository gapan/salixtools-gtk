
pot:
	intltool-extract --type="gettext/ini" gtkkeyboardsetup.desktop.in
	intltool-extract --type="gettext/ini" gtkkeyboardsetup-kde.desktop.in
	xgettext --from-code=utf-8 \
		-x po/EXCLUDE \
		-L Glade \
		-o po/gtkkeyboardsetup.pot \
		gtkkeyboardsetup.ui
	xgettext --from-code=utf-8 \
		-j \
		-L Python \
		-o po/gtkkeyboardsetup.pot \
		gtkkeyboardsetup
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkkeyboardsetup.pot gtkkeyboardsetup.desktop.in.h
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkkeyboardsetup.pot gtkkeyboardsetup-kde.desktop.in.h
	rm gtkkeyboardsetup.desktop.in.h gtkkeyboardsetup-kde.desktop.in.h

update-po:
	for i in `ls po/*.po`; do \
		msgmerge -U $$i po/gtkkeyboardsetup.pot ;\
	done
	rm -f po/*~

.PHONY: pot update-po
