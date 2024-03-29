#!/usr/bin/python3
# vim:et:sta:sts=4:sw=4:ts=8:tw=79:

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import sys
import re
from ipaddress import ip_address

# Internationalization
import locale
import gettext
locale.setlocale(locale.LC_ALL, '')
locale.bindtextdomain("gtkhostsetup", "/usr/share/locale")
gettext.bindtextdomain("gtkhostsetup", "/usr/share/locale")
gettext.textdomain("gtkhostsetup")
_ = gettext.gettext

hostname_os_file = '/etc/HOSTNAME'
hostname_file = '/etc/hostname_new'
hosts_file = '/etc/hosts'


def get_hostname():
    try:
        if os.access(hostname_file, os.R_OK):
            with open(hostname_file, 'r') as f:
                line = f.readline().replace('\n', '')
        else:
            with open(hostname_os_file, 'r') as f:
                line = f.readline().replace('\n', '')
    except IOError:
        return ['', '']
    if len(line) == 0:
        return ['', '']
    else:
        hostname = line.partition('.')[0]
        domain = line.partition('.')[2]
        return hostname, domain


def get_other_hosts():
    try:
        with open(hosts_file, 'r') as f:
            contents = f.readlines()
    except IOError:
        return [[]]
    hostlines = []
    use_ipv6 = False
    for line in contents:
        temp = line.replace('\t', ' ').replace(
            '\n', '').partition('#')[0].split()
        line = ' '.join(temp)
        if not line == '':
            ip = line.partition(' ')[0]
            hostname = line.partition(' ')[2].partition('.')[0]
            domain = line.partition(' ')[2].partition('.')[2].partition(' ')[0]
            if ip == '::1':
                use_ipv6 = True
            elif ip != '127.0.0.1':
                hostlines.append([ip, hostname, domain])
    return sorted(hostlines), use_ipv6


def check_hostname(ip, hostname, domain):
    error = False
    msg = ''
    if ip == '':
        error = True
        msg = _('The IP address cannot be empty.')
    elif hostname == '':
        error = True
        msg = _('The hostname cannot be empty.')
    elif hostname.startswith('-'):
        error = True
        msg = _('The hostname cannot start with a hyphen.')
    elif hostname.endswith('-'):
        error = True
        msg = _('The hostname cannot end with a hyphen.')
    elif domain.startswith('-'):
        error = True
        msg = _('The domain cannot start with a hyphen.')
    elif domain.endswith('-'):
        error = True
        msg = _('The domain cannot end with a hyphen.')
    if error == False:
        for i in ip:
            try:
                valid_ip = ip_address(ip)
            except ValueError:
                error = True
                msg = _('Not a valid IP address.')
    if error == False:
        for i in hostname:
            if not i in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-':
                error = True
                msg = _(
                    'The hostname can consist solely of latin letters, numbers and hyphens.')
    if error == False:
        for i in domain:
            if not i in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.':
                error = True
                msg = _(
                    'The domain can consist solely of latin letters, numbers, hyphens and dots.')
    return error, msg


def write_hosts(hostname, domain, host_list, use_ipv6):
    with open(hostname_file, 'w') as f:
        if domain == '':
            f.write(hostname + '\n')
        else:
            f.write(hostname + '.' + domain + '\n')
    with open(hosts_file, 'w') as f:
        f.write('#\n')
        f.write('# hosts\tThis file describes a number of hostname-to-address\n')
        f.write('#\t\tmappings for the TCP/IP subsystem. It is mostly\n')
        f.write('#\t\tused at boot time, when no name servers are running.\n')
        f.write('#\t\tOn small systems, this file can be used instead of a\n')
        f.write('#\t\t"named" name server.  Just add the names, addresses\n')
        f.write('#\t\tand any aliases to this file...\n')
        f.write('#\n')
        f.write('# By the way, Arnt Gulbrandsen <agulbra@nvg.unit.no> says that 127.0.0.1\n')
        f.write('# should NEVER be named with the name of the machine. It causes problems\n')
        f.write('# for some (stupid) programs, irc and reputedly talk. :^)\n')
        f.write('#\n')
        f.write('# For loopbacking.\n')
        f.write('127.0.0.1\tlocalhost\n')
        if use_ipv6:
            f.write('::1\t\tlocalhost\n')
        if domain == '':
            f.write('127.0.0.1\t' + hostname + '\n')
            if use_ipv6:
                f.write('::1\t\t' + hostname + '\n')
        else:
            f.write('127.0.0.1\t' + hostname + '.' +
                    domain + ' ' + hostname + '\n')
            if use_ipv6:
                f.write('::1\t\t' + hostname + '.' +
                        domain + ' ' + hostname + '\n')
        f.write('\n')
        for i in host_list:
            ip, hostname, domain = i
            if domain == '':
                f.write(ip + '\t' + hostname + '\n')
            else:
                f.write(ip + '\t' + hostname + '.' +
                        domain + ' ' + hostname + '\n')
        f.write('\n# End of hosts.\n')


