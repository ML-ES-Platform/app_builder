"""GUI For Application Builder."""

import wx
import wx.dataview

import app_panel_project_cfg as cfg_panel
import app_panel_platform as plf_panel
import app_panel_builder as bld_panel
import app_popup_menu as popup_menu
import app_builder_prj
import app_builder_gen

import requests
from pathlib import Path
import os

#https://www.techiediaries.com/python-gui-wxpython-tutorial-urllib-json/
#https://wiki.wxpython.org/PopupMenuRevised#CA-820ada62f4d016da4f82cd230d4ce75424bf9c3f_43
# TODO https://pythonspot.com/wxpython-tabs/
# http://zetcode.com/wxpython/menustoolbars/
# http://www.blog.pythonlibrary.org/2011/01/04/wxpython-wx-listctrl-tips-and-tricks/  Editable list
# some JSON:

# https://pypi.org/project/CppHeaderParser/

curPrj = app_builder_prj.AppBuilderProject("")

curPrj.compsUrl = "https://raw.githubusercontent.com/ML-ES-Platform/app_builder/master/components.json"
curPrj.platformDir = "TOOLS"
curPrj.platformFileName = "components.json"
curPrj.prjDir = ""
curPrj.prjFileName = ""
curPrj.compDefaultPath = "COMPS"
curPrj.headerFile = "c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo_cfg_gen.h"
curPrj.srcFile = "c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo_cfg_gen.cpp"

app_title = "Embedded Systems Application Builder"
app_panel_color = "light gray"
#  wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)



