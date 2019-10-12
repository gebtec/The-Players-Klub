import urllib,urllib2,re,xbmcplugin,xbmcgui,requests,base64,xbmcaddon

pluginname = 'TPK'
Plugin = 'plugin.video.%s'%(pluginname)
grabsettings = xbmcaddon.Addon(id=Plugin)
username = grabsettings.getSetting('username')
password = grabsettings.getSetting('password')
HOME = 'http://00100.co:2086/enigma2.php?username=%s&password=%s&type=get_live_categories'%(username,password)

def CATEGORIES():
		site = requests.get(HOME)
		match = re.compile('<title>(.+?)</title>.+?<!\[CDATA\[(.+?)]]>').findall(site.content)
		for title,url in match:
				title = base64.b64decode(title)
				addDir(title,url,1,'')
		if not match:
				addDir('Your Password/Username May Not Be Correct','',1,'')
def INDEX(url):
	r = requests.get(url)
	match = re.compile('<title>(.+?)<.+?>(.+?)<.+?<!\[CDATA\[(.+?)\].+?\[CDATA\[(.+?)\]').findall(r.content)
	for name,description,icon,url in match:
		name = base64.b64decode(name)
		icon = icon.replace('[','\n[')
		description = description.replace('<description>','')
		description = base64.b64decode(description)
		try:
			if '[' in name:
				name2 = name.split('[')
				name3 = name.split('min')
				description = description.split('\n(')
				addLink('[COLOR white][B]%s[/B][/COLOR] - [COLOR gold][I]%s[/I][/COLOR]'%(name2[0],description[0].replace('\n','').replace('','')),url,'','')
			else:
				addLink('[COLOR white][B]%s[/B][/COLOR]'%(name),url,'','')
		except:
			pass       
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
def addLink(name,url,iconimage,urlType):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable','true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

	  
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)




xbmcplugin.endOfDirectory(int(sys.argv[1]))
