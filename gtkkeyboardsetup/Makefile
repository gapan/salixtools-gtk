DESTDIR ?= /

export DESTDIR

.PHONY: desktop
desktop: mo
	intltool-merge po/ -d -u gtkkeyboardsetup.desktop.in gtkkeyboardsetup.desktop
	intltool-merge po/ -d -u gtkkeyboardsetup-kde.desktop.in gtkkeyboardsetup-kde.desktop

.PHONY: mo
mo:
	$(MAKE) mo -C po

.PHONY: install
install:
	install -d -m 755 $(DESTDIR)/usr/sbin
	install -d -m 755 $(DESTDIR)/usr/share/applications
	install -d -m 755 $(DESTDIR)/usr/share/salixtools/gtkkeyboardsetup
	install -m 755 gtkkeyboardsetup $(DESTDIR)/usr/sbin/
	install -m 644 gtkkeyboardsetup.desktop $(DESTDIR)/usr/share/applications
	install -m 644 gtkkeyboardsetup-kde.desktop $(DESTDIR)/usr/share/applications/
	install -m 644 gtkkeyboardsetup.ui $(DESTDIR)/usr/share/salixtools/gtkkeyboardsetup/
	$(MAKE) install -C po
	$(MAKE) install -C icons

.PHONY: clean
clean:
	rm -f *.desktop
	$(MAKE) clean -C po

.PHONY: pot
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

.PHONY: update-po
update-po:
	for i in `ls po/*.po`; do \
		msgmerge -U $$i po/gtkkeyboardsetup.pot ;\
	done
	rm -f po/*~

.PHONY: tx-pull
tx-pull:
	tx pull -a
	$(MAKE) remove-empty -C po

.PHONY: stat
stat:
	$(MAKE) stat -C po
