#!/usr/bin/python3
# vim:et:sta:sts=4:sw=4:ts=8:tw=79:

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import sys
import subprocess

# Internationalization
import locale
import gettext
locale.setlocale(locale.LC_ALL, '')
locale.bindtextdomain("gtklocalesetup", "/usr/share/locale")
_ = gettext.gettext

def availablelocales():
    locales = []
    cmd = 'LANG=C locale -cva | grep "^locale\|title |"'
    localeoutput = subprocess.getoutput(cmd).splitlines()
    for i in localeoutput:
        newlocale = False
        if i.startswith('locale:'):
            if 'utf8' in i or 'UTF-8' in i:
                localecode = i.replace('locale:', '').lstrip(
                ).partition('directory:')[0].rstrip().replace('UTF-8', 'utf8')
                utf8locale = True
            else:
                utf8locale = False
        elif 'title |' in i:
            if utf8locale == True:
                localedesc = i.lstrip().replace('title | ', '')
                newlocale = True
        if newlocale == True:
            locales.append([localedesc, localecode])
        locales.sort()
    return locales


def currentlocale():
    localeoutput = subprocess.getoutput("locale").splitlines()
    for i in localeoutput:
        if i.startswith('LANG='):
            locale = i.replace('LANG=', '').replace('UTF-8', 'utf8')
    if 'utf8' not in locale:
        if locale == 'C':
            locale = 'en_US'
        locale = locale + '.utf8'
    return locale


def setlocale(locale):
    cmd = ['localesetup', locale]
    process = subprocess.Popen(cmd)
    process.wait()


class GTKLocaleSetup:

    def on_button_about_clicked(self, widget, data=None):
        self.aboutdialog.show()

    def on_aboutdialog_response(self, widget, data=None):
        self.aboutdialog.hide()

    def on_aboutdialog_delete_event(self, widget, event):
        self.aboutdialog.hide()
        return True

    def on_button_ok_clicked(self, widget, data=None):
        self.window.hide()
        while Gtk.events_pending():
            Gtk.main_iteration()
        selectedlocale = self.localelist.get_selection()
        self.localeliststore, iter = selectedlocale.get_selected()
        setlocale(self.localeliststore.get_value(iter, 1))
        Gtk.main_quit()

    def on_button_cancel_clicked(self, widget, data=None):
        Gtk.main_quit()

    def gtk_main_quit(self, widget, data=None):
        Gtk.main_quit()

    def __init__(self):
        builder = Gtk.Builder()
        builder.set_translation_domain("gtklocalesetup")
        if os.path.exists('gtklocalesetup.ui'):
            builder.add_from_file('gtklocalesetup.ui')
        elif os.path.exists('/usr/share/salixtools/gtklocalesetup/gtklocalesetup.ui'):
            builder.add_from_file(
                '/usr/share/salixtools/gtklocalesetup/gtklocalesetup.ui')
        self.window = builder.get_object('gtklocalesetup')
        self.aboutdialog = builder.get_object('aboutdialog')

        builder.connect_signals(self)
        self.localelist = builder.get_object('localelist')
        self.localeliststore = builder.get_object('localeliststore')
        self.localeliststore.clear()

        cursorpos = 0
        locale = currentlocale()
        for i in availablelocales():
            self.localeliststore.append(i)
            if i[1] == locale:
                self.localelist.set_cursor(cursorpos)
                if cursorpos > 5:
                    self.localelist.scroll_to_cell(cursorpos - 4)
            cursorpos += 1

if __name__ == "__main__":
    app = GTKLocaleSetup()
    app.window.show()
    Gtk.main()
