import wx,vlc,sys

class playerGui(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title="YouTube Player v0.1", size=(350,200)) 
		self.ctrlspanel = wx.Panel(self)
		self.vidpanel=wx.Panel(self)
		self.vidpanel.SetBackgroundColour(wx.BLACK)
		self.boxsizer=wx.BoxSizer(wx.VERTICAL)
		self.playb = wx.Button(self.ctrlspanel,wx.ID_DEFAULT,"&Play")
		self.playb.Bind(wx.EVT_BUTTON, self.OnPlay)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.boxsizer.Add(self.playb,0,wx.ALL,5)
		self.muteb = wx.Button(self.ctrlspanel,wx.ID_DEFAULT,"&Mute")
		self.muteb.Bind(wx.EVT_BUTTON, self.OnMute)
		self.boxsizer.Add(self.muteb,0,wx.ALL,5)
		self.timesliderlabel = wx.StaticText(self.ctrlspanel,-1,"time ")
		self.timeslider = wx.Slider(self.ctrlspanel, -1, 0, 0, 1000)
		self.timeslider.SetRange(0, 1000)
		self.boxsizer.Add(self.timesliderlabel,0,wx.ALL,5)
		self.boxsizer.Add(self.timeslider,0,wx.ALL,5)
		self.volumelabel = wx.StaticText(self.ctrlspanel,-1,"Volume ")
		self.volslider = wx.Slider(self.ctrlspanel, -1, 0, 0, 100, size=(100, -1))
		self.Bind(wx.EVT_SLIDER, self.OnSetVolume, self.volslider)
		self.detailslabel = wx.StaticText(self.ctrlspanel,-1,"&Video details ")
		self.detailslist = wx.ListBox(self.ctrlspanel,-1)
		self.detailslist.Bind(wx.EVT_CONTEXT_MENU, self.onContext1)
		self.boxsizer.Add(self.detailslabel,0,wx.ALL,5)
		self.boxsizer.Add(self.detailslist,0,wx.ALL,5)
		self.ctrlspanel.SetSizer(self.boxsizer)
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.vidpanel, 1, flag=wx.EXPAND)
		sizer.Add(self.ctrlspanel, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, border=10)
		self.SetSizer(sizer)
		self.SetMinSize((350, 300))
		self.Instance = vlc.Instance()
		self.player = self.Instance.media_player_new()
	def onContext1(self,something):
		if not hasattr(self, "popupID1"):
			self.popupID1 = wx.NewId()
			self.Bind(wx.EVT_MENU, self.Copydetail, id=self.popupID1)
		rmenu = wx.Menu()
		copyDetails = rmenu.Append(self.itemOneId, "Copy to the clipboard.")
		self.PopupMenu(rmenu)
		rmenu.Destroy()
	def Copydetail(self,detail):
		self.detailname = self.detailslist.GetStringSelection()
		clipboard.copy(self.detailname)
	def Load(self,url,title):
		self.OnStop(None)
		self.Media = self.Instance.media_new(url)
		self.player.set_media(self.Media)
		self.videoname = title
		self.SetTitle(self.videoname+" YouTube Player v0.1")
		handle = self.vidpanel.GetHandle()
		if sys.platform.startswith('linux'): 
			self.player.set_xwindow(handle)
		elif sys.platform == "win32": 
			self.player.set_hwnd(handle)
		elif sys.platform == "darwin":
			self.player.set_nsobject(handle)
		if self.player.play() == -1:
			speak.alert("Error:","Unable to play the audio")
		self.volslider.SetValue(self.player.audio_get_volume())
	def OnPlay(self, event):
		if self.player.is_playing()==0:
			self.timer.Start()
			self.player.pause()
			self.playb.SetLabel("&Pause")
		elif self.player.is_playing()==1:
			self.timer.Stop()
			self.player.pause()
			self.playb.SetLabel("&Play")
	def OnPause(self, event):
		self.player.pause()
	def OnStop(self,event):
		self.player.stop()
		self.timeslider.SetValue(0)
		self.timer.Stop()
	def OnTimer(self, event):
		length = self.player.get_length()
		self.timeslider.SetRange(-1, length)
		time = self.player.get_time()
		self.timeslider.SetValue(time)
	def OnMute(self,event):
		is_mute = self.player.audio_get_mute()
		self.player.audio_set_mute(not is_mute)
		if is_mute==0:
			self.muteb.SetLabel("Un&mute")
		elif is_mute==1:
			self.muteb.SetLabel("&Mute")
		self.volslider.SetValue(self.player.audio_get_volume() / 2)
	def OnSetVolume(self, event):
		volume = self.volslider.GetValue() * 2
		if self.player.audio_set_volume(volume) == -1:
			speak.alert("Error:","Failed to set volume")
	def OnClose(self,event):
		self.OnStop(None)
		self.Hide()