DESTDIR ?= /

export DESTDIR

.PHONY: desktop
desktop: mo
	intltool-merge po/ -d -u gtkclocksetup.desktop.in gtkclocksetup.desktop
	intltool-merge po/ -d -u gtkclocksetup-kde.desktop.in gtkclocksetup-kde.desktop

.PHONY: mo
mo:
	$(MAKE) mo -C po

.PHONY: install
install:
	install -d -m 755 $(DESTDIR)/usr/sbin
	install -d -m 755 $(DESTDIR)/usr/share/applications
	install -d -m 755 $(DESTDIR)/usr/share/salixtools/gtkclocksetup
	install -m 755 gtkclocksetup $(DESTDIR)/usr/sbin/
	install -m 644 gtkclocksetup.desktop $(DESTDIR)/usr/share/applications
	install -m 644 gtkclocksetup-kde.desktop $(DESTDIR)/usr/share/applications/
	install -m 644 gtkclocksetup.ui $(DESTDIR)/usr/share/salixtools/gtkclocksetup/
	$(MAKE) install -C po
	$(MAKE) install -C icons

.PHONY: clean
clean:
	rm -f *.desktop
	$(MAKE) clean -C po

.PHONY: pot
pot:
	intltool-extract --type="gettext/ini" gtkclocksetup.desktop.in
	intltool-extract --type="gettext/ini" gtkclocksetup-kde.desktop.in
	xgettext --from-code=utf-8 \
		-x po/EXCLUDE \
		-L Glade \
		-o po/gtkclocksetup.pot \
		gtkclocksetup.ui
	xgettext --from-code=utf-8 \
		-j \
		-L Python \
		-o po/gtkclocksetup.pot \
		gtkclocksetup
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkclocksetup.pot gtkclocksetup.desktop.in.h
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkclocksetup.pot gtkclocksetup-kde.desktop.in.h
	rm gtkclocksetup.desktop.in.h gtkclocksetup-kde.desktop.in.h

.PHONY: update-po
update-po:
	for i in `ls po/*.po`; do \
		msgmerge -U $$i po/gtkclocksetup.pot ;\
	done
	rm -f po/*~

.PHONY: tx-pull
tx-pull:
	tx pull -a
	$(MAKE) remove-empty -C po

.PHONY: tx-pull-f
tx-pull:
	tx pull -a -f
	$(MAKE) remove-empty -C po

.PHONY: stat
stat:
	$(MAKE) stat -C po