class GTKHostSetup:

    def on_button_about_clicked(self, widget, data=None):
        self.aboutdialog.show()

    def on_aboutdialog_response(self, widget, data=None):
        self.aboutdialog.hide()

    def on_aboutdialog_delete_event(self, widget, event):
        self.aboutdialog.hide()
        return True

    def create_host_list(self, widget):
        other_hosts, self.use_ipv6 = get_other_hosts()
        for i in other_hosts:
            self.liststore_hosts.append(i)

    def on_button_ok_clicked(self, widget, data=None):
        this_hostname = self.entry_hostname.get_text()
        this_domain = self.entry_domain.get_text()
        error, message = check_hostname(
            '127.0.0.1', this_hostname, this_domain)
        if error:
            self.label_main_error.set_text(message)
            self.error_main_window.show()
        else:
            host_list = []
            if len(self.liststore_hosts) > 0:
                iter = self.liststore_hosts.get_iter(0)
                while (iter):
                    ip = self.liststore_hosts.get_value(iter, 0)
                    hostname = self.liststore_hosts.get_value(iter, 1)
                    domain = self.liststore_hosts.get_value(iter, 2)
                    host_list.append([ip, hostname, domain])
                    iter = self.liststore_hosts.iter_next(iter)
            write_hosts(self.entry_hostname.get_text(),
                        self.entry_domain.get_text(), sorted(host_list),
                        self.switch_ipv6.get_state())
            Gtk.main_quit()

    def on_button_cancel_clicked(self, widget, data=None):
        Gtk.main_quit()

    def gtk_main_quit(self, widget, data=None):
        Gtk.main_quit()

    def on_button_add_clicked(self, widget, data=None):
        self.add_host_window.show()

    def on_add_host_window_delete_event(self, widget, data=None):
        self.add_host_window.hide()
        return True

    def on_button_edit_clicked(self, widget, data=None):
        try:
            host = self.treeview_hosts.get_selection()
            self.liststore_hosts, iter = host.get_selected()
            self.entry_edit_ip.set_text(
                self.liststore_hosts.get_value(iter, 0))
            self.entry_edit_hostname.set_text(
                self.liststore_hosts.get_value(iter, 1))
            self.entry_edit_domain.set_text(
                self.liststore_hosts.get_value(iter, 2))
            self.edit_host_window.show()
        except TypeError:
            pass

    def on_button_edit_ok_clicked(self, widget, data=None):
        ip = self.entry_edit_ip.get_text()
        hostname = self.entry_edit_hostname.get_text()
        domain = self.entry_edit_domain.get_text()
        error, message = check_hostname(ip, hostname, domain)
        if error:
            self.label_edit_error.set_text(message)
            self.edit_error_window.show()
        else:
            try:
                self.edit_host_window.hide()
                host = self.treeview_hosts.get_selection()
                self.liststore_hosts, iter = host.get_selected()
                self.liststore_hosts.remove(iter)
                self.liststore_hosts.append([ip, hostname, domain])
                self.entry_edit_ip.set_text('')
                self.entry_edit_hostname.set_text('')
                self.entry_edit_domain.set_text('')
                self.liststore_hosts.set_sort_column_id(0, Gtk.SortType.ASCENDING)
            except TypeError:
                pass

    def on_button_edit_cancel_clicked(self, widget, data=None):
        self.edit_host_window.hide()

    def on_edit_host_window_delete_event(self, widget, data=None):
        self.edit_host_window.hide()
        return True

    def on_button_delete_clicked(self, widget, data=None):
        try:
            host = self.treeview_hosts.get_selection()
            self.liststore_hosts, iter = host.get_selected()
            self.liststore_hosts.remove(iter)
        except TypeError:
            pass

    def on_button_add_ok_clicked(self, widget, data=None):
        ip = self.entry_new_ip.get_text()
        hostname = self.entry_new_hostname.get_text()
        domain = self.entry_new_domain.get_text()
        error, message = check_hostname(ip, hostname, domain)
        if error:
            self.label_add_error.set_text(message)
            self.add_error_window.show()
        else:
            self.add_host_window.hide()
            self.liststore_hosts.append([ip, hostname, domain])
            self.entry_new_ip.set_text('')
            self.entry_new_hostname.set_text('')
            self.entry_new_domain.set_text('')
            self.liststore_hosts.set_sort_column_id(0, Gtk.SortType.ASCENDING)

    def on_button_add_cancel_clicked(self, widget, data=None):
        self.add_host_window.hide()

    def on_button_add_error_ok_clicked(self, widget, data=None):
        self.add_error_window.hide()

    def on_add_error_window_delete_event(self, widget, data=None):
        self.add_error_window.hide()
        return True

    def on_button_edit_error_ok_clicked(self, widget, data=None):
        self.edit_error_window.hide()

    def on_edit_error_window_delete_event(self, widget, data=None):
        self.edit_error_window.hide()
        return True

    def on_button_error_main_ok_clicked(self, widget, data=None):
        self.error_main_window.hide()

    def on_error_main_window_delete_event(self, widget, data=None):
        self.error_main_window.hide()
        return True

    def __init__(self):
        builder = Gtk.Builder()
        builder.set_translation_domain("gtkhostsetup")
        if os.path.exists('gtkhostsetup.ui'):
            builder.add_from_file('gtkhostsetup.ui')
        elif os.path.exists('/usr/share/salixtools/gtkhostsetup/gtkhostsetup.ui'):
            builder.add_from_file(
                '/usr/share/salixtools/gtkhostsetup/gtkhostsetup.ui')
        self.window = builder.get_object('gtkhostsetup')

        #
        # Main window
        #
        self.entry_hostname = builder.get_object('entry_hostname')
        self.entry_domain = builder.get_object('entry_domain')
        current_hostname, current_domain = get_hostname()
        self.entry_hostname.set_text(current_hostname)
        self.entry_domain.set_text(current_domain)

        #self.use_ipv6 = False
        self.switch_ipv6 = builder.get_object('switch_ipv6')

        self.treeviewcolumn_ip = builder.get_object('treeviewcolumn_ip')
        self.treeviewcolumn_hostname = builder.get_object(
            'treeviewcolumn_hostname')
        self.treeviewcolumn_domain = builder.get_object(
            'treeviewcolumn_domain')
        self.treeviewcolumn_ip.set_title(_('IP address'))
        self.treeviewcolumn_hostname.set_title(_('Hostname'))
        self.treeviewcolumn_domain.set_title(_('Domain'))

        self.treeview_hosts = builder.get_object('treeview_hosts')
        self.liststore_hosts = builder.get_object('liststore_hosts')
        self.liststore_hosts.clear()
        self.create_host_list(self) # this also sets self.use_ipv6

        self.switch_ipv6.set_state(self.use_ipv6)

        #
        # Add host window
        #
        self.add_host_window = builder.get_object('add_host_window')
        self.entry_new_ip = builder.get_object('entry_new_ip')
        self.entry_new_hostname = builder.get_object('entry_new_hostname')
        self.entry_new_domain = builder.get_object('entry_new_domain')

        #
        # Edit host window
        #
        self.edit_host_window = builder.get_object('edit_host_window')
        self.entry_edit_ip = builder.get_object('entry_edit_ip')
        self.entry_edit_hostname = builder.get_object('entry_edit_hostname')
        self.entry_edit_domain = builder.get_object('entry_edit_domain')

        #
        # Error message in main window
        #
        self.error_main_window = builder.get_object('error_main_window')
        self.label_main_error = builder.get_object('label_main_error')

        #
        # Error message in add window
        #
        self.add_error_window = builder.get_object('add_error_window')
        self.label_add_error = builder.get_object('label_add_error')

        #
        # Error message in edit window
        #
        self.edit_error_window = builder.get_object('edit_error_window')
        self.label_edit_error = builder.get_object('label_edit_error')

        #
        # About dialog
        #
        self.aboutdialog = builder.get_object('aboutdialog')

        builder.connect_signals(self)

if __name__ == "__main__":
    app = GTKHostSetup()
    app.window.show()
    Gtk.main()