class MainWindow(wx.Frame):
    """Main Window Frame."""
    def __init__(self, parent, title):
        """Init Main Window."""
        super(MainWindow, self).__init__(parent, title=title, size=(800, 700))
        self.Centre()
        self.parent = parent
        self.createStatusBar()
        self.createMenu()
        # Create a panel and notebook (tabs holder)
        main_panel = wx.Panel(self)
        nb = wx.Notebook(main_panel, wx.NB_MULTILINE)
        # Create the tab windows
        self.prj_panel = cfg_panel.ProjectConfigPanel(nb, curPrj, app_panel_color)
        self.prj_panel.main_window = self

        self.comp_panel = plf_panel.PlatformPanel(nb, curPrj, app_panel_color)
        self.prj_panel.main_window = self


        self.build_panel = bld_panel.ProjectBuilderPanel(nb, curPrj, app_panel_color)
        self.prj_panel.main_window = self

        # Add the windows to tabs and name them.
        nb.AddPage(self.build_panel, "App Builder")
        nb.AddPage(self.prj_panel, "Project Configuration")
        nb.AddPage(self.comp_panel, "ES Platform ")
        # nb.AddPage(self.grp_panel, "ADD group to the channel")
        nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnTabChange)
        # Set noteboook in a sizer to create the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        main_panel.SetSizer(sizer)

    def OnTabChange(self, event):
        # self.grp_panel.OnEnterWindow(event)
        self.build_panel.OnEnterWindow(event)

    def createStatusBar(self):
        """Add Status bar to Main Window."""
        self.CreateStatusBar()  #A Statusbar at the bottom of the window

    def createMenu(self):
        """Create the menu of the Main Window."""
        # Create Menu Bar
        menuBar = wx.MenuBar()
        # File Menu
        file_menu = wx.Menu()
        menuNew = file_menu.Append(wx.ID_NEW, "&New\tCtrl+N",
                                   "New Configuration")
        menuSave = file_menu.Append(wx.ID_SAVE, "&Save\tCtrl+S",
                                    "Save Configuration")
        menuSaveAs = file_menu.Append(wx.ID_SAVE, "&Save As\tCtrl+A",
                                      "Save Configuration with a new name")
        menuOpen = file_menu.Append(wx.ID_OPEN, "&Open\tCtrl+O",
                                    "Open Configuration")
        menuOpenLast = file_menu.Append(wx.ID_OPEN, "&Open last\tCtrl+L",
                                        "Open Last Configuration")
        menuReload = file_menu.Append(wx.ID_OPEN, "&Reload\tCtrl+R",
                                      "Reload Configuration")
        menuExit = file_menu.Append(wx.ID_EXIT, "&Quit\tCtrl+Q",
                                    "Quit application")
        file_menu.AppendSeparator()
        self.filehistory = wx.FileHistory(8)
        self.config = wx.Config("Your-Programs-Name",
                                style=wx.CONFIG_USE_LOCAL_FILE)
        self.filehistory.Load(self.config)
        menu_recent = wx.Menu()
        self.filehistory.UseMenu(menu_recent)
        self.filehistory.AddFilesToMenu()
        # file_menu.AppendMenu(wx.ID_ANY, "&Open Recent Files", menu_recent)
        file_menu.AppendSubMenu(menu_recent, "&Open Recent Files",
                                "Open Recent Files")
        # Append File Menu to Menu Bar
        menuBar.Append(file_menu, "&File")
        # Generate Menu
        genMenu = wx.Menu()
        menuCfg = genMenu.Append(
            wx.ID_ANY, "Generate &Config ",
            "Generate Configuration file for dependencies")
        menuDot = genMenu.Append(wx.ID_ANY, "Generate &Dot",
                                 "Generate dot file for dependencies")
        menuTree = genMenu.Append(wx.ID_ANY, "Generate &Tree",
                                  "Generate Project Tree")
        menuBar.Append(genMenu, "&Generate")
        toolsMenu = wx.Menu()
        menuCompsView = toolsMenu.Append(wx.ID_ANY, "Load Platform Components",
                                         "Load platform")
        menuCompUpdate = toolsMenu.Append(
            wx.ID_ANY, "Update Platform Components from URL",
            "Update platform")
        menuBar.Append(toolsMenu, "&Tools")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnNew, menuNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnOpenLast, menuOpenLast)
        self.Bind(wx.EVT_MENU, self.OnReload, menuReload)
        self.Bind(wx.EVT_MENU_RANGE,
                  self.OnOpenRecent,
                  id=wx.ID_FILE1,
                  id2=wx.ID_FILE9)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSaveAs)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnDotGen, menuDot)
        self.Bind(wx.EVT_MENU, self.OnCfgGen, menuCfg)
        self.Bind(wx.EVT_MENU, self.OnTreeGen, menuTree)
        self.Bind(wx.EVT_MENU, self.OnPlatformLoad, menuCompsView)
        self.Bind(wx.EVT_MENU, self.OnPlatformUpdate, menuCompUpdate)

    def OnPlatformLoad(self, event):
        """Open Platform Component List."""
        print("Item OnPlatformLoad selected")
        curPrj.LoadPlatformFile()
        self.comp_panel.UpdatePlatformComptList()

    def OnPlatformUpdate(self, event):
        """Update Platform Component List."""
        compDir = str(curPrj.prjDir + "/" + curPrj.compsDir + "/")
        curPrj.UpdatePlatform(curPrj.compsUrl, compDir)

    def OnNew(self, event):
        """Save current Configuration."""
        #TODO
        if curPrj.prjContentNotSaved:
            if wx.MessageBox("Current content has not been saved! Proceed?",
                             "Please confirm", wx.ICON_QUESTION | wx.YES_NO,
                             self) == wx.NO:
                return
        with wx.FileDialog(self,
                           "Create new ES Platform",
                           wildcard="ES Cfg (*.json)|*.json",
                           style=wx.FD_SAVE
                           | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            # save the current contents in the file
            pathname = fileDialog.GetPath()
            curPrj.NewProjectFile(pathname)
            self.prj_panel.UpdateProjectComptList()
            self.prj_panel.showCompConfig("")
            self.filehistory.AddFileToHistory(pathname)
            self.filehistory.Save(self.config)
            self.config.Flush()

    def OnReload(self, event):
        # Proceed loading the file chosen by the user
        pathname = curPrj.GetProjectFilePath()
        self.OpenProjectFile(pathname)

    def OnOpenLast(self, event):
        # Proceed loading the file chosen by the user
        fileNum = 1 #- wx.ID_FILE1
        print(fileNum)
        pathname = self.filehistory.GetHistoryFile(fileNum)
        # Proceed loading the file chosen by the user
        self.OpenProjectFile(pathname)

        return

    def OnOpen(self, event):
        """Process Open a project file event."""
        filePath = curPrj.GetProjectFilePath()
        if os.path.isfile(filePath):
            if wx.MessageBox(
                    "You are about to change the project :" + filePath,
                    "Please confirm", wx.ICON_QUESTION | wx.YES_NO,
                    self) == wx.NO:
                return
        #TODO
        # notify if project is not saved
        if curPrj.GetProjectFileName() != "null":
            if curPrj.prjContentNotSaved:
                if wx.MessageBox(
                        "Current content has not been saved! Proceed?",
                        "Please confirm", wx.ICON_QUESTION | wx.YES_NO,
                        self) == wx.NO:
                    return
        # otherwise ask the user what new file to open
        with wx.FileDialog(self,
                           "Open Platform Configuration file",
                           wildcard="ES Cfg (*.json)|*.json",
                           style=wx.FD_OPEN
                           | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.OpenProjectFile(pathname)

    def OnOpenRecent(self, event):
        """Process Open a recent file event."""
        # Notify changing project
        filePath = curPrj.GetProjectFilePath()
        if os.path.isfile(filePath):
            if wx.MessageBox(
                    "You are about to change the project :" + filePath,
                    "Please confirm", wx.ICON_QUESTION | wx.YES_NO,
                    self) == wx.NO:
                return
        # notify if project is not saved
        if curPrj.prjContentNotSaved:
            if wx.MessageBox("Current content has not been saved! Proceed?",
                             "Please confirm", wx.ICON_QUESTION | wx.YES_NO,
                             self) == wx.NO:
                return
        # extract selected file path
        fileNum = event.GetId() - wx.ID_FILE1
        print(fileNum)
        pathname = self.filehistory.GetHistoryFile(fileNum)
        # Proceed loading the file chosen by the user
        self.OpenProjectFile(pathname)

    def OpenProjectFile(self, pathname):
        """Open a project File"""
        # Open Project File
        try:
            curPrj.LoadProjectFile(pathname)
            # Update window title with file name
            title = app_title + " - " + curPrj.prjFileName
            self.SetTitle(title)
            #register file in file history
            self.filehistory.AddFileToHistory(pathname)
            self.filehistory.Save(self.config)
            self.config.Flush()
        except IOError:
            wx.LogError("Cannot open project file '%s'." % pathname)
        try:
            platformFilePath = curPrj.GetProjectHomeDir(
            ) + "/" + curPrj.platformDir + "/" + curPrj.platformFileName
            curPrj.LoadPlatformFile()
        except IOError:
            wx.LogError("Cannot open Platform File file '%s'." %
                        platformFilePath)
        #update Application windows
        self.prj_panel.UpdateProjectComptList()
        self.comp_panel.UpdatePlatformComptList()
        self.build_panel.UpdatePanel()

    def OnSaveAs(self, event):
        """Save current Configuration."""
        with wx.FileDialog(self,
                           "Save Platform Configuration file",
                           wildcard="ES Cfg (*.json)|*.json",
                           style=wx.FD_SAVE
                           | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            # save the current contents in the file
            pathname = fileDialog.GetPath()
            self.doSaveData(pathname)

    def OnSave(self, event):
        """Process Save project menu event"""
        pathname = curPrj.GetProjectFilePath()
        # check if the file exists
        if not os.path.isfile(pathname):
            # if no create it by file dialog
            with wx.FileDialog(self,
                               "Save Platform Configuration file",
                               wildcard="ES Cfg (*.json)|*.json",
                               style=wx.FD_SAVE
                               | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # the user changed their mind
                # save the current contents in the file
                pathname = fileDialog.GetPath()
        # save the content into file
        self.doSaveData(pathname)

    def doSaveData(self, pathname):
        """Save current Configuration to a json file."""
        curPrj.SetProjectFilePath(pathname)
        # global JSON_object
        try:
            curPrj.SaveProjectFile()
            self.filehistory.AddFileToHistory(pathname)
            self.filehistory.Save(self.config)
            self.config.Flush()
        except IOError:
            wx.LogError("Cannot save current data in file '%s'." % pathname)

    def OnExit(self, event):
        """Handle Exit Action."""
        self.Close(True)

    def OnCfgGen(self, event):
        """Handle Config Generate Action."""
        curPrj.GenProjectConfig()

    def OnDotGen(self, event):
        """Handle Dot Generate Action."""
        curPrj.GenProjectDot()

    def OnTreeGen(self, event):
        """Handle Project Tree Generate Action."""
        curPrj.GenProjectTree()


if __name__ == '__main__':
    app = wx.App()
    window = MainWindow(None, app_title)
    window.Show()
    app.MainLoop()