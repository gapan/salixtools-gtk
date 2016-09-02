DESTDIR ?= /

export DESTDIR

.PHONY: desktop
desktop: mo
	intltool-merge po/ -d -u gtkiconrefresh.desktop.in gtkiconrefresh.desktop

.PHONY: mo
mo:
	$(MAKE) mo -C po

.PHONY: install
install:
	install -d -m 755 $(DESTDIR)/usr/sbin
	install -d -m 755 $(DESTDIR)/usr/share/applications
	install -d -m 755 $(DESTDIR)/usr/share/salixtools/gtkiconrefresh
	install -m 755 gtkiconrefresh $(DESTDIR)/usr/sbin/
	install -m 644 gtkiconrefresh.desktop $(DESTDIR)/usr/share/applications
	install -m 644 gtkiconrefresh.ui $(DESTDIR)/usr/share/salixtools/gtkiconrefresh/
	$(MAKE) install -C po
	$(MAKE) install -C icons

.PHONY: clean
clean:
	rm -f *.desktop
	$(MAKE) clean -C po

.PHONY: pot
pot:
	intltool-extract --type="gettext/ini" gtkiconrefresh.desktop.in
	xgettext --from-code=utf-8 \
		-x po/EXCLUDE \
		-L Glade \
		-o po/gtkiconrefresh.pot \
		gtkiconrefresh.ui
	xgettext --from-code=utf-8 \
		-j \
		-L Python \
		-o po/gtkiconrefresh.pot \
		gtkiconrefresh
	xgettext --from-code=utf-8 -j -L C -kN_ -o po/gtkiconrefresh.pot gtkiconrefresh.desktop.in.h
	rm gtkiconrefresh.desktop.in.h

.PHONY: update-po
update-po:
	for i in `ls po/*.po`; do \
		msgmerge -U $$i po/gtkiconrefresh.pot ;\
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
