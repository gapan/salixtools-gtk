DESTDIR ?= /

export DESTDIR

.PHONY: desktop
desktop: mo
	intltool-merge po/ -d -u gtklocalesetup.desktop.in gtklocalesetup.desktop
	intltool-merge po/ -d -u gtklocalesetup-kde.desktop.in gtklocalesetup-kde.desktop

.PHONY: mo
mo:
	$(MAKE) mo -C po

.PHONY: install
install:
	install -d -m 755 $(DESTDIR)/usr/sbin
	install -d -m 755 $(DESTDIR)/usr/share/applications
	install -d -m 755 $(DESTDIR)/usr/share/salixtools/gtklocalesetup
	install -m 755 gtklocalesetup.py $(DESTDIR)/usr/sbin/gtklocalesetup
	install -m 644 gtklocalesetup.desktop $(DESTDIR)/usr/share/applications
	install -m 644 gtklocalesetup-kde.desktop $(DESTDIR)/usr/share/applications/
	install -m 644 gtklocalesetup.ui $(DESTDIR)/usr/share/salixtools/gtklocalesetup/
	$(MAKE) install -C po
	$(MAKE) install -C icons

.PHONY: clean
clean:
	rm -f *.desktop
	$(MAKE) clean -C po

.PHONY: pot
pot:
	intltool-extract --type="gettext/ini" gtklocalesetup.desktop.in
	intltool-extract --type="gettext/ini" gtklocalesetup-kde.desktop.in
	xgettext --from-code=utf-8 \
		-x po/EXCLUDE \
		-L Glade \
		-o po/gtklocalesetup.pot \
		gtklocalesetup.ui
	xgettext --from-code=utf-8 \
		-j \
		-L Python \
		-o po/gtklocalesetup.pot \
		gtklocalesetup
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtklocalesetup.pot gtklocalesetup.desktop.in.h
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtklocalesetup.pot gtklocalesetup-kde.desktop.in.h
	rm gtklocalesetup.desktop.in.h gtklocalesetup-kde.desktop.in.h

.PHONY: update-po
update-po:
	for i in `ls po/*.po`; do \
		msgmerge -U $$i po/gtklocalesetup.pot ;\
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
