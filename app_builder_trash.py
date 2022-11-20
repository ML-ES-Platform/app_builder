import wx

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
        self.comp_list.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.OnRightDown)

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
        comp = event.GetText()
        self.GetGroups(comp)

    def OnChannelSelected(self, event):
        """Call Action when channel in list is selected."""
        webbrowser.open(event.GetText())


    def GetComponents(self):
        """Show component on Panel."""
        comp_list = curPrj.GetProjectCompList()
        self.comp_list.DeleteAllItems()
        # Groups Iterate
        for comp in comp_list:
            self.comp_list.InsertItem(0, comp)


    def GetGroups(self, comp):
        """Show component Channels on Panel."""
        self.cnl_list.DeleteAllItems()
        # Groups Iterate
        grp_list = curPrj.GetGroupList(comp)
        for grp in grp_list:
            # Update Group List
            self.grp_list.InsertItem(0, grp)
            # Channels Iterate
            cnl_list = curPrj.GetGroupCnlList(comp,grp)
            for cnl in cnl_list:
                index = 0
                self.cnl_list.InsertItem(index, cnl)
                lnk = curPrj.GetGroupCnlLink(comp,grp,cnl)
                self.cnl_list.SetItem(index, 1, lnk)
            
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
        self.SetStatusText('Right Click for options')


class GroupAddPanel(wx.Panel):
    """Panel for component list and the references in the project and git."""
    def __init__(self, parent):
        """Init Component list Panel."""
        self.parent = parent
        wx.Panel.__init__(self, parent)
        # self.SetBackgroundColour("gray")


        # Component Name
        self.grp_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Group Name : ')
        # name_lbl.SetSize(size = (-1 , - 1))
        self.grp_name_txt = wx.TextCtrl(self, wx.ID_ANY |  wx.EXPAND, '')
        # name_lbl.SetSize(size = (-1 , - 1))
        self.grp_add_btn = wx.Button(self, -1, 'Add Group')
        self.grp_add_btn.Bind(wx.EVT_BUTTON, self.OnAddGroupBtnClicked) 
        # group name selection from comp list
        self.comp_list = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.comp_list.InsertColumn(0, "Group Name Hint", width=150)

        # Group List
        self.grp_list = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.grp_list.InsertColumn(0, 'Group list', width=150)
 
        # All component elements
        topSizer = wx.BoxSizer(wx.VERTICAL)
        
        # List for components
        comp_name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        hintSizer =  wx.BoxSizer(wx.HORIZONTAL)


        #build general configuration Sizer: Name, Git, Path, Group
        topSizer.Add(comp_name_sizer, 0, wx.ALL | wx.EXPAND, 5)
        topSizer.Add(hintSizer, 0, wx.ALL | wx.EXPAND, 5)

 
         # build comp Name Sizer
        comp_name_sizer.Add(self.grp_name_lbl, 0, wx.ALL , 5)
        comp_name_sizer.Add(self.grp_name_txt, 1, wx.ALL , 5)
        comp_name_sizer.Add(self.grp_add_btn, 1, wx.ALL , 5)

        hintSizer.Add(self.comp_list, 1, wx.ALL | wx.EXPAND,5)
        hintSizer.Add(self.grp_list, 1, wx.ALL | wx.EXPAND,5)

        self.SetSizer(topSizer)
        self.comp_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnComponentSelected)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.ShowGroupHints()
        comp = curPrj.activeComponent
        self.ShowGroups(comp)


    def OnEnterWindow(self, event):
        self.ShowGroupHints()
        comp = curPrj.activeComponent
        self.ShowGroups(comp)

    def OnAddGroupBtnClicked(self, event): 
        btn = event.GetEventObject().GetLabel() 
        comp = curPrj.activeComponent
        grp = self.grp_name_txt.GetValue()
        x = curPrj.GetGroupDict(comp, grp)
        if (x != "null"):
            print (">< EXISTS ><")
        else:
            curPrj.AddGroup(comp,grp)
        self.ShowGroups(comp)
 
    def OnPaint(self, evt):
        """Update window."""
        width, height = self.comp_list.GetSize()
        self.comp_list.SetColumnWidth(0, width)
        evt.Skip()

    def ShowGroupHints(self):
        """Show component on Panel."""
        # global curPrj
        comp_list = curPrj.GetProjectCompList()
        self.comp_list.DeleteAllItems()
        # Groups Iterate
        for comp in comp_list:
            self.comp_list.InsertItem(0, comp)

    def ShowGroups(self, comp):
        """Show component on Panel."""
        # global curPrj
        grp_list = curPrj.GetGroupList(comp)
        self.grp_list.DeleteAllItems()
        # Groups Iterate
        for grp in grp_list:
            self.grp_list.InsertItem(0, grp)

    def OnComponentSelected(self, event):
        """Call Action when component in list is selected."""
        comp = event.GetText()
        self.grp_name_txt.SetValue(comp + "_grp")


class GroupAddFrame(wx.Frame):
    """Platform Component List window."""
    def __init__(self, parent, title):
        """Platform Component List window Init."""
        super(GroupAddFrame, self).__init__(parent,
                                                 title=title,
                                                 size=(600, 400))
        self.Centre()
        self.parent = parent
        self.panel = GroupAddPanel(self)
        # self.panel.SetBackgroundColour("gray")
        self.createStatusBar()

    def createStatusBar(self):
        """Attach the status Bar."""
        self.CreateStatusBar()  #A Statusbar at the bottom of the window
        self.SetStatusText('ADD group to the channel')

class ChannelAddFrame(wx.Frame):
    """Platform Component List window."""
    def __init__(self, parent, title):
        """Platform Component List window Init."""
        super(ChannelAddFrame, self).__init__(parent,
                                                 title=title,
                                                 size=(600, 600))
        self.Centre()
        self.parent = parent
        self.panel = ChannelAddPanel(self)
        # self.panel.SetBackgroundColour("gray")
        self.createStatusBar()

    def createStatusBar(self):
        """Attach the status Bar."""
        self.CreateStatusBar()  #A Statusbar at the bottom of the window
        self.SetStatusText('ADD Channel to the Group')


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

