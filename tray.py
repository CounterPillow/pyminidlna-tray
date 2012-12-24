#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import dbus
from PyQt4 import QtGui, QtCore
from PyKDE4.kdeui import *

class DLNATrayApp():
    
    
    def __init__(self):
        self.initDBUS()
        self.initUI()
    
    def initUI(self):
        self.tray = QtGui.QSystemTrayIcon(KIcon("applications-multimedia"))
        self.m = QtGui.QMenu()
        
        self.control = self.m.addAction("", self.toggleMediaSharing)
        if self.isMiniDLNARunning():
            self.control.setIcon(KIcon("media-playback-stop")) 
            self.control.setText("Disable media sharing")
        else:
            self.control.setIcon(KIcon("media-playback-start"))
            self.control.setText("Enable media sharing")
        
        self.m.addAction(KIcon("window-close"), 'Quit', QtCore.QCoreApplication.instance().quit) 
        self.tray.setContextMenu(self.m)
        self.tray.show()

    def initDBUS(self):
        self.bus = dbus.SystemBus()
        self.systemd = self.bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        self.interface = dbus.Interface(self.systemd, 'org.freedesktop.systemd1.Manager')

    def toggleMediaSharing(self):
        if self.isMiniDLNARunning():
            self.stopMediaSharing()
            self.control.setIcon(KIcon("media-playback-start"))
            self.control.setText("Enable media sharing")
        
        else:
            self.startMediaSharing()
            self.control.setIcon(KIcon("media-playback-stop"))
            self.control.setText("Disable media sharing")


    def startMediaSharing(self):
        print("Starting...")
        self.interface.StartUnit("minidlna.service", "replace")

    def stopMediaSharing(self):
        print("Stopping...")
        self.interface.StopUnit("minidlna.service", "replace")

    def isMiniDLNARunning(self):
        try:
            unit_object = self.interface.GetUnit("minidlna.service")
            unit = self.bus.get_object('org.freedesktop.systemd1', unit_object)
            interface = dbus.Interface(unit, 'org.freedesktop.DBus.Properties')
            if interface.Get('org.freedesktop.systemd1.Unit', 'ActiveState') == 'active':
                return True     # loaded and running
            else:
                return False    # loaded but not running

        except dbus.exceptions.DBusException:
            return False    # not loaded


def main():
    app = QtGui.QApplication(sys.argv)
    dta = DLNATrayApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
