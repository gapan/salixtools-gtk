DESTDIR ?= /

TOOLS = gtkclocksetup \
		gtkhostsetup \
		gtkiconrefresh \
		gtkkeyboardsetup \
		gtklocalesetup \
		gtkservicesetup \
		gtkusersetup

export DESTDIR

.PHONY: all
all:
	for i in $(TOOLS); do \
		$(MAKE) -C $$i;\
	done

.PHONY: install
install:
	for i in $(TOOLS); do \
		$(MAKE) install -C $$i; \
	done

.PHONY: clean
clean:
	for i in $(TOOLS); do \
		$(MAKE) clean -C $$i;\
	done

.PHONY: pot
pot:
	for i in $(TOOLS); do \
		$(MAKE) pot -C $$i;\
	done

.PHONY: update-po
update-po:
	for i in $(TOOLS); do \
		$(MAKE) update-po -C $$i;\
	done

.PHONY: tx-pull
tx-pull:
	for i in $(TOOLS); do \
		$(MAKE) tx-pull -C $$i;\
	done

.PHONY: stat
stat:
	for i in $(TOOLS); do \
		$(MAKE) stat -C $$i;\
	done
