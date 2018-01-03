DESTDIR ?= /

export DESTDIR

.PHONY: desktop
desktop: mo
	intltool-merge po/ -d -u gtkreposetup.desktop.in gtkreposetup.desktop
	intltool-merge po/ -d -u gtkreposetup-kde.desktop.in gtkreposetup-kde.desktop

.PHONY: mo
mo:
	$(MAKE) mo -C po

.PHONY: install
install:
	install -d -m 755 $(DESTDIR)/usr/sbin
	install -d -m 755 $(DESTDIR)/usr/share/applications
	install -d -m 755 $(DESTDIR)/usr/share/salixtools/gtkreposetup
	install -m 755 gtkreposetup.py $(DESTDIR)/usr/sbin/gtkreposetup
	install -m 644 gtkreposetup.desktop $(DESTDIR)/usr/share/applications
	install -m 644 gtkreposetup-kde.desktop $(DESTDIR)/usr/share/applications/
	install -m 644 gtkreposetup.ui $(DESTDIR)/usr/share/salixtools/gtkreposetup/
	$(MAKE) install -C po
	$(MAKE) install -C icons

.PHONY: clean
clean:
	rm -f *.desktop
	$(MAKE) clean -C po

.PHONY: pot
pot:
	intltool-extract --type="gettext/ini" gtkreposetup.desktop.in
	intltool-extract --type="gettext/ini" gtkreposetup-kde.desktop.in
	xgettext --from-code=utf-8 \
		-x po/EXCLUDE \
		-L Glade \
		-o po/gtkreposetup.pot \
		gtkreposetup.ui
	xgettext --from-code=utf-8 \
		-j \
		-L Python \
		-o po/gtkreposetup.pot \
		gtkreposetup
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkreposetup.pot gtkreposetup.desktop.in.h
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkreposetup.pot gtkreposetup-kde.desktop.in.h
	rm gtkreposetup.desktop.in.h gtkreposetup-kde.desktop.in.h

.PHONY: update-po
update-po:
	for i in `ls po/*.po`; do \
		msgmerge -U $$i po/gtkreposetup.pot ;\
	done
	rm -f po/*~

.PHONY: tx-pull
tx-pull:
	tx pull -a
	$(MAKE) fix-charset -C po
	$(MAKE) remove-empty -C po

.PHONY: tx-pull-f
tx-pull-f:
	tx pull -a -f
	$(MAKE) fix-charset -C po
	$(MAKE) remove-empty -C po

.PHONY: stat
stat:
	$(MAKE) stat -C po
