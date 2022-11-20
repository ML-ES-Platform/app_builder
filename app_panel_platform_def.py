"""GUI - Project configuration Panel."""
import wx
from wx import *
import app_builder_prj as app_prj
import app_builder_utils as utils


class PlatformDefPanel(wx.Panel):
    """Main config window Component Panel."""
    def __init__(self, parent, curPrj, panel_color):
        """Init Main config window Component Panel."""
        self.curPrj = app_prj.AppBuilderProject("")

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
                                           'Component Name : ',
                                           wx.DefaultPosition,
                                           wx.Size(100, -1), wx.ALIGN_RIGHT)
        comp_name_sizer.Add(self.comp_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        self.comp_name_txt = wx.TextCtrl(self, wx.ID_ANY | wx.TE_READONLY, '')
        comp_name_sizer.Add(self.comp_name_txt, 1, wx.ALL | wx.EXPAND, 3)

        comp_main_cfg_sizer.Add(comp_name_sizer, 0, wx.ALL | wx.EXPAND, 3)

        # build comp Name Sizer ==================================
        # Definition Tree List
        self.panel_item_tree = wx.dataview.TreeListCtrl(self,
                                                 size=(-1, -1),
                                                 style=wx.LC_REPORT)
        comp_main_cfg_sizer.Add(self.panel_item_tree, 1, wx.ALL | wx.EXPAND, 3)
        self.panel_item_tree.AppendColumn('Definition Name', width=200)
        self.panel_item_tree.AppendColumn('Value')

        self.panel_item_tree.Bind(wx.dataview.EVT_TREELIST_SELECTION_CHANGED,
                           self.OnTreeListSelected)
        # Comp Git line ====================================================
        tree_path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.tree_path_lbl = wx.StaticText(self, wx.ID_ANY,
                                           'Definition Path : ',
                                           wx.DefaultPosition,
                                           wx.Size(120, -1), wx.ALIGN_RIGHT)
        tree_path_sizer.Add(self.tree_path_lbl, 0, wx.ALL | wx.EXPAND, 3)
        self.tree_path_txt = wx.TextCtrl(self, wx.ID_ANY | wx.TE_READONLY, '')
        tree_path_sizer.Add(self.tree_path_txt, 1, wx.ALL | wx.EXPAND, 3)
        comp_main_cfg_sizer.Add(tree_path_sizer, 0, wx.ALL | wx.EXPAND, 3)
        # Comp Path line ====================================================
        tree_value_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.path_lbl = wx.StaticText(self, wx.ID_ANY, 'Definition Value : ',
                                      wx.DefaultPosition, wx.Size(120, -1),
                                      wx.ALIGN_RIGHT)
        tree_value_sizer.Add(self.path_lbl, 0, wx.ALL | wx.EXPAND, 3)
        self.tree_value_txt = wx.TextCtrl(self, wx.ID_ANY | wx.TE_READONLY, '')
        tree_value_sizer.Add(self.tree_value_txt, 1, wx.ALL | wx.EXPAND, 3)
        comp_main_cfg_sizer.Add(tree_value_sizer, 0, wx.ALL | wx.EXPAND, 3)

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

        # Update Path
        comp_path = self.curPrj.GetPrjCompPath(comp)
        self.tree_value_txt.SetValue(comp_path)

        utils.ShowCompDef(self.curPrj.JSON_comp_config, self.panel_item_tree, comp)

        # Update Tree Path
        tree_path = utils.GetSelectedTreePath(self.panel_item_tree)
        self.tree_path_txt.SetValue(
            str(tree_path)[2:-2].replace("\",\"", " / "))

    def OnTreeListSelected(self, event):
        """Call Action when component in list is selected."""
        sel_item = event.GetItem()
        item_name = self.panel_item_tree.GetItemText(sel_item)

        # Update Tree Path
        tree_path = utils.GetSelectedTreePath(self.panel_item_tree)
        self.tree_path_txt.SetValue(
            str(tree_path)[2:-2].replace("', '", " / "))

        item_val = self.curPrj.GetValueByKeyList(self.curPrj.JSON_comp_config,
                                                    ["Components"] + tree_path)
        self.tree_value_txt.SetValue(str(item_val))

        print(item_name)
        print(str(tree_path))

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
        sel_comp = self.main_window.build_panel.UpdateProjectCompList(
            self.comp_list)

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
