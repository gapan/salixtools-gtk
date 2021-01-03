DESTDIR ?= /

export DESTDIR

.PHONY: desktop
desktop: mo
	intltool-merge po/ -d -u gtkhostsetup.desktop.in gtkhostsetup.desktop
	intltool-merge po/ -d -u gtkhostsetup-kde.desktop.in gtkhostsetup-kde.desktop

.PHONY: mo
mo:
	$(MAKE) mo -C po

.PHONY: install
install:
	install -d -m 755 $(DESTDIR)/usr/sbin
	install -d -m 755 $(DESTDIR)/usr/share/applications
	install -d -m 755 $(DESTDIR)/usr/share/salixtools/gtkhostsetup
	install -m 755 gtkhostsetup.py $(DESTDIR)/usr/sbin/gtkhostsetup
	install -m 644 gtkhostsetup.desktop $(DESTDIR)/usr/share/applications
	install -m 644 gtkhostsetup-kde.desktop $(DESTDIR)/usr/share/applications/
	install -m 644 gtkhostsetup.ui $(DESTDIR)/usr/share/salixtools/gtkhostsetup/
	$(MAKE) install -C po
	$(MAKE) install -C icons

.PHONY: clean
clean:
	rm -f *.desktop *.pyc
	rm -rf .cache __pycache__
	$(MAKE) clean -C po

.PHONY: pot
pot:
	intltool-extract --type="gettext/ini" gtkhostsetup.desktop.in
	intltool-extract --type="gettext/ini" gtkhostsetup-kde.desktop.in
	xgettext --from-code=utf-8 \
		-x po/EXCLUDE \
		-L Glade \
		-o po/gtkhostsetup.pot \
		gtkhostsetup.ui
	xgettext --from-code=utf-8 \
		-j \
		-L Python \
		-o po/gtkhostsetup.pot \
		gtkhostsetup
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkhostsetup.pot gtkhostsetup.desktop.in.h
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkhostsetup.pot gtkhostsetup-kde.desktop.in.h
	rm gtkhostsetup.desktop.in.h gtkhostsetup-kde.desktop.in.h

.PHONY: update-po
update-po:
	for i in `ls po/*.po`; do \
		msgmerge -U $$i po/gtkhostsetup.pot ;\
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
