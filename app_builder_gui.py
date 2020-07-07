
import wx
import json
import app_builder_gen

#https://www.techiediaries.com/python-gui-wxpython-tutorial-urllib-json/


# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'
JSON_object  = json.loads(x)



class NewsPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour("gray")

        self.component_list = wx.ListCtrl(
            self, 
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.component_list.InsertColumn(0, "Component Group", width=200)
        
        self.channel_list = wx.ListCtrl(
            self, 
            size = (-1 , - 1),
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.channel_list.InsertColumn(0, 'Upper Channel')
        self.channel_list.InsertColumn(1, 'Lower Channel')
        
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.component_list, 0, wx.ALL | wx.EXPAND)
        sizer.Add(self.channel_list, 1, wx.ALL | wx.EXPAND)
        
        self.SetSizer(sizer)
        # self.getComponents()
        self.component_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnComponentSelected)
        self.channel_list.Bind(wx.EVT_LIST_ITEM_SELECTED , self.OnChannelSelected)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    def OnPaint(self, evt):
        width, height = self.channel_list.GetSize()
        for i in range(2):
            self.channel_list.SetColumnWidth(i, width/2)
        evt.Skip()
    
    def OnComponentSelected(self, event):
         component = event.GetText().replace(" ", "-")
        #  print(component)
         self.getChannels(component)
    
    
    def OnChannelSelected(self, event):
          print(event.GetText()) 
          webbrowser.open(event.GetText())           

                   
    def getChannels(self, component):
        with open("c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo.json", "r") as read_file:
            JSON_object = json.load(read_file)
        
        # print(component)
        self.channel_list.DeleteAllItems()
        linkGroup = JSON_object["Components"][component]["Groups"]
        for grp in linkGroup:
            linkCnl = JSON_object["Components"][component]["Groups"][grp]["Channels"]
            
            for cnl in linkCnl:

                print (cnl)
                print (linkCnl[cnl])
                index = 0
                self.channel_list.InsertItem(index, cnl)
                self.channel_list.SetItem(index, 1, linkCnl[cnl])
                index += 1


    def getComponents(self, file):
        # with open("c:/MicroLabOS_WS/ES_Platform/src/ASW/arm_6dof/demo/arm_6dof_demo.json", "r") as read_file:
        #     JSON_object = json.load(read_file)
        JSON_Open_object = json.load(file)
        
        self.component_list.DeleteAllItems()
        # print( JSON_object["Components"] )
        for el in JSON_Open_object["Components"]:
            print (el)
            self.component_list.InsertItem(0, el)
        return JSON_Open_object



class MainWindow(wx.Frame):

    def __init__(self, parent, title):

        super(MainWindow, self).__init__(parent, title = title, size = (600,500))
        self.Centre()

        self.panel = NewsPanel(self)
        self.panel.SetBackgroundColour("gray")
        self.createStatusBar()
        self.createMenu()
        
    def createStatusBar(self):
        self.CreateStatusBar() #A Statusbar at the bottom of the window

    def createMenu(self):
    
        menu= wx.Menu()
        menuNew = menu.Append(wx.ID_NEW, "&New", "New Configuration")
        menuOpen = menu.Append(wx.ID_OPEN, "&Open", "Open Configuration")
        menuSave = menu.Append(wx.ID_SAVE, "&Save", "Open Configuration")
        menuExit = menu.Append(wx.ID_EXIT, "E&xit", "Quit application")
              
        menuBar = wx.MenuBar()
        menuBar.Append(menu,"&File")

        genMenu = wx.Menu()
        menuCfg = genMenu.Append(wx.ID_ANY, "Generate &Config ", "Generate Configuration file for dependencies")
        menuDot = genMenu.Append(wx.ID_ANY, "Generate &Dot", "Generate dot file for dependencies")

        menuBar.Append(genMenu,"&Generate")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnNew , menuNew )
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSave)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        
        self.Bind(wx.EVT_MENU, self.OnDotGen, menuDot)
        self.Bind(wx.EVT_MENU, self.OnCfgGen, menuCfg)

        # self.Bind(wx.EVT_MENU, self.OnCfgGen, genMenu)



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

            # self.panel.getComponents()

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
    window= MainWindow(None, "Newsy - read worldwide news!")
    window.Show()
    app.MainLoop()