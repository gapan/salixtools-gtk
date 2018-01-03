DESTDIR ?= /

export DESTDIR

.PHONY: desktop
desktop: mo
	intltool-merge po/ -d -u gtkservicesetup.desktop.in gtkservicesetup.desktop
	intltool-merge po/ -d -u gtkservicesetup-kde.desktop.in gtkservicesetup-kde.desktop

.PHONY: mo
mo:
	$(MAKE) mo -C po

.PHONY: install
install:
	install -d -m 755 $(DESTDIR)/usr/sbin
	install -d -m 755 $(DESTDIR)/usr/share/applications
	install -d -m 755 $(DESTDIR)/usr/share/salixtools/gtkservicesetup
	install -m 755 gtkservicesetup.py $(DESTDIR)/usr/sbin/gtkservicesetup
	install -m 644 gtkservicesetup.desktop $(DESTDIR)/usr/share/applications
	install -m 644 gtkservicesetup-kde.desktop $(DESTDIR)/usr/share/applications/
	install -m 644 gtkservicesetup.ui $(DESTDIR)/usr/share/salixtools/gtkservicesetup/
	$(MAKE) install -C po
	$(MAKE) install -C icons

.PHONY: clean
clean:
	rm -f *.desktop
	$(MAKE) clean -C po

.PHONY: pot
pot:
	intltool-extract --type="gettext/ini" gtkservicesetup.desktop.in
	intltool-extract --type="gettext/ini" gtkservicesetup-kde.desktop.in
	xgettext --from-code=utf-8 \
		-x po/EXCLUDE \
		-L Glade \
		-o po/gtkservicesetup.pot \
		gtkservicesetup.ui
	xgettext --from-code=utf-8 \
		-j \
		-L Python \
		-o po/gtkservicesetup.pot \
		gtkservicesetup
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkservicesetup.pot gtkservicesetup.desktop.in.h
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkservicesetup.pot gtkservicesetup-kde.desktop.in.h
	rm gtkservicesetup.desktop.in.h gtkservicesetup-kde.desktop.in.h

.PHONY: update-po
update-po:
	for i in `ls po/*.po`; do \
		msgmerge -U $$i po/gtkservicesetup.pot ;\
	done
	rm -f po/*~

.PHONY: tx-pull
tx-pull:
	tx pull -a
	$(MAKE) remove-empty -C po

.PHONY: tx-pull-f
tx-pull-f:
	tx pull -a -f
	$(MAKE) remove-empty -C po

.PHONY: stat
stat:
	$(MAKE) stat -C po
