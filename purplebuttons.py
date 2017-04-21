import wx
from wx.lib.buttons import GenButton	
from colours import *

class PurpleButtons:
    def __init__(self, parent, font, clickedCallback, texts, default):
        self.texts = texts
        self.clickedCallback = clickedCallback 
        self.buttons = []
        btnId = 10000
        for text in self.texts:
            btn = GenButton(parent, id = btnId, label = text)
            btn.SetBezelWidth(0)
            btn.SetUseFocusIndicator(False)
            btn.SetBackgroundColour(basePurple)
            if text == default:
        		btn.SetForegroundColour(btnForegroundSel)
            else:			
               	btn.SetForegroundColour(btnForeground)
            btn.SetFont(font)
            btn.Bind(wx.EVT_LEFT_DOWN, self.OnDown)
            btn.Bind(wx.EVT_LEFT_UP, self.OnUp)
            btn.Bind(wx.EVT_LEFT_DCLICK, self.DoNothing)
            btn.Bind(wx.EVT_MOTION, self.DoNothing)
    	    self.buttons.append(btn)
            btnId+=1
    	self.current = default

    def SetBaseColours(self):
        for btn in self.buttons:
            btn.SetForegroundColour(btnForeground)
            btn.SetBackgroundColour(basePurple)
    
    def DoNothing(self, event):
    	pass

    def OnDown(self,event):
        self.SetBaseColours()
        for btn in self.buttons:
            if btn.GetId() == event.Id:
                btn.SetForegroundColour(btnForegroundSel)
                btn.CaptureMouse()	

    def OnUp(self,event):
        self.SetBaseColours()
        for btn in self.buttons:
            if btn.GetId() == event.Id:		
                btn.SetForegroundColour(btnForegroundSel)
                if btn.HasCapture():               	
                    btn.ReleaseMouse()
                label = btn.GetLabelText()
                if self.current != label:
                    self.current = label                	
                self.clickedCallback(btn.GetLabelText())

class PurpleButton(GenButton):
    def __init__(self,parent, label, pos, sz, font, clickedCallback, col = btnForeground, colSel = btnForegroundSel ):
        GenButton.__init__(self,parent,id=-1,pos = pos, size = sz, label = label)
        self.SetBezelWidth(0)
        self.SetUseFocusIndicator(False)
        self.SetBackgroundColour(basePurple)
        self.colSel = colSel
        self.col = col
        self.SetForegroundColour(col)
        self.SetFont(font)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self.DoNothing)
        self.Bind(wx.EVT_MOTION, self.DoNothing)
    	self.clickedCallback = clickedCallback

    def DoNothing(self, event):
    	pass

    def OnUp(self,event):
        self.SetForegroundColour(self.col)
        if(self.HasCapture()):        
		    self.ReleaseMouse()
        self.clickedCallback(self.GetLabelText())

    def OnDown(self,event):
        self.SetForegroundColour(self.colSel)
        self.CaptureMouse()

class PurpleState(GenButton):
    def __init__(self,parent, labelOn, labelOff, pos, sz, font, clickedCallback):
        GenButton.__init__(self,parent,id = -1,pos = pos, size = sz,label = labelOn)
        self.SetBezelWidth(0)
        self.SetUseFocusIndicator(False)
        self.SetBackgroundColour(basePurple)
        self.SetForegroundColour(btnForeground)
        self.SetFont(font)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self.DoNothing)
        self.Bind(wx.EVT_MOTION, self.DoNothing)
        self.labelOn = labelOn
        self.labelOff = labelOff
        self.clickedCallback = clickedCallback

    def DoNothing(self, event):
	    pass

    def OnUp(self,event):
        if(self.HasCapture()):        
            self.ReleaseMouse()
        self.SetForegroundColour(btnForeground)
        label = self.GetLabelText()
        if label == self.labelOn:
		    self.SetLabel(self.labelOff)
        else:
            self.SetLabel(self.labelOn)
        self.clickedCallback(self.GetLabelText())

    def OnDown(self,event):
        self.SetForegroundColour(btnForegroundSel)
        self.CaptureMouse()
        
