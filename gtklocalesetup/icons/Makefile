DESTDIR ?= /

.PHONY: all
all:
	@echo "Nothing to make."

.PHONY: install
install:
	install -d -m 755 $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/; \
	install -m 644 gtklocalesetup.svg $(DESTDIR)/usr/share/icons/hicolor/scalable/apps/; \
	for i in 32 24 22 16; do \
		install -d -m 755 \
			$(DESTDIR)/usr/share/icons/hicolor/$${i}x$${i}/apps; \
		install -m 644 gtklocalesetup-$${i}.png \
			$(DESTDIR)/usr/share/icons/hicolor/$${i}x$${i}/apps/gtklocalesetup.png; \
	done

