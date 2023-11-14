import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib
import os
import sys
import _thread
import time


def add_notification(text):
    # do something with the notification here
    print(text)

class NotificationFetcher(dbus.service.Object):
    @dbus.service.method("org.freedesktop.Notifications",
                         in_signature='susssasa{sv}i',
                         out_signature='u')
    def Notify(self, app_name, notification_id, app_icon,
               summary, body, actions, hints, expire_timeout):
        text = f"({app_name}): {summary} {body}".strip()
        add_notification(text)
        return 0

    @dbus.service.method("org.freedesktop.Notifications", in_signature='', out_signature='as')
    def GetCapabilities(self):
        return ("body")

    @dbus.service.signal('org.freedesktop.Notifications', signature='uu')
    def NotificationClosed(self, id_in, reason_in):
        pass

    @dbus.service.method("org.freedesktop.Notifications", in_signature='u', out_signature='')
    def CloseNotification(self, id):
        pass

    @dbus.service.method("org.freedesktop.Notifications", in_signature='', out_signature='ssss')
    def GetServerInformation(self):
        return ("statnot-term", "", "0.0.0", "1")

def message_thread(dummy):
    while True:
        time.sleep(1)


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("org.freedesktop.Notifications", session_bus)
    nf = NotificationFetcher(session_bus, '/org/freedesktop/Notifications')
    
    context = GLib.MainLoop().get_context()
    _thread.start_new_thread(message_thread, (None,))

    while True:
        context.iteration(True)
