#!/bin/sh
# install script for salixtools

cd $(dirname $0)

# Create base dirs
install -d -m 755 $DESTDIR/usr/sbin
install -d -m 755 $DESTDIR/usr/share/applications
install -d -m 755 $DESTDIR/usr/share/salixtools

# Install icons
for i in `ls icons/*.svg`; do
	install -d -m 755 $DESTDIR/usr/share/icons/hicolor/scalable/apps/
	install -m 644 $i $DESTDIR/usr/share/icons/hicolor/scalable/apps/
done

for i in 64 48 32 24 22 16; do
	for j in `ls icons/*-$i.png 2> /dev/null`; do
		install -d -m 755 \
		$DESTDIR/usr/share/icons/hicolor/${i}x${i}/apps/ \
		2> /dev/null
		install -m 644 $j \
		$DESTDIR/usr/share/icons/hicolor/${i}x${i}/apps/`basename $j|sed "s/-$i//"`
	done
done

# Install tools + lang files
for i in gtkalsasetup gtkclocksetup gtkkeyboardsetup gtklocalesetup gtkusersetup gtkservicesetup; do
	install -m 755 $i/$i $DESTDIR/usr/sbin/
	install -m 644 $i/$i.desktop $DESTDIR/usr/share/applications/
	install -m 644 $i/$i-kde.desktop $DESTDIR/usr/share/applications/
	install -d -m 755 $DESTDIR/usr/share/salixtools/$i
	install -m 644 $i/$i.glade $DESTDIR/usr/share/salixtools/$i/
	for j in `ls $i/po/*.mo`; do
		install -d -m 755 \
		$DESTDIR/usr/share/locale/`basename $j|sed "s/.mo//"`/LC_MESSAGES \
		2> /dev/null
		install -m 644 $j \
		$DESTDIR/usr/share/locale/`basename $j|sed "s/.mo//"`/LC_MESSAGES/$i.mo
	done
done

# Install man pages
#install -d -m 755 $DESTDIR/usr/man/man8
#for i in clocksetup keyboardsetup localesetup usersetup servicesetup; do
#	(
#	cd $i/man
#	for j in `ls *.8`; do
#		install -m644 $j $DESTDIR/usr/man/man8/
#	done
#	)
#done

