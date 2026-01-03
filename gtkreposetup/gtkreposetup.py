#!/usr/bin/python3
# vim:et:sta:sts=4:sw=4:ts=8:tw=79:


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import os
import sys
import subprocess
import threading
import time
import platform
import re
import urllib.request, urllib.error, urllib.parse
from textconfig import TextConfig

# Internationalization
import locale
import gettext
locale.setlocale(locale.LC_ALL, '')
locale.bindtextdomain("gtkreposetup", "/usr/share/locale")
gettext.bindtextdomain("gtkreposetup", "/usr/share/locale")
gettext.textdomain("gtkreposetup")
_ = gettext.gettext

canceltask = False

def threaded(f):
    def wrapper(*args):
        t = threading.Thread(target=f, args=args)
        t.daemon = True
        t.start()
    return wrapper

class BreakConnection(Exception):
    '''
    An exception class to help break connections when hitting the cancel
    button.
    '''
    pass

def show_error_dialog(error_msg, parent):
    dialog = Gtk.MessageDialog(parent=parent, flags=0, type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK, message_format=error_msg)
    dialog.set_title(_('Error'))
    dialog.set_modal(True)
    dialog.set_transient_for(parent)
    dialog.run()
    dialog.destroy()

def get_arch():
    '''
    Determine the CPU architecture. Should be:
    - 'arm' for any arm* system
    - 'i486' for 32bit systems
    - 'x86_64' for 64bit systems
    '''
    m = platform.machine()
    if re.match('i.86$', m):
        return 'i486'
    elif re.match('arm', m):
        return 'arm'
    else:
        return m

def get_salix_version(parent_window):
    '''
    Read the Salix version.
    '''
    p = subprocess.Popen(['lsb_release', '-rs'], stdout=subprocess.PIPE)
    if p.wait() == 0:
        return p.communicate()[0].strip().decode()
    else:
        msg1 = _('lsb_release is not installed.')
        msg2 = _('Exiting.')
        show_error_dialog('%s\n\n%s' % (msg1, msg2), parent_window)
        sys.exit(1)

def get_current_repo(parent_window):
    '''
    Return the currently selected repository. Just runs the command line
    reposetup tool with the -p option to get it.
    '''
    p = subprocess.Popen(['reposetup', '-p'], stdout=subprocess.PIPE)
    if p.wait() == 0:
        return p.communicate()[0].strip().decode()
    # error code 11 is thrown by reposetup when lsb_release is not installed
    elif p.wait() == 11:
        msg1 = _('lsb_release is not installed.')
        msg2 = _('Exiting.')
        show_error_dialog('%s\n\n%s' % (msg1, msg2), parent_window)
        sys.exit(1)
    else:
        return None

def get_repo_list_from_file(parent_window):
    '''
    Reads the list of mirrors from the file they are stored in and returns it
    as a list.
    '''
    repolist = []
    fname = '/usr/share/salixtools/reposetup/repomirrors'
    try:
        with open(fname, 'r') as f:
            while True:
                line = f.readline().rstrip()
                if len(line) == 0:
                    break
                url = line.partition(' ')[0]
                country = line.partition(' ')[2]
                repolist.append([url, country])
    except IOError:
        msg1 = _('Could not read file:')
        msg2 = _('Exiting.')
        show_error_dialog('%s %s\n\n%s' % (msg1, fname, msg2), parent_window)
        sys.exit(1)
    try:
        with open('/etc/salixtools/repos-custom', 'r') as f:
            while True:
                line = f.readline().rstrip()
                if len(line) == 0:
                    break
                if line.startswith('file:///') or line.startswith('http://') \
                        or line.startswith('ftp://'):
                    url = line
                    country = '..'
                    repolist.append([url, country])
    except IOError:
        # not a big deal if the repos-custom file is not there
        pass
    return repolist

