"""GUI For Application Builder."""

import wx
import wx.dataview

import json
import app_builder_gen
import app_builder_prj

import requests
from pathlib import Path
import os

#https://www.techiediaries.com/python-gui-wxpython-tutorial-urllib-json/
#https://wiki.wxpython.org/PopupMenuRevised#CA-820ada62f4d016da4f82cd230d4ce75424bf9c3f_43
# TODO https://pythonspot.com/wxpython-tabs/

# some JSON:

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


class ProjectConfigPanel(wx.Panel):
    """Main config window Component Panel."""
    def __init__(self, parent):
        """Init Main config window Component Panel."""
        self.parent = parent
        wx.Panel.__init__(self, parent)

        self.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
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
        curPrj.activeComponent = comp
        self.showCompConfig(comp)

    def OnGroupSelected(self, event):
        """Call Action when component in list is selected."""
        grp = event.GetText()
        curPrj.activeGroup = grp
        self.showGroupConfig(curPrj.activeComponent, grp)

    def OnChannelSelected(self, event):
        """Call Action when channel in list is selected."""
        cnl = event.GetText()
        curPrj.activeChannel = cnl

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
        comp_name = curPrj.GetPrjCompName(comp)
        self.comp_name_txt.SetValue(comp_name)

        # Update Git
        comp_git = curPrj.GetPrjCompGit(comp)
        self.comp_git_txt.SetValue(comp_git)

        # Update Path
        comp_path = curPrj.GetPrjCompPath(comp)
        self.comp_path_txt.SetValue(comp_path)

        self.UpdateGroupListSrc(comp)

    def UpdateGroupListSrc(self, comp):
        """Show component on Panel."""
        # global curPrj
        grp_list = curPrj.GetPrjGrpList(comp)
        self.cnl_tree_src.DeleteAllItems()
        root = self.cnl_tree_src.GetRootItem()
        # Groups Iterate
        for grp in grp_list:
            child = self.cnl_tree_src.AppendItem(root, grp)
            cnl_list = curPrj.GetPrjGrpCnlList(comp, grp)
            for cnl in cnl_list:
                cnl_item = self.cnl_tree_src.AppendItem(child, cnl)
                # Show Link
                res = curPrj.GetPrjGrpCnlLink(comp, grp, cnl)
                self.cnl_tree_src.SetItemText(cnl_item, 1, res)
                # Show Dependency
                res = curPrj.GetPrjCompGrpDep(comp, grp)
                self.cnl_tree_src.SetItemText(cnl_item, 2, res)
                # Show Push
                res = curPrj.GetPrjCompGrpPush(comp, grp)
                self.cnl_tree_src.SetItemText(cnl_item, 3, res)
                # Show Link
                res = curPrj.GetPrjCompGrpPull(comp, grp)
                self.cnl_tree_src.SetItemText(cnl_item, 4, res)

            self.cnl_tree_src.Expand(child)

    def showGroupConfig(self, comp, grp):
        """Show component Channels on Panel."""
        self.cnl_list.DeleteAllItems()
        # Channels Iterate
        cnl_list = curPrj.GetPrjGrpCnlList(comp, grp)
        for cnl in cnl_list:
            index = 0
            self.cnl_list.InsertItem(index, cnl)
            lnk = curPrj.GetPrjGrpCnlLink(comp, grp, cnl)
            self.cnl_list.SetItem(index, 1, lnk)

        return

    def UpdateProjectComptList(self):
        """Show component on Panel."""
        # global curPrj
        comp_list = curPrj.GetProjectCompList()
        self.comp_list.DeleteAllItems()
        # Groups Iterate
        for comp in comp_list:
            self.comp_list.InsertItem(0, comp)


