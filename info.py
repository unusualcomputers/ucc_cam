import wx
import wx.lib.stattext as ST
from colors import *

class InfoBox(ST.GenStaticText):
    def __init__(self, parent, pos, size,font, values, rotateOnce = True):
        ST.GenStaticText.__init__(self,parent,-1,"", pos, size, style = wx.ALIGN_LEFT |  wx.ST_NO_AUTORESIZE)
        self.btnTimer = wx.Timer(self,-1)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.btnTimer)
        self.SetFont(font)
        self.SetValues(values)
        self.SetBackgroundColour(basePurple)
        self.SetForegroundColour(btnForegroundSel)
        self.rotateOnce = rotateOnce

    def SetValues(self, values, rotateOnce = True):
        self.rotateOnce = rotateOnce
        self.values = values
        if len(self.values) == 0:
            self.current = -1
            self.SetLabel("")
            self.btnTimer.Stop()
        else:
            self.current = 0
            self.SetLabel(self.values[0])
        if len(self.values): self.btnTimer.Start(3000)          
        
    def OnTimer(self,event):
        self.current += 1
        if self.current == len(self.values): 
            if self.rotateOnce: 
                self.current -= 1	
                self.btnTimer.Stop()
            else:
                self.current = 0
        self.SetLabel(self.values[self.current])