def get_slaptget_settings():
    exclude_default = '^aaa_elflibs,^aaa_base,^devs,^glibc.*,^kernel-.*,^udev,' \
                      '^rootuser-settings,^zzz-settings.*'
    fname = '/etc/slapt-get/slapt-getrc'
    xfce418 = False
    xfce420 = False
    kernel612 = False
    try:
        c = TextConfig(fname)
    except IOError:
        msg1 = _('WARNING:')
        msg2 = _('Could not read file:')
        print('%s %s %s' % (msg1, msg2, fname))
        working_dir = '/var/slapt-get'
        exclude = exclude_default
        if arch == 'x86_64':
            exclude = exclude + ',-i?86-'
        else:
            exclude = exclude + ',x86_64'
        custom_repos = []
    else:
        try:
            working_dir = c.get('WORKINGDIR')
        except ValueError:
            working_dir = '/var/slapt-get'
        try:
            exclude = c.get('EXCLUDE')
        except ValueError:
            exclude = exclude_default
            arch = get_arch()
            if arch != 'arm':
                if arch == 'x86_64':
                    exclude = exclude + ',-i?86-'
                else:
                    exclude = exclude + ',x86_64'
        try:
            sources = c.get_all('SOURCE')
            custom_repos = []
            for s in sources:
                if s.endswith(':CUSTOM'):
                    custom_repos.append(s)
                if 'xfce4.18' in s:
                    xfce418 = True
                if 'xfce4.20' in s:
                    xfce420 = True
                if 'kernel6.12' in s:
                    kernel612 = True
        except ValueError:
            custom_repos = []
        settings = {
                'working_dir': working_dir,
                'exclude': exclude,
                'custom_repos': custom_repos,
                'xfce418': xfce418,
                'xfce420': xfce420,
                'kernel612': kernel612
            }
    return settings

def get_slaptsrc_settings():
    fname = '/etc/slapt-get/slapt-srcrc'
    try:
        c = TextConfig(fname)
    except IOError:
        msg1 = _('WARNING:')
        msg2 = _('Could not read file:')
        print('%s %s %s' % (msg1, msg2, fname))
        build_dir = '/usr/src/slapt-src'
        pkg_ext = 'txz'
    else:
        try:
            build_dir = c.get('BUILDDIR')
        except ValueError:
            build_dir = '/usr/src/slapt-src'
        try:
            pkg_ext = c.get('PKGEXT')
        except ValueError:
            pkg_ext = 'txz'
    settings = {
            'build_dir': build_dir,
            'pkg_ext': pkg_ext
        }
    return settings

def write_conf(repo, parent_window):
    '''
    Write configuration files.
    '''
    slaptget_settings = get_slaptget_settings()
    slaptsrc_settings = get_slaptsrc_settings()
    arch = get_arch()
    if arch == 'arm':
        slackdir = 'slackwarearm'
    else:
        slackdir = 'slackware'
    version = get_salix_version(parent_window)
    success = True
    #
    # slapt-getrc
    #
    fname = '/etc/slapt-get/slapt-getrc'
    try:
        with open(fname, 'w') as f:
            f.write('# Working directory for local storage/cache.\n')
            f.write('WORKINGDIR={}\n\n'.format(slaptget_settings['working_dir']))
            f.write('# Exclude package names and expressions.\n')
            f.write('# To exclude pre and beta packages, add this to the exclude:\n')
            f.write('#   [0-9\_\.\-]{1}pre[0-9\-\.\-]{1}\n')
            f.write('EXCLUDE={}\n\n'.format(slaptget_settings['exclude']))
            f.write('# The Slackware repositories, including dependency information\n')
            f.write('SOURCE={r}/{a}/{s}-{v}/:OFFICIAL\n'.format(
                r=repo, a=arch, s=slackdir, v=version))
            f.write('SOURCE={r}/{a}/{s}-{v}/extra/:OFFICIAL\n\n'.format(
                r=repo, a=arch, s=slackdir, v=version))
            f.write('# The Salix repository\n')
            f.write('SOURCE={r}/{a}/{v}/:PREFERRED\n'.format(
                r=repo, a=arch, v=version))
            if slaptget_settings['xfce418']:
                f.write('# The Xfce 4.18 repo for Salix 15.0\n')
                f.write('SOURCE={r}/{a}/xfce4.18-{v}/:PREFERRED\n'.format(
                    r=repo, a=arch, v=version))
            if slaptget_settings['xfce420']:
                f.write('# The Xfce 4.20 repo for Salix 15.0\n')
                f.write('SOURCE={r}/{a}/xfce4.20-{v}/:PREFERRED\n'.format(
                    r=repo, a=arch, v=version))
            if slaptget_settings['kernel612']:
                f.write('# The Kernel 6.12 repo for Salix 15.0\n')
                f.write('SOURCE={r}/{a}/kernel6.12-{v}/:PREFERRED\n'.format(
                    r=repo, a=arch, v=version))
            f.write('# And the Salix extra repository\n')
            f.write('SOURCE={r}/{a}/extra-{v}/:OFFICIAL\n\n'.format(
                r=repo, a=arch, v=version))
            f.write('# Local repositories\n')
            f.write('# SOURCE=file:///var/www/packages/:CUSTOM\n')
            for repo in slaptget_settings['custom_repos']:
                f.write('SOURCE={r}\n'.format(r=repo))
    except IOError:
        msg1 = _('Could not write to file:')
        msg2 = _('Exiting.')
        show_error_dialog('%s %s\n\n%s' % (msg1, fname, msg2), parent_window)
        sys.exit(1)
    #
    # slapt-srcrc
    #
    #
    fname = '/etc/slapt-get/slapt-srcrc'
    try:
        with open(fname, 'w') as f:
            f.write('BUILDDIR={}\n'.format(slaptsrc_settings['build_dir']))
            f.write('PKGEXT={}\n'.format(slaptsrc_settings['pkg_ext']))
            f.write('SOURCE={r}/slkbuild/{v}/\n'.format(
                r=repo, v=version))
            f.write('SOURCE={r}/sbo/{v}/\n'.format(
                r=repo, v=version))
    except IOError:
        msg1 = _('Could not write to file:')
        msg2 = _('Exiting.')
        show_error_dialog('%s %s\n\n%s' % (msg1, fname, msg2), parent_window)
        sys.exit(1)
    return success

