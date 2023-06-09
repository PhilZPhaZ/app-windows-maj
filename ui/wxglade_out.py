import wx

class ChangeText(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ChangeText.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((325, 135))
        self.SetMinSize((325, 135))
        self.SetTitle("Changer le texte")

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
        # end wxGlade

# end of class ChangeText

class MyApp(wx.App):
    def OnInit(self):
        self.frame = ChangeText(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    changetext = MyApp(0)
    changetext.MainLoop()
