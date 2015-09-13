
pot:
	intltool-extract --type="gettext/ini" gtkiconrefresh.desktop.in
	xgettext --from-code=utf-8 \
		-x po/EXCLUDE \
		-L Glade \
		-o po/gtkiconrefresh.pot \
		gtkiconrefresh.glade
	xgettext --from-code=utf-8 \
		-j \
		-L Python \
		-o po/gtkiconrefresh.pot \
		gtkiconrefresh
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkiconrefresh.pot gtkiconrefresh.desktop.in.h
	rm gtkiconrefresh.desktop.in.h

update-po:
	for i in `ls po/*.po`; do \
		msgmerge -U $$i po/gtkiconrefresh.pot ;\
	done
	rm -f po/*~

.PHONY: pot update-po
