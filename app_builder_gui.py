"""GUI For Application Builder."""

import wx
import json
import app_builder_gen
import app_builder_prj

import requests
from pathlib import Path
import os

#https://www.techiediaries.com/python-gui-wxpython-tutorial-urllib-json/
#https://wiki.wxpython.org/PopupMenuRevised#CA-820ada62f4d016da4f82cd230d4ce75424bf9c3f_43

# some JSON:

curPrj = app_builder_prj.AppBuilderProject("")

curPrj.compsUrl = "https://raw.githubusercontent.com/ML-ES-Platform/app_builder/master/components.json"
curPrj.compsDir = "TOOLS"
curPrj.compsFileName = "components.json"
curPrj.prjDir = ""
curPrj.prjFileName = ""
curPrj.compDefaultPath = "COMPS"

class CompEditPanel(wx.Panel):
    """Panel for component list and the references in the project and git."""
    def __init__(self, parent):
        """Init Component list Panel."""
        self.parent = parent
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("gray")

        self.comp_list = wx.ListCtrl(self,
                                     style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.comp_list.InsertColumn(0, "Component Group", width=200)

        self.cnl_list = wx.ListCtrl(self,
                                    size=(-1, -1),
                                    style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.cnl_list.InsertColumn(0, 'Upper Channel')
        self.cnl_list.InsertColumn(1, 'Lower Channel')

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.comp_list, 0, wx.ALL | wx.EXPAND)
        sizer.Add(self.cnl_list, 1, wx.ALL | wx.EXPAND)

        self.SetSizer(sizer)

        self.comp_list.Bind(wx.EVT_LIST_ITEM_SELECTED,
                            self.OnComponentSelected)
        self.comp_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightDown)

        self.cnl_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnChannelSelected)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        """Refresh Graphics."""
        width, height = self.cnl_list.GetSize()
        for i in range(2):
            self.cnl_list.SetColumnWidth(i, width / 2)
        evt.Skip()

    def OnRightDown(self, event):
        """Execute the right click Event."""
        menu = CompListPopupMenu(self, "gray")
        self.PopupMenu(menu)
        menu.Destroy()

    def OnComponentSelected(self, event):
        """Call Action when component in list is selected."""
        comp = event.GetText().replace(" ", "-")
        #  print(comp)
        self.getChannels(comp)

    def OnChannelSelected(self, event):
        """Call Action when channel in list is selected."""
        #   print(event.GetText())
        webbrowser.open(event.GetText())


    def getComponents(self):
        """Show component on Panel."""
        # global curPrj
        comp_list = curPrj.getComponentList()
        comp_list.sort(reverse=True)
        # print(comp_list)

        self.comp_list.DeleteAllItems()
        # Groups Iterate
        for comp in comp_list:
            #print ("Comp ->" +comp +" : " +linkComps[comp] +" *")
            self.comp_list.InsertItem(0, comp)


    def getChannels(self, comp):
        """Show component Channels on Panel."""

        self.cnl_list.DeleteAllItems()

        # Groups Iterate
        grp_list = curPrj.getGroupList(comp)
        for grp in grp_list:

            # Update Group List
            self.grp_list.InsertItem(0, grp)

            # Channels Iterate
            cnl_list = curPrj.getGroupCnlList(comp,grp)
            for cnl in cnl_list:
                index = 0
                self.cnl_list.InsertItem(index, cnl)
                lnk = curPrj.getGroupCnlLink(comp,grp,cnl)
                self.cnl_list.SetItem(index, 1, lnk)
            print ("Here ...")
            
        return