class PlatformPanel(wx.Panel):
    """Panel for component list and the references in the project and git."""
    def __init__(self, parent):
        """Init Component list Panel."""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(app_panel_color)

        self.parent = parent

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

        res = curPrj.LoadCompConfigFile(comp)
        # if res == True:
        res = curPrj.GetPlatformCompName(comp)
        self.comp_name_txt.SetValue(res)

        res = curPrj.GetPlatformCompGit(comp)
        self.comp_git_txt.SetValue(res)

        res = curPrj.GetPlatformCompPath(comp)
        self.comp_path_txt.SetValue(res)

        item_list = curPrj.GetDefCompGrpList(comp)
        self.grp_list.DeleteAllItems()
        for item in item_list:
            self.grp_list.InsertItem(0, item)

        item_list = curPrj.GetDefCompGrpNameList(comp)
        self.grp_name_txt.SetValue(str(item_list))

        item_list = curPrj.GetDefCompDefineList(comp)
        self.def_list.DeleteAllItems()
        for item in item_list:
            self.def_list.InsertItem(0, item)

        item_list = curPrj.GetDefCompPushList(comp)
        self.grp_push_list.DeleteAllItems()
        for item in item_list:
            self.grp_push_list.InsertItem(0, item)

        item_list = curPrj.GetDefCompPullList(comp)
        self.grp_pull_list.DeleteAllItems()
        for item in item_list:
            self.grp_pull_list.InsertItem(0, item)

        item_list = curPrj.GetDefCompDepList(comp)
        self.grp_dep_list.DeleteAllItems()
        for item in item_list:
            self.grp_dep_list.InsertItem(0, item)

    def OnGroupSelected(self, event):
        grp = event.GetText()
        comp = self.compSelected
        self.UpdateGroupView(comp, grp)

    def UpdateGroupView(self, comp, grp):

        res = curPrj.GetDefCompGrpName(comp, grp)
        self.grp_name_txt.SetValue(res)

        res = curPrj.GetDefCompGrpMultiplicity(comp, grp)
        self.grp_mult_txt.SetValue(res)

        res = curPrj.GetDefCompGrpNamespace(comp, grp)
        self.grp_name_space_txt.SetValue(res)

        item_list = curPrj.GetDefCompGrpDefList(comp, grp)
        self.def_list.DeleteAllItems()
        for item in item_list:
            self.def_list.InsertItem(0, item)

        item_list = curPrj.GetDefCompGrpPushList(comp, grp)
        self.grp_push_list.DeleteAllItems()
        for item in item_list:
            self.grp_push_list.InsertItem(0, item)

        item_list = curPrj.GetDefCompGrpPullList(comp, grp)
        self.grp_pull_list.DeleteAllItems()
        for item in item_list:
            self.grp_pull_list.InsertItem(0, item)

        item_list = curPrj.GetDefCompGrpDepList(comp, grp)
        self.grp_dep_list.DeleteAllItems()
        for item in item_list:
            self.grp_dep_list.InsertItem(0, item)

        res = curPrj.GetDefCompCnlNameSpace(comp, grp)
        self.cnl_name_space_txt.SetValue(res)

        res = curPrj.GetDefCompCnlMultiplicity(comp, grp)
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
        the_list = curPrj.GetPlatformCompList()
        for comp in the_list:
            self.comp_list.InsertItem(0, comp)

            # Mark Installed component
            res = curPrj.GetPrjCompName(comp)
            if res != "null":
                self.comp_list.SetItemTextColour(0, "blue")
            # Mark Unavailable component
            curPrj.LoadCompConfigFile(comp)
            res = curPrj.GetPlatformCompName(comp)
            if res == "null":
                self.comp_list.SetItemTextColour(0, "red")

        return


