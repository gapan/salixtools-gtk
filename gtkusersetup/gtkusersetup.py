#!/usr/bin/python3
# vim:et:sta:sts=4:sw=4:ts=8:tw=79:

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import sys
import subprocess
import datetime
import pwd
import grp


class SystemUsers:

    def all_users_data(self):
        userdata = []
        for i in pwd.getpwall():
            login = i[0]
            uid = i[2]
            gid = i[3]
            gecos = i[4]
            homedir = i[5]
            shell = i[6]
            if ',' in gecos:
                fullname = gecos.partition(',')[0]
                officeinfo = gecos.partition(',')[2].partition(',')[0]
                officeext = gecos.partition(',')[2].partition(',')[
                    2].partition(',')[0]
                homephone = gecos.partition(',')[2].partition(
                    ',')[2].partition(',')[2].partition(',')[0]
            else:
                fullname = gecos
                officeinfo = ''
                officeext = ''
                homephone = ''
            userdata.append([login, uid, gid, fullname, officeinfo,
                             officeext, homephone, homedir, shell])
        return userdata

    def default_groups(self):
        groups = []
        groups_to_try = ('audio', 'video', 'cdrom', 'floppy',
                         'lp', 'plugdev', 'polkitd', 'pulse',
                         'scanner', 'power', 'netdev')
        for i in groups_to_try:
            try:
                groups.append(grp.getgrnam(i)[0])
            except KeyError:
                pass

        return groups

    def user_list(self, all=False):
        userlist = []
        for i in self.all_users_data():
            if all == False:
                if i[1] >= 500:
                    userlist.append(i)
            else:
                userlist.append(i)
        return userlist

    def get_uid(self, login):
        uid = pwd.getpwnam(login)[2]
        return uid

    def get_gid(self, group):
        gid = grp.getgrnam(group)[2]
        return gid

    def get_fullname(self, login):
        for i in self.all_users_data():
            if i[0] == login:
                fullname = i[3]
        return fullname

    def get_officeinfo(self, login):
        for i in self.all_users_data():
            if i[0] == login:
                officeinfo = i[4]
        return officeinfo

    def get_officeext(self, login):
        for i in self.all_users_data():
            if i[0] == login:
                officeext = i[5]
        return officeext

    def get_homephone(self, login):
        for i in self.all_users_data():
            if i[0] == login:
                homephone = i[6]
        return homephone

    def get_homedir(self, login):
        homedir = pwd.getpwnam(login)[5]
        return homedir

    def get_shell(self, login):
        shell = pwd.getpwnam(login)[6]
        return shell

    def get_maingroup(self, login):
        group = subprocess.getoutput(
            'groups ' + login).partition(' : ')[2].partition(' ')[0]
        return group

    def get_groups(self, login):
        groups = []
        allgroups = grp.getgrall()
        for i in allgroups:
            if login in i[3]:
                groups.append(i[0])
        return groups

    def get_expiry_date(self, login):
        now = datetime.datetime.now()
        expirydays = subprocess.getoutput(
            'grep -e "^' + login + ':.*$" /etc/shadow | cut -d : -f 8')
        if expirydays == '':
            state = False
            year = now.year
            month = now.month
            day = now.day
        else:
            state = True
            expirydate = subprocess.getoutput(
                'date -u --date "Jan 1, 1970 + ' + expirydays + ' days" +%Y-%m-%d')
            year = int(expirydate.partition('-')[0])
            month = int(expirydate.partition('-')[2].partition('-')[0]) - 1
            day = int(expirydate.partition('-')
                      [2].partition('-')[2].partition('-')[0])
        return state, year, month, day

    def create_user(self, login, shell, group, groups, password):
        os.system('useradd -s ' + shell + ' -g ' +
                  group + ' -m -k /etc/skel ' + login)
        self.set_password(login, password)
        for i in groups:
            self.add_user_to_group(login, i)

    def create_group(self, groupname, gid):
        os.system('groupadd -g ' + str(gid) + ' ' + groupname)

    def del_user(self, login, remove_home=False):
        if remove_home == True:
            homedir = self.get_homedir(login)
            os.system('rm -rf ' + homedir)
        os.system('userdel ' + login)

    def del_group(self, groupname):
        os.system('groupdel ' + groupname)

    def set_password(self, login, password):
        os.system('echo "' + login + ':' + password + '" | chpasswd')

    def set_uid(self, login, uid):
        os.system('usermod -u ' + str(uid) + ' ' + login)

    def set_gid(self, group, gid):
        os.system('groupmod -g ' + str(gid) + ' ' + group)

    def set_group(self, login, group):
        os.system('usermod -g ' + group + ' ' + login)

    def add_user_to_group(self, login, group):
        os.system('gpasswd -a ' + login + ' ' + group + ' > /dev/null')

    def remove_user_from_group(self, login, group):
        os.system('gpasswd -d ' + login + ' ' + group + ' > /dev/null')

    def set_fullname(self, login, fullname):
        fullname = '"' + fullname + '"'
        os.system('chfn -f ' + fullname + ' ' + login)

    def set_officeinfo(self, login, officeinfo):
        officeinfo = '"' + officeinfo + '"'
        os.system('chfn -r ' + officeinfo + ' ' + login)

    def set_officeext(self, login, officeext):
        officeext = '"' + officeext + '"'
        os.system('chfn -w ' + officeext + ' ' + login)

    def set_homephone(self, login, homephone):
        homephone = '"' + homephone + '"'
        os.system('chfn -h ' + homephone + ' ' + login)

    def set_homedir(self, login, homedir):
        os.system('usermod -d ' + homedir + ' ' + login)

    def set_shell(self, login, shell):
        os.system('usermod -s ' + shell + ' ' + login)

    def set_expiry_date(self, login, year, month, day):
        expirydate = str(year) + '-' + str(month) + '-' + str(day)
        os.system('usermod -e ' + expirydate + ' ' + login)

    def set_no_expiry_date(self, login):
        os.system('usermod -e "" ' + login)

    def get_all_groups(self):
        groups = []
        for i in grp.getgrall():
            groupname = i[0]
            gid = i[2]
            members = i[3]
            groups.append([groupname, gid, members])
        return groups

    def user_in_group(self, login, group):
        if group in self.get_groups(login):
            member = True
        else:
            member = False
        return member

    def check_password(self, password1, password2):
        if password1 == password2:
            if len(password1) < 5:
                setpassword = False
                msg = _(
                    "Password is too short. It has to be at least 5 characters long.")
            elif '\\' in password1:
                setpassword = False
                msg = _("Password cannot include the backslash character.")
            else:
                setpassword = True
                msg = ''
        else:
            setpassword = False
            msg = _("Passwords don't match")
        return setpassword, msg

    def check_username(self, username):
        u = SystemUsers()
        setusername = True
        msg = ''
        if username == '':
            setusername = False
            msg = _("Username cannot be empty.")
        elif len(username) > 31:
            setusername = False
            msg = _("Username cannot exceed 31 characters")
        elif ' ' in username:
            setusername = False
            msg = _("Username cannot include the space character.")
        elif username.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
            setusername = False
            msg = _("Username cannot start with a number.")
        elif username.startswith('_'):
            setusername = False
            msg = _("Username cannot start with an underscore.")
        elif username.startswith('-'):
            setusername = False
            msg = _("Username cannot start with a dash.")
        if setusername == True:
            for i in username:
                if not i in 'abcdefghijklmnopqrstuvwxyz-_0123456789':
                    setusername = False
                    msg = _(
                        "Username can consist solely of latin lower case letters, numbers, dashes and underscores.")
                    break
        if setusername == True:
            for i in u.user_list():
                if username == i[0]:
                    setusername = False
                    msg = _("Username \"{0}\" already exists.").format(
                        username)
                    break
        return setusername, msg

    def check_groupname(self, groupname):
        g = SystemUsers()
        setgroupname = True
        msg = ''
        if groupname == '':
            setgroupname = False
            msg = _("Group name cannot be empty.")
        elif len(groupname) > 31:
            setgroupname = False
            msg = _("Group name cannot exceed 31 characters")
        elif ' ' in groupname:
            setgroupname = False
            msg = _("Group name cannot include the space character.")
        elif groupname.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
            setgroupname = False
            msg = _("Group name cannot start with a number.")
        elif groupname.startswith('_'):
            setgroupname = False
            msg = _("Group name cannot start with an underscore.")
        elif groupname.startswith('-'):
            setgroupname = False
            msg = _("Group name cannot start with a dash.")
        if setgroupname == True:
            for i in groupname:
                if not i in 'abcdefghijklmnopqrstuvwxyz-_0123456789':
                    setgroupname = False
                    msg = _(
                        "Group name can consist solely of latin lower case letters, numbers, dashes and underscores.")
                    break
        if setgroupname == True:
            for i in g.get_all_groups():
                if groupname == i[0]:
                    setgroupname = False
                    msg = _("Group name \"{0}\" already exists.").format(
                        groupname)
                    break
        return setgroupname, msg

    def check_shell(self, shell):
        if os.path.exists(shell):
            setshell = True
            msg = ''
        else:
            setshell = False
            msg = _("Shell does not exist.")
        return setshell, msg

    def check_uid(self, uid):
        u = SystemUsers()
        setuid = True
        msg = ''
        for i in u.all_users_data():
            if uid == i[1]:
                setuid = False
                msg = _("UID {0} is assigned to another user.").format(uid)
                break
        return setuid, msg

    def check_gid(self, gid):
        setgid = True
        msg = ''
        for i in grp.getgrall():
            if i[2] == gid:
                setgid = False
                msg = _("GID {0} is assigned to another group.").format(gid)
                break
        return setgid, msg

# Internationalization
import locale
import gettext
locale.setlocale(locale.LC_ALL, '')
locale.bindtextdomain("gtkusersetup", "/usr/share/locale")
gettext.bindtextdomain("gtkusersetup", "/usr/share/locale")
gettext.textdomain("gtkusersetup")
_ = gettext.gettext


class GTKUserSetup:

    def on_button_about_clicked(self, widget, data=None):
        self.aboutdialog.show()

    def on_aboutdialog_response(self, widget, data=None):
        self.aboutdialog.hide()

    def on_aboutdialog_delete_event(self, widget, event):
        self.aboutdialog.hide()
        return True

    def gtk_main_quit(self, widget, data=None):
        Gtk.main_quit()

    def on_button_close_clicked(self, widget, data=None):
        Gtk.main_quit()

    def on_button_properties_clicked(self, widget, data=None):
        try:
            u = SystemUsers()
            self.task_add_user = False
            user = self.userlist.get_selection()
            self.userliststore, iter = user.get_selected()
            username = self.userliststore.get_value(iter, 1)
            fullname = u.get_fullname(username)
            officeinfo = u.get_officeinfo(username)
            officeext = u.get_officeext(username)
            homephone = u.get_homephone(username)
            maingroup = u.get_maingroup(username)
            homedir = u.get_homedir(username)
            shell = u.get_shell(username)
            uid = u.get_uid(username)
            expirydate = u.get_expiry_date(username)

            #
            # Set existing values
            #
            self.user_properties_window.set_title(
                _("User account properties for \"{0}\"").format(username))
            self.notebook_userproperties.set_current_page(0)

            # Account tab
            self.entry_login.set_text(username)
            self.entry_login.set_sensitive(False)
            self.entry_fullname.set_text(fullname)
            self.label_passwordheader.set_label(_("<b>Set new password</b>"))
            self.entry_password1.set_text('')
            self.entry_password2.set_text('')

            # Contact tab
            self.entry_officeinfo.set_text(officeinfo)
            self.entry_officeext.set_text(officeext)
            self.entry_homephone.set_text(homephone)

            # Groups tab
            allgroups = u.get_all_groups()
            self.groupliststore.clear()
            count = 0
            for i in allgroups:
                self.groupliststore.append([i[0]])
                if i[0] == maingroup:
                    self.combobox_maingroup.set_active(count)
                count += 1
            self.user_groupliststore.clear()
            for i in allgroups:
                group = i[0]
                gid = i[1]
                groupmembers = i[2]
                if u.user_in_group(username, group):
                    ismember = True
                else:
                    ismember = False
                self.user_groupliststore.append([ismember, group, gid, False])

            # Advanced tab
            self.label_homedir.show()
            self.entry_homedir.show()
            self.entry_homedir.set_text(homedir)
            self.entry_shell.set_text(shell)
            self.label_uid.show()
            self.spinbutton_uid.show()
            self.spinbutton_uid.set_value(uid)
            if expirydate[0] == False:
                self.checkbutton_user_expiration.set_active(False)
                self.calendar_user_expiration.set_sensitive(False)
            else:
                self.checkbutton_user_expiration.set_active(True)
                self.calendar_user_expiration.set_sensitive(True)
            self.calendar_user_expiration.select_month(
                expirydate[2] - 1, expirydate[1])
            self.calendar_user_expiration.select_day(expirydate[3])

            self.user_properties_window.show()
        except TypeError:
            pass

    def on_button_adduser_clicked(self, widget):
        u = SystemUsers()
        now = datetime.datetime.now()
        self.task_add_user = True
        #
        # Set existing values
        #
        self.user_properties_window.set_title(_("Add new user"))
        self.notebook_userproperties.set_current_page(0)

        # Account tab
        self.entry_login.set_sensitive(True)
        self.entry_login.set_text('')
        self.entry_fullname.set_text('')
        self.label_passwordheader.set_label(_("<b>Set password</b>"))
        self.entry_password1.set_text('')
        self.entry_password2.set_text('')

        # Contact tab
        self.entry_officeinfo.set_text('')
        self.entry_officeext.set_text('')
        self.entry_homephone.set_text('')

        # Groups tab
        allgroups = u.get_all_groups()
        defaultgroups = u.default_groups()
        self.groupliststore.clear()
        count = 0
        for i in allgroups:
            self.groupliststore.append([i[0]])
            if i[0] == 'users':
                self.combobox_maingroup.set_active(count)
            count += 1
        self.user_groupliststore.clear()
        for i in allgroups:
            group = i[0]
            gid = i[1]
            groupmembers = i[2]
            if group in defaultgroups:
                ismember = True
            else:
                ismember = False
            self.user_groupliststore.append([ismember, group, gid, False])

        # Advanced tab
        self.label_homedir.hide()
        self.entry_homedir.hide()
        self.entry_shell.set_text('/bin/bash')
        self.label_uid.hide()
        self.spinbutton_uid.hide()
        self.checkbutton_user_expiration.set_active(False)
        self.calendar_user_expiration.set_sensitive(False)
        self.calendar_user_expiration.select_month(now.month - 1, now.year)
        self.calendar_user_expiration.select_day(now.day)

        self.user_properties_window.show()

    def on_button_deleteuser_clicked(self, widget):
        try:
            u = SystemUsers()
            user = self.userlist.get_selection()
            self.userliststore, iter = user.get_selected()
            username = self.userliststore.get_value(iter, 1)
            self.checkbutton_delete_user_homedir.set_active(False)
            self.delete_user_window.set_title(
                _("Delete user {0}?").format(username))
            self.label_delete_user.set_text(
                _("You are about to remove user account \"{0}\" from your system. Do you really want to continue?").format(username))
            self.checkbutton_delete_user_homedir.set_label(
                _("Completely remove user's home directory ({0}) with all its contents").format(u.get_homedir(username)))
            self.delete_user_window.show()
        except TypeError:
            pass

    def on_button_managegroups_clicked(self, widget):
        self.refresh_group_list()
        self.group_settings_window.show()

    def on_checkbutton_showall_toggled(self, widget, data=None):
        self.userliststore.clear()
        status = self.checkbutton_showall.get_active()
        u = SystemUsers()
        for i in u.user_list(status):
            self.userliststore.append([i[3], i[0], i[7], i[1]])

    def on_button_user_properties_ok_clicked(self, widget, data=None):
        u = SystemUsers()
        if self.task_add_user:
            #
            # Adding new user
            #
            username = self.entry_login.get_text()
            fullname = self.entry_fullname.get_text()
            password1 = self.entry_password1.get_text()
            password2 = self.entry_password2.get_text()
            officeinfo = self.entry_officeinfo.get_text()
            officeext = self.entry_officeext.get_text()
            homephone = self.entry_homephone.get_text()
            maingroup = self.combobox_maingroup.get_active_text()
            shell = self.entry_shell.get_text()
            expiry = self.checkbutton_user_expiration.get_active()

            checkusername = u.check_username(username)
            checkpassword = u.check_password(password1, password2)
            checkshell = u.check_shell(shell)
            if checkusername[0] == False:
                self.label_properties_error_msg.set_label(checkusername[1])
                self.properties_error_window.show()
            elif checkpassword[0] == False:
                self.label_properties_error_msg.set_label(checkpassword[1])
                self.properties_error_window.show()
            elif checkshell[0] == False:
                self.label_properties_error_msg.set_label(checkshell[1])
                self.properties_error_window.show()
            else:
                groups = []
                for i in self.user_groupliststore:
                    if i[0] == True:
                        groups.append(i[1])
                u.create_user(username, shell, maingroup, groups, password1)
                u.set_fullname(username, fullname)
                u.set_officeinfo(username, officeinfo)
                u.set_officeext(username, officeext)
                u.set_homephone(username, homephone)
                if expiry:
                    year = int("%04d" %
                               (self.calendar_user_expiration.get_date()[0]))
                    month = int(
                        "%02d" % (self.calendar_user_expiration.get_date()[1])) + 1
                    day = int("%02d" %
                              (self.calendar_user_expiration.get_date()[2]))
                    u.set_expiry_date(username, year, month, day)

                self.user_properties_window.hide()
                self.on_checkbutton_showall_toggled(self)
        else:
            #
            # Editing existing user info
            #
            username = self.entry_login.get_text()
            fullname = u.get_fullname(username)
            officeinfo = u.get_officeinfo(username)
            officeext = u.get_officeext(username)
            homephone = u.get_homephone(username)
            maingroup = u.get_maingroup(username)
            homedir = u.get_homedir(username)
            shell = u.get_shell(username)
            uid = u.get_uid(username)
            expiry_date = u.get_expiry_date(username)

            new_fullname = self.entry_fullname.get_text()
            new_password1 = self.entry_password1.get_text()
            new_password2 = self.entry_password2.get_text()
            new_officeinfo = self.entry_officeinfo.get_text()
            new_officeext = self.entry_officeext.get_text()
            new_homephone = self.entry_homephone.get_text()
            new_maingroup = self.combobox_maingroup.get_active_text()
            new_shell = self.entry_shell.get_text()
            new_uid = self.spinbutton_uid.get_value_as_int()
            new_expiry_date = self.checkbutton_user_expiration.get_active()

            bool_raise_error = False
            bool_set_fullname = False
            bool_set_password = False
            bool_set_officeinfo = False
            bool_set_officeext = False
            bool_set_homephone = False
            bool_set_maingroup = False
            bool_set_shell = False
            bool_set_uid = False
            bool_set_expirydate = False

            if not new_fullname == fullname:
                u.set_fullname(username, new_fullname)

            if not new_password1 == "":
                checkpass = u.check_password(new_password1, new_password2)
                if checkpass[0] == True:
                    bool_set_password = True
                else:
                    bool_raise_error = True
                    self.label_properties_error_msg.set_label(checkpass[1])
                    self.properties_error_window.show()

            if not new_officeinfo == officeinfo:
                bool_set_officeinfo = True

            if not new_officeext == officeext:
                bool_set_officeext = True

            if not new_homephone == homephone:
                bool_set_homephone = True

            if not new_maingroup == maingroup:
                bool_set_maingroup = True

            if not new_shell == shell:
                checkshell = u.check_shell(new_shell)
                if checkshell[0] == True:
                    bool_set_shell = True
                else:
                    bool_raise_error = True
                    self.label_properties_error_msg.set_label(checkshell[1])
                    self.properties_error_window.show()

            if not new_uid == uid:
                checkuid = u.check_uid(new_uid)
                if checkuid[0] == True:
                    bool_set_uid = True
                else:
                    bool_set_uid = False
                    bool_raise_error = True
                    self.label_properties_error_msg.set_label(checkuid[1])
                    self.properties_error_window.show()

            if bool_raise_error == False:
                if bool_set_fullname == True:
                    u.set_fullname(username, new_fullname)
                if bool_set_password == True:
                    u.set_password(username, new_password1)
                if bool_set_officeinfo == True:
                    u.set_officeinfo(username, new_officeinfo)
                if bool_set_officeext == True:
                    u.set_officeext(username, new_officeext)
                if bool_set_homephone == True:
                    u.set_homephone(username, new_homephone)
                if bool_set_maingroup == True:
                    u.set_group(username, new_maingroup)
                if bool_set_shell == True:
                    u.set_shell(username, new_shell)
                if bool_set_uid == True:
                    u.set_uid(username, new_uid)
                if new_expiry_date == True:
                    year = int("%04d" %
                               (self.calendar_user_expiration.get_date()[0]))
                    month = int(
                        "%02d" % (self.calendar_user_expiration.get_date()[1])) + 1
                    day = int("%02d" %
                              (self.calendar_user_expiration.get_date()[2]))
                    u.set_expiry_date(username, year, month, day)
                else:
                    if expiry_date[0] == True:
                        u.set_no_expiry_date(username)
                for i in self.user_groupliststore:
                    if i[3] == True:
                        if i[0] == True:
                            u.add_user_to_group(username, i[1])
                        else:
                            u.remove_user_from_group(username, i[1])
                self.user_properties_window.hide()
                self.on_checkbutton_showall_toggled(self)

    def on_button_user_properties_cancel_clicked(self, widget, data=None):
        self.user_properties_window.hide()

    def on_group_checkbox_toggled(self, widget, data=None):
        selectedgroup = self.user_grouplist.get_selection()
        self.user_groupliststore, iter = selectedgroup.get_selected()
        selectedgroupname = self.user_groupliststore.get_value(iter, 1)
        for i in self.user_groupliststore:
            if i[1] == selectedgroupname:
                i[3] = True
                if i[0] == 0:
                    i[0] = 1
                else:
                    i[0] = 0

    def on_checkbutton_visible_password_toggled(self, widget, data=None):
        state = self.entry_password1.get_visibility()
        if state == False:
            self.entry_password1.set_visibility(True)
            self.entry_password2.set_visibility(True)
        else:
            self.entry_password1.set_visibility(False)
            self.entry_password2.set_visibility(False)

    def on_checkbutton_user_expiration_toggled(self, widget, data=None):
        state = self.checkbutton_user_expiration.get_active()
        self.calendar_user_expiration.set_sensitive(state)

    def on_user_properties_window_delete_event(self, widget, event):
        self.user_properties_window.hide()
        return True

    def on_button_error_window_ok_clicked(self, widget, data=None):
        self.properties_error_window.hide()

    def on_properties_error_window_delete_event(self, widget, event):
        self.properties_error_window.hide()
        return True

    def on_button_deleteuser_ok_clicked(self, widget):
        u = SystemUsers()
        user = self.userlist.get_selection()
        self.userliststore, iter = user.get_selected()
        username = self.userliststore.get_value(iter, 1)
        delete_homedir = self.checkbutton_delete_user_homedir.get_active()
        u.del_user(username, delete_homedir)
        self.delete_user_window.hide()
        self.on_checkbutton_showall_toggled(self)

    def on_button_deleteuser_cancel_clicked(self, widget):
        self.delete_user_window.hide()

    def on_delete_user_window_delete_event(self, widget, event):
        self.delete_user_window.hide()
        return True

    def on_button_group_settings_close_clicked(self, widget):
        self.group_settings_window.hide()

    def on_group_settings_window_delete_event(self, widget, event):
        self.group_settings_window.hide()
        return True

    def on_button_group_properties_clicked(self, widget):
        g = SystemUsers()
        self.group_task_add_group = False
        group = self.grouplist.get_selection()
        self.groupliststore, iter = group.get_selected()
        groupname = self.groupliststore.get_value(iter, 0)
        self.group_properties_window.set_title(
            _("Group \"{0}\" properties").format(groupname))
        self.entry_groupname.set_sensitive(False)
        self.entry_groupname.set_text(groupname)
        self.spinbutton_gid.set_value(g.get_gid(groupname))
        self.groupmembersliststore.clear()
        for i in g.user_list(True):
            user = i[0]
            if g.user_in_group(user, groupname):
                member = True
            else:
                member = False
            self.groupmembersliststore.append([member, user, False])
        self.group_properties_window.show()

    def on_button_group_add_clicked(self, widget):
        g = SystemUsers()
        self.group_task_add_group = True
        self.entry_groupname.set_sensitive(True)
        self.entry_groupname.set_text('')
        self.group_properties_window.set_title(_("Add new group"))
        gidlist = []
        for i in grp.getgrall():
            gidlist.append(int(i[2]))
        maxgid = max(gidlist)
        if maxgid >= 65535:
            maxgid = 1000
        self.spinbutton_gid.set_value(maxgid + 1)
        self.groupmembersliststore.clear()
        for i in g.user_list(True):
            user = i[0]
            self.groupmembersliststore.append([False, user, False])
        self.group_properties_window.show()

    def on_button_group_delete_clicked(self, widget):
        g = SystemUsers()
        group = self.grouplist.get_selection()
        self.groupliststore, iter = group.get_selected()
        groupname = self.groupliststore.get_value(iter, 0)
        bool_del_group = True
        for i in g.user_list(True):
            if g.get_maingroup(i[0]) == groupname:
                bool_del_group = False
                break
        if bool_del_group == True:
            self.label_delete_group.set_text(
                _("You are about to delete the \"{0}\" group from your system. Are you sure you want to continue?").format(groupname))
            self.delete_group_window.show()
        else:
            self.label_cannot_delete_group.set_text(
                _("Group \"{0}\" cannot be deleted as it is the main group for user \"{1}\". If you want to delete group \"{0}\", you have to set the main group for user \"{1}\" to another group first.").format(groupname, i[0]))
            self.cannot_delete_group_window.show()

    def refresh_group_list(self):
        allgroups = grp.getgrall()
        self.groupliststore.clear()
        count = 0
        for i in allgroups:
            self.groupliststore.append([i[0]])

    def on_button_group_properties_ok_clicked(self, widget):
        g = SystemUsers()
        bool_raise_error = False
        if self.group_task_add_group == True:
            # Adding a group
            group = self.entry_groupname.get_text()
            gid = self.spinbutton_gid.get_value_as_int()
            checkgroupname = g.check_groupname(group)
            if checkgroupname[0]:
                checkgid = g.check_gid(gid)
                if checkgid[0]:
                    g.create_group(group, gid)
                else:
                    bool_raise_error = True
                    self.label_group_error_msg.set_label(checkgid[1])
                    self.group_properties_error_window.show()
            else:
                bool_raise_error = True
                self.label_group_error_msg.set_label(
                    g.check_groupname(group)[1])
                self.group_properties_error_window.show()
            if bool_raise_error == False:
                for i in self.groupmembersliststore:
                    if i[0] == True:
                        g.add_user_to_group(i[1], group)
                self.refresh_group_list()
                self.group_properties_window.hide()
        else:
            # Editing an existing group
            group = self.entry_groupname.get_text()
            gid = g.get_gid(group)
            new_gid = self.spinbutton_gid.get_value_as_int()
            if not new_gid == gid:
                checkgid = g.check_gid(new_gid)
                if checkgid[0]:
                    g.set_gid(group, new_gid)
                    self.group_properties_window.hide()
                else:
                    bool_raise_error = True
                    self.label_group_error_msg.set_label(checkgid[1])
                    self.group_properties_error_window.show()
            if bool_raise_error == False:
                for i in self.groupmembersliststore:
                    if i[2] == True:
                        if i[0] == False:
                            g.remove_user_from_group(i[1], group)
                        else:
                            g.add_user_to_group(i[1], group)
                self.refresh_group_list()
                self.group_properties_window.hide()

    def on_button_group_properties_cancel_clicked(self, widget):
        self.group_properties_window.hide()

    def on_group_properties_window_delete_event(self, widget, event):
        self.group_properties_window.hide()
        return True

    def on_groupmembers_checkbox_toggled(self, widget, data=None):
        selecteduser = self.groupmembers.get_selection()
        self.groupmembersliststore, iter = selecteduser.get_selected()
        selectedusername = self.groupmembersliststore.get_value(iter, 1)
        for i in self.groupmembersliststore:
            if i[1] == selectedusername:
                i[2] = True
                if i[0] == False:
                    i[0] = True
                else:
                    i[0] = False

    def on_button_group_error_ok_clicked(self, widget):
        self.group_properties_error_window.hide()

    def on_group_properties_error_window_delete_event(self, widget, event):
        self.group_properties_error_window.hide()
        return True

    def on_button_delete_group_ok_clicked(self, widget):
        g = SystemUsers()
        group = self.grouplist.get_selection()
        self.groupliststore, iter = group.get_selected()
        groupname = self.groupliststore.get_value(iter, 0)
        g.del_group(groupname)
        self.refresh_group_list()
        self.delete_group_window.hide()

    def on_button_delete_group_cancel_clicked(self, widget):
        self.delete_group_window.hide()

    def on_delete_group_window_delete_event(self, widget, event):
        self.delete_group_window.hide()
        return True

    def on_button_cannot_delete_group_ok_clicked(self, widget):
        self.cannot_delete_group_window.hide()

    def on_cannot_delete_group_window_delete_event(self, widget, event):
        self.cannot_delete_group_window.hide()
        return True

    def __init__(self):
        builder = Gtk.Builder()
        builder.set_translation_domain("gtkusersetup")
        if os.path.exists('gtkusersetup.ui'):
            builder.add_from_file('gtkusersetup.ui')
        elif os.path.exists('/usr/share/salixtools/gtkusersetup/gtkusersetup.ui'):
            builder.add_from_file(
                '/usr/share/salixtools/gtkusersetup/gtkusersetup.ui')

        #
        # Main window objects
        #
        self.window = builder.get_object('gtkusersetup')
        self.namecolumn = builder.get_object('namecolumn')
        self.logincolumn = builder.get_object('logincolumn')
        self.homedircolumn = builder.get_object('homedircolumn')
        self.userlist = builder.get_object('userlist')
        self.userliststore = builder.get_object('userliststore')
        self.checkbutton_showall = builder.get_object('checkbutton_showall')
        self.image_manageuser = builder.get_object('image_manageuser')
        self.logincolumn.set_title(_('Username'))
        self.namecolumn.set_title(_('Real name'))
        self.homedircolumn.set_title(_('Home directory'))

        self.on_checkbutton_showall_toggled(self)
        self.userlist.set_cursor(1)

        #
        # About dialog
        #
        self.aboutdialog = builder.get_object('aboutdialog')

        #
        # User properties/Add user window objects
        #
        self.notebook_userproperties = builder.get_object(
            'notebook_userproperties')
        self.user_properties_window = builder.get_object(
            'user_properties_window')

        # Account tab
        self.entry_login = builder.get_object('entry_login')
        self.entry_fullname = builder.get_object('entry_fullname')
        self.label_passwordheader = builder.get_object('label_passwordheader')
        self.entry_password1 = builder.get_object('entry_password1')
        self.entry_password2 = builder.get_object('entry_password2')
        self.checkbutton_visible_password = builder.get_object(
            'checkbutton_visible_password')

        # Contact tab
        self.entry_officeinfo = builder.get_object('entry_officeinfo')
        self.entry_officeext = builder.get_object('entry_officeext')
        self.entry_homephone = builder.get_object('entry_homephone')

        # Groups tab
        self.combobox_maingroup = builder.get_object('combobox_maingroup')
        self.groupliststore = builder.get_object('groupliststore')
        self.user_grouplist = builder.get_object('user_grouplist')
        self.user_groupliststore = builder.get_object('user_groupliststore')
        self.column_user_membership_checked = builder.get_object(
            'column_user_membership_checked')
        self.column_user_membership_group = builder.get_object(
            'column_user_membership_group')
        self.column_user_membership_gid = builder.get_object(
            'column_user_membership_gid')
        self.column_user_membership_checked.set_title(_('Member'))
        self.column_user_membership_group.set_title(_('Group'))
        self.column_user_membership_gid.set_title('GID')

        # Advanced tab
        self.label_homedir = builder.get_object('label_homedir')
        self.entry_homedir = builder.get_object('entry_homedir')
        self.entry_shell = builder.get_object('entry_shell')
        self.label_uid = builder.get_object('label_uid')
        self.spinbutton_uid = builder.get_object('spinbutton_uid')
        self.checkbutton_user_expiration = builder.get_object(
            'checkbutton_user_expiration')
        self.calendar_user_expiration = builder.get_object(
            'calendar_user_expiration')

        #
        # Error message for user properties window
        #
        self.properties_error_window = builder.get_object(
            'properties_error_window')
        self.button_error_window_ok = builder.get_object(
            'button_error_window_ok')
        self.label_properties_error_msg = builder.get_object(
            'label_properties_error_msg')

        #
        # Delete user message confirmation
        #
        self.delete_user_window = builder.get_object('delete_user_window')
        self.label_delete_user = builder.get_object('label_delete_user')
        self.checkbutton_delete_user_homedir = builder.get_object(
            'checkbutton_delete_user_homedir')

        #
        # Main group settings window
        #
        self.group_settings_window = builder.get_object(
            'group_settings_window')

        #
        # Group properties window
        #
        self.group_properties_window = builder.get_object(
            'group_properties_window')
        self.grouplist = builder.get_object('grouplist')
        self.label_groupname = builder.get_object('label_groupname')
        self.entry_groupname = builder.get_object('entry_groupname')
        self.spinbutton_gid = builder.get_object('spinbutton_gid')
        self.groupmembers = builder.get_object('groupmembers')
        self.groupmembersliststore = builder.get_object(
            'groupmembersliststore')

        #
        # Group properties error window
        #
        self.group_properties_error_window = builder.get_object(
            'group_properties_error_window')
        self.label_group_error_msg = builder.get_object(
            'label_group_error_msg')

        #
        # Delete group message confirmation
        #
        self.delete_group_window = builder.get_object('delete_group_window')
        self.label_delete_group = builder.get_object('label_delete_group')

        #
        # Cannot delete group window
        #
        self.cannot_delete_group_window = builder.get_object(
            'cannot_delete_group_window')
        self.label_cannot_delete_group = builder.get_object(
            'label_cannot_delete_group')
        # Connect all signals
        builder.connect_signals(self)

if __name__ == "__main__":
    app = GTKUserSetup()
    app.window.show()
    Gtk.main()
