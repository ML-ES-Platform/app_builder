"""GUI - Project configuration Panel."""
import wx

class ProjectConfigPanel(wx.Panel):
    """Main config window Component Panel."""

    def __init__(self, parent,curPrj, panel_color):
        """Init Main config window Component Panel."""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(panel_color)

        self.parent = parent
        self.curPrj = curPrj


        # All component elements
        #build general configuration Sizer: Name, Git, Path, Group
        topSizer = wx.BoxSizer(wx.HORIZONTAL)

        # List for components
        compListSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # component List
        self.comp_list = wx.ListCtrl(self, style=wx.LC_REPORT)
        compListSizer.Add(self.comp_list, 0, wx.ALL | wx.EXPAND, 3)
        self.comp_list.InsertColumn(0, "Component", width=150)

        topSizer.Add(compListSizer, 0, wx.ALL | wx.EXPAND)

        #component general configuration: Name, Git, Path, Group
        comp_main_cfg_sizer = wx.BoxSizer(wx.VERTICAL)

        # Comp Name line ====================================================
        comp_name_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.comp_name_lbl = wx.StaticText(self, wx.ID_ANY,
                                           'Name : ', wx.DefaultPosition,
                                           wx.Size(35, -1), wx.ALIGN_RIGHT)
        comp_name_sizer.Add(self.comp_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        self.comp_name_txt = wx.TextCtrl(self, wx.ID_ANY | wx.TE_READONLY, '')
        comp_name_sizer.Add(self.comp_name_txt, 1, wx.ALL | wx.EXPAND, 3)

        comp_main_cfg_sizer.Add(comp_name_sizer, 0, wx.ALL | wx.EXPAND, 3)

        # Comp Git line ====================================================
        comp_git_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.git_lbl = wx.StaticText(self, wx.ID_ANY,
                                     'Git : ', wx.DefaultPosition,
                                     wx.Size(35, -1), wx.ALIGN_RIGHT)
        comp_git_sizer.Add(self.git_lbl, 0, wx.ALL | wx.EXPAND, 3)
        self.comp_git_txt = wx.TextCtrl(self, wx.ID_ANY | wx.TE_READONLY, '')
        comp_git_sizer.Add(self.comp_git_txt, 1, wx.ALL | wx.EXPAND, 3)
        comp_main_cfg_sizer.Add(comp_git_sizer, 0, wx.ALL | wx.EXPAND, 3)
        # Comp Path line ====================================================
        comp_path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.path_lbl = wx.StaticText(self, wx.ID_ANY,
                                      'Path : ', wx.DefaultPosition,
                                      wx.Size(35, -1), wx.ALIGN_RIGHT)
        comp_path_sizer.Add(self.path_lbl, 0, wx.ALL | wx.EXPAND, 3)
        self.comp_path_txt = wx.TextCtrl(self, wx.ID_ANY | wx.TE_READONLY, '')
        comp_path_sizer.Add(self.comp_path_txt, 1, wx.ALL | wx.EXPAND, 3)
        comp_main_cfg_sizer.Add(comp_path_sizer, 0, wx.ALL | wx.EXPAND, 3)
        # build comp Name Sizer ==================================
        # Source Channel List
        self.cnl_tree_src = wx.dataview.TreeListCtrl(self,
                                                     size=(-1, -1),
                                                     style=wx.LC_REPORT)
        comp_main_cfg_sizer.Add(self.cnl_tree_src, 1, wx.ALL | wx.EXPAND, 3)
        self.cnl_tree_src.AppendColumn('Group Channel', width=100)
        self.cnl_tree_src.AppendColumn('Channel Link')
        self.cnl_tree_src.AppendColumn('Dependency')
        self.cnl_tree_src.AppendColumn('Push')
        self.cnl_tree_src.AppendColumn('Pull')
        topSizer.Add(comp_main_cfg_sizer, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(topSizer)
        self.comp_list.Bind(wx.EVT_LIST_ITEM_SELECTED,
                            self.OnComponentSelected)
        self.comp_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnCompRightDown)
        self.comp_list.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.OnCompRightDown)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        """Refresh Graphics."""
        # width, height = self.cnl_list.GetSize()
        # for i in range(2):
        #     self.cnl_list.SetColumnWidth(i, width / 2)
        # evt.Skip()

    def OnComponentSelected(self, event):
        """Call Action when component in list is selected."""
        comp = event.GetText()
        self.curPrj.activeComponent = comp
        self.showCompConfig(comp)

    def OnGroupSelected(self, event):
        """Call Action when component in list is selected."""
        grp = event.GetText()
        self.curPrj.activeGroup = grp
        self.showGroupConfig(self.curPrj.activeComponent, grp)

    def OnChannelSelected(self, event):
        """Call Action when channel in list is selected."""
        cnl = event.GetText()
        self.curPrj.activeChannel = cnl

    def OnCompRightDown(self, event):
        """Execute the right click Event."""
        menu = CompPopupMenu(self, "gray")
        self.PopupMenu(menu)
        menu.Destroy()

    def OnGroupRightDown(self, event):
        """Execute the right click Event."""
        menu = GroupPopupMenu(self, "gray")
        self.PopupMenu(menu)
        menu.Destroy()

    def OnChannelRightDown(self, event):
        """Execute the right click Event."""
        menu = ChannelPopupMenu(self, "gray")
        self.PopupMenu(menu)
        menu.Destroy()

    def showCompConfig(self, comp):
        """Show component Channels on Panel."""
        # Update Name

        comp_name = comp
        self.comp_name_txt.SetValue(comp_name)
        # Update Git
        comp_git = self.curPrj.GetPrjCompGit(comp)
        self.comp_git_txt.SetValue(comp_git)
        # Update Path
        comp_path = self.curPrj.GetPrjCompPath(comp)
        self.comp_path_txt.SetValue(comp_path)
        self.main_window.build_panel.UpdateGroupSrcTreeList(comp, self.cnl_tree_src)

    def showGroupConfig(self, comp, grp):
        """Show component Channels on Panel."""
        self.cnl_list.DeleteAllItems()
        # Channels Iterate
        cnl_list = self.curPrj.GetPrjCompGrpCnlList(comp, grp)
        for cnl in cnl_list:
            index = 0
            self.cnl_list.InsertItem(index, cnl)
            lnk = self.curPrj.GetPrjGrpCnlLink(comp, grp, cnl)
            self.cnl_list.SetItem(index, 1, lnk)
        return

    def UpdateProjectComptList(self):
        """Show component on Panel."""
        sel_comp = self.main_window.build_panel.UpdateProjectCompList(self.comp_list)
