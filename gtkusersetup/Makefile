DESTDIR ?= /

export DESTDIR

.PHONY: desktop
desktop: mo
	intltool-merge po/ -d -u gtkusersetup.desktop.in gtkusersetup.desktop
	intltool-merge po/ -d -u gtkusersetup-kde.desktop.in gtkusersetup-kde.desktop

.PHONY: mo
mo:
	$(MAKE) mo -C po

.PHONY: install
install:
	install -d -m 755 $(DESTDIR)/usr/sbin
	install -d -m 755 $(DESTDIR)/usr/share/applications
	install -d -m 755 $(DESTDIR)/usr/share/salixtools/gtkusersetup
	install -m 755 gtkusersetup.py $(DESTDIR)/usr/sbin/gtkusersetup
	install -m 644 gtkusersetup.desktop $(DESTDIR)/usr/share/applications
	install -m 644 gtkusersetup-kde.desktop $(DESTDIR)/usr/share/applications/
	install -m 644 gtkusersetup.ui $(DESTDIR)/usr/share/salixtools/gtkusersetup/
	$(MAKE) install -C po
	$(MAKE) install -C icons

.PHONY: clean
clean:
	rm -f *.desktop
	$(MAKE) clean -C po

.PHONY: pot
pot:
	intltool-extract --type="gettext/ini" gtkusersetup.desktop.in
	intltool-extract --type="gettext/ini" gtkusersetup-kde.desktop.in
	xgettext --from-code=utf-8 \
		-x po/EXCLUDE \
		-L Glade \
		-o po/gtkusersetup.pot \
		gtkusersetup.ui
	xgettext --from-code=utf-8 \
		-j \
		-L Python \
		-o po/gtkusersetup.pot \
		gtkusersetup
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkusersetup.pot gtkusersetup.desktop.in.h
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkusersetup.pot gtkusersetup-kde.desktop.in.h
	rm gtkusersetup.desktop.in.h gtkusersetup-kde.desktop.in.h

.PHONY: update-po
update-po:
	for i in `ls po/*.po`; do \
		msgmerge -U $$i po/gtkusersetup.pot ;\
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
