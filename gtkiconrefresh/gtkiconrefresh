#!/usr/bin/env python
# vim:et:sta:sts=4:sw=4:ts=8:tw=79:

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject
import os
import subprocess

# Internationalization
import locale
import gettext
locale.setlocale(locale.LC_ALL, '')
locale.bindtextdomain("gtkiconrefresh", "/usr/share/locale")
gettext.bindtextdomain("gtkiconrefresh", "/usr/share/locale")
gettext.textdomain("gtkiconrefresh")
_ = gettext.gettext


def icon_dirs():
    icondir = '/usr/share/icons/'
    dirs = []
    for i in os.listdir(icondir):
        if os.path.isdir(icondir + i):
            dirs.append(icondir + i)
    return dirs


class GTKIconRefresh:

    def do_rebuild(self):
        number_of_dirs = len(icon_dirs())
        step = 0.999 / number_of_dirs
        position = 0
        for i in icon_dirs():
            self.progressbar.set_fraction(position)
            while Gtk.events_pending():
                Gtk.main_iteration()
            cmd = ['gtk-update-icon-cache', '-f', i]
            process = subprocess.Popen(cmd)
            process.wait()
            position = position + step
            yield True
        self.progressbar.set_fraction(1)
        Gtk.main_quit()
        while Gtk.events_pending():
            Gtk.main_iteration()
        yield False

    def rebuild_icon_cache(self):
        task = self.do_rebuild()
        GObject.idle_add(task.next)

    def gtk_main_quit(self, widget, data=None):
        Gtk.main_quit()

    def on_gtkiconrefresh_delete_event(self, widget, data=None):
        Gtk.main_quit()

    def __init__(self):
        builder = Gtk.Builder()
        builder.set_translation_domain("gtkiconrefresh")
        if os.path.exists('gtkiconrefresh.ui'):
            builder.add_from_file('gtkiconrefresh.ui')
        elif os.path.exists('/usr/share/salixtools/gtkiconrefresh/gtkiconrefresh.ui'):
            builder.add_from_file(
                '/usr/share/salixtools/gtkiconrefresh/gtkiconrefresh.ui')
        self.window = builder.get_object('gtkiconrefresh')
        self.progressbar = builder.get_object('progressbar')

        builder.connect_signals(self)

        self.rebuild_icon_cache()

if __name__ == "__main__":
    app = GTKIconRefresh()
    app.window.show()
    Gtk.main()
