#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time
import utils, recordings
import net
from hashlib import md5
import json

#ADDON      = xbmcaddon.Addon(id='plugin.video.wozboxntv')
import definition
ADDON      = definition.getADDON()
pyfile = sys.argv[0]
xbmc.log('recordtimeshift.py: sys.argv= %s' %(str(repr(sys.argv))))
try:
	program  = sys.argv[0]
	uri           = sys.argv[1].replace('AAabBB',' ').replace('aAabBb','?').replace('BBabAA','=')
	title         = sys.argv[2]
	HANDLE	      = int(sys.argv[3])
	recordname    = sys.argv[4]
	channel       = sys.argv[5]
except:
	pass
	title = 'TimeShiftShow'
try:
	xbmc.log('recordtimeshiftshow.py: os.environ= %s' % os.environ['OS'] ) #put in LOG
except: pass

if ADDON.getSetting('timeshift') == '0':
	utils.notification('TimeShift %s [COLOR red]NOT enabled[/COLOR]' % (title))
else:
	utils.notification('Record TimeShift Started: %s (%s)' % (recordname,channel))
	#LoopCountMax = int(ADDON.getSetting('LoopCount'))

	timeshiftfile = ADDON.getSetting('timeshiftfile')
	utils.log(pyfile,'RecordTimeShift 0+ file= %s' % repr(timeshiftfile))
	playername = title
	count = 0
	while timeshiftfile == '' and count < 1000:
		utils.log(pyfile,'RecordTimeShift 0++ file= %s' % repr(timeshiftfile))
		time.sleep(1)
		count += 1
		timeshiftfile = ADDON.getSetting('timeshiftfile')
		utils.log(pyfile,'RecordTimeShift count= %s' % repr(count))
		utils.log(pyfile,'RecordTimeShift 0+++ file= %s' % repr(timeshiftfile))
		utils.notification('Record TimeShift Waiting for Agent: #%s %s (%s)' % (str(count),recordname,channel))
	utils.log(pyfile,'RecordTimeShift count= %s' % repr(count))
	count = 0
	timeshiftrunning = os.path.isfile(timeshiftfile)
	while not timeshiftrunning == True and count < 1000: 
		time.sleep(1)
		count += 1
		timeshiftrunning = os.path.isfile(timeshiftfile)
		utils.log(pyfile,'RecordTimeShiftRunning count= %s - %s (%s)' % (repr(count),recordname,channel))
		utils.notification('Record TimeShift Waiting for File: #%s %s (%s)' % (str(count),recordname,channel))
	utils.log(pyfile,'RecordTimeShiftRunning count= %s - %s (%s)' % (repr(count),recordname,channel))
	#liz=xbmcgui.ListItem(title, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz=xbmcgui.ListItem(playername)
	liz.setInfo( type="Video", infoLabels={ "Title": playername} )
	liz.setProperty("IsPlayable","true")
	utils.log(pyfile,'timeshiftfile= %s' % (timeshiftfile))
	liz.setPath(timeshiftfile)
	utils.log(pyfile,'RecordTimeShift 0++++ file= %s liz= %s' % (repr(timeshiftfile), repr(liz)))
	xbmc.sleep(250)
	player = xbmc.Player()
	#for retry in range(0, 10):
	#	    if player.isPlaying():
	#	        break
	#	    utils.notification('Record TimeShift Waiting: #%s %s (%s)' % (str(retry),recordname,channel))
	#	    time.sleep( 1 )
	#	    #xbmc.sleep(250)
	xbmc.sleep(10000)
	### int(sys.argv[1]) -- HANDLE
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	#xbmc.executebuiltin("xbmc.PlayMedia("+timeshiftfile+")",True)
	while (xbmc.Player().isPlayingVideo() == True) and (not xbmc.abortRequested):
		count += 1
		utils.notification('Record TimeShift Running: #%s %s (%s)' % (str(count),recordname,channel))
		time.sleep( 1 )
	utils.notification('Record TimeShift Ended: #%s %s (%s)' % (str(count),recordname,channel))
	"""
	while not player.isPlaying() and count < LoopCountMax:
		xbmc.sleep(250)
		count += 1
		#xbmc.executebuiltin("PlayMedia("+timeshiftfile+")")
		utils.log(pyfile,'RecordTimeShiftNotPlaying count= %s' % repr(count))
	while player.isPlaying():  #keep alive ?
		xbmc.sleep(1000)
		count += 1
		#xbmc.executebuiltin("PlayMedia("+timeshiftfile+")")
		utils.log(pyfile,'RecordTimeShiftPlaying count= %s' % repr(count))
	"""
	##########################################################
	"""
	#item = xbmcgui.ListItem(path=timeshiftfile)
	datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
	playlist = os.path.join(datapath, 'TimeShift') + '.m3u'
 	if os.path.isfile(playlist ) == False: 
		LF = open(playlist , 'a')
		LF.write('#EXTM3U \n')
		LF.write(timeshiftfile + '\n')
	else:
		LF = open(playlist , 'a')
		LF.write(timeshiftfile + '\n')
	#printL('Play Video')
	#xbmcplugin.setResolvedUrl(HANDLE, timeshiftfile is not None, item)
	utils.log(pyfile,'HANDLE= %s' % repr(HANDLE))
	xbmcplugin.setResolvedUrl(HANDLE, true, liz)
	"""
	"""
	if ADDON.getSetting('enable.subtitles') == 'true':
	    if video['SubtitlesUri']:
		player = xbmc.Player()
		for retry in range(0, 20):
		    if player.isPlaying():
		        break
		    xbmc.sleep(250)
		xbmc.Player().setSubtitles(video['SubtitlesUri'])
	"""
	################################################################
	"""
	if os.path.isfile(timeshiftfile) == True: 
		utils.log(pyfile,'RecordTimeShift 1')
		###xbmc.Player().play(timeshiftfile)
		xbmc.executebuiltin("PlayMedia("+timeshiftfile+")")
		###xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)  ### TimeShift - show timeshift recording
	else:
		utils.log('default.py','RecordTimeShift 2-')
		time.sleep(1)
		utils.log(pyfile,'RecordTimeShift 2')
		###xbmc.Player().play(timeshiftfile)
		xbmc.executebuiltin("PlayMedia("+timeshiftfile+")")
		###xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)  ### TimeShift - show timeshift recording
		#################################################################
	"""
