"""GUI For Application Builder."""

import wx
import json
import app_builder_gen

#https://www.techiediaries.com/python-gui-wxpython-tutorial-urllib-json/
#https://wiki.wxpython.org/PopupMenuRevised#CA-820ada62f4d016da4f82cd230d4ce75424bf9c3f_43

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'
JSON_object  = json.loads(x)


class CompListPanel(wx.Panel):
    """Panel for component list and the references in the project and git."""

    def __init__(self, parent):
        """Init Component list Panel."""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("gray")

        self.comp_list = wx.ListCtrl(
            self, 
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.comp_list.InsertColumn(0, "Component")
        

        self.comp_list.InsertColumn(1, 'Project Path')
        self.comp_list.InsertColumn(2, 'Git reference')
        
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.comp_list, 1, wx.ALL | wx.EXPAND)
        
        self.SetSizer(sizer)
        self.getComponentList()
        self.comp_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnComponentSelected)
        self.comp_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightDown)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
       
    
    def OnRightDown(self,event):
        """Right Click on Comp List."""
        menu = MyPopupMenu("gray")
        self.PopupMenu(menu)
        menu.Destroy()
   

    def OnComponentSelected(self, event):
        """Component Selection action."""
        comp = event.GetText().replace(" ", "-")
        #  print(comp)
        #  self.getChannels(comp, JSON_object)
    
    def OnPaint(self, evt):
        """Update window."""
        width, height = self.comp_list.GetSize()
        self.comp_list.SetColumnWidth(0, 150)
        self.comp_list.SetColumnWidth(1, 150)
        self.comp_list.SetColumnWidth(2, width-300)
        evt.Skip()
                   
 

    def getComponentList(self):
        """Extract component list and the references in a panel."""
        #
        with open("c:/MicroLabOS_WS/ES_Platform/src/TOOLS/app_builder/components.json", "r") as read_file:
            JSON_Open_object = json.load(read_file)

            # JSON_Open_object = json.load(file)
            
            self.comp_list.DeleteAllItems()
            # print( JSON_object["Components"] )
            # Groups Iterate
            if "Components" in JSON_Open_object:
                linkComps = JSON_Open_object["Components"]
                index = 0
                for comp in linkComps:

                    componentName = linkComps[comp]
                    gitReference = "null"
                    pathReference = "null"
                    if "Name" in linkComps[comp]:
                        componentName = linkComps[comp]["Name"]
                    if "git" in linkComps[comp]:
                        gitReference = linkComps[comp]["git"]
                    if "Path" in linkComps[comp]:
                        pathReference = linkComps[comp]["Path"]

                    if (componentName != "null"):                    
                        self.comp_list.InsertItem(index, componentName)
                        if (pathReference != "null"):
                            self.comp_list.SetItem(index, 1, pathReference)
                        if (gitReference != "null"):
                            self.comp_list.SetItem(index, 2, gitReference)
                        index += 1

                
                    # index = 0
                    # self.channel_list.InsertItem(index, cnl)
                    # self.channel_list.SetItem(index, 1, linkCnl[cnl])
                    # 
               
            # return JSON_Open_object

class ComponentListFrame(wx.Frame):
    """Platform Component List window."""

    def __init__(self, parent, title):
        """Platform Component List window Init.""" 
        super(ComponentListFrame, self).__init__(parent, title = title, size = (600,400))
        self.Centre()

        self.panel = CompListPanel(self)
        self.panel.SetBackgroundColour("gray")
        self.createStatusBar()

    def createStatusBar(self):
        """Attach the status Bar."""
        self.CreateStatusBar() #A Statusbar at the bottom of the window