def get_mirrors(repo):
    '''
    Retrieves the MIRRORS file from repo.
    '''
    try:
        f = urllib.request.urlopen('{}/MIRRORS'.format(repo))
        mirrors = f.read().splitlines()
        mirrors[:] = [x.decode() for x in mirrors]
    except urllib.error.HTTPError:
        return None
    except urllib.error.URLError:
        return None
    except BreakConnection :
        return None
    except ValueError:
        return None
    except ConnectionResetError:
        return None
    return mirrors

def write_mirrors(mirror_list):
    fname = '/usr/share/salixtools/reposetup/repomirrors'
    try:
        f = open(fname, 'w')
    except IOError:
        msg1 = _('WARNING:')
        msg2 = _('Could not write to file:')
        print("%s %s %s" % (msg1, msg2, fname))
    else:
        for line in mirror_list:
            f.write('{}\n'.format(line))
        f.close()

def update_mirror_list_from_repo(repo):
    '''
    Updates the mirror list from the specified repo.
    '''
    mirrors = get_mirrors(repo)
    if mirrors:
        write_mirrors(mirrors)
        return True
    else:
        return False

class GTKRepoSetup:

    #
    # Main Window
    #
    def on_button_about_clicked(self, widget, data=None):
        self.aboutdialog.show()

    def on_aboutdialog_response(self, widget, data=None):
        self.aboutdialog.hide()

    def on_aboutdialog_delete_event(self, widget, event):
        self.aboutdialog.hide()
        return True

    @threaded
    def on_button_ok_clicked(self, widget, data=None):
        global canceltask
        canceltask = False
        selectedrepo = self.repolist.get_selection()
        self.liststore_repo, iter = selectedrepo.get_selected()
        new_repo = self.liststore_repo.get_value(iter, 0)
        success = True
        update_repos = self.switch_update.get_active()
        error_msg = 'No error'
        if self.current_repo != new_repo:
            GLib.idle_add(self.dialog_update_repos.show)
            # write new configuration files
            ret_conf = write_conf(new_repo, self.window)
            if not ret_conf:
                error_msg = _('Could not write configuration files.')
                success = False
            if success and update_repos:
                # update slapt-getrc
                GLib.idle_add(self.label_update_repos.set_text, _('Updating package information...'))
                self.p = subprocess.Popen(['slapt-get', '--update'])
                while self.p.poll() is None:
                    GLib.idle_add(self.progressbar_update_repos.pulse)
                    time.sleep(0.1)
                retval = self.p.returncode
                if retval != 0:
                    error_msg = _('Could not update package information.')
                    success = False
            if success and update_repos:
                # update slapt-srcrc
                GLib.idle_add(self.label_update_repos.set_text, _('Updating SlackBuild information...'))
                self.p = subprocess.Popen(['slapt-src', '--update'])
                while self.p.poll() is None:
                    GLib.idle_add(self.progressbar_update_repos.pulse)
                    time.sleep(0.1)
                retval = self.p.returncode
                if retval != 0:
                    error_msg = _('Could not update SlackBuild information.')
                    success = False
        GLib.idle_add(self.dialog_update_repos.hide)
        if success and not canceltask:
            Gtk.main_quit()
        elif canceltask:
            GLib.idle_add(self.dialog_update_repos.hide)
        else:
            GLib.idle_add(self.dialog_update_repos.hide)
            GLib.idle_add(show_error_dialog, error_msg, parent=self.window)

    def on_button_update_repos_cancel_clicked(self, widget):
        global canceltask
        canceltask = True
        try:
            self.p.kill()
        except AttributeError: # object has no attribute 'p'
            pass

    def on_button_cancel_clicked(self, widget, data=None):
        Gtk.main_quit()

    def on_gtkreposetup_delete_event(self, widget, event):
        Gtk.main_quit()

    def gtk_main_quit(self, widget, data=None):
        Gtk.main_quit()

    #
    # Update Mirror List Dialog
    #
    @threaded
    def update_mirror_list(self):
        '''
        Tries to update the mirror list from the currently selected repo
        online. If it fails, it reads the local repomirrors file and tries
        to update the mirror list from each one of the repos listed in there.
        '''
        global canceltask
        canceltask = False
        GLib.idle_add(self.dialog_update_list.show)
        repos = [[self.current_repo, None]] + get_repo_list_from_file(self.window)
        for repo in repos:
            GLib.idle_add(self.progressbar_update_list.pulse)
            if not canceltask:
                url = repo[0]
                ret = update_mirror_list_from_repo(url)
                if ret:
                    break
        GLib.idle_add(self.dialog_update_list.hide)
        cursorpos = 0
        selectedpos = 0
        for i in get_repo_list_from_file(self.window):
            self.liststore_repo.append(i)
            if self.current_repo == i[0]:
                selectedpos = cursorpos
            cursorpos += 1
        GLib.idle_add(self.repolist.set_cursor, selectedpos)
        if selectedpos > 5:
            if selectedpos > cursorpos - 5:
                scrollto = cursorpos - 1
            else:
                scrollto = selectedpos + 1
            GLib.idle_add(self.repolist.scroll_to_cell, scrollto)

    def on_button_update_list_cancel_clicked(self, widget):
        GLib.idle_add(self.dialog_update_list.hide)
        global canceltask
        canceltask = True
        raise BreakConnection

    def __init__(self):
        builder = Gtk.Builder()
        builder.set_translation_domain("gtkreposetup")
        if os.path.exists('gtkreposetup.ui'):
            builder.add_from_file('gtkreposetup.ui')
        elif os.path.exists('/usr/share/salixtools/gtkreposetup/gtkreposetup.ui'):
            builder.add_from_file(
                '/usr/share/salixtools/gtkreposetup/gtkreposetup.ui')
        self.window = builder.get_object('gtkreposetup')
        self.switch_update = builder.get_object('switch_update')
        self.switch_update.set_state(True)
        self.aboutdialog = builder.get_object('aboutdialog')

        self.repolist = builder.get_object('repolist')
        self.liststore_repo = builder.get_object('liststore_repo')
        self.liststore_repo.clear()

        # update mirror list dialog
        self.dialog_update_list = builder.get_object('dialog_update_list')
        self.progressbar_update_list = builder.get_object('progressbar_update_list')

        # update package and SlackBuild caches dialog
        self.dialog_update_repos = builder.get_object('dialog_update_repos')
        self.label_update_repos = builder.get_object('label_update_repos')
        self.progressbar_update_repos = builder.get_object('progressbar_update_repos')

        # populate the list of mirrors
        self.current_repo = get_current_repo(parent_window = self.dialog_update_list)

        builder.connect_signals(self)

        self.update_mirror_list()

if __name__ == "__main__":
    app = GTKRepoSetup()
    app.window.show()
    Gtk.main()
