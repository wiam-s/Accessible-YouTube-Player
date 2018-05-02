# -*- coding: utf-8 -*-
import os
import ytsearch
import pyperclip as clipboard
import vlc
import player
import pafy
import BaseHTTPServer
import json
from googleapiclient.errors import HttpError
import wx
app = wx.App()
player = player.playerGui()
class MainGui(wx.Frame):
	def __init__(self,parent,id,title):
		super(MainGui,self).__init__(parent,id,title)
		self.p = wx.Panel(self)
		self.boxsizer = wx.BoxSizer(wx.VERTICAL)
		self.searchlabel = wx.StaticText(self.p,-1,"Search")
		self.searchbox = wx.TextCtrl(self.p,-1,"",style=wx.TE_PROCESS_ENTER)
		self.searchbox.Bind(wx.EVT_TEXT_ENTER,self.OnSearch)
		self.boxsizer.Add(self.searchlabel,0,wx.ALL,5)
		self.boxsizer.Add(self.searchbox,0,wx.ALL,5)
		self.searchbutton=wx.Button(self.p,wx.ID_DEFAULT,"S&earch")
		self.searchbutton.Bind(wx.EVT_BUTTON,self.OnSearch)
		self.boxsizer.Add(self.searchbutton,0,wx.ALL,5)
		self.list_name = wx.StaticText(self.p,-1,"R&esults")
		self.listbox = wx.ListBox(self.p, -1)
		self.listbox.Bind(wx.EVT_CONTEXT_MENU, self.onContext)
		self.boxsizer.Add(self.list_name,0,wx.ALL,5)
		self.boxsizer.Add(self.listbox,0,wx.ALL,5)
		self.p.SetSizer(self.boxsizer)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Show(True)
	def OnClose(self,event):
		self.Destroy()
		os._exit(0)
	def onContext(self, event):
		if not hasattr(self, "popupID1"):
			self.popupID1 = wx.NewId()
			self.itemTwoId = wx.NewId()
			self.itemThreeId = wx.NewId()
			self.Bind(wx.EVT_MENU, self.onPlayAudio, id=self.popupID1)
			self.Bind(wx.EVT_MENU, self.CopyURL, id=self.itemTwoId)
		remenu = wx.Menu()
		Playved = remenu.Append(self.popupID1, "Play")
		copyURL = remenu.Append(self.itemTwoId, "Copy URL address to the clipboard")
		self.PopupMenu(remenu)
		remenu.Destroy()

	def onPlayAudio(self,event):
		self.videoname = self.listbox.GetSelection()
		self.vidID = self.video_dict['youID'][self.videoname]
		URL = "https://www.youtube.com/watch?v="+self.vidID
		audioplay = pafy.new(URL)
		urlv = audioplay.getbest()
		audiourl = urlv.url
		vidnam = audioplay.title
		player.detailslist.Clear()
		player.detailslist.Append("Title: "+audioplay.title)
		player.detailslist.Append("Uploaded by: "+audioplay.author)
		player.detailslist.Append("Description: "+audioplay.description)
		player.detailslist.Append("Duration: "+audioplay.duration)
		rating = str(float(audioplay.rating))
		player.detailslist.Append("video rating: "+rating)
		player.detailslist.Append("Total views: "+str(audioplay.viewcount))
		player.detailslist.Append("Total likes: "+str(audioplay.likes))
		player.detailslist.Append("Total dislikes: "+str(audioplay.dislikes))

		player.Load(audiourl,vidnam)
		player.Show()
	def CopyAURL(self,url):
		self.videoname = self.listbox.GetSelection()
		self.vidID = self.video_dict['youID'][self.videoname]
		URL = "https://www.youtube.com/watch?v="+self.vidID
		audioplay = pafy.new(URL)
		urlv = audioplay.getaudio()
		audiourl = urlv.url[2]
		clipboard.copy(audiourl)
	def CopyURL(self,url):
		self.videoname = self.listbox.GetSelection()
		self.vidID = self.video_dict['youID'][self.videoname]
		URL = "https://www.youtube.com/watch?v="+self.vidID
		clipboard.copy(URL)
	def OnSearch(self,meow,token=None):
		searchword = self.searchbox.GetValue()
		self.listbox.Clear()
		self.video_dict = {'youID':[], 'title':[], 'pub_date':[]}
		try:
			search = ytsearch.youtube_search(searchword,token=token)
			token = search[0]
			videos = search[1]
			for vid in videos:
				self.video_dict['youID'].append(vid['id']['videoId'])
				self.video_dict['title'].append(vid['snippet']['title'])
				self.video_dict['pub_date'].append(vid['snippet']['publishedAt'])
				self.listbox.Append(vid['snippet']['title'])
		except HttpError: 
			wx.MessageBox("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content),"Error",wx.OK)
MainGui(None,-1,'YouTube Player 0.1')
app.MainLoop()
