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
locale.bindtextdomain("gtkkeyboardsetup", "/usr/share/locale")
gettext.bindtextdomain("gtkkeyboardsetup", "/usr/share/locale")
gettext.textdomain("gtkkeyboardsetup")
_ = gettext.gettext


keymapdir = '/usr/share/kbd/keymaps/i386/'


def getkeymap():
    keymap = 'us'
    try:
        with open('/etc/rc.d/rc.keymap', 'r') as f:
            while True:
                line = f.readline().lstrip(' ')
                if len(line) == 0:
                    break
                if line.startswith('/usr/bin/loadkeys'):
                    keymap = line.replace('\n', '').partition(
                        '/usr/bin/loadkeys ')[2].partition('.map')[0].replace('-u ', '')
    except FileNotFoundError:
        # default to 'us' keymap if it's not already set
        keymap = 'us'
    return keymap


def getkeybtype(keymap):
    keybtype = 'qwerty'
    currentkeymap = getkeymap()
    for i in availablekeymaps():
        if i[1] == currentkeymap:
            keybtype = i[0]
            break
    return keybtype


def getnumlock():
    numlock = False
    if os.access('/etc/rc.d/rc.numlock', os.X_OK):
        numlock = True
    return numlock


def ibusavailable():
    ibus = False
    if os.access('/usr/bin/ibus-daemon', os.X_OK):
        if os.path.exists('/etc/profile.d/ibus.sh'):
            ibus = True
    return ibus


def getibus():
    ibus = False
    if ibusavailable() == True:
        if os.access('/etc/profile.d/ibus.sh', os.X_OK):
            ibus = True
    return ibus


def scimavailable():
    scim = False
    if os.access('/usr/bin/scim', os.X_OK):
        if os.path.exists('/etc/profile.d/scim.sh'):
            scim = True
    return scim


def getscim():
    scim = False
    if scimavailable() == True:
        if os.access('/etc/profile.d/scim.sh', os.X_OK):
            scim = True
    return scim


def setkeymap(keymap):
    cmd = ['/usr/sbin/keyboardsetup', '-k', keymap]
    process = subprocess.Popen(cmd)
    process.wait()


def setnumlock(numlock):
    if numlock == True:
        state = 'on'
    else:
        state = 'off'
    cmd = ['/usr/sbin/keyboardsetup', '-n', state]
    process = subprocess.Popen(cmd)
    process.wait()


def setibus(ibus):
    if ibus == True:
        state = 'on'
    else:
        state = 'off'
    cmd = ['keyboardsetup', '-i', state]
    process = subprocess.Popen(cmd)
    process.wait()


def setscim(scim):
    if scim == True:
        state = 'on'
    else:
        state = 'off'
    cmd = ['keyboardsetup', '-s ', state]
    process = subprocess.Popen(cmd)
    process.wait()


def availablekeybtypes():
    searchlist = ['azerty', 'dvorak', 'olpc', 'qwerty', 'qwertz']
    keybtypes = []
    for i in searchlist:
        if os.path.isdir(keymapdir + i):
            keybtypes.append(i)
    return keybtypes


def availablekeymaps():
    registered = []
    keymaps = []
    with open('/usr/share/salixtools/keymaps', 'r') as keymapfile:
        while True:
            line = keymapfile.readline()
            if len(line) == 0:
                break
            if not line.startswith('#'):
                registered.append(line.partition('|')[0])
    for keyboard_type in availablekeybtypes():
        for filename in os.listdir(keymapdir + keyboard_type):
            if filename.endswith('.map.gz'):
                key_map = filename.replace('.map.gz', '')
                if key_map in registered:
                    keymaps.append([keyboard_type, key_map])
    keymaps.sort()
    return keymaps


def updatedkeymaplist(keybtype):
    keymaplist = []
    for i in availablekeymaps():
        if i[0] == keybtype:
            keymaplist.append([i[1]])
    return keymaplist


class GTKKeyboardSetup:

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
        selectedkeymap = self.keymaplist.get_selection()
        self.keymapliststore, iter = selectedkeymap.get_selected()
        keymap = self.keymapliststore.get_value(iter, 0)
        if not keymap == getkeymap():
            setkeymap(keymap)
        if not self.numlock.get_active() == getnumlock():
            setnumlock(self.numlock.get_active())
        if not self.ibus.get_active() == getibus():
            setibus(self.ibus.get_active())
        if not self.scim.get_active() == getscim():
            setscim(self.scim.get_active())
        Gtk.main_quit()

    def on_button_cancel_clicked(self, widget, data=None):
        Gtk.main_quit()

    def on_keybtypelist_cursor_changed(self, widget, data=None):
        pos = self.keybtypelist.get_cursor()[0][0]
        selectedkeybtype = availablekeybtypes()[pos]
        currentkeymap = getkeymap()
        count = 0
        set = False
        self.keymapliststore.clear()
        for i in updatedkeymaplist(selectedkeybtype):
            self.keymapliststore.append(i)
            if i[0] == currentkeymap:
                set = True
                self.keymaplist.set_cursor(count)
                self.keymaplist.scroll_to_cell(count)
            count += 1
        if set == False:
            self.keymaplist.set_cursor(0)

    def gtk_main_quit(self, widget, data=None):
        Gtk.main_quit()

    def __init__(self):
        builder = Gtk.Builder()
        builder.set_translation_domain("gtkkeyboardsetup")
        if os.path.exists('gtkkeyboardsetup.ui'):
            builder.add_from_file('gtkkeyboardsetup.ui')
        elif os.path.exists('/usr/share/salixtools/gtkkeyboardsetup/gtkkeyboardsetup.ui'):
            builder.add_from_file(
                '/usr/share/salixtools/gtkkeyboardsetup/gtkkeyboardsetup.ui')
        self.window = builder.get_object('gtkkeyboardsetup')

        builder.connect_signals(self)
        self.keybtypelist = builder.get_object('keybtypelist')
        self.keybtypecolumn = builder.get_object('keybtypecolumn')
        self.keybtypecolumn.set_title(_('Keyboard type'))
        self.keybtypeliststore = builder.get_object('keybtypeliststore')
        self.keymaplist = builder.get_object('keymaplist')
        self.keymapcolumn = builder.get_object('keymapcolumn')
        self.keymapcolumn.set_title(_('Keyboard map'))
        self.keymapliststore = builder.get_object('keymapliststore')
        self.numlock = builder.get_object('numlockcheckbutton')
        self.ibus = builder.get_object('ibuscheckbutton')
        self.scim = builder.get_object('scimcheckbutton')
        self.aboutdialog = builder.get_object('aboutdialog')

        currentkeymap = getkeymap()
        currentkeybtype = getkeybtype(currentkeymap)
        count = 0
        self.keybtypeliststore.clear()
        for i in availablekeybtypes():
            self.keybtypeliststore.append([i])
            if i == currentkeybtype:
                self.keybtypelist.set_cursor(count)
            count += 1

        if ibusavailable() == True:
            self.ibus.set_active(getibus())
        else:
            self.ibus.set_sensitive(False)
            self.ibus.set_active(False)

        if scimavailable() == True:
            self.scim.set_active(getscim())
        else:
            self.scim.set_sensitive(False)
            self.scim.set_active(False)

        self.numlock.set_active(getnumlock())

if __name__ == "__main__":
    app = GTKKeyboardSetup()
    app.window.show()
    Gtk.main()
