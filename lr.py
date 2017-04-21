import wx
import wx.lib.stattext as ST
from colours import *

class LRBase(ST.GenStaticText):
    def __init__(self, parent, pos, size,font, title, initVal, callback):
        ST.GenStaticText.__init__(self,parent,-1,title, pos, size, style = wx.ALIGN_CENTER |  wx.ST_NO_AUTORESIZE)
        self.SetFont(font)
        self.SetLabel(title)
        self.SetBackgroundColour(basePurple)
        self.SetForegroundColour(btnForeground)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDbl)

        self.btnTimer = wx.Timer(self,-1)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.btnTimer)
        self.ldown = False
        self.rdown = False
        self.resetClick = False
        self.infoClick = False
        self.isTitle = True
        self.initVal = initVal
        self.title= title
        self.currentVal = title
        self.callback = callback
    def Press(self, isLeft):
        if(self.isTitle):
            self.isTitle = False
            self.SetLabel(self.initVal)
        elif(isLeft):
            self.SetLabel(self.Prev())
        else:
            self.SetLabel(self.Next())
    def OnDbl(self,ev):
        x = ev.GetX()
        (cx,cy) = self.GetSize()
        if(x<self.szLetter or x>(cx-self.szLetter)):
            self.OnLeftUp(ev)
        else:
            self.currentVal = self.title
            self.reset()
        
    def OnLeftDown(self,ev):
        if(ev.ButtonDClick()): return
        self.currentSpeed = 300
        x = ev.GetX()
        (cx,cy) = self.GetSize()
        if(x<self.szLetter): 
            self.isLeft = True
            self.ldown = True
            self.btnTimer.Start(500)
        elif(x>(cx-self.szLetter)):            
            self.isLeft = False
            self.rdown = True
            self.btnTimer.Start(500)
        else:
            self.currentVal = self.GetLabel()
            self.SetLabel(self.title)
            self.infoClick = True
            self.btnTimer.Start(3000)
            
    def OnLeftUp(self,ev):
        self.currentSpeed = 300
        self.btnTimer.Stop()
        self.ldown = False
        self.rdown = False
        self.resetClick = False
        self.infoClick = False
        x = ev.GetX()
        (cx,cy) = self.GetSize()
        if(x<self.szLetter): self.Press(True)
        elif(x>(cx-self.szLetter)): self.Press(False)
        else: self.SetLabel(self.currentVal)
	if self.callback != None: self.callback(self.GetLabel())
        
    def OnTimer(self,event):
        if self.infoClick:
            self.btnTimer.Stop()
            self.btnTimer.Start(2000)
            self.resetClick = True
            self.infoClick = False
            self.Refresh()
            return
        if self.resetClick:
            self.currentVal = self.title
            self.resetClick = False
            self.Refresh()
            self.btnTimer.Stop()
            self.reset()
            return    
        if self.currentSpeed > 10:
            self.currentSpeed -= 10
               
        self.Press(self.isLeft)
        self.btnTimer.Start(self.currentSpeed)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)
    
    def Draw(self, dc):
        (clientW, clientH) = self.GetClientSize()
        if not clientW or not clientH:
            return
        dc.SetFont(self.font)
        backColour = self.GetBackgroundColour()
        backBrush = wx.Brush(backColour, wx.SOLID)
        dc.SetBackground(backBrush)
        dc.Clear()
        dc.SetTextForeground(self.GetForegroundColour())
        dc.SetFont(self.GetFont())
        currentText = self.GetLabel()
        (btnW, btnH) = dc.GetTextExtent('< ')
        self.szLetter = 2*btnW
        (textW, textH) = dc.GetTextExtent( currentText )
        topB = (clientH-btnH)/2
        lftBtnPos = (0,topB)
        rghtBtnPos = (clientW-btnW,topB)
        
        textPos = ((clientW-textW)/2,(clientH-textH)/2)
        if(self.ldown):
            dc.SetTextForeground(btnForegroundSel)
        else:
            dc.SetTextForeground(btnForeground)
        dc.DrawText('< ', lftBtnPos[0], lftBtnPos[1])
        if(self.rdown):
            dc.SetTextForeground(btnForegroundSel)
        else:
            dc.SetTextForeground(btnForeground)
        dc.DrawText(' >', rghtBtnPos[0], rghtBtnPos[1])
        if(self.ldown or self.rdown or self.infoClick):
            dc.SetTextForeground(btnForegroundSel)
        else:
            dc.SetTextForeground(btnForeground)
        dc.DrawText(currentText, textPos[0], textPos[1])
        
    def OnEraseBackground(self, event):
        """ Handles the wx.EVT_ERASE_BACKGROUND event for CustomCheckBox. """
        # This is intentionally empty, because we are using the combination
        # of wx.BufferedPaintDC + an empty OnEraseBackground event to
        # reduce flicker
        pass
    

class LRVal(LRBase):
    def __init__(self, parent, title, start, smallest, largest, pos, size, font, increment = 1, callback = None):
        self.increment = increment
        self.current = start
        self.font = font
        self.smallest = smallest
        self.largest = largest
        self.start = start
        LRBase.__init__(self,parent, pos, size, font, title, self.formatVal(), callback)

    def reset(self):
        self.current = self.start
        self.SetLabel(self.title)
        self.isTitle = True
        
    def formatVal(self):
        return str(self.current)
            
    def Next(self):
        self.current += self.increment
        if(self.current > self.largest):
            self.current = self.smallest
        return self.formatVal()

    def Prev(self):
        self.current -= self.increment
        if(self.current < self.smallest):
            self.current = self.largest
        return self.formatVal()
   

class LRTime(LRBase):
    def __init__(self, parent, title, perSecond, pos,size,font,callback = None):
        self.current = 0
        self.currentSpeed = 300
        if(perSecond):
            self.increment = 1
        else:
            self.increment = 60
        self.font = font
        LRBase.__init__(self,parent, pos, size, font, title, self.formatTime(), callback)
        
    def reset(self):
        self.current = 0
        self.SetLabel(self.title)
        self.isTitle = True
        
    def formatTime(self):
        s = self.current
        d = s / (24*3600)
        s = s - d * (24 * 3600)
        h = s/3600
        s = s - h*3600
        m = s/60
        s = s - m * 60
        if(self.increment == 1):
            if( d > 0):
                return '%02dd %02dh %02dm %02ds' % (d,h,m,s)
            elif (h > 0):
                return '%02dh %02dm %02ds' % (h,m,s)
            else:
                return '%02dm %02ds' % (m,s)
        else:
            if( d > 0):
                return '%02dd %02dh %02dm' % (d,h,m)
            else:
                return '%02dh %02dm' % (h,m)
            
    def Next(self):
        self.current += self.increment
        return self.formatTime()

    def Prev(self):
        self.current -= self.increment
        if(self.current < 0):
            self.current = 0
        return self.formatTime()
   




class LRList(LRBase):
    def __init__(self, parent, title, options,pos,size,font, callback = None):
        self.current = 0
        self.options = options
        self.font = font
	
        LRBase.__init__(self,parent, pos, size, font, title, self.options[self.current], callback)

    def reset(self):
        self.current = 0
        self.SetLabel(self.title)
        self.isTitle = True

    def Next(self):
        self.current += 1
        if self.current >= len(self.options):
            self.current = 0
        return self.options[self.current]

    def Prev(self):
        if(self.current == 0):
            self.current = len(self.options)-1
        else:
            self.current -= 1

        return self.options[self.current]
    
