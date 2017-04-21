import wx
from colours import *
from purplebuttons import PurpleButton
from wx.lib.embeddedimage import PyEmbeddedImage
import wx.lib.stattext as ST
(screenWidth,screenHeight) = (480, 320)
(boxWidth,boxHeight) = (320, 120)

btnWidth = 60
btnHeight = 18
btnSpaceX = 20
btnSpaceY = 10
borderMax = 60
borderMin = 20
borderTxt = 30
fontSz = 12
radius = 15

class Message(wx.Frame):
    # text is text to display initially
    # buttons are buttons to display along the bottom
    # onClickFn is a callback for when a button is clicked onClickFn( thisFrame, btnText)
    def __init__(self, text, buttons, onClickFn):
        style = ( wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.NO_BORDER | wx.FRAME_SHAPED  )
        
        wx.Frame.__init__(self, None, -1,'purple message', style = style )
        self.SetSize((boxWidth, boxHeight))
        
        
        
        self.SetPosition(((screenWidth-boxWidth)/2,(screenHeight-boxHeight)/2))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_WINDOW_CREATE, self.SetRoundShape)
        
        self.bmp = self.GetRoundShape( boxWidth,boxHeight, radius ) 
        
        font = self.GetFont()
        font.SetPointSize(fontSz)
        self.SetFont(font)
        
        static = ST.GenStaticText(self, label = text, pos = (borderMin, borderTxt), size = (boxWidth-2*borderMin, boxHeight- btnHeight - btnSpaceY-borderTxt), style = wx.ALIGN_CENTER | wx.ALIGN_CENTER_VERTICAL)
        static.SetFont(font)
        static.SetForegroundColour(btnForegroundSel)
        static.SetBackgroundColour(btnPurple)
        self.clickedCallback = onClickFn
        
        totalBtnWidth = len(buttons)*(btnWidth+btnSpaceX) - btnSpaceX
        border = borderMax
        while (totalBtnWidth > (boxWidth-2*border)) and border > borderMin:
            border = border - 10
        if totalBtnWidth > (boxWidth-2*border):
            raise Exception('Too many buttons')
        xStart = border + btnWidth/2
        xEnd = boxWidth - border - btnWidth/2
        xDist = (xEnd-xStart)/(len(buttons)-1)
        
        btnY = boxHeight-btnHeight-btnSpaceY
       
        btnX = xStart - btnWidth/2
        for t in buttons:
            b = PurpleButton(self, t, (btnX,btnY), (btnWidth, btnHeight), font, self.OnClicked, btnForegroundSel, btnForeground)
            btnX = btnX+xDist
        self.Show(True)


    def SetRoundShape(self, event=None):
        w, h = self.GetSizeTuple()
        self.SetShape(self.bmp )

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc = wx.GCDC(dc)
        w, h = self.GetSizeTuple()
        r = radius
        dc.SetPen( wx.Pen(btnForegroundSel, width = 3 ) )
        dc.SetBrush( wx.Brush((94,0,100)) )
        dc.DrawRoundedRectangle( 0,0,w,h,r )

    def GetRoundBitmap( self, w, h, r ):
        maskColor = (0,0,0)
        shownColor = btnPurple
        b = wx.EmptyBitmap(w,h)
        dc = wx.MemoryDC(b)
        dc.SetBrush(wx.Brush(maskColor))
        dc.DrawRectangle(0,0,w,h)
        dc.SetBrush(wx.Brush(shownColor))
        dc.SetPen(wx.Pen(shownColor))
        dc.DrawRoundedRectangle(0,0,w,h,r)
        dc.SelectObject(wx.NullBitmap)
        b.SetMaskColour(maskColor)
        return b

    def GetRoundShape( self, w, h, r ):
        return wx.RegionFromBitmap( self.GetRoundBitmap(w,h,r) )        
    
    def OnClicked( self, label):
        self.clickedCallback(self,label)
        self.Close()


def clicked(m, l) : print(l)

if __name__ == '__main__':

        app = wx.PySimpleApp()
        kbd = Message('hello world!  This is a bit longer and it\n keeps getting longer', ['OK', 'Maybe','Cancel'], clicked)
        kbd.Show(True)
        app.MainLoop()