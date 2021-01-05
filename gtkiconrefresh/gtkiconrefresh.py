#!/usr/bin/python3
# vim:et:sta:sts=4:sw=4:ts=8:tw=79:

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import os
import subprocess
import threading

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

    def rebuild_icon_cache(self):
        number_of_dirs = len(icon_dirs())
        step = 0.999 / number_of_dirs
        position = 0
        for i in icon_dirs():
            GLib.idle_add(self.update_progress, position)
            cmd = ['gtk-update-icon-cache', '-f', i]
            process = subprocess.Popen(cmd)
            process.wait()
            position = position + step
        self.progressbar.set_fraction(1)
        Gtk.main_quit()

    def update_progress(self, position):
        self.progressbar.set_fraction(position)
        return False

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

        thread = threading.Thread(target=self.rebuild_icon_cache)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    app = GTKIconRefresh()
    app.window.show()
    Gtk.main()