class ComponentEditFrame(wx.Frame):
    """Platform Component Edit window."""

    def __init__(self, parent, title):
        """Platform Component Edit window Init.""" 
        super(ComponentEditFrame, self).__init__(parent, title = title, size = (600,400))
        self.Centre()

        # self.panel = CompListPanel(self)
        self.panel.SetBackgroundColour("gray")
        self.createStatusBar()

    def createStatusBar(self):
        """Attach the status Bar."""
        self.CreateStatusBar() #A Statusbar at the bottom of the window

        # self.btn = wx.Button(panel, wx.ID_OK, label = "ok", size = (50,20), pos = (75,50))


class MyPopupMenu(wx.Menu):
    """Component Mangement PopUp menu."""

    def __init__(self, WinName):
        """Component Mangement PopUp menu init."""
        wx.Menu.__init__(self)

        self.WinName = WinName
    
        item = wx.MenuItem(self, wx.NewId(), "Add Component")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnItem1, item)

        item = wx.MenuItem(self, wx.NewId(),"Edit Component")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnEditPopUp, item)

        item = wx.MenuItem(self, wx.NewId(),"Remove Component")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnItem3, item)

    def OnItem1(self, event):
        """On Item One selected."""
        print ("Item One selected")

    def OnEditPopUp(self, event):
        """On Item Edit selected."""
        print ("Item Two selected")
        ComponentEditFrame( self, "Edit Component")


    def OnItem3(self, event):
        """On Item Three selected."""
        print ("Item Three selected")
  


class ConfigPanel(wx.Panel):
    """Main config window Component Panel."""

    def __init__(self, parent):
        """Main config window Component Panel Init."""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("gray")

        self.comp_list = wx.ListCtrl(
            self, 
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.comp_list.InsertColumn(0, "Component Group", width=200)
        
        self.channel_list = wx.ListCtrl(
            self, 
            size = (-1 , - 1),
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.channel_list.InsertColumn(0, 'Upper Channel')
        self.channel_list.InsertColumn(1, 'Lower Channel')
        
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.comp_list, 0, wx.ALL | wx.EXPAND)
        sizer.Add(self.channel_list, 1, wx.ALL | wx.EXPAND)
        
        self.SetSizer(sizer)
        # self.getComponents()
        self.comp_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnComponentSelected)
        self.comp_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightDown)

        self.channel_list.Bind(wx.EVT_LIST_ITEM_SELECTED , self.OnChannelSelected)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    def OnPaint(self, evt):
        width, height = self.channel_list.GetSize()
        for i in range(2):
            self.channel_list.SetColumnWidth(i, width/2)
        evt.Skip()

    def OnRightDown(self,event):
        menu = MyPopupMenu("gray")
        self.PopupMenu(menu)
        menu.Destroy()
   

    def OnComponentSelected(self, event):
         comp = event.GetText().replace(" ", "-")
        #  print(comp)
         self.getChannels(comp, JSON_object)
    
    
    def OnChannelSelected(self, event):
        #   print(event.GetText()) 
          webbrowser.open(event.GetText())           

                   
    def getChannels(self, comp, JSON_object):
        # with open("c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo.json", "r") as read_file:
        #     JSON_object = json.load(read_file)
        
        # print(comp)
        self.channel_list.DeleteAllItems()

        # Groups Iterate
        if "Components" in JSON_object:
            linkComps = JSON_object["Components"]
            # print ("Comp ->" +comp +" : " +linkComps[comp] +" ")

            # Groups Iterate
            if "Groups" in linkComps[comp]:
                linkGroup = linkComps[comp]["Groups"]
                for grp in linkGroup:
                    # print ("  Grp ->" +grp +" : " +linkGroup[grp] +" ")

                    # Channels Iterate
                    if "Channels" in linkGroup[grp]:
                        linkCnl = linkGroup[grp]["Channels"]
                        for cnl in linkCnl:

                            # print ("    Cnl ->" +cnl +" : " +linkCnl[cnl] +" ")
                            index = 0
                            self.channel_list.InsertItem(index, cnl)
                            self.channel_list.SetItem(index, 1, linkCnl[cnl])
                            index += 1


    def getComponents(self, file):
        # with open("c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo.json", "r") as read_file:
        #     JSON_object = json.load(read_file)
        JSON_Open_object = json.load(file)
        
        self.comp_list.DeleteAllItems()
        # print( JSON_object["Components"] )
        # Groups Iterate
        if "Components" in JSON_Open_object:
            linkComps = JSON_Open_object["Components"]
            for comp in linkComps:
                #print ("Comp ->" +comp +" : " +linkComps[comp] +" *")
                self.comp_list.InsertItem(0, comp)
            
        return JSON_Open_object


