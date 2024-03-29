#!/usr/bin/python3
# vim:et:sta:sts=4:sw=4:ts=8:tw=79:

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import sys
import datetime
import subprocess

# Internationalization
import locale
import gettext
locale.setlocale(locale.LC_ALL, '')
locale.bindtextdomain("gtkclocksetup", "/usr/share/locale")
gettext.bindtextdomain("gtkclocksetup", "/usr/share/locale")
gettext.textdomain("gtkclocksetup")
_ = gettext.gettext


def continents():
    continents = ['Africa', 'America', 'Antarctica', 'Asia',
                  'Atlantic', 'Australia', 'Europe', 'Indian',
                  'Pacific', 'US', 'Mexico', 'Chile', 'Mideast',
                  'Canada', 'Brazil', 'Arctic', 'Etc']
    continents.sort()
    return continents


def alltimezones():
    zoneinfo = '/usr/share/zoneinfo/'
    availablecontinents = []
    timezones = []
    for i in continents():
        if os.path.isdir(zoneinfo + i):
            availablecontinents.append(i)
    availablecontinents.sort()

    for i in availablecontinents:
        for file in os.listdir(zoneinfo + i):
            if os.path.isdir(zoneinfo + i + '/' + file):
                for file2 in os.listdir(zoneinfo + i + '/' + file):
                    timezones.append([i, file + '/' + file2])
            else:
                timezones.append([i, file])

    return timezones


def cities(continent):
    cities = []
    for i in alltimezones():
        if i[0] == continent:
            cities.append(i[1])
    cities.sort()
    return cities


def currenttimezone():
    try:
        tz = os.readlink(
            '/etc/localtime').replace('/usr/share/zoneinfo/', '')
    except OSError:
        tz = 'Etc/GMT'
    continent = tz.partition('/')[0]
    location = tz.partition('/')[2]
    return continent, location


def settimezone(continent, location):
    current_continent, current_location= currenttimezone()
    if continent != current_continent or location != current_location:
        cmd = ['rm', '-f', '/etc/localtime']
        process = subprocess.Popen(cmd)
        process.wait()
        cmd = ['ln', '-sf', '/usr/share/zoneinfo/' + continent +
               '/' + location, '/etc/localtime']
        process = subprocess.Popen(cmd)
        process.wait()


def ntpstate():
    if os.access('/etc/rc.d/rc.ntpd', os.X_OK):
        state = True
    else:
        state = False
    return state


def ntppresent():
    if os.path.isfile('/etc/rc.d/rc.ntpd'):
        state = True
    else:
        state = False
    return state


def utcstate():
    utc = False
    try:
        with open('/etc/hardwareclock', 'r') as f:
            while True:
                line = f.readline()
                if len(line) == 0:
                    break
                elif line.rstrip("\n") == 'localtime':
                    utc = False
                    break
                elif line.rstrip("\n") == 'UTC':
                    utc = True
                    break
    except (IOError, FileNotFoundError):
        setutc(False)
    return utc


def setutc(state):
    with open('/etc/hardwareclock', 'w') as f:
        if state == True:
            time = 'UTC'
        else:
            time = 'localtime'
        f.write('# /etc/hardwareclock\n')
        f.write('#\n')
        f.write('# Tells how the hardware clock time is stored.\n')
        f.write('# You should run (gtk)clocksetup or timeconfig to edit this file.\n\n')
        f.write(time + '\n')

def ntp_sync_now():
    cmd = ['/usr/sbin/ntpd', '-gq']
    process = subprocess.Popen(cmd)
    process.wait()
    cmd = ['/sbin/hwclock', '-w']
    process = subprocess.Popen(cmd)
    process.wait()


def setntp(state):
    if state == True:
        cmd = ['/usr/sbin/service', 'start', 'ntpd']
        process = subprocess.Popen(cmd)
        process.wait()
    else:
        cmd = ['/usr/sbin/service', 'stop', 'ntpd']
        process = subprocess.Popen(cmd)
        process.wait()


