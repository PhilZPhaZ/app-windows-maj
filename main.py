import time
import threading
import keyboard
import win32clipboard
import wx

class ClipboardWatcher:
    def __init__(self):
        self.setup_hotkey()

    def get_clipboard_data(self) -> str:
        # on ouvre le clipboard
        win32clipboard.OpenClipboard()
        data = None
        # on si on a rien selectionner ça evite les erreurs
        try:
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
                data = win32clipboard.GetClipboardData()
        finally:
            win32clipboard.CloseClipboard()
        return data

    def copy_to_clipboard(self, data) -> None:
        # on copie les données transformées dans le presse papier
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(data)
        win32clipboard.CloseClipboard()

    def modify_data(self, data: str) -> str:
        # methode permettant de modifier le texte
        sentences = data.split('. ')
        return '. '.join(sentence.capitalize() for sentence in sentences)

    def get_data(self) -> None:
        # on recupere le texte du presse papier
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()

        keyboard.press_and_release('ctrl+x')

        # il faut un delai sinon ça ne marche pas
        time.sleep(0.01)

        # si on a pas de données, on ne colle pas le texte modifié
        if data := self.get_clipboard_data():
            self.copy_to_clipboard(self.modify_data(data))
            keyboard.press_and_release('ctrl+v')

    def handle_hotkey(self) -> None:
        self.get_data()

    def setup_hotkey(self) -> None:
        keyboard.add_hotkey('f8', self.handle_hotkey)


class ClipboardWatcherThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.clipboard_watcher = ClipboardWatcher()
        self.stop_event = threading.Event()

    def run(self):
        print('thread running')

    def stop(self):
        print('thread stopping')
        self.stop_event.set()


class ChangeText(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ChangeText.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((325, 135))
        self.SetMinSize((325, 135))
        self.SetTitle("Changer le texte")

        # Ici on relie la fermeture de l'application a une methode pour fermer le thread
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Creation de la fenetre
        self.panel = wx.Panel(self, wx.ID_ANY)

        label_sizer = wx.BoxSizer(wx.VERTICAL)

        label_position_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_sizer.Add(label_position_sizer, 0, wx.EXPAND, 0)

        label = wx.StaticText(self.panel, wx.ID_ANY, "Pour modifier le texte, il faut selectionner le texte et appuyer sur la touche F8", style=wx.ALIGN_CENTER_HORIZONTAL)
        label.SetMinSize((361, 100))
        label.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        label_position_sizer.Add(label, 1, wx.ALL, 0)

        self.panel.SetSizer(label_sizer)

        self.Layout()

        # Ici on instancie la classe pour faire tourner sur un autre thread
        self.clipboard_thread = ClipboardWatcherThread()

        # Démarrez le thread
        self.clipboard_thread.start()

    def OnClose(self, event):
        # On ferme le thread
        self.clipboard_thread.stop()

        event.Skip()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = ChangeText(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    changetext = MyApp(0)
    changetext.MainLoop()