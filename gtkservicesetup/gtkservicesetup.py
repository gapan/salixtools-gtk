#!/usr/bin/python3
# vim:et:sta:sts=4:sw=4:ts=8:tw=79:

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import subprocess
import os
import sys

# Internationalization
import locale
import gettext
locale.setlocale(locale.LC_ALL, '')
locale.bindtextdomain("gtkservicesetup", "/usr/share/locale")
gettext.bindtextdomain("gtkservicesetup", "/usr/share/locale")
gettext.textdomain("gtkservicesetup")
_ = gettext.gettext

def blacklisted():
    fname = '/usr/share/salixtools/servicesetup/service-blacklist'
    with open(fname, 'r') as f:
        servicestrings = []
        while True:
            line = f.readline().replace('\n', '')
            if len(line) == 0:
                break
            servicestrings.append(line)
    return servicestrings


def isblacklisted(service):
    val = False
    for i in blacklisted():
        if i in service:
            val = True
    return val


def isenabled(service):
    if os.access('/etc/rc.d/' + service, os.X_OK):
        enabled = True
    else:
        enabled = False
    return enabled


def servicedesc(service):
    description = _('The {0} service').format(service[3:])
    filelist = os.listdir('/etc/rc.d/desc.d')
    for i in filelist:
        with open('/etc/rc.d/desc.d/' + i, 'r') as f:
            while True:
                line = f.readline()
                if len(line) == 0:
                    break
                elif 'rc.' + line.partition(':')[0] == service:
                    description = line.partition(':')[2].partition(':')[0]
                    break
    return description


def availableservices():
    filelist = os.listdir('/etc/rc.d')
    services = []
    for i in filelist:
        if os.path.isfile('/etc/rc.d/' + i):
            if not isblacklisted(i):
                services.append(i)
    services.sort()
    return services


def serviceslist():
    list = []
    for i in availableservices():
        list.append([isenabled(i), i.replace(
            'rc.', ''), servicedesc(i), False])
    return list


def enableservice(service):
    cmd = ['/usr/sbin/service', 'start', service]
    process = subprocess.Popen(cmd)
    process.wait()


def disableservice(service):
    cmd = ['/usr/sbin/service', 'stop', service]
    process = subprocess.Popen(cmd)
    process.wait()


class GTKServiceSetup:

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
        for i in self.servicesliststore:
            if i[3] == True:
                if i[0] == True:
                    enableservice(i[1])
                else:
                    disableservice(i[1])
        Gtk.main_quit()

    def on_button_cancel_clicked(self, widget, data=None):
        Gtk.main_quit()

    def on_checkbox_toggled(self, widget, data=None):
        selectedservice = self.serviceslist.get_selection()
        self.servicesliststore, iter = selectedservice.get_selected()
        selectedservicename = self.servicesliststore.get_value(iter, 1)
        for i in self.servicesliststore:
            if i[1] == selectedservicename:
                i[3] = True
                if i[0] == 0:
                    i[0] = 1
                else:
                    i[0] = 0

    def gtk_main_quit(self, widget, data=None):
        Gtk.main_quit()

    def __init__(self):
        builder = Gtk.Builder()
        builder.set_translation_domain("gtkservicesetup")
        if os.path.exists('gtkservicesetup.ui'):
            builder.add_from_file('gtkservicesetup.ui')
        elif os.path.exists('/usr/share/salixtools/gtkservicesetup/gtkservicesetup.ui'):
            builder.add_from_file(
                '/usr/share/salixtools/gtkservicesetup/gtkservicesetup.ui')
        self.window = builder.get_object('gtkservicesetup')
        self.aboutdialog = builder.get_object('aboutdialog')

        builder.connect_signals(self)
        self.serviceslist = builder.get_object('serviceslist')
        self.servicesliststore = builder.get_object('servicesliststore')
        self.columnenabled = builder.get_object('columnEnabled')
        self.columnenabled.set_title(_('Enabled'))
        self.columnservicename = builder.get_object('columnServiceName')
        self.columnservicename.set_title(_('Service name'))
        self.columnservicedesc = builder.get_object('columnServiceDesc')
        self.columnservicedesc.set_title(_('Service description'))
        self.servicesliststore.clear()
        for i in serviceslist():
            self.servicesliststore.append(i)

if __name__ == "__main__":
    app = GTKServiceSetup()
    app.window.show()
    Gtk.main()