class ProjectBuilderPanel(wx.Panel):
    """Panel for component list and the references in the project and git."""
    def __init__(self, parent):
        """Init Component list Panel."""
        self.parent = parent

        self.activeCompSrc = "null"
        self.activeCompDst = "null"
        self.activeGrpSrc = "null"
        self.activeGrpDst = "null"

        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(app_panel_color)

        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # All component elements
        build_tree_sizer = wx.BoxSizer(wx.VERTICAL)

        # build comp Name Sizer ==================================
        linkSrcSizer = wx.BoxSizer(wx.HORIZONTAL)
        # Link source component List
        self.comp_list_src = wx.ListCtrl(self, style=wx.LC_REPORT)
        linkSrcSizer.Add(self.comp_list_src, 0, wx.ALL | wx.EXPAND, 3)
        self.comp_list_src.InsertColumn(0, " Source Component", width=150)
        self.comp_list_src.Bind(wx.EVT_LIST_ITEM_SELECTED,
                                self.OnCompSrcSelected)

        # Source Channel List
        self.cnl_tree_src = wx.dataview.TreeListCtrl(self,
                                                     size=(-1, -1),
                                                     style=wx.LC_REPORT
                                                     | wx.EXPAND)
        linkSrcSizer.Add(self.cnl_tree_src, 1, wx.ALL | wx.EXPAND, 3)
        self.cnl_tree_src.AppendColumn('Channel ', width=100)
        self.cnl_tree_src.AppendColumn('Channel Link')
        self.cnl_tree_src.AppendColumn('Dependency')
        self.cnl_tree_src.AppendColumn('Push')
        self.cnl_tree_src.AppendColumn('Pull')
        self.cnl_tree_src.Bind(wx.dataview.EVT_TREELIST_SELECTION_CHANGED,
                               self.OnCompGrpSrcSelected)

        # Auto fill from destination tree
        autoFillSrcSizer = wx.BoxSizer(wx.VERTICAL)

        self.fill_src_btn = wx.Button(self, -1, 'Fill settings')
        autoFillSrcSizer.Add(self.fill_src_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.fill_src_btn.Bind(wx.EVT_BUTTON, self.OnAddGroupBtnClicked)

        self.auto_src_cb = wx.CheckBox(self, wx.ID_ANY, u"Auto fill")
        autoFillSrcSizer.Add(self.auto_src_cb, 0, wx.ALL, 5)

        linkSrcSizer.Add(autoFillSrcSizer, 0, wx.ALL | wx.EXPAND, 3)

        build_tree_sizer.Add(linkSrcSizer, 1, wx.ALL | wx.EXPAND, 3)

        # build dependency tree Sizer ==================================
        dependencySizer = wx.BoxSizer(wx.HORIZONTAL)

        # dependency component List

        self.comp_tree_dep = wx.TreeCtrl(self, wx.ID_ANY, wx.DefaultPosition,
                                         wx.Size(150, 150))
        dependencySizer.Add(self.comp_tree_dep, 1, wx.ALL | wx.EXPAND, 3)

        # Auto fill from destination tree
        autoFillTreeSizer = wx.BoxSizer(wx.VERTICAL)

        self.dep_add_btn = wx.Button(self, -1, 'Fill settings')
        autoFillTreeSizer.Add(self.dep_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.dep_add_btn.Bind(wx.EVT_BUTTON, self.OnAddDepBtnClicked)

        self.auto_tree_cb = wx.CheckBox(self, wx.ID_ANY, u"Auto fill")
        autoFillTreeSizer.Add(self.auto_tree_cb, 0, wx.ALL, 5)

        # self. = wx.Button(self, -1, 'Fill settings')
        # .Add(self., 0, wx.ALL | wx.EXPAND, 3)
        # self..Bind(wx.EVT_BUTTON, self.)

        dependencySizer.Add(autoFillTreeSizer, 0, wx.ALL | wx.EXPAND, 3)

        build_tree_sizer.Add(dependencySizer, 1, wx.ALL | wx.EXPAND, 3)

        # build comp Name Sizer ==================================
        linkDstSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Link destination component List
        self.comp_list_dst = wx.ListCtrl(self, style=wx.LC_REPORT)
        linkDstSizer.Add(self.comp_list_dst, 0, wx.ALL | wx.EXPAND, 3)
        self.comp_list_dst.InsertColumn(0, " Destination Component", width=150)
        self.comp_list_dst.Bind(wx.EVT_LIST_ITEM_SELECTED,
                                self.OnCompDstSelected)

        # Destination Channel List
        self.cnl_tree_dst = wx.dataview.TreeListCtrl(self,
                                                     size=(-1, -1),
                                                     style=wx.LC_REPORT
                                                     | wx.EXPAND)
        linkDstSizer.Add(self.cnl_tree_dst, 1, wx.ALL | wx.EXPAND, 3)
        self.cnl_tree_dst.AppendColumn('Channel', width=100)
        self.cnl_tree_dst.AppendColumn('Channel Link')
        self.cnl_tree_dst.AppendColumn('Dependency')
        self.cnl_tree_dst.AppendColumn('Push')
        self.cnl_tree_dst.AppendColumn('Pull')
        self.cnl_tree_dst.Bind(wx.dataview.EVT_TREELIST_SELECTION_CHANGED,
                               self.OnCompGrpDstSelected)

        # Auto fill from destination tree
        autoFillDstSizer = wx.BoxSizer(wx.VERTICAL)

        self.fill_dst_btn = wx.Button(self, -1, 'Fill settings')
        autoFillDstSizer.Add(self.fill_dst_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.fill_dst_btn.Bind(wx.EVT_BUTTON, self.OnCompDstSelected)


        self.auto_dst_cb = wx.CheckBox(self, wx.ID_ANY, u"Auto fill")
        autoFillDstSizer.Add(self.auto_dst_cb, 0, wx.ALL, 5)

        linkDstSizer.Add(autoFillDstSizer, 0, wx.ALL | wx.EXPAND, 3)

        # build comp Name Sizer
        build_tree_sizer.Add(linkDstSizer, 1, wx.ALL | wx.EXPAND, 3)

        top_sizer.Add(build_tree_sizer, 1, wx.ALL | wx.EXPAND, 3)

        # build Edit / Add Sizer ==================================
        editSizer = wx.BoxSizer(wx.VERTICAL)

        self.comp_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Component')
        editSizer.Add(self.comp_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        # self.comp_name_txt = wx.TextCtrl(self, wx.ID_ANY | wx.EXPAND, '')
        # editSizer.Add(self.comp_name_txt, 0, wx.ALL | wx.EXPAND, 3)
        comp_name_cb_choices = []
        self.comp_name_cb = wx.ComboBox( self, wx.ID_ANY, u"none", wx.DefaultPosition, wx.DefaultSize, comp_name_cb_choices, 0 )
        editSizer.Add( self.comp_name_cb, 0, wx.ALL, 5 )

        self.comp_add_btn = wx.Button(self, -1, 'Add Component')
        editSizer.Add(self.comp_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.comp_add_btn.Bind(wx.EVT_BUTTON, self.OnAddCompBtnClicked)

        self.grp_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Group')
        editSizer.Add(self.grp_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        # self.grp_name_txt = wx.TextCtrl(self, wx.ID_ANY | wx.EXPAND, '')
        # editSizer.Add(self.grp_name_txt, 0, wx.ALL | wx.EXPAND, 3)
        grp_name_cb_choices = []
        self.grp_name_cb = wx.ComboBox( self, wx.ID_ANY, u"none", wx.DefaultPosition, wx.DefaultSize, grp_name_cb_choices, 0 )
        editSizer.Add( self.grp_name_cb, 0, wx.ALL, 5 )
        self.grp_add_btn = wx.Button(self, -1, 'Add Group')
        editSizer.Add(self.grp_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.grp_add_btn.Bind(wx.EVT_BUTTON, self.OnAddGroupBtnClicked)

        self.cnl_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Channel')
        editSizer.Add(self.cnl_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        # self.cnl_name_txt = wx.TextCtrl(self, wx.ID_ANY | wx.EXPAND, '')
        # editSizer.Add(self.cnl_name_txt, 0, wx.ALL | wx.EXPAND, 3)
        cnl_name_cb_choices = []
        self.cnl_name_cb = wx.ComboBox( self, wx.ID_ANY, u"none", wx.DefaultPosition, wx.DefaultSize, cnl_name_cb_choices, 0 )
        editSizer.Add( self.cnl_name_cb, 0, wx.ALL, 5 )
        self.cnl_add_btn = wx.Button(self, -1, 'Add Channel')
        editSizer.Add(self.cnl_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.cnl_add_btn.Bind(wx.EVT_BUTTON, self.OnAddChannelBtnClicked)

        self.link_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Link')
        editSizer.Add(self.link_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        # self.link_name_txt = wx.TextCtrl(self, wx.ID_ANY | wx.EXPAND, '')
        # editSizer.Add(self.link_name_txt, 0, wx.ALL | wx.EXPAND, 3)
        link_name_cb_choices = []
        self.link_name_cb = wx.ComboBox( self, wx.ID_ANY, u"none", wx.DefaultPosition, wx.DefaultSize, link_name_cb_choices, 0 )
        editSizer.Add( self.link_name_cb, 0, wx.ALL, 5 )
        self.link_add_btn = wx.Button(self, -1, 'Add Link')
        editSizer.Add(self.link_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.link_add_btn.Bind(wx.EVT_BUTTON, self.OnAddLinkBtnClicked)

        self.dep_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Dependency')
        editSizer.Add(self.dep_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        # self.dep_name_txt = wx.TextCtrl(self, wx.ID_ANY | wx.EXPAND, '')
        # editSizer.Add(self.dep_name_txt, 0, wx.ALL | wx.EXPAND, 3)
        dep_name_cb_choices = []
        self.dep_name_cb = wx.ComboBox( self, wx.ID_ANY, u"none", wx.DefaultPosition, wx.DefaultSize, dep_name_cb_choices, 0 )
        editSizer.Add( self.dep_name_cb, 0, wx.ALL, 5 )
        self.dep_add_btn = wx.Button(self, -1, 'Add Dependency')
        editSizer.Add(self.dep_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.dep_add_btn.Bind(wx.EVT_BUTTON, self.OnAddDepBtnClicked)

        self.push_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Push')
        editSizer.Add(self.push_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        # self.push_name_txt = wx.TextCtrl(self, wx.ID_ANY | wx.EXPAND, '')
        # editSizer.Add(self.push_name_txt, 0, wx.ALL | wx.EXPAND, 3)
        push_name_cb_choices = []
        self.push_name_cb = wx.ComboBox( self, wx.ID_ANY, u"none", wx.DefaultPosition, wx.DefaultSize, push_name_cb_choices, 0 )
        editSizer.Add( self.push_name_cb, 0, wx.ALL, 5 )
        self.push_add_btn = wx.Button(self, -1, 'Add Push')
        editSizer.Add(self.push_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.push_add_btn.Bind(wx.EVT_BUTTON, self.OnAddPushBtnClicked)

        self.pull_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Pull')
        editSizer.Add(self.pull_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        # self.pull_name_txt = wx.TextCtrl(self, wx.ID_ANY | wx.EXPAND, '')
        # editSizer.Add(self.pull_name_txt, 0, wx.ALL | wx.EXPAND, 3)
        pull_name_cb_choices = []
        self.pull_name_cb = wx.ComboBox( self, wx.ID_ANY, u"none", wx.DefaultPosition, wx.DefaultSize, pull_name_cb_choices, 0 )
        editSizer.Add( self.pull_name_cb, 0, wx.ALL, 5 )
        self.pull_add_btn = wx.Button(self, -1, 'Add Pull')
        editSizer.Add(self.pull_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.pull_add_btn.Bind(wx.EVT_BUTTON, self.OnAddPullBtnClicked)

        top_sizer.Add(editSizer, 0, wx.ALL | wx.EXPAND, 3)

        self.SetSizer(top_sizer)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.UpdateCompList()
        comp = curPrj.activeComponent
        self.UpdateGroupListSrc(comp)
        self.UpdateGroupListDst(comp)

    def OnEnterWindow(self, event):
        self.UpdateCompList()
        comp = curPrj.activeComponent
        self.UpdateGroupListSrc(comp)
        self.UpdateGroupListDst(comp)

    def OnAddCompBtnClicked(self, event):
        comp_name = self.comp_name_cb.GetValue()

        curPrj.activeComponent = comp_name


        print("====================================")
        print(curPrj.JSON_project)

        curPrj.AddPrjComp(comp_name)
        print(curPrj.JSON_project)

        curPrj.SetPrjCompName(comp_name, comp_name)
        print(curPrj.JSON_project)


        self.UpdateCompList()

        


    def OnAddGroupBtnClicked(self, event):

        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()


        print("====================================")
        print(curPrj.JSON_project)

        curPrj.AddPrjCompGrp(comp_name, grp_name)
        print(curPrj.JSON_project)

        curPrj.SetPrjCompGrpName(comp_name, grp_name, grp_name)
        print(curPrj.JSON_project)

        self.UpdateCompList()

        return

    def OnAddChannelBtnClicked(self, event):

        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        cnl_name = self.cnl_name_cb.GetValue()

        print("====================================")
        print(curPrj.JSON_project)

        curPrj.AddPrjCompGrpCnl(comp_name, grp_name, cnl_name)
        print(curPrj.JSON_project)

        self.UpdateCompList()

        return

    def OnAddLinkBtnClicked(self, event):

        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        cnl_name = self.cnl_name_cb.GetValue()
        link_name = self.link_name_cb.GetValue()

        print("====================================")
        print(curPrj.JSON_project)

        curPrj.AddPrjCompGrpCnlLink(comp_name, grp_name, cnl_name, link_name)
        print(curPrj.JSON_project)

        self.UpdateCompList()

        return

    def OnAddDepBtnClicked(self, event):

        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        dep_name = self.dep_name_cb.GetValue()

        print("====================================")
        print(curPrj.JSON_project)

        curPrj.SetPrjCompGrpDep(comp_name, grp_name, dep_name)
        print(curPrj.JSON_project)

        self.UpdateCompList()

        return

    def OnAddPushBtnClicked(self, event):

        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        push_name = self.push_name_cb.GetValue()

        print("====================================")
        print(curPrj.JSON_project)

        curPrj.SetPrjCompGrpPush(comp_name, grp_name, push_name)
        print(curPrj.JSON_project)

        self.UpdateCompList()

        return

    def OnAddPullBtnClicked(self, event):

        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        pull_name = self.pull_name_cb.GetValue()

        print("====================================")
        print(curPrj.JSON_project)

        curPrj.SetPrjCompGrpPull(comp_name, grp_name, pull_name)
        print(curPrj.JSON_project)

        self.UpdateCompList()

        return


    def OnPaint(self, evt):
        """Update window."""
        width, height = self.comp_list_src.GetSize()
        self.comp_list_src.SetColumnWidth(0, width)
        # self.comp_list.SetColumnWidth(1, 150)
        # self.comp_list.SetColumnWidth(2, width - 300)
        evt.Skip()

    def UpdateCompList(self):
        """Show component on Panel."""
        # global curPrj
        comp_list = curPrj.GetProjectCompList()

        self.comp_list_src.DeleteAllItems()
        self.comp_list_dst.DeleteAllItems()
        # Groups Iterate
        for comp in comp_list:
            self.comp_list_src.InsertItem(0, comp)
            self.comp_list_dst.InsertItem(0, comp)
            # Mark installed components
            res = curPrj.GetPrjCompName(comp)
            if res != "null":
                self.comp_list_src.SetItemTextColour(0, "blue")
                self.comp_list_dst.SetItemTextColour(0, "blue")
            # Mark unavailable components
            curPrj.LoadCompConfigFile(comp)
            res = curPrj.GetPlatformCompName(comp)
            if res == "null":
                self.comp_list_src.SetItemTextColour(0, "red")
                self.comp_list_dst.SetItemTextColour(0, "red")




    def UpdateGroupListSrc(self, comp):
        """Show component on Panel."""
        # global curPrj
        grp_list = curPrj.GetPrjGrpList(comp)

        self.cnl_tree_src.DeleteAllItems()
        root = self.cnl_tree_src.GetRootItem()
        # Groups Iterate
        for grp in grp_list:
            child = self.cnl_tree_src.AppendItem(root, grp)

            cnl_list = curPrj.GetPrjGrpCnlList(comp, grp)
            for cnl in cnl_list:
                cnl_item = self.cnl_tree_src.AppendItem(child, cnl)
                # Show Link
                cnl_link = curPrj.GetPrjGrpCnlLink(comp, grp, cnl)
                self.cnl_tree_src.SetItemText(cnl_item, 1, cnl_link)
                # Show Dependency
                res = curPrj.GetPrjCompGrpDep(comp, grp)
                self.cnl_tree_src.SetItemText(cnl_item, 2, res)
                # Show Push
                res = curPrj.GetPrjCompGrpPush(comp, grp)
                self.cnl_tree_src.SetItemText(cnl_item, 3, res)
                # Show Link
                res = curPrj.GetPrjCompGrpPull(comp, grp)
                self.cnl_tree_src.SetItemText(cnl_item, 4, res)

            self.cnl_tree_src.Expand(child)

    def UpdateGroupListDst(self, comp):
        """Show component on Panel."""
        # global curPrj
        grp_list = curPrj.GetPrjGrpList(comp)

        self.cnl_tree_dst.DeleteAllItems()
        root = self.cnl_tree_dst.GetRootItem()
        # Groups Iterate
        for grp in grp_list:
            child = self.cnl_tree_dst.AppendItem(root, grp)

            cnl_list = curPrj.GetPrjGrpCnlList(comp, grp)
            for cnl in cnl_list:
                cnl_item = self.cnl_tree_dst.AppendItem(child, cnl)
                # Show Link
                cnl_link = curPrj.GetPrjGrpCnlLink(comp, grp, cnl)
                self.cnl_tree_dst.SetItemText(cnl_item, 1, cnl_link)
                # Show Dependency
                res = curPrj.GetPrjCompGrpDep(comp, grp)
                self.cnl_tree_dst.SetItemText(cnl_item, 2, res)
                # Show Push
                res = curPrj.GetPrjCompGrpPush(comp, grp)
                self.cnl_tree_dst.SetItemText(cnl_item, 3, res)
                # Show Pull
                res = curPrj.GetPrjCompGrpPull(comp, grp)
                self.cnl_tree_dst.SetItemText(cnl_item, 4, res)

            self.cnl_tree_dst.Expand(child)

    def OnCompSrcSelected(self, event):
        """Call Action when component in list is selected."""
        comp = event.GetText()
        self.activeCompSrc = comp

        self.UpdateGroupListSrc(comp)
        self.BuildDependencyTree(comp)

        self.comp_name_cb.SetValue(comp)

    def OnCompDstSelected(self, event):
        """Call Action when component in list is selected."""
        comp = event.GetText()
        self.activeCompDst = comp
        self.UpdateGroupListDst(comp)
        self.dep_name_cb.SetValue(comp)

    def GetTreeLevel(self, tree, item):
        # first level back
        tmp_grp_item = tree.GetItemParent(item)
        # second Level Back
        tmp_root_item = self.cnl_tree_src.GetItemParent(tmp_grp_item)

        if tmp_root_item.IsOk():
            return "Channel"
        else:
            return "Group"

    def OnCompGrpSrcSelected(self, event):
        """Call Action when component in list is selected."""
        sel_item = event.GetItem()

        level = self.GetTreeLevel(self.cnl_tree_src, sel_item)

        if level == "Channel":
            cnl_item = sel_item
            grp_item = self.cnl_tree_src.GetItemParent(cnl_item)
            cnl_name = self.cnl_tree_src.GetItemText(cnl_item)
        else:
            cnl_item = "null"
            cnl_name = "null"
            grp_item = sel_item

        self.cnl_name_cb.SetValue(cnl_name)

        grp_name = self.cnl_tree_src.GetItemText(grp_item)
        self.grp_name_cb.SetValue(grp_name)

        link_name = self.cnl_tree_src.GetItemText(sel_item, 1)
        self.link_name_cb.SetValue(link_name)

        dep_name = self.cnl_tree_src.GetItemText(sel_item, 2)
        self.dep_name_cb.SetValue(dep_name)

        push_name = self.cnl_tree_src.GetItemText(sel_item, 3)
        self.push_name_cb.SetValue(push_name)

        pull_name = self.cnl_tree_src.GetItemText(sel_item, 4)
        self.pull_name_cb.SetValue(pull_name)

    def OnCompGrpDstSelected(self, event):
        """Call Action when component in list is selected."""
        sel_item = event.GetItem()

        level = self.GetTreeLevel(self.cnl_tree_src, sel_item)

        if level == "Channel":
            cnl_item = sel_item
            grp_item = self.cnl_tree_src.GetItemParent(cnl_item)
            cnl_name = self.cnl_tree_src.GetItemText(cnl_item)
        else:
            cnl_item = "null"
            cnl_name = "null"
            grp_item = sel_item

    def BuildDependencyTree(self, comp):

        self.comp_tree_dep.DeleteAllItems()

        root = self.comp_tree_dep.AddRoot(comp)
        self.BuildTreeDependency(root, comp)
        self.comp_tree_dep.ExpandAll()

    def BuildTreeDependency(self, parent, comp):
        curPrj.LoadCompConfigFile(comp)
        dep_list = curPrj.GetDefCompDepList(comp)
        for comp_it in dep_list:
            if str(comp_it) != str(comp):
                child = self.comp_tree_dep.AppendItem(parent, comp_it)

                # Mark installed components
                res = curPrj.GetPrjCompName(comp_it)
                if res != "null":
                    self.comp_tree_dep.SetItemTextColour(child, "blue")
                # Mark unavailable components
                curPrj.LoadCompConfigFile(comp_it)
                res = curPrj.GetPlatformCompName(comp_it)
                if res == "null":
                    self.comp_tree_dep.SetItemTextColour(child, "red")

                # self.comp_tree_dep.SetItemTextColour(child,"red")
                # self.comp_tree_dep.SetItemBackgroundColour(child,"green")
                self.BuildTreeDependency(child, comp_it)


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
        curPrj.AddProjectCompFromPlatform(self.comp)

        window.prj_panel.UpdateProjectComptList()
        window.comp_panel.UpdatePlatformComptList()


class CompPopupMenu(wx.Menu):
    """Component Mangement PopUp menu."""
    def __init__(self, parent, title):
        """Component Mangement PopUp menu init."""
        wx.Menu.__init__(self)

        self.WinName = title
        self.parent = parent

        item = wx.MenuItem(self, wx.ID_ANY, "Add Component")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnAddComponent, item)

        item = wx.MenuItem(self, wx.ID_ANY, "Edit Component")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnEditPopUp, item)

        item = wx.MenuItem(self, wx.ID_ANY, "Remove Component")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnItem3, item)

    def OnAddComponent(self, event):
        """Open Platform Component List."""
        print("Item OnAddComponent selected")
        # ComponentListFrame(window, "ES Platform Component List").Show()

    def OnEditPopUp(self, event):
        """On Item Edit selected."""
        print("Item OnEditPopUp selected")
        # ComponentEditFrame(self.parent.parent.parent, "Edit").Show()

    def OnItem3(self, event):
        """On Item Three selected."""
        print("Item Three selected")


class GroupPopupMenu(wx.Menu):
    """Component Mangement PopUp menu."""
    def __init__(self, parent, title):
        """Component Mangement PopUp menu init."""
        wx.Menu.__init__(self)

        self.WinName = title
        self.parent = parent

        item = wx.MenuItem(self, wx.ID_ANY, "Add Group")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnAddGroup, item)

        item = wx.MenuItem(self, wx.ID_ANY, "Edit Group")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnEditGroup, item)

        item = wx.MenuItem(self, wx.ID_ANY, "Remove Group")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnItem3, item)

    def OnAddGroup(self, event):
        """Open Platform Component List."""
        print("Item OnAddGroup selected")
        # GroupAddFrame(self.parent.parent.parent, "Add Group to component").Show()

    def OnEditGroup(self, event):
        """On Item Edit selected."""
        print("Item OnEditGroup selected")
        # ChannelAddFrame(self.parent.parent.parent, "Edit Group").Show()

    def OnItem3(self, event):
        """On Item Three selected."""
        print("Item Three selected")


class ChannelPopupMenu(wx.Menu):
    """Component Mangement PopUp menu."""
    def __init__(self, parent, title):
        """Component Mangement PopUp menu init."""
        wx.Menu.__init__(self)

        self.WinName = title
        self.parent = parent

        item = wx.MenuItem(self, wx.ID_ANY, "Add Channel")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnAddChannel, item)

        item = wx.MenuItem(self, wx.ID_ANY, "Edit Channel")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnEditChannel, item)

        item = wx.MenuItem(self, wx.ID_ANY, "Remove Channel")
        self.Append(item)
        self.Bind(wx.EVT_MENU, self.OnItem3, item)

    def OnAddChannel(self, event):
        """Open Platform Component List."""
        print("Item OnAddChannel selected")
        # ChannelAddFrame(self.parent.parent.parent, "Add Channel to group").Show()

    def OnEditChannel(self, event):
        """On Item Edit selected."""
        print("Item OnEditChannel selected")
        # ComponentEditFrame(self.parent.parent.parent, "Edit Channel").Show()

    def OnItem3(self, event):
        """On Item Three selected."""
        print("Item Three selected")


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
        self.prj_panel = ProjectConfigPanel(nb)
        self.comp_panel = PlatformPanel(nb)
        # self.grp_panel = GroupAddPanel(nb)
        self.cnl_panel = ProjectBuilderPanel(nb)

        # Add the windows to tabs and name them.
        nb.AddPage(self.cnl_panel, "App Builder")
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
        self.cnl_panel.OnEnterWindow(event)

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
        menuCompsView = toolsMenu.Append(wx.ID_ANY, "Load Platform Components",
                                         "Load platform")
        menuCompUpdate = toolsMenu.Append(
            wx.ID_ANY, "Update Platform Components from URL",
            "Update platform")

        menuBar.Append(toolsMenu, "&Tools")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnNew, menuNew)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSave)
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
        # ComponentListFrame(self, "ES Platform Component List").Show()

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

    def OnOpen(self, event):
        """Open an existing Configuration json."""
        #TODO
        if curPrj.prjContentNotSaved:
            if wx.MessageBox("Current content has not been saved! Proceed?",
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
            try:
                curPrj.LoadProjectFile(pathname)
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)

        self.prj_panel.UpdateProjectComptList()
        curPrj.LoadPlatformFile()
        self.comp_panel.UpdatePlatformComptList()
        title = app_title + " - " + curPrj.prjFileName
        self.SetTitle(title)

    def doSaveData(self):
        """Save current Configuration to a json file."""
        # global JSON_object
        try:
            curPrj.SaveProjectFile()
        except IOError:
            pathname = curPrj.GetProjectFilePath()
            wx.LogError("Cannot save current data in file '%s'." % pathname)

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
            curPrj.SetProjectFilePath()
            self.doSaveData()

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