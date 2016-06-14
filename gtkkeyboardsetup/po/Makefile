DESTDIR ?= /

.PHONY: mo
mo:
	for j in `ls *.po`; do \
		msgfmt $$j -o `echo $$j | sed "s/\.po//"`.mo; \
	done

.PHONY: update-po
update-po:
	for i in *.po; do \
		msgmerge -U $$i gtkkeyboardsetup.pot ;\
	done
	rm -f *.po~

.PHONY: install
install:
	for j in `ls *.mo`; do \
		install -d -m 755 \
		$(DESTDIR)/usr/share/locale/`echo $$j|sed "s/.mo//"`/LC_MESSAGES; \
		install -m 644 $$j \
		$(DESTDIR)/usr/share/locale/`echo $$j|sed "s/.mo//"`/LC_MESSAGES/gtkkeyboardsetup.mo; \
	done

.PHONY: remove-empty
remove-empty:
	for j in `ls *.po`; do \
		msgfmt --statistics $$j 2>&1 | grep "^0 translated" > /dev/null \
			&& rm $$j || true; \
		rm -f messages.mo; \
	done

.PHONY: stat
stat:   
	@for j in `ls *.po`; do \
		echo -en "$$j:\n  "; \
			msgfmt --statistics $$j 2>&1; \
		rm -f messages.mo; \
	done

.PHONY: clean
clean:
	rm -f *.mo
	rm -f *.po~
