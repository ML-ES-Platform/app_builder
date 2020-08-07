
"""GUI - Platform Management Panel."""
import wx


class PlatformPanel(wx.Panel):
    """Panel for component list and the references in the project and git."""

    def __init__(self, parent, curPrj, panel_color):
        """Init Component list Panel."""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(panel_color)
        
        self.parent = parent
        self.curPrj = curPrj

        self.LayoutBuild()
        self.comp_list.InsertColumn(0, "Platform Component", width=150)
        self.grp_list.InsertColumn(0, "Component Groups", width=150)
        self.def_list.InsertColumn(0, "Project Defines", width=150)
        self.grp_push_list.InsertColumn(0, "Push Methods", width=150)
        self.grp_pull_list.InsertColumn(0, "Pull Methods", width=150)
        self.grp_dep_list.InsertColumn(0, "Project dependencies", width=150)
        self.UpdatePlatformComptList()
        self.comp_list.Bind(wx.EVT_LIST_ITEM_SELECTED,
                            self.OnComponentSelected)
        self.comp_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightDown)
        self.comp_list.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.OnRightDown)
        self.grp_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnGroupSelected)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.compSelected = ""

    def LayoutBuild(self):
        """Build panel Layout configuration."""
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.comp_list = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition,
                                     wx.Size(150, -1), wx.LC_REPORT)
        topSizer.Add(self.comp_list, 0, wx.ALL | wx.EXPAND, 3)
        comp_main_cfg_sizer = wx.BoxSizer(wx.VERTICAL)
        comp_name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.comp_name_lbl = wx.StaticText(self, wx.ID_ANY, u"Component Name",
                                           wx.DefaultPosition,
                                           wx.Size(100, -1), wx.ALIGN_RIGHT)
        self.comp_name_lbl.Wrap(-1)
        comp_name_sizer.Add(self.comp_name_lbl, 0, wx.ALL, 3)
        self.comp_name_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        comp_name_sizer.Add(self.comp_name_txt, 1, wx.ALL, 3)
        comp_main_cfg_sizer.Add(comp_name_sizer, 0, wx.ALL | wx.EXPAND, 3)
        comp_git_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.comp_git_lbl = wx.StaticText(self, wx.ID_ANY,
                                          u"Component Git", wx.DefaultPosition,
                                          wx.Size(100, -1), wx.ALIGN_RIGHT)
        self.comp_git_lbl.Wrap(-1)
        comp_git_sizer.Add(self.comp_git_lbl, 0, wx.ALL, 3)
        self.comp_git_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        comp_git_sizer.Add(self.comp_git_txt, 1, wx.ALL, 3)

        comp_main_cfg_sizer.Add(comp_git_sizer, 0, wx.ALL | wx.EXPAND, 3)
        comp_path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.comp_path_lbl = wx.StaticText(self, wx.ID_ANY, u"Component Path",
                                           wx.DefaultPosition,
                                           wx.Size(100, -1), wx.ALIGN_RIGHT)
        self.comp_path_lbl.Wrap(-1)
        comp_path_sizer.Add(self.comp_path_lbl, 0, wx.ALL, 3)
        self.comp_path_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        comp_path_sizer.Add(self.comp_path_txt, 1, wx.ALL, 3)
        comp_main_cfg_sizer.Add(comp_path_sizer, 0, wx.ALL | wx.EXPAND, 3)
        comp_cfg_sizer = wx.BoxSizer(wx.HORIZONTAL)
        comp_lists_cfg_sizer = wx.BoxSizer(wx.VERTICAL)
        self.grp_list = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition,
                                    wx.Size(150, 150), wx.LC_REPORT)
        comp_lists_cfg_sizer.Add(self.grp_list, 0, wx.ALL, 3)
        self.def_list = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition,
                                    wx.Size(150, 150), wx.LC_REPORT)
        comp_lists_cfg_sizer.Add(self.def_list, 0, wx.ALL, 3)
        comp_cfg_sizer.Add(comp_lists_cfg_sizer, 1, wx.EXPAND, 3)
        grp_cfg_sizer = wx.BoxSizer(wx.VERTICAL)
        grp_name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.grp_name_lbl = wx.StaticText(self, wx.ID_ANY,
                                          u"Group Name", wx.DefaultPosition,
                                          wx.Size(150, -1), wx.ALIGN_RIGHT)
        self.grp_name_lbl.Wrap(-1)
        grp_name_sizer.Add(self.grp_name_lbl, 0, wx.ALL, 3)
        self.grp_name_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        grp_name_sizer.Add(self.grp_name_txt, 1, wx.ALL, 3)
        grp_cfg_sizer.Add(grp_name_sizer, 0, wx.EXPAND, 3)
        grp_mult_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.grp_mult_lbl = wx.StaticText(self, wx.ID_ANY,
                                          u"Group Multiplicity",
                                          wx.DefaultPosition, wx.Size(150, -1),
                                          wx.ALIGN_RIGHT)
        self.grp_mult_lbl.Wrap(-1)
        grp_mult_sizer.Add(self.grp_mult_lbl, 0, wx.ALL, 3)
        self.grp_mult_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        grp_mult_sizer.Add(self.grp_mult_txt, 1, wx.ALL, 3)
        grp_cfg_sizer.Add(grp_mult_sizer, 0, wx.EXPAND, 3)
        grp_lists_cfg_sizer = wx.BoxSizer(wx.HORIZONTAL)
        grp_cfg_sizer.Add(grp_lists_cfg_sizer, 0, wx.EXPAND, 3)
        grp_name_space_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.grp_name_space_lbl = wx.StaticText(self, wx.ID_ANY,
                                                u"Group Namespace",
                                                wx.DefaultPosition,
                                                wx.Size(150,
                                                        -1), wx.ALIGN_RIGHT)
        self.grp_name_space_lbl.Wrap(-1)
        grp_name_space_sizer.Add(self.grp_name_space_lbl, 0, wx.ALL, 3)
        self.grp_name_space_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                              wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        grp_name_space_sizer.Add(self.grp_name_space_txt, 1, wx.ALL, 3)
        grp_cfg_sizer.Add(grp_name_space_sizer, 0, wx.EXPAND, 3)
        grp_lists_cfg_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.grp_push_list = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition,
                                         wx.Size(150, 150), wx.LC_REPORT)
        grp_lists_cfg_sizer.Add(self.grp_push_list, 0, wx.ALL, 3)
        self.grp_pull_list = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition,
                                         wx.Size(150, 150), wx.LC_REPORT)
        grp_lists_cfg_sizer.Add(self.grp_pull_list, 0, wx.ALL, 3)
        self.grp_dep_list = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition,
                                        wx.Size(150, 150), wx.LC_REPORT)
        grp_lists_cfg_sizer.Add(self.grp_dep_list, 0, wx.ALL, 3)
        grp_cfg_sizer.Add(grp_lists_cfg_sizer, 0, wx.EXPAND, 3)
        cnl_name_space_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cnl_name_space_lbl = wx.StaticText(self, wx.ID_ANY,
                                                u"Channel Namespace",
                                                wx.DefaultPosition,
                                                wx.Size(150,
                                                        -1), wx.ALIGN_RIGHT)
        self.cnl_name_space_lbl.Wrap(-1)
        cnl_name_space_sizer.Add(self.cnl_name_space_lbl, 0, wx.ALL, 3)
        self.cnl_name_space_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                              wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        cnl_name_space_sizer.Add(self.cnl_name_space_txt, 1, wx.ALL, 3)
        grp_cfg_sizer.Add(cnl_name_space_sizer, 0, wx.EXPAND, 3)
        cnl_mult_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cnl_mult_lbl = wx.StaticText(self, wx.ID_ANY,
                                          u"Channel Multiplicity",
                                          wx.DefaultPosition, wx.Size(150, -1),
                                          wx.ALIGN_RIGHT)
        self.cnl_mult_lbl.Wrap(-1)
        cnl_mult_sizer.Add(self.cnl_mult_lbl, 0, wx.ALL, 3)
        self.cnl_mult_txt = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        cnl_mult_sizer.Add(self.cnl_mult_txt, 1, wx.ALL, 3)
        grp_cfg_sizer.Add(cnl_mult_sizer, 0, wx.EXPAND, 3)
        comp_cfg_sizer.Add(grp_cfg_sizer, 1, wx.EXPAND, 3)
        comp_main_cfg_sizer.Add(comp_cfg_sizer, 1, wx.EXPAND, 3)
        topSizer.Add(comp_main_cfg_sizer, 1, wx.EXPAND, 3)
        self.SetSizer(topSizer)

    def OnRightDown(self, event):
        """Right Click on Comp List."""
        menu = CompListPopupMenu(self, "gray", self.compSelected)
        self.PopupMenu(menu)
        menu.Destroy()

    def OnComponentSelected(self, event):
        """Component Selection action."""
        self.compSelected = event.GetText()
        comp = self.compSelected
        self.UpdateComponentView(comp)

    def UpdateComponentView(self, comp):
        """Component Selection action."""
        # res = self.curPrj.LoadCompConfigFile(comp)
        # if res == True:
        res = self.curPrj.GetPlatformComp(comp)
        self.comp_name_txt.SetValue(res)
        res = self.curPrj.GetPlatformCompGit(comp)
        self.comp_git_txt.SetValue(res)
        res = self.curPrj.GetPlatformCompPath(comp)
        self.comp_path_txt.SetValue(res)
        item_list = self.curPrj.GetDefCompGrpList(comp)
        self.grp_list.DeleteAllItems()
        for item in item_list:
            self.grp_list.InsertItem(0, item)
        item_list = self.curPrj.GetDefCompGrpList(comp)
        self.grp_name_txt.SetValue(str(item_list))
        item_list = self.curPrj.GetDefCompDefineList(comp)
        self.def_list.DeleteAllItems()
        for item in item_list:
            self.def_list.InsertItem(0, item)
        item_list = self.curPrj.GetDefCompPushList(comp)
        self.grp_push_list.DeleteAllItems()
        for item in item_list:
            self.grp_push_list.InsertItem(0, item)
        item_list = self.curPrj.GetDefCompPullList(comp)
        self.grp_pull_list.DeleteAllItems()
        for item in item_list:
            self.grp_pull_list.InsertItem(0, item)
        item_list = self.curPrj.GetDefCompDepList(comp)
        self.grp_dep_list.DeleteAllItems()
        for item in item_list:
            self.grp_dep_list.InsertItem(0, item)

    def OnGroupSelected(self, event):
        """Handle group selection event."""
        grp = event.GetText()
        comp = self.compSelected
        self.UpdateGroupView(comp, grp)

    def UpdateGroupView(self, comp, grp):
        """Update Group list vew (ListCtrl)."""
        # self.curPrj.LoadCompConfigFile(comp)
        res = grp
        self.grp_name_txt.SetValue(res)
        res = self.curPrj.GetDefCompGrpMultiplicity(comp, grp)
        print(res)
        self.grp_mult_txt.SetValue(res)
        res = self.curPrj.GetDefCompGrpNameSpace(comp, grp)
        self.grp_name_space_txt.SetValue(res)
        item_list = self.curPrj.GetDefCompGrpDefList(comp, grp)
        self.def_list.DeleteAllItems()
        for item in item_list:
            self.def_list.InsertItem(0, item)
        item_list = self.curPrj.GetDefCompGrpPushList(comp, grp)
        self.grp_push_list.DeleteAllItems()
        for item in item_list:
            self.grp_push_list.InsertItem(0, item)
        item_list = self.curPrj.GetDefCompGrpPullList(comp, grp)
        self.grp_pull_list.DeleteAllItems()
        for item in item_list:
            self.grp_pull_list.InsertItem(0, item)
        item_list = self.curPrj.GetDefCompGrpDepList(comp, grp)
        self.grp_dep_list.DeleteAllItems()
        for item in item_list:
            self.grp_dep_list.InsertItem(0, item)
        res = self.curPrj.GetDefCompCnlNameSpace(comp, grp)
        self.cnl_name_space_txt.SetValue(res)
        res = self.curPrj.GetDefCompCnlMultiplicity(comp, grp)
        self.cnl_mult_txt.SetValue(res)

    def OnPaint(self, evt):
        """Update window."""
        width, height = self.comp_list.GetSize()
        self.comp_list.SetColumnWidth(0, 150)
        # self.comp_list.SetColumnWidth(1, 150)
        # self.comp_list.SetColumnWidth(2, width - 300)
        evt.Skip()

    def UpdatePlatformComptList(self):
        """Extract component list and the references in a panel."""
        self.comp_list.DeleteAllItems()
        comp_list = self.curPrj.GetAllCompList()
        index = 0
        for comp in comp_list:
            # Insert item in the list
            self.comp_list.InsertItem(index, comp)
            # Color Mark component in the project
            color = self.curPrj.GetCompStatusColor(comp)
            self.comp_list.SetItemTextColour(index, color)
            index += 1
                    
        return

