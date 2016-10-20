import xbmc,xbmcaddon,xbmcgui,xbmcplugin,os,sys,re,urllib2,urllib,shutil,upload,time,extract,datetime,settings,advancedsettings
from addon.common.addon import Addon
from addon.common.net import Net
from metahandler import metahandlers
metainfo=metahandlers.MetaData()
AddonTitle="WOZBOX Tutorials"
addon_id='plugin.video.wozboxtutorialsbeta'
local=xbmcaddon.Addon(id=addon_id); maintenancepath=xbmc.translatePath(local.getAddonInfo('path'))
addon=Addon(addon_id,sys.argv); net=Net(); datapath=addon.get_profile()
art=xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
TribecaUrl='http://wozboxtv.com/downloads/'
mainurl=TribecaUrl+'wizard'
def getArt(n): 
    if os.path.isfile(os.path.join(art,n))==True: return os.path.join(art,n)
    else: return mainurl+'/thumbs/'+n
howtourl='http://www.wozboxtv.com/downloads/tutorials/videos_beta.xml'
defaulticon=xbmc.translatePath(os.path.join(maintenancepath,'icon.png')); #defaulticon=xbmc.translatePath(os.path.join(art,'icon.jpg')); 
defaultfanart=xbmc.translatePath(os.path.join(maintenancepath,'fanart.jpg')); #defaultfanart=os.path.join(art,'fanart.jpg')
feed=TribecaUrl+'tools/maintenance/news/feed.txt'
PC_ENABLE=settings.pc_enable_pc(); PC_WATERSHED=settings.pc_watershed_pc(); PC_RATING=settings.pc_pw_required_at(); PC_PASS=settings.pc_pass(); PC_DEFAULT=settings.pc_default(); PC_TOGGLE=settings.pc_enable_pc_settings(); CUSTOM_PC=settings.pc_custom_pc_file()
restore_path=xbmc.translatePath(os.path.join('special://profile','addon_data'))
restorexbmc_path=xbmc.translatePath('special://profile')
backup_path=local.getSetting('backup_path')
def SetView(n=500): xbmc.executebuiltin("Container.SetViewMode("+str(n)+")")
def nolines(t):
	it=t.splitlines(); t=''
	for L in it: t=t+L
	t=((t.replace("\r","")).replace("\n","").replace("\a","").replace("\t","")); return t
def File_Open(path): #print 'File: '+path
	if os.path.isfile(path): file=open(path,'r'); contents=file.read(); file.close(); return contents ## File found. #print 'Found: '+path
	else: return '' ## File not found.
def CATEGORIES():
    count=int(local.getSetting('opened')); print count; add=count+1; addone=str(add); print add; local.setSetting('opened',addone); show=['1','10','20','30','40','50','60','70','80','90','100','110','120','130','140','150','160','170','180','190','200']
    if addone not in show: CATEGORIES2()
    else: CATEGORIES2()

def CATEGORIES2():
    addDir("Tutorial Videos",howtourl,1,getArt('tutorial_videos.png'),defaultfanart)


################################
###       How to Videos      ###
################################
def HOWTOS(url,fanart):
    match=re.compile('<w:t>&lt;title&gt;(.+?);/title&gt;</w:t></w:r></w:p><w:p><w:pPr></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Courier" w:h-ansi="Courier" w:cs="Courier"/><wx:font wx:val="Courier"/><w:sz w:val="26"/><w:sz-cs w:val="26"/></w:rPr><w:t>&lt;link&gt;(.+?);/link&gt;</w:t></w:r></w:p><w:p><w:pPr></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Courier" w:h-ansi="Courier" w:cs="Courier"/><wx:font wx:val="Courier"/><w:sz w:val="26"/><w:sz-cs w:val="26"/></w:rPr><w:t>&lt;thumb&gt;</w:t></w:r></w:p><w:p><w:pPr></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Courier" w:h-ansi="Courier" w:cs="Courier"/><wx:font wx:val="Courier"/><w:sz w:val="26"/><w:sz-cs w:val="26"/></w:rPr><w:t>(.+?)</w:t></w:r></w:p><w:p><w:pPr></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Courier" w:h-ansi="Courier" w:cs="Courier"/><wx:font wx:val="Courier"/><w:sz w:val="26"/><w:sz-cs w:val="26"/></w:rPr><w:t>&lt;/thumb&gt;</w:t>').findall(net.http_GET(url).content)
    for name,link,icon in match:
        link=link.replace('http://www.youtube.com/embed?v=',''); link=link.replace('http://www.youtube.com/watch?v=',''); link=link.replace('&lt',''); name=name.replace('&lt','')
        if icon=='none': iconimage='http://i.ytimg.com/vi/%s/0.jpg' % link
        else: iconimage=str(icon)
        fanart=str(fanart); url='plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % link
        addDir(name,url,3,iconimage,fanart)        
def PLAY_STREAM(name,url,iconimage): liz=xbmcgui.ListItem(name,iconImage="DefaultVideo.png",thumbnailImage=iconimage); liz.setInfo(type="Video",infoLabels={"Title":name}); liz.setProperty("IsPlayable","true"); pl=xbmc.PlayList(xbmc.PLAYLIST_VIDEO); pl.clear(); pl.add(url,liz); xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)
################################
###    End How to Videos     ###
################################