class MainWindow(wx.Frame):

    def __init__(self, parent, title):

        super(MainWindow, self).__init__(parent, title = title, size = (600,500))
        self.Centre()

        self.panel = ConfigPanel(self)
        self.panel.SetBackgroundColour("gray")
        self.createStatusBar()
        self.createMenu()
        
    def createStatusBar(self):
        self.CreateStatusBar() #A Statusbar at the bottom of the window

    def createMenu(self):
    
        menu= wx.Menu()
        menuNew = menu.Append(wx.ID_NEW, "&New", "New Configuration")
        menuOpen = menu.Append(wx.ID_OPEN, "&Open", "Open Configuration")
        menuSave = menu.Append(wx.ID_SAVE, "&Save As", "Save Configuration")
        menuExit = menu.Append(wx.ID_EXIT, "E&xit", "Quit application")
              
        menuBar = wx.MenuBar()
        menuBar.Append(menu,"&File")

        genMenu = wx.Menu()
        menuCfg = genMenu.Append(wx.ID_ANY, "Generate &Config ", "Generate Configuration file for dependencies")
        menuDot = genMenu.Append(wx.ID_ANY, "Generate &Dot", "Generate dot file for dependencies")

        menuBar.Append(genMenu,"&Generate")

        toolsMenu = wx.Menu()
        menuComps = toolsMenu.Append(wx.ID_ANY, "Components", "component List")

        menuBar.Append(toolsMenu,"&Tools")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnNew , menuNew )
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSave)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        
        self.Bind(wx.EVT_MENU, self.OnDotGen, menuDot)
        self.Bind(wx.EVT_MENU, self.OnCfgGen, menuCfg)

        self.Bind(wx.EVT_MENU, self.OnComps, menuComps)



    def OnComps (self, event):
      
        a = ComponentListFrame(self, "Dialog").Show()
   
    def OnNew (self, event):
        self.Close(True) 


    def OnOpen(self, event):
        global JSON_object
        
        # if self.contentNotSaved:
        #     if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
        #                     wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
        #         return

        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open Platform Configuration file", wildcard="ES Cfg (*.json)|*.json",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    JSON_object = self.panel.getComponents(file)
                    # self.doLoadDataOrWhatever(file)
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)


    def doSaveData(self,file, JSON_object):
        # global JSON_object
        json.dump(JSON_object, file,indent=4) 

    def OnSaveAs(self, event):
        
        with wx.FileDialog(self, "Save Platform Configuration file", wildcard="ES Cfg (*.json)|*.json",
                        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    self.doSaveData(file, JSON_object)

            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)



    def OnExit(self, event):
        self.Close(True) 

    def OnDotGen(self, event):
        jsonFile = "c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo.json"
        dotFile = "c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo_cfg_gen.dot"
        app_builder_gen.DotGen(jsonFile, dotFile)

    def OnCfgGen(self, event):
        jsonFile = "c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo.json"
        headerFile = "c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo_cfg_gen.h"
        srcFile = "c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo_cfg_gen.cpp"
        app_builder_gen.CfgHeadGen(jsonFile, headerFile)
        app_builder_gen.CfgSrcGen(jsonFile, srcFile)
    

if __name__ == '__main__':
    app = wx.App()
    window= MainWindow(None, "Embedded Systems Application Builder")
    window.Show()
    app.MainLoop()