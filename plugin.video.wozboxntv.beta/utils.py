
import xbmc
import xbmcaddon
import os

ADDON = xbmcaddon.Addon(id='plugin.video.wozboxntv.beta')
IMAGE = os.path.join(ADDON.getAddonInfo('path'), 'icon.jpg')


def notification(message, time = 0):
	message = message.replace('"',  '')
	message = message.replace('\'', '')
	message = message.replace(',',  '')
	message = message.replace('(',  '')
	message = message.replace(')',  '')
 
	if time == 0:
		try:
			time = int(ADDON.getSetting('NotificationTime'))
		except:
			pass
		if time == 0:
			time = 30

	header = 'WOZBOX NTV..........'

	cmd  = 'XBMC.Notification(%s, %s, %d, %s)' % (header, message, time*1000, IMAGE)
	print cmd  # Put in LOG
	xbmc.executebuiltin(cmd)
