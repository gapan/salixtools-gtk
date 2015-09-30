DESTDIR ?= /

ALL_PROJECTS = gtkalsasetup gtkclocksetup gtkhostsetup gtkiconrefresh \
			gtkkeyboardsetup gtklocalesetup gtkusersetup gtkservicesetup
PROJECTS_NO_ICONREFRESH = gtkalsasetup gtkclocksetup gtkhostsetup \
			gtkkeyboardsetup gtklocalesetup gtkusersetup gtkservicesetup

all:
	for i in $(PROJECTS_NO_ICONREFRESH); do \
		for j in `ls $$i/po/*.po`; do \
			echo "Compiling `echo $$j|sed "s|/po||"`"; \
			msgfmt $$j -o `echo $$j | sed "s/\.po//"`.mo; \
		done; \
		intltool-merge $$i/po/ -d -u $$i/$$i.desktop.in $$i/$$i.desktop; \
		intltool-merge $$i/po/ -d -u $$i/$$i-kde.desktop.in $$i/$$i-kde.desktop; \
	done

transifex:
	for i in $(ALL_PROJECTS); do \
		cd $$i; \
		tx pull -a; \
		cd ..; \
	done

clean:
	rm -f */po/*.mo
	rm -f */po/*.po~
	rm -f */*.desktop

install:
	install -d -m 755 $(DESTDIR)/usr/sbin
	install -d -m 755 $(DESTDIR)/usr/share/applications
	install -d -m 755 $(DESTDIR)/usr/share/salixtools
	for i in `ls icons/*.svg`; do \
		install -d -m 755 $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/; \
		install -m 644 $$i $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/; \
	done; \
	for i in 64 48 32 24 22 16; do \
		for j in `ls icons/*-$$i.png 2> /dev/null`; do \
			install -d -m 755 \
			$(DESTDIR)/usr/share/icons/hicolor/$${i}x$${i}/apps/ \
			2> /dev/null; \
			install -m 644 $$j \
			$(DESTDIR)/usr/share/icons/hicolor/$${i}x$${i}/apps/`basename $$j|sed "s/-$$i//"`; \
		done; \
	done
	for i in gtkalsasetup gtkclocksetup gtkhostsetup gtkkeyboardsetup gtklocalesetup gtkusersetup gtkservicesetup; do \
		install -m 755 $$i/$$i $(DESTDIR)/usr/sbin/; \
		install -m 644 $$i/$$i.desktop $(DESTDIR)/usr/share/applications/; \
		install -m 644 $$i/$$i-kde.desktop $(DESTDIR)/usr/share/applications/; \
		install -d -m 755 $(DESTDIR)/usr/share/salixtools/$$i; \
		install -m 644 $$i/$$i.glade $(DESTDIR)/usr/share/salixtools/$$i/; \
		for j in `ls $$i/po/*.mo`; do \
			install -d -m 755 \
			$(DESTDIR)/usr/share/locale/`basename $$j|sed "s/.mo//"`/LC_MESSAGES \
			2> /dev/null; \
			install -m 644 $$j \
			$(DESTDIR)/usr/share/locale/`basename $$j|sed "s/.mo//"`/LC_MESSAGES/$$i.mo; \
		done; \
	done

pot:
	for i in $(ALL_PROJECTS); do \
		$(MAKE) pot -C $$i;\
	done

update-po:
	for i in $(ALL_PROJECTS); do \
		$(MAKE) update-po -C $$i;\
	done
	
.PHONY: all clean install transifex pot update-po
