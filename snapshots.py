import  wx

from wx.lib.statbmp  import GenStaticBitmap as StaticBitmap


class Snapshots(StaticBitmap):
    def __init__(self, parent, pos, getPicFn, clickFn):
        self.getPic = getPicFn
        self.click = clickFn
        StaticBitmap.__init__(self,parent, -1,self.getPic(), pos)
        
        self.tickSnap = wx.Timer(self,-1)
        self.frames = 10
        self.currentSleep = 1000./self.frames
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.tickSnap)
        self.Bind(wx.EVT_LEFT_UP,self.OnClick)
        
        self.tickSnap.Start(self.currentSleep, False)
    def OnClick(self,event):
        self.click()
        
    def OnTimer(self,event):
        self.SetBitmap(self.getPic())
        self.tickSnap.Start(self.currentSleep)
     
