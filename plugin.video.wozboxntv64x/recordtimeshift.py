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
timeshiftfilename = 'timeshift'
#xbmc.log('recordtimeshift.py: sys.argv= %s' %(str(repr(sys.argv))))
try:
	program  = sys.argv[0]
	uri           = sys.argv[1].replace('AAabBB',' ').replace('aAabBb','?').replace('BBabAA','=')
	title         = sys.argv[2]
except:
	pass
	title = 'TimeShift'
try:
	xbmc.log('recordtimeshift.py: os.environ= %s' % os.environ['OS'] ) #put in LOG
except: pass

timeshiftsetting = ADDON.getSetting('timeshift')
#print timeshiftsetting
#utils.notification('TimeShift Setting = ' + repr(timeshiftsetting))
if timeshiftsetting == '0':
	#utils.notification('TimeShift %s [COLOR red]NOT enabled[/COLOR]' % (title))
	utils.notificationbox('TimeShift %s [COLOR red]NOT enabled[/COLOR]' % (title))

else:

	LoopCountMax = int(ADDON.getSetting('LoopCount'))

	rtmpdumpEXEp = utils.rtmpdumpFilename()
	rtmpdumpEXE = os.path.join(ADDON.getAddonInfo('path'),'rtmpdump',rtmpdumpEXEp)
	xbmc.log('recordtimeshift.py: stats os.F_OK: %s' % os.access(rtmpdumpEXE, os.F_OK))
	xbmc.log('recordtimeshift.py: stats os.W_OK: %s' % os.access(rtmpdumpEXE, os.W_OK))
	xbmc.log('recordtimeshift.py: stats os.X_OK: %s' % os.access(rtmpdumpEXE, os.X_OK))
	#xbmc.log('1')
	if not xbmc.getCondVisibility('system.platform.windows'):
		if os.access(rtmpdumpEXE, os.X_OK):
			print 'Permissions ------ 0777 ----- GREAT !!'  # Put in LOG
		else:
			print 'Permissions -----------------   BAD !!'  # Put in LOG
			for dirpath, dirnames, filenames in os.walk(os.path.join(ADDON.getAddonInfo('path'),'rtmpdump')):
				for filename in filenames:
					path = os.path.join(dirpath, filename)
					try:
						os.chmod(path, 0777)
						print 'Permissions set with: CHMOD 0777 !!'  # Put in LOG
					except: pass
	if os.access(rtmpdumpEXE, os.X_OK):
		RecordingDisabled = False
	else:
		time.sleep(1)
		utils.notification('Recording %s [COLOR red]NOT possible! Set this program executable:[/COLOR] %s' % (title,rtmpdumpEXE))
		time.sleep(5)
		RecordingDisabled = True
	recordPath = xbmc.translatePath(os.path.join(ADDON.getSetting('record_path')))
	if not utils.folderwritable(recordPath):
		utils.notification('Recording %s [COLOR red]FAILED - You must set the recording path writable![/COLOR]' % title)
	else:
		datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
		nowHM=datetime.datetime.today().strftime('%H:%M:%S')
		rtmp  = uri.replace('xXx',' ').replace('###',',')
		
		cmdoption = ' -t ' +str(2*60*60)  ### TimeShift recording time 2h
		if os.access('/system/vendor/bin/ffmpeg', os.X_OK):
			cmd = '/system/vendor/bin/ffmpeg -y -i '  # Use seperately installed ffmpeg program ###
		else:
			cmd = 'ffmpeg -y -i '  # Use seperately installed ffmpeg program ###
		cmd += '"' + rtmp + '"'
		
		cmd += ' -f flv -c:v libx264 -b:v 2000k -c:a aac -strict experimental -b:a 128k -ar 44100 ' + cmdoption + ' ' ### SLOW For use with ffmpeg
		###	cmd += ' -c copy -bsf:a aac_adtstoasc ' + cmdoption + ' ' ### FAST For use with ffmpeg
		
		recordstarttime = datetime.datetime.today().strftime('%Y-%m-%d %H-%M')
		
		cmd += '"' + recordPath + timeshiftfilename
		cmd += '.mp4"'
	
		timeshiftfile = recordPath + timeshiftfilename + '.mp4'
		ADDON.setSetting('timeshiftfile',timeshiftfile)
		xbmc.log( 'recordtimeshift: cmd= %s' % repr(cmd))
		nowHM=datetime.datetime.today().strftime('%H:%M')
		if not RecordingDisabled:
			utils.log('TimeShift', 'Recording %s [COLOR green]started %s[/COLOR]' % (title, nowHM))
		
		if ADDON.getSetting('os')=='11':
			utils.runCommand(cmd, LoopCount=0, libpath=None)
		else:
			libpath = utils.libPath()
			utils.runCommand(cmd, LoopCount=0, libpath=libpath)

		if not RecordingDisabled:
			nowHM=datetime.datetime.today().strftime('%H:%M')
			utils.log('TimeShift', 'Recording %s [COLOR red]complete[/COLOR] %s' % (title, nowHM))
