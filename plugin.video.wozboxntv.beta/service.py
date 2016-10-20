import recordings, utils, locking
import xbmcaddon, xbmc, datetime
#print 'service.py: start'
PLUGIN='plugin.video.wozboxntv.beta'
ADDON = xbmcaddon.Addon(id=PLUGIN)

try:
	Platform = recordings.FindPlatform()
	if not Platform == '':
		utils.notification('[COLOR green]Platform found and set[/COLOR]')
except:
	pass
	print 'service.py: FAILED recordings.FindPlatform()'  # Put in LOG
locking.recordUnlockAll()
locking.scanUnlockAll()
recordings.ftvntvlist()
if ADDON.getSetting('enable_record')=='true':
	now = recordings.parseDate(datetime.datetime.now()) 
	startDate=now - datetime.timedelta(days = 10)
	endDate=now + datetime.timedelta(days = 10)
	recordingsActive=recordings.getRecordingsActive(startDate, endDate)
	try:
		recordings.backupDataBase()
		recordings.reschedule()
		utils.notification('[COLOR green]Reschedule Complete[/COLOR]')
		ADDON.setSetting('DebugRecording','false')
	except:
		pass
		utils.notification('[COLOR red]Reschedule failed:[/COLOR] Check your planned recordings! - Recording Debug has been set')
		ADDON.setSetting('DebugRecording','true')
		xbmc.sleep(5000)

