from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, config, ConfigYesNo, ConfigText, ConfigSelection, ConfigClock
from Components.Sources.List import List
from Components.Network import iNetwork
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, resolveFilename, SCOPE_CURRENT_SKIN
from os import system, remove as os_remove, rename as os_rename, popen, getcwd, chdir
from Plugins.SystemPlugins.NetworkBrowser.NetworkBrowser import NetworkBrowser
from Screens.Setup import Setup



class DeliteSettings(Screen):
	skin = """
	<screen position="160,110" size="390,360" title="Black Pole Extra Settings">
		<widget source="list" render="Listbox" position="10,10" size="370,330" scrollbarMode="showOnDemand" >
			<convert type="TemplatedMultiContent">
                		{"template": [
                		MultiContentEntryText(pos = (60, 1), size = (300, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
                		MultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),
                		],
                		"fonts": [gFont("Regular", 24)],
                		"itemHeight": 36
                		}
            		</convert>
		</widget>
	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self.list = []
		self["list"] = List(self.list)
		self.updateList()
		
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.KeyOk,
			"back": self.close

		})
		
	def KeyOk(self):
		self.sel = self["list"].getCurrent()
		self.sel = self.sel[2]
		
		if self.sel == 0:
			from Screens.BpDevice import DeliteDevicesPanel
			self.session.open(DeliteDevicesPanel)
		elif self.sel == 1:
			self.session.open(BhNetBrowser)
		elif self.sel == 2:
			from Screens.BpFormat import Bp_UsbFormat
			self.session.open(Bp_UsbFormat)
		elif self.sel == 3:
			from Screens.BpDevice import BlackPoleSwap
			self.session.open(BlackPoleSwap)
		elif self.sel == 4:
			self.session.open(Setup, "userinterface")
		elif self.sel == 5:
			from Plugins.SystemPlugins.UIPositionSetup.plugin import UIPositionSetup
			self.session.open(UIPositionSetup)
		elif self.sel == 6:
			from Plugins.SystemPlugins.UI3DSetup.plugin import UI3DSetupScreen
			self.session.open(UI3DSetupScreen)
		elif self.sel == 7:
			self.session.open(Setup, "epgsettings")
		elif self.sel == 8:
			self.session.open(Setup, "recording")
		elif self.sel == 9:
			from Screens.RecordPaths import RecordPathsSettings
			self.session.open(RecordPathsSettings)
		elif self.sel == 10:
			self.session.open(Setup, "subtitlesetup")
		elif self.sel == 11:
			self.session.open(Setup, "autolanguagesetup")
		
		else:
			self.noYet()
		
	def noYet(self):
		nobox = self.session.open(MessageBox, "Function Not Yet Available", MessageBox.TYPE_INFO)
		nobox.setTitle(_("Info"))
	
		
	def updateList(self):
		self.list = [ ]
		mypath = resolveFilename(SCOPE_CURRENT_SKIN, "")
		if mypath == "/usr/share/enigma2/":
			mypath = "/usr/share/enigma2/skin_default/"
		
		mypixmap = mypath + "icons/infopanel_space.png"
		png = LoadPixmap(mypixmap)
		name = "Devices Manager & Mountpoints"
		idx = 0
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/mountwizard.png"
		png = LoadPixmap(mypixmap)
		name = "Network Browse & Mountpoints"
		idx = 1
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_space.png"
		png = LoadPixmap(mypixmap)
		name = "Usb Format Wizard"
		idx = 2
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/swapsettings.png"
		png = LoadPixmap(mypixmap)
		name = "Swap File settings"
		idx = 3
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_osd.png"
		png = LoadPixmap(mypixmap)
		name = "Osd settings"
		idx = 4
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_osd.png"
		png = LoadPixmap(mypixmap)
		name = "Osd Position setup"
		idx = 5
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_osd.png"
		png = LoadPixmap(mypixmap)
		name = "Osd 3D setup"
		idx = 6
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_samba.png"
		png = LoadPixmap(mypixmap)
		name = "Internal Epg settings"
		idx = 7
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_cron.png"
		png = LoadPixmap(mypixmap)
		name = "Record settings"
		idx = 8
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/infopanel_space.png"
		png = LoadPixmap(mypixmap)
		name = "Recording paths"
		idx = 9
		res = (name, png, idx)
		self.list.append(res)
				
		mypixmap = mypath + "icons/infopanel_kmod.png"
		png = LoadPixmap(mypixmap)
		name = "Subtitle settings"
		idx = 10
		res = (name, png, idx)
		self.list.append(res)
		
		mypixmap = mypath + "icons/inadynsettings.png"
		png = LoadPixmap(mypixmap)
		name = "Auto language settings"
		idx = 11
		res = (name, png, idx)
		self.list.append(res)
		
		
		self["list"].list = self.list
		
		

class BhNetBrowser(Screen):
	skin = """
	<screen position="center,center" size="800,520" title="Select Network Interface">
		<widget source="list" render="Listbox" position="10,10" size="780,460" scrollbarMode="showOnDemand" >
			<convert type="StringList" />
		</widget>
    		<ePixmap pixmap="skin_default/buttons/red.png" position="200,480" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="440,480" size="140,40" alphatest="on" />
		<widget name="key_red" position="200,480" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget name="key_yellow" position="440,480" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
    	</screen>"""
	
	def __init__(self, session):
		Screen.__init__(self, session)
		
		self["key_red"] = Label(_("Select"))
		self["key_yellow"] = Label(_("Close"))
		
		self.list = []
		self["list"] = List(self.list)
		
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.selectInte,
			"back": self.close,
			"red": self.selectInte,
			"yellow": self.close
		})
		
		self.list = [ ]
		self.adapters = [(iNetwork.getFriendlyAdapterName(x),x) for x in iNetwork.getAdapterList()]
		for x in self.adapters:
			res = (x[0], x[1])
			self.list.append(res)

		self["list"].list = self.list
		
	def selectInte(self):
		mysel = self["list"].getCurrent()
		if mysel:
			inter = mysel[1]
			self.session.open(NetworkBrowser, inter, "/usr/lib/enigma2/python/Plugins/SystemPlugins/NetworkBrowser")