class GTKClockSetup:

    def on_button_ok_clicked(self, widget, data=None):
        self.window.hide()
        while Gtk.events_pending():
            Gtk.main_iteration()
        if not self.switch_sync.get_active == ntpstate():
            setntp(self.switch_sync.get_active())
            if self.switch_sync.get_active() == False:
                year = "%04d" % (self.calendar.get_date()[0])
                month = "%02d" % (self.calendar.get_date()[1] + 1)
                day = "%02d" % (self.calendar.get_date()[2])
                hour = "%02d" % self.spinbutton_hrs.get_value()
                min = "%02d" % self.spinbutton_min.get_value()
                sec = "%02d" % self.spinbutton_sec.get_value()
                cmd = ['date', '+%Y%m%d', '-s', year + month + day]
                process = subprocess.Popen(cmd)
                process.wait()
                cmd = ['date', '+T', '-s', hour + ':' + min + ':' + sec]
                process = subprocess.Popen(cmd)
                process.wait()
                cmd = ['hwclock', '--systohc']
                process = subprocess.Popen(cmd)
                process.wait()
        if not self.switch_utc.get_active() == utcstate():
            setutc(self.switch_utc.get_active())
        Gtk.main_quit()

    def on_button_cancel_clicked(self, widget, data=None):
        Gtk.main_quit()

    def gtk_main_quit(self, widget, data=None):
        Gtk.main_quit()

    def on_button_timezone_clicked(self, widget, data=None):
        self.tzwindow.show()

    def on_button_sync_now_clicked(self, widget, data=None):
        ntp_sync_now()
        self.update_calendar()
        self.update_time()

    def on_button_about_clicked(self, widget, data=None):
        self.aboutdialog.show()

    def on_aboutdialog_response(self, widget, data=None):
        self.aboutdialog.hide()

    def on_aboutdialog_delete_event(self, widget, event):
        self.aboutdialog.hide()
        return True

    def on_tz_button_ok_clicked(self, widget, data=None):
        pos = self.continentlist.get_cursor()[0][0]
        selectedcontinent = continents()[pos]
        pos = self.locationlist.get_cursor()[0][0]
        selectedlocation = cities(selectedcontinent)[pos]
        self.update_timezone_label(selectedcontinent, selectedlocation)
        settimezone(selectedcontinent, selectedlocation)
        self.tzwindow.hide()

    def on_tz_button_cancel_clicked(self, widget, data=None):
        self.tzwindow.hide()

    def on_timezonewindow_delete_event(self, widget, event):
        self.tzwindow.hide()
        return True

    def on_continentlist_cursor_changed(self, widget, data=None):
        try:
            pos = self.continentlist.get_cursor()[0][0]
        except TypeError:
            pos = 0
        self.locationliststore.clear()
        selectedcontinent = continents()[pos]
        currenttz = currenttimezone()[1]
        count = 0
        set = False
        for i in cities(selectedcontinent):
            self.locationliststore.append([i])
            if i == currenttz:
                set = True
                self.locationlist.set_cursor(count)
                self.locationlist.scroll_to_cell(count)
            count += 1
            if set == False:
                self.locationlist.set_cursor(0)
                self.locationlist.scroll_to_cell(0)

    def update_timezone_label(self, continent, location):
        self.label_timezone.set_label(
            _('Time zone:') + '      ' + continent + '/' + location)

    def on_switch_sync_toggled(self, widget, data=None):
        state = not self.switch_sync.get_active()
        self.label_date.set_sensitive(state)
        self.calendar.set_sensitive(state)
        self.label_time.set_sensitive(state)
        self.spinbutton_hrs.set_sensitive(state)
        self.spinbutton_min.set_sensitive(state)
        self.spinbutton_sec.set_sensitive(state)
        self.button_sync_now.set_sensitive(state)

    def update_calendar(self):
        now = datetime.datetime.now()
        self.calendar.select_month(now.month - 1, now.year)
        self.calendar.select_day(now.day)

    def update_time(self):
        now = datetime.datetime.now()
        self.spinbutton_hrs.set_value(now.hour)
        self.spinbutton_min.set_value(now.minute)
        self.spinbutton_sec.set_value(now.second)

    def __init__(self):
        builder = Gtk.Builder()
        builder.set_translation_domain("gtkclocksetup")
        if os.path.exists('gtkclocksetup.ui'):
            builder.add_from_file('gtkclocksetup.ui')
        elif os.path.exists('/usr/share/salixtools/gtkclocksetup/gtkclocksetup.ui'):
            builder.add_from_file(
                '/usr/share/salixtools/gtkclocksetup/gtkclocksetup.ui')
        self.window = builder.get_object('gtkclocksetup')
        self.tzwindow = builder.get_object('timezonewindow')
        self.tzsyncwindow = builder.get_object('tzsyncwindow')
        self.label_timezone = builder.get_object('label_timezone')
        self.label_timezone.set_label(
            _('Time zone:') + '      ' + currenttimezone()[0] + '/' + currenttimezone()[1])
        self.continentlist = builder.get_object('continentlist')
        self.continentcolumn = builder.get_object('continentcolumn')
        self.continentliststore = builder.get_object('continentliststore')
        self.locationlist = builder.get_object('locationlist')
        self.locationcolumn = builder.get_object('locationcolumn')
        self.locationliststore = builder.get_object('locationliststore')
        self.switch_sync = builder.get_object('switch_sync')
        self.button_sync_now = builder.get_object('button_sync_now')
        self.button_timezone = builder.get_object('button_timezone')
        self.label_date = builder.get_object('label_date')
        self.calendar = builder.get_object('calendar1')
        self.label_time = builder.get_object('label_time')
        self.spinbutton_hrs = builder.get_object('spinbutton_hrs')
        self.spinbutton_min = builder.get_object('spinbutton_min')
        self.spinbutton_sec = builder.get_object('spinbutton_sec')
        self.continentcolumn.set_title(_('General area'))
        self.locationcolumn.set_title(_('Location'))
        self.switch_utc = builder.get_object('switch_utc')
        self.switch_utc.set_active(utcstate())
        self.aboutdialog = builder.get_object('aboutdialog')

        ntp = ntppresent()
        self.switch_sync.set_sensitive(ntp)
        self.button_sync_now.set_sensitive(not ntp)
        ntp = ntpstate()
        self.switch_sync.set_active(ntp)
        self.on_switch_sync_toggled(self)

        currentcontinent = currenttimezone()[0]
        count = 0
        self.continentliststore.clear()
        for i in continents():
            self.continentliststore.append([i])
            if i == currentcontinent:
                self.continentlist.set_cursor(count)
                self.continentlist.scroll_to_cell(count)
            count += 1
        self.on_continentlist_cursor_changed(self)
        builder.connect_signals(self)

        self.update_calendar()
        self.update_time()

if __name__ == "__main__":
    app = GTKClockSetup()
    app.window.show()
    Gtk.main()
