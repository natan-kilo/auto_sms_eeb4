from win10toast import ToastNotifier

def makeNotification(title, text, icon=None, duration=2):
    toaster = ToastNotifier()
    toaster.show_toast(title=title, msg=text, icon_path=icon, duration=duration)
