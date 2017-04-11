import wx
from wx.lib.buttons import GenButton
import wx.lib.agw.gradientbutton as GB
from lr import *
from purplebuttons import *
from snapshots import *
from colours import *
from info import *

fontSz =12
btnHeight = 30
btnTopWdth = 80
btnBottomWdth = 120
btnRightWidth = 120

picWidth = 320
btnTopSpace = 4
borderSz = 10
screenWidth = 480
screenHeight = 320

leftX = borderSz
rightX = screenWidth - 2*borderSz - btnRightWidth 
bottomY = screenHeight - btnHeight - borderSz
defaultQuality = 100

def rightY( p ):
	first = 2*borderSz + btnHeight
	return first + p * (btnHeight)

topTexts = ["Photo", "Timelapse", "Video", "Sound", "Preview"]

class Main(wx.Frame):
    def SetInfoBox(self):
    	self.info = InfoBox(self.panel,(leftX, bottomY + 7), (picWidth, btnHeight),self.font, ['Tap picture to snap', ''], True)

    def SetRightPhoto(self):
        sz = (btnRightWidth, btnHeight)
        # Basic
        resolution = LRList(self.panel, 'Resolution', 
            ['2mp', '8mp', 'hd1080', 'hd720', 'vga'],
            (rightX, rightY(0)),sz,self.font,
            self.OnPhotoRes)
        fixCurrent = PurpleState(self.panel, 'Measure&Fix', 'Release', 
            (rightX, rightY(1)),sz,self.font,
            self.OnPhotoFix)
        rotation = LRList(self.panel, 'Rotation', 
            ['0', '90', '180', '270'],
            (rightX, rightY(3)),sz,self.font,
            self.OnPhotoRotation)
        resetAll = PurpleButton(self.panel, 'Reset all', 
            (rightX,rightY(5)), sz, self.font, self.OnResetPhoto)    
        # Effects
        wb = LRList(self.panel, 'Wh Balance', #auto-white-balance PiCamera.AWB_MODES
            ['auto','sunlight','cloudy','shade','tungsten','fluorescent','incandescent','flash','horizon'],
            (rightX, rightY(0)),sz,self.font,
            self.OnWhiteBalance)
        exp = LRList(self.panel, 'Exp Mode', #exposure_mode (PiCamera.EXPOSURE_MODES)
            ['auto','night','nightpreview','backlight','spotlight','sports','snow',
		    'beach','verylong','fixedfps','antishake','fireworks'],
		    (rightX, rightY(1)),sz,self.font,
            self.OnExposureMode)
        imageEffect = LRList(self.panel, 'Image Effect', #image_effect (PiCamera.IMAGE_EFFECTS)
            ['none','negative','solarize','sketch','denoise','emboss','oilpaint','hatch',
		        'gpen','pastel','watercolor','film','blur','saturation','colorswap','washedout',
		        'posterise','colorpoint','colorbalance','cartoon','deinterlace1','deinterlace2'],
		    (rightX, rightY(2)),sz,self.font,
            self.OnImageEffect)
            
        #colour_effects
	    #       black and white (128,128)
	    #       sepia 100:150 
        colourEffect = LRList(self.panel, 'Colour Effect', 
            ['none','grayscale','sepia'],
		    (rightX, rightY(3)),sz,self.font,
            self.OnColourEffect)
        denoise = PurpleState(self.panel, 'Denoise', 'Noisy', 
            (rightX, rightY(4)),sz,self.font,
            self.OnDenoise) 
        stabilisation = PurpleState(self.panel, 'Stabilise', 'Unstable', 
            (rightX, rightY(5)),sz,self.font,
            self.OnStabilisation)        
        # Details    
        iso = LRList(self.panel, 'iso', 
            ['auto','100', '200', '320', '400', '500', '640', '800'],
		    (rightX, rightY(0)),sz,self.font,
            self.OnIso)
        shutter = LRList(self.panel, 'Shutter Sp', 
            ['auto','1/500','1/250','1/125','1/60','1/30','1/15','1/8','1/4','1/2','1','2','4','8','15','30','60','120','300','600', '1200'],
		    (rightX, rightY(1)),sz,self.font,
            self.OnShutterSpeed)
        quality = LRVal(self.panel, 'Quality', 50, 0, 100, 
            (rightX,rightY(2)), sz, self.font, 1, 
            self.OnQuality)
        brightness = LRVal(self.panel, 'Brightness', 50, 0, 100, 
            (rightX,rightY(3)), sz, self.font, 1,
            self.OnBrightness)
        contrast = LRVal(self.panel, 'Contrast', 0, -100, 100, 
            (rightX,rightY(4)), sz, self.font, 1,
            self.OnContrast)
        sharpness = LRVal(self.panel, 'Sharpness', 0, -100, 100, 
            (rightX,rightY(5)), sz, self.font, 1,
            self.OnSharpness)
        saturation = LRVal(self.panel, 'Saturation', 0, -100, 100, 
            (rightX,rightY(6)), sz, self.font, 1,
            self.OnSaturation)
        self.photoRight = {
            'Basic' : [resolution, fixCurrent,rotation, resetAll],
            'Effects' : [wb,exp,imageEffect,colourEffect, denoise, stabilisation],
            'Details' : [iso, shutter, quality, brightness, contrast, sharpness, saturation]}

                                          
    def SetTopButtons(self):
        self.topButtons = PurpleButtons(self.panel, self.font, self.OnClickedTop, topTexts, topTexts[0])
        self.closeButton = PurpleButton(self.panel, 'X', 
        (screenWidth - 20,borderSz),(10, btnHeight),
        self.font, self.OnClickedExit)
        
        for i in range(0,5):
            b = self.topButtons.buttons[i]
            b.SetPosition((i*(btnTopWdth+btnTopSpace),borderSz))
            b.SetSize((btnTopWdth,btnHeight))
    
    def SetBottomButtons(self):
        self.photoSettings = LRList(self.panel, 'Settings',
            ['Basic', 'Effects', 'Details'], 
            (rightX,bottomY),(btnBottomWdth, btnHeight),self.font, self.OnPhotoSettings)
        
        self.bottomRow = { 
		    'Photo' : [self.photoSettings],
            'Video' : [self.photoSettings],
            'Timelapse' : [self.photoSettings],
            'Sound' : [],
            'Other' : []}

    def UpdateBottom(self, top):
        for k in self.bottomRow:
            for b in self.bottomRow[k]: b.Show(False)
        for b in self.bottomRow[top]: b.Show(True)
        self.UpdateRight()
        self.Layout()
	    
    def UpdateRight( self ):
        if(self.photoSettings.IsShown()):
            current = self.photoSettings.GetLabel()
            for k in self.photoRight:
                for j in self.photoRight[k]: 
                    j.Show(k==current)
        else:
            for k in self.photoRight:
                for j in self.photoRight[k]: 
                    j.Show(False)
        
    def __init__(self):
        wx.Frame.__init__(self,None, id = 0, pos=(0,0), size=(screenWidth,screenHeight),style = wx.STAY_ON_TOP)
        
        self.SetBackgroundColour(basePurple)
        
        self.font = self.GetFont()
        self.font.SetPointSize(fontSz)
        self.SetFont(self.font)
        
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(basePurple)
        self.SetTopButtons()
        self.currentTop = 'Photo'
        
        self.SetBottomButtons()
        self.SetRightPhoto()
        self.UpdateBottom(self.currentTop)
        self.SetInfoBox()
        self.Show(True)

    def EmptyHandler(self, label):
        pass

    def OnPhotoSettings(self, label):
        self.UpdateRight()
        print('clicked ' + label)

    def OnVideoRes(self, label):
        print('clicked ' + label)

    def OnStartTimelapse(self, label):
        print('clicked ' + label)

    def OnVideoStartStop(self, label):
        print('clicked ' + label)
    def OnAudioStartStop(self, label):
        print('clicked ' + label)
        
    def OnPhotoRes(self,label):
        print('clicked ' + label)
    def OnPhotoFix(self,label):
        print('clicked ' + label)
    def OnPhotoRotation(self,label):
        print('clicked ' + label)
    def OnResetPhoto(self,label):
        print('clicked ' + label)
        for k in self.photoRight:
            for v in self.photoRight[k]: 
                if(hasattr(v,'reset')): v.reset()
    def OnWhiteBalance(self,label):
        print('clicked ' + label)
    def OnExposureMode(self,label):
        print('clicked ' + label)
    def OnImageEffect(self,label):
        print('clicked ' + label)
    def OnColourEffect(self,label):
        print('clicked ' + label)
    def OnDenoise(self,label):
        print('clicked ' + label)
    def OnStabilisation(self,label):
        print('clicked ' + label)
    def OnIso(self,label):
        print('clicked ' + label)
    def OnShutterSpeed(self,label):
        print('clicked ' + label)
    def OnQuality(self,label):
        print('clicked ' + label)
    def OnBrightness(self,label):
        print('clicked ' + label)
    def OnContrast(self,label):
        print('clicked ' + label)
    def OnSharpness(self,label):
        print('clicked ' + label)
    def OnSaturation(self,label):
        print('clicked ' + label)
    
    def OnClickedTop(self, label):
        self.currentTop = label
        self.UpdateBottom(label)
        if label == 'Photo':
            self.info.SetValues(['Tap picture to snap', ''])
        elif label == 'Video':
            self.info.SetValues(['Tap picture to start recording', ''])
        elif label == 'Timelapse':
            self.info.SetValues(['Tap picture to start timelapsing', ''])
        elif label == 'Sound':
            self.info.SetValues(['Tap middle of screen to start recording', 'another', 'and yet more', 'and last',''], True)
        else:
            self.info.SetValues([])
        print('clicked ' + label)
    def OnClickedExit(self, label):
        quit()
app = wx.App(False)
frame = Main()
app.MainLoop()
