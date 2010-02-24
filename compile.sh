#!/bin/sh

cd $(dirname $0)
for i in gtkclocksetup gtkkeyboardsetup gtklocalesetup gtkusersetup gtkservicesetup;do
	for j in `ls $i/locale/$i-*.po`;do
		echo "Compiling `echo $j|sed "s|/locale||"`"
		msgfmt $j -o `echo $j | sed "s/.po//"`.mo
	done
done
#for i in gtkclocksetup gtkkeyboardsetup gtklocalesetup gtkusersetup gtkservicesetup;do
#	(
#	cd $i/man
#	echo "Compiling $i manpage"
#	txt2tags *.t2t || exit 1
#	#txt2tags apparently doesn't have an option to change the man
#	#page number
#	for j in `ls *.man`;do
#		sed -i "1s/ 1 / 8 /" $j
#		mv $j `echo $j | sed "s/\.man//"`.8
#	done
#	)
#done