class CompListPanel(wx.Panel):
    """Panel for component list and the references in the project and git."""
    def __init__(self, parent):
        """Init Component list Panel."""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("gray")

        self.parent = parent

        self.comp_list = wx.ListCtrl(self,
                                     style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.comp_list.InsertColumn(0, "Component")
        self.comp_list.InsertColumn(1, 'Project Path')
        self.comp_list.InsertColumn(2, 'Git reference')

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.comp_list, 1, wx.ALL | wx.EXPAND)

        self.SetSizer(sizer)
        self.getComponentList()
        self.comp_list.Bind(wx.EVT_LIST_ITEM_SELECTED,
                            self.OnComponentSelected)
        self.comp_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightDown)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.compSelected = ""

    def OnRightDown(self, event):
        """Right Click on Comp List."""
        menu = CompListPopupMenu(self, "gray", self.compSelected)
        self.PopupMenu(menu)
        menu.Destroy()

    def OnComponentSelected(self, event):
        """Component Selection action."""
        self.compSelected = event.GetText().replace(" ", "-")
        #  print(comp)
        #  self.getChannels(comp)

    def OnPaint(self, evt):
        """Update window."""
        width, height = self.comp_list.GetSize()
        self.comp_list.SetColumnWidth(0, 150)
        self.comp_list.SetColumnWidth(1, 150)
        self.comp_list.SetColumnWidth(2, width - 300)
        evt.Skip()

    def getComponentList(self):
        """Extract component list and the references in a panel."""
        global curPrj
        the_list = curPrj.getPlatformPathList()

        if the_list is not None:
            # print(" - >>>> -----> ")
            # print(the_list)

            self.comp_list.DeleteAllItems()

            index = 0
            for comp in the_list:
                pathSet = the_list[comp]
                # print(pathSet)
                if "Name" in pathSet:
                    componentName = pathSet["Name"]
                    # print(pathSet["Name"])
                    if componentName != "null":
                        self.comp_list.InsertItem(index, componentName)

                        if "Path" in pathSet:
                            pathReference = pathSet["Path"]
                            if pathReference != "null":
                                self.comp_list.SetItem(index, 1, pathReference)

                        if "git" in pathSet:
                            gitReference = pathSet["git"]
                            if gitReference != "null":
                                self.comp_list.SetItem(index, 2, gitReference)

                        index += 1

            return


class ComponentListFrame(wx.Frame):
    """Platform Component List window."""
    def __init__(self, parent, title):
        """Platform Component List window Init."""
        super(ComponentListFrame, self).__init__(parent,
                                                 title=title,
                                                 size=(600, 400))
        self.Centre()
        self.parent = parent
        self.panel = CompListPanel(self)
        self.panel.SetBackgroundColour("gray")
        self.createStatusBar()

    def createStatusBar(self):
        """Attach the status Bar."""
        self.CreateStatusBar()  #A Statusbar at the bottom of the window


class ComponentEditFrame(wx.Frame):
    """Platform Component Edit window."""
    def __init__(self, parent, title):
        """Platform Component Edit window Init."""
        super(ComponentEditFrame, self).__init__(parent,
                                                 title=title,
                                                 size=(600, 400))
        self.Centre()

        self.panel = CompEditPanel(self)
        self.panel.SetBackgroundColour("gray")
        self.createStatusBar()

    def createStatusBar(self):
        """Attach the status Bar."""
        self.CreateStatusBar()  #A Statusbar at the bottom of the window

        # self.btn = wx.Button(panel, wx.ID_OK, label = "ok", size = (50,20), pos = (75,50))


class CompListPopupMenu(wx.Menu):
    """Component Mangement PopUp menu."""
    def __init__(self, parent, title, compSelected):
        """Component Mangement PopUp menu init."""
        wx.Menu.__init__(self)

        self.WinName = title
        self.parent = parent

        item = wx.MenuItem(self, wx.ID_ANY, "Add Component")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.onAddComponent, item)
        self.comp = compSelected

    def onAddComponent(self, event):
        """On Item One selected."""
        global curPrj


        curPrj.addProjectCompFromPlatform(self.comp)


        # self.parent.parent.parent.OnCompUpdate(event)

        self.parent.parent.parent.panel.getComponents()
        print("Item One selected")


class MyPopupMenu(wx.Menu):
    """Component Mangement PopUp menu."""
    def __init__(self, parent, title):
        """Component Mangement PopUp menu init."""
        wx.Menu.__init__(self)

        self.WinName = title
        self.parent = parent

        item = wx.MenuItem(self, wx.ID_ANY, "Add Component")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnItem1, item)

        item = wx.MenuItem(self, wx.ID_ANY, "Edit Component")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnEditPopUp, item)

        item = wx.MenuItem(self, wx.ID_ANY, "Remove Component")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnItem3, item)

    def OnItem1(self, event):
        """On Item One selected."""
        print("Item One selected")

    def OnEditPopUp(self, event):
        """On Item Edit selected."""
        print("Item Two selected")
        ComponentEditFrame(self.parent.parent.parent, "Edit").Show()

    def OnItem3(self, event):
        """On Item Three selected."""
        print("Item Three selected")


class ConfigPanel(wx.Panel):
    """Main config window Component Panel."""

    def __init__(self, parent):
        """Init Main config window Component Panel."""
        self.parent = parent
        wx.Panel.__init__(self, parent)
        # self.SetBackgroundColour("grey")

        # component List
        self.comp_list = wx.ListCtrl(self,
                                     style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.comp_list.InsertColumn(0, "Component", width=150)

        # Component Name
        self.name_lbl = wx.StaticText(self, wx.ID_ANY, 'Name : ')
        # name_lbl.SetSize(size = (-1 , - 1))
        self.comp_name_lbl = wx.TextCtrl(self, wx.ID_ANY | wx.TE_READONLY, '')

        # self.Component git
        self.git_lbl = wx.StaticText(self, wx.ID_ANY, 'Git : ')
        self.comp_git_lbl = wx.TextCtrl(self, wx.ID_ANY | wx.TE_READONLY, '')

        # Component Path
        self.path_lbl = wx.StaticText(self, wx.ID_ANY, 'Path : ')
        self.comp_path_lbl = wx.TextCtrl(self, wx.ID_ANY | wx.TE_READONLY, '')

        # Group List
        self.grp_list = wx.ListCtrl(self,
                                    style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.grp_list.InsertColumn(0, 'Group list', width=150)

        # Channel List
        self.cnl_list = wx.ListCtrl(self,
                                    size=(-1, -1),
                                    style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.cnl_list.InsertColumn(0, 'Group Channels')
        self.cnl_list.InsertColumn(1, 'Linked Channel')

        # All component elements
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        # List for components
        compListSizer = wx.BoxSizer(wx.HORIZONTAL)
        #component general configuration: Name, Git, Path, Group
        compCfgSizer = wx.BoxSizer(wx.VERTICAL)
        # Comp Name line
        compNameSizer = wx.BoxSizer(wx.HORIZONTAL)
        # Comp Git line
        compGitSizer = wx.BoxSizer(wx.HORIZONTAL)
        # Comp Path line
        compPathSizer = wx.BoxSizer(wx.HORIZONTAL)
        # All Group Elements: group list , Channels
        compGroupSizer = wx.BoxSizer(wx.HORIZONTAL)

        compListSizer.Add(self.comp_list, 0, wx.ALL | wx.EXPAND)

        # build comp Name Sizer
        compNameSizer.Add(self.name_lbl, 0, wx.ALL | wx.EXPAND, 5)
        compNameSizer.Add(self.comp_name_lbl, 1, wx.ALL | wx.EXPAND, 5)

        # build comp Name Sizer
        compGitSizer.Add(self.git_lbl, 0, wx.ALL | wx.EXPAND, 5)
        compGitSizer.Add(self.comp_git_lbl, 1, wx.ALL | wx.EXPAND, 5)

        # build comp Name Sizer
        compPathSizer.Add(self.path_lbl, 0, wx.ALL | wx.EXPAND, 5)
        compPathSizer.Add(self.comp_path_lbl, 1, wx.ALL | wx.EXPAND, 5)

        # buld group Sizer
        compGroupSizer.Add(self.grp_list, 0, wx.ALL | wx.EXPAND)
        compGroupSizer.Add(self.cnl_list, 1, wx.ALL | wx.EXPAND)

        #build general configuration Sizer: Name, Git, Path, Group
        compCfgSizer.Add(compNameSizer, 0, wx.ALL | wx.EXPAND, 5)
        compCfgSizer.Add(compGitSizer, 0, wx.ALL | wx.EXPAND, 5)
        compCfgSizer.Add(compPathSizer, 0, wx.ALL | wx.EXPAND, 5)
        compCfgSizer.Add(compGroupSizer, 0, wx.ALL | wx.EXPAND, 5)

        #build top SIzer
        topSizer.Add(compListSizer, 0, wx.ALL | wx.EXPAND)
        topSizer.Add(compCfgSizer, 1, wx.ALL | wx.EXPAND)

        self.SetSizer(topSizer)

        self.comp_list.Bind(wx.EVT_LIST_ITEM_SELECTED,
                            self.OnComponentSelected)
        self.comp_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightDown)

        self.cnl_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnChannelSelected)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        """Refresh Graphics."""
        width, height = self.cnl_list.GetSize()
        for i in range(2):
            self.cnl_list.SetColumnWidth(i, width / 2)
        evt.Skip()

    def OnRightDown(self, event):
        """Execute the right click Event."""
        menu = MyPopupMenu(self, "gray")
        self.PopupMenu(menu)
        menu.Destroy()

    def OnComponentSelected(self, event):
        """Call Action when component in list is selected."""
        comp = event.GetText().replace(" ", "-")
        #  print(comp)
        self.getConfig(comp)

    def OnChannelSelected(self, event):
        """Call Action when channel in list is selected."""
        #   print(event.GetText())
        webbrowser.open(event.GetText())

        # Data from the 2 items are equal
        return 0

    def getConfig(self, comp):
        """Show component Channels on Panel."""
        self.cnl_list.DeleteAllItems()
        self.grp_list.DeleteAllItems()

        # Update Name
        comp_name = curPrj.getCompName(comp)
        self.comp_name_lbl.SetValue(comp_name)

        # Update Git
        comp_git = curPrj.getCompGit(comp)
        self.comp_git_lbl.SetValue(comp_git)

        # Update Path
        comp_path = curPrj.getCompPath(comp)
        self.comp_path_lbl.SetValue(comp_path)

        # Groups Iterate
        grp_list = curPrj.getGroupList(comp)
        for grp in grp_list:

            # Update Group List
            self.grp_list.InsertItem(0, grp)

            # Channels Iterate
            cnl_list = curPrj.getGroupCnlList(comp,grp)
            for cnl in cnl_list:
                index = 0
                self.cnl_list.InsertItem(index, cnl)
                lnk = curPrj.getGroupCnlLink(comp,grp,cnl)
                self.cnl_list.SetItem(index, 1, lnk)

    def getChannels(self, comp):
        """Show component Channels on Panel."""
        self.cnl_list.DeleteAllItems()

        # Groups Iterate
        grp_list = curPrj.getGroupList(comp)
        for grp in grp_list:

            # Update Group List
            self.grp_list.InsertItem(0, grp)

            # Channels Iterate
            cnl_list = curPrj.getGroupCnlList(comp,grp)
            for cnl in cnl_list:
                index = 0
                self.cnl_list.InsertItem(index, cnl)
                lnk = curPrj.getGroupCnlLink(comp,grp,cnl)
                self.cnl_list.SetItem(index, 1, lnk)
            print ("Here ...")

        return



    def getComponents(self):
        """Show component on Panel."""
        # global curPrj
        comp_list = curPrj.getComponentList()
        comp_list.sort(reverse=True)
        # print(comp_list)

        self.comp_list.DeleteAllItems()
        # Groups Iterate
        for comp in comp_list:
            #print ("Comp ->" +comp +" : " +linkComps[comp] +" *")
            self.comp_list.InsertItem(0, comp)


class MainWindow(wx.Frame):
    """Main Window Frame."""
    def __init__(self, parent, title):
        """Init Main Window."""
        super(MainWindow, self).__init__(parent, title=title, size=(600, 500))
        self.Centre()
        self.parent = parent
        self.panel = ConfigPanel(self)
        # self.panel.SetBackgroundColour("white")
        self.createStatusBar()
        self.createMenu()

    def createStatusBar(self):
        """Add Status bar to Main Window."""
        self.CreateStatusBar()  #A Statusbar at the bottom of the window

    def createMenu(self):
        """Create the menu of the Main Window."""
        menu = wx.Menu()
        menuNew = menu.Append(wx.ID_NEW, "&New", "New Configuration")
        menuOpen = menu.Append(wx.ID_OPEN, "&Open", "Open Configuration")
        menuSave = menu.Append(wx.ID_SAVE, "&Save As", "Save Configuration")
        menuExit = menu.Append(wx.ID_EXIT, "E&xit", "Quit application")

        menuBar = wx.MenuBar()
        menuBar.Append(menu, "&File")

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
        menuComps = toolsMenu.Append(wx.ID_ANY, "Component List",
                                     "component List")
        menuCompUpdate = toolsMenu.Append(wx.ID_ANY, "Components Update",
                                          "component List")

        menuBar.Append(toolsMenu, "&Tools")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnNew, menuNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSave)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.Bind(wx.EVT_MENU, self.OnDotGen, menuDot)
        self.Bind(wx.EVT_MENU, self.OnCfgGen, menuCfg)
        self.Bind(wx.EVT_MENU, self.OnTreeGen, menuTree)

        self.Bind(wx.EVT_MENU, self.OnComps, menuComps)
        self.Bind(wx.EVT_MENU, self.OnCompUpdate, menuCompUpdate)

    def OnComps(self, event):
        """Open Platform Component List."""
        ComponentListFrame(self, "ES Platform Component List").Show()

    def ComponentsUpdate(self, compsUrl, compsDir):

        resp = requests.get(compsUrl)
        filename = compsUrl.split("/")[-1]

        if not os.path.exists(compsDir):
            os.makedirs(compsDir)

        # print(curPrj.prjDir + "\\"+curPrj.compsDir+"\\" + filename)
        # print(resp.text)

        open(compsDir + "\\" + filename, 'w').write(resp.text)

    def OnCompUpdate(self, event):
        """Update Platform Component List."""
        # global curPrj
        # global curPrj.compsUrl

        self.ComponentsUpdate(curPrj.compsUrl,
                              str(curPrj.prjDir + "/" + curPrj.compsDir + "/"))

    def OnNew(self, event):
        """Save current Configuration."""
        global curPrj

        with wx.FileDialog(self,
                           "Create new ES Platform",
                           wildcard="ES Cfg (*.json)|*.json",
                           style=wx.FD_SAVE
                           | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind
            # save the current contents in the file
            pathname = fileDialog.GetPath()

            print(pathname)
            curPrj.newProjectFile(pathname)

            self.panel.getComponents()
            self.panel.getConfig("")



    def OnOpen(self, event):
        """Open an existing Configuration json."""
        global curPrj
        # if self.contentNotSaved:
        #     if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
        #                     wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
        #         return

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

            try:
                curPrj.openProjectFile(pathname)
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)

            self.panel.getComponents()


    def doSaveData(self):
        """Save current Configuration to a json file."""
        # global JSON_object
        try:
            curPrj.saveProjectFile()
        except IOError:
            wx.LogError("Cannot save current data in file '%s'." %
                        filePath)


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


            curPrj.prjDir = os.path.dirname(pathname).replace("\\", "/")
            print(curPrj.prjDir)

            curPrj.prjFileName = os.path.basename(pathname).replace("\\", "/")
            print(curPrj.prjFileName)

            self.doSaveData()


    def OnExit(self, event):
        """Handle Exit Action."""
        self.Close(True)

    def OnCfgGen(self, event):
        """Handle Config Generate Action."""
        jsonFile = "c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo.json"
        headerFile = "c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo_cfg_gen.h"
        srcFile = "c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo_cfg_gen.cpp"
        app_builder_gen.CfgHeadGen(jsonFile, headerFile)
        app_builder_gen.CfgSrcGen(jsonFile, srcFile)

    def OnDotGen(self, event):
        """Handle Dot Generate Action."""
        jsonFile = "c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo.json"
        dotFile = "c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo_cfg_gen.dot"
        app_builder_gen.DotGen(jsonFile, dotFile)

    def OnTreeGen(self, event):
        global curPrj
        curPrj.GenerateTree()


if __name__ == '__main__':
    app = wx.App()
    window = MainWindow(None, "Embedded Systems Application Builder")
    window.Show()
    app.MainLoop()