def addDir(name,url,mode,iconimage,fanart):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart); ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage); liz.setInfo(type="Video",infoLabels={"Title":name,"Plot":name}); liz.setProperty("Fanart_Image",fanart)
    if mode==3 or mode==9 or mode==6 or mode==15 or mode==17 or mode==21 or mode==23 or mode==28 or mode==42 or mode==37 or mode==38 or mode==25 or mode==32 or mode==33 or mode==34 or mode==35 or mode==22 or mode==19 or mode==26 or mode==18 or mode==16 or mode==27 or mode==5 or mode==61 or mode==62 or mode==63:
          ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    else: ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok
def get_params(param=[]):
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]; cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&'); param={}
        for i in range(len(pairsofparams)):
             splitparams={}; splitparams=pairsofparams[i].split('=')
             if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
    return param
params=get_params(); url=None; name=None; mode=None; iconimage=None; fanart=None
try:    url=urllib.unquote_plus(params["url"])
except: pass
try:    name=urllib.unquote_plus(params["name"])
except: pass
try:    iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try:    mode=int(params["mode"])
except: pass
try:    fanart=urllib.unquote_plus(params["fanart"])
except: pass
print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name); print "IconImage: "+str(iconimage)
if mode==None or url==None or len(url)<1: CATEGORIES(); xbmc.executebuiltin("Container.SetViewMode(500)")
elif mode==1: HOWTOS(url,fanart); xbmc.executebuiltin("Container.SetViewMode(500)")
elif mode==2: HOWTOVIDEOS(name,url,fanart)
elif mode==3: PLAY_STREAM(name,url,iconimage)
elif mode==4: CLEARCACHE(url)
elif mode==5: ERASELOGS(url)
elif mode==6: PURGEPACKAGES(url)
elif mode==7: MAINTENANCE(url); xbmc.executebuiltin("Container.SetViewMode(500)")
elif mode==8: FINDADDON(url,name)
elif mode==9: REMOVEADDON(url)
elif mode==10: SYSTEMTWEAKS(url); xbmc.executebuiltin("Container.SetViewMode(500)")
elif mode==11: WALLPAPERDIR()
elif mode==12: WALLPAPER(name,url,iconimage)
elif mode==13: WALLPAPER2(name,url,iconimage)
elif mode==14: WALLPAPER3(name,url,iconimage); xbmc.executebuiltin("Container.SetViewMode(500)")
elif mode==15: WALLPAPERDOWNLOAD(name,url,iconimage)
elif mode==16: ADVANCEDXML(url,name)
elif mode==17: CHECKADVANCEDXML(url,name)
elif mode==18: DELETEADVANCEDXML(url)
elif mode==19: ADD7ICONS(url)
elif mode==20: HOMEICONS(url)
elif mode==21: HOMEICONS2(name)
elif mode==22: ADDONINSTALLER(url)
elif mode==23: UPLOADLOG(url)
elif mode==24: FUSIONINSTALLER(url)
elif mode==25: FACTORYRESET(url)
elif mode==26: ANDROIDPLAYER(url)
elif mode==27: pop()
elif mode==28: CONFIGWIZARD(url)
elif mode==29: AUTOSTART(url); xbmc.executebuiltin("Container.SetViewMode(500)")
elif mode==30: AUTOSTARTADD(url,name)
elif mode==31: XMLBACKUP(); xbmc.executebuiltin("Container.SetViewMode(500)")
elif mode==32: MYIP()
elif mode==33: backup_xml(url)
elif mode==34: restore_xml(url)
elif mode==35: local.openSettings()
elif mode==36: MODULES(url); xbmc.executebuiltin("Container.SetViewMode(50)")
elif mode==37: INSTALLMODULE(url)
elif mode==38: XBMCVERSION(url)
elif mode==39: XBMCDOWNLOAD(); xbmc.executebuiltin("Container.SetViewMode(500)")
elif mode==40: XBMCDOWNLOAD2(); xbmc.executebuiltin("Container.SetViewMode(500)")
elif mode==41: XBMCDOWNLOAD3(url)
elif mode==42: DownloaderClass2(url)
elif mode==43: XBMCDOWNLOAD4(url)
elif mode==44: XBMCDOWNLOAD5(url)
elif mode==45: XBMCDOWNLOAD6(url); xbmc.executebuiltin("Container.SetViewMode(500)")
elif mode==46: XBMCDOWNLOAD7(url)
elif mode==47: XBMCDOWNLOAD8(url)
elif mode==48: XBMCDOWNLOAD9(url)
elif mode==49: XBMCDOWNLOAD10(url); xbmc.executebuiltin("Container.SetViewMode(500)")
elif mode==50: XBMCDOWNLOAD11(url)
elif mode==51: XBMCDOWNLOAD12(url)
elif mode==52: XBMCDOWNLOAD13(url)
elif mode==53: XBMCDOWNLOAD14(url); xbmc.executebuiltin("Container.SetViewMode(500)")
elif mode==54: XBMCDOWNLOAD15(url)
elif mode==55: XBMCDOWNLOAD16(url)
elif mode==56: XBMCDOWNLOAD17(url)
elif mode==57: NEWSANNOUNCEMENTS(url); xbmc.executebuiltin("Container.SetViewMode(51)")
elif mode==58: LOGANALYZER(url); xbmc.executebuiltin("Container.SetViewMode(51)")
elif mode==59: advancedsettings.MENU(name)
elif mode==60: parental_controls(name)
elif mode==61: parentalcontrol_help(name)
elif mode==62: pc_setting()
elif mode==63: local.openSettings()	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
