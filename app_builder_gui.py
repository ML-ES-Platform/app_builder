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
# http://zetcode.com/wxpython/menustoolbars/
# http://www.blog.pythonlibrary.org/2011/01/04/wxpython-wx-listctrl-tips-and-tricks/  Editable list
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

        comp_name = comp
        self.comp_name_txt.SetValue(comp_name)
        # Update Git
        comp_git = curPrj.GetPrjCompGit(comp)
        self.comp_git_txt.SetValue(comp_git)
        # Update Path
        comp_path = curPrj.GetPrjCompPath(comp)
        self.comp_path_txt.SetValue(comp_path)
        window.build_panel.UpdateGroupTreeList(comp, self.cnl_tree_src)

    def showGroupConfig(self, comp, grp):
        """Show component Channels on Panel."""
        self.cnl_list.DeleteAllItems()
        # Channels Iterate
        cnl_list = curPrj.GetPrjCompGrpCnlList(comp, grp)
        for cnl in cnl_list:
            index = 0
            self.cnl_list.InsertItem(index, cnl)
            lnk = curPrj.GetPrjGrpCnlLink(comp, grp, cnl)
            self.cnl_list.SetItem(index, 1, lnk)
        return

    def UpdateProjectComptList(self):
        """Show component on Panel."""
        sel_comp = window.build_panel.UpdateProjectCompList(self.comp_list)


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
        res = curPrj.GetPlatformComp(comp)
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
        curPrj.LoadCompConfigFile(comp)
        res = grp
        self.grp_name_txt.SetValue(res)
        res = curPrj.GetDefCompGrpMultiplicity(comp, grp)
        print(res)
        self.grp_mult_txt.SetValue(res)
        res = curPrj.GetDefCompGrpNameSpace(comp, grp)
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
        comp_list = curPrj.GetAllCompList()
        index = 0
        for comp in comp_list:
            # Insert item in the list
            self.comp_list.InsertItem(index, comp)
            # Color Mark component in the project
            color = curPrj.GetCompStatusColor(comp)
            self.comp_list.SetItemTextColour(index, color)
            index += 1

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
        self.activeCnlSrc = "null"
        self.activeCnlDst = "null"

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
        comp_name_cb_choices = []
        self.comp_name_cb = wx.ComboBox(self, wx.ID_ANY, u"none",
                                        wx.DefaultPosition, wx.DefaultSize,
                                        comp_name_cb_choices, 0)
        editSizer.Add(self.comp_name_cb, 0, wx.ALL, 5)
        self.comp_name_cb.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.OnCompNameDown)
        self.comp_add_btn = wx.Button(self, -1, 'Add Component')
        editSizer.Add(self.comp_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.comp_add_btn.Bind(wx.EVT_BUTTON, self.OnAddCompBtnClicked)
        self.grp_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Group')
        editSizer.Add(self.grp_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        grp_name_cb_choices = []
        self.grp_name_cb = wx.ComboBox(self, wx.ID_ANY, u"none",
                                       wx.DefaultPosition, wx.DefaultSize,
                                       grp_name_cb_choices, 0)
        editSizer.Add(self.grp_name_cb, 0, wx.ALL, 5)
        self.grp_add_btn = wx.Button(self, -1, 'Add Group')
        editSizer.Add(self.grp_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.grp_add_btn.Bind(wx.EVT_BUTTON, self.OnAddGroupBtnClicked)
        self.cnl_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Channel')
        editSizer.Add(self.cnl_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        cnl_name_cb_choices = []
        self.cnl_name_cb = wx.ComboBox(self, wx.ID_ANY, u"none",
                                       wx.DefaultPosition, wx.DefaultSize,
                                       cnl_name_cb_choices, 0)
        editSizer.Add(self.cnl_name_cb, 0, wx.ALL, 5)
        self.cnl_add_btn = wx.Button(self, -1, 'Add Channel')
        editSizer.Add(self.cnl_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.cnl_add_btn.Bind(wx.EVT_BUTTON, self.OnAddChannelBtnClicked)
        # Channel Link section
        self.link_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Link')
        editSizer.Add(self.link_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        link_name_cb_choices = []
        self.link_name_cb = wx.ComboBox(self, wx.ID_ANY, u"none",
                                        wx.DefaultPosition, wx.DefaultSize,
                                        link_name_cb_choices, 0)
        editSizer.Add(self.link_name_cb, 0, wx.ALL, 5)
        self.link_add_btn = wx.Button(self, -1, 'Add Link')
        editSizer.Add(self.link_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.link_add_btn.Bind(wx.EVT_BUTTON, self.OnAddLinkBtnClicked)
        # Dependency section
        self.dep_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Dependency')
        editSizer.Add(self.dep_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        dep_name_cb_choices = []
        self.dep_name_cb = wx.ComboBox(self, wx.ID_ANY, u"none",
                                       wx.DefaultPosition, wx.DefaultSize,
                                       dep_name_cb_choices, 0)
        editSizer.Add(self.dep_name_cb, 0, wx.ALL, 5)
        self.dep_add_btn = wx.Button(self, -1, 'Add Dependency')
        editSizer.Add(self.dep_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.dep_add_btn.Bind(wx.EVT_BUTTON, self.OnAddDepBtnClicked)
        # Push Section
        self.push_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Push')
        editSizer.Add(self.push_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        push_name_cb_choices = []
        self.push_name_cb = wx.ComboBox(self, wx.ID_ANY, u"none",
                                        wx.DefaultPosition, wx.DefaultSize,
                                        push_name_cb_choices, 0)
        editSizer.Add(self.push_name_cb, 0, wx.ALL, 5)
        self.push_add_btn = wx.Button(self, -1, 'Add Push')
        editSizer.Add(self.push_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.push_add_btn.Bind(wx.EVT_BUTTON, self.OnAddPushBtnClicked)
        self.pull_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Pull')
        editSizer.Add(self.pull_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        pull_name_cb_choices = []
        self.pull_name_cb = wx.ComboBox(self, wx.ID_ANY, u"none",
                                        wx.DefaultPosition, wx.DefaultSize,
                                        pull_name_cb_choices, 0)
        editSizer.Add(self.pull_name_cb, 0, wx.ALL, 5)
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
        curPrj.AddPrjComp(comp_name)
        # curPrj.SetPrjCompName(comp_name, comp_name)
        self.UpdatePanel()

    def OnAddGroupBtnClicked(self, event):
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        curPrj.AddPrjCompGrp(comp_name, grp_name)
        # curPrj.SetPrjCompGrpName(comp_name, grp_name, grp_name)
        self.UpdateCompList()
        return

    def OnAddChannelBtnClicked(self, event):
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        cnl_name = self.cnl_name_cb.GetValue()
        curPrj.AddPrjCompGrpCnl(comp_name, grp_name, cnl_name)
        self.UpdateCompList()
        return

    def OnAddLinkBtnClicked(self, event):
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        cnl_name = self.cnl_name_cb.GetValue()
        link_name = self.link_name_cb.GetValue()
        curPrj.AddPrjCompGrpCnlLink(comp_name, grp_name, cnl_name, link_name)
        self.UpdateCompList()
        return

    def OnAddDepBtnClicked(self, event):
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        dep_name = self.dep_name_cb.GetValue()
        curPrj.SetPrjCompGrpDep(comp_name, grp_name, dep_name)
        self.UpdateCompList()
        return

    def OnAddPushBtnClicked(self, event):
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        push_name = self.push_name_cb.GetValue()
        curPrj.SetPrjCompGrpPush(comp_name, grp_name, push_name)
        self.UpdateCompList()
        return

    def OnAddPullBtnClicked(self, event):

        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        pull_name = self.pull_name_cb.GetValue()
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

    def UpdatePanel(self):
        """Update App Builder Panel."""
        self.UpdateCompList()

    def UpdateCompList(self):
        """Show component on Panel."""
        sel_comp = self.UpdateProjectCompList(self.comp_list_src)
        self.UpdateCompComboBox(self.comp_name_cb, sel_comp)
        sel_grp = self.UpdateGroupListSrc(sel_comp)

        sel_comp = self.UpdateProjectCompList(self.comp_list_dst)
        self.UpdateGroupListSrc(sel_comp)

    def OnCompNameDown(self, event):
        # self.UpdateCompComboBox(self.comp_name_cb, self.activeCompSrc)
        return

    def UpdateCompComboBox(self, comp_name_cb, comp="null"):
        """Update Component Selector."""
        comp_list = curPrj.GetAllCompList()
        comp_name_cb.Clear()
        index = comp_name_cb.Append("< new >")
        for item in comp_list:
            index = comp_name_cb.Append(item)

        comp_name_cb.SetValue(comp)

        return

    def UpdateGrpSrcComboBoxSet(self, comp_name, selDict):

        self.activeGrpSrc = selDict["Group"]
        self.activeCnlSrc = selDict["Channel"]

        self.UpdateGrpSrcComboBox(self.grp_name_cb, comp_name,
                                  selDict["Group"])
        self.UpdateCnlSrcComboBox(self.cnl_name_cb, comp_name,
                                  selDict["Group"], selDict["Channel"])
        self.UpdateSrcLinkComboBox(self.link_name_cb, comp_name,
                                   selDict["Group"], selDict["Channel"])
        self.UpdateDepSrcComboBox(self.dep_name_cb, comp_name,
                                  selDict["Group"], selDict["Dependency"])
        self.UpdatePushSrcComboBox(self.push_name_cb, comp_name,
                                   selDict["Group"], selDict["Push"])
        self.UpdatePullSrcComboBox(self.pull_name_cb, comp_name,
                                   selDict["Group"], selDict["Pull"])

        return

    def UpdateGrpDstComboBoxSet(self, comp_name, selDict):

        self.activeGrpDst = selDict["Group"]
        self.activeCnlDst = selDict["Channel"]

        self.UpdateCnlSrcComboBox(self.link_name_cb, comp_name,
                                  selDict["Group"], selDict["Channel"])

        self.UpdatePushDstComboBox(self.push_name_cb, comp_name)
        self.UpdatePullDstComboBox(self.pull_name_cb, comp_name)

        return

    def UpdateGrpSrcComboBox(self, grp_name_cb, comp, grp_in="null"):
        """Update Group Selector."""
        curPrj.LoadCompConfigFile(comp)
        prj_item_list = curPrj.GetPrjCompGrpList(comp)
        def_item_list = curPrj.GetDefCompGrpList(comp)

        prj_item_nr_of = len(prj_item_list)
        max_prj_item_nr_of = 5

        # Insert new group item
        item_list = ["< new >"]

        # Insert  Existing Component Groups
        for item in prj_item_list:
            item_list.append(item)

        #go through definitions
        for item in def_item_list:
            # Extract predefined group names
            item_names_list = curPrj.GetDefCompGrpNames(comp, item)
            # if there are predefined names
            if item_names_list == "null":
                item_names_list = []

            # insert Predefined Group Names
            items_inserted = 0
            for item_name in item_names_list:
                if item_name not in item_list:
                    items_inserted += 1
                    item_list.append(str(item_name))
                elif item_name in prj_item_list:
                    items_inserted += 1

            # Extract Namespace
            item_name_space = curPrj.GetDefCompGrpNameSpace(comp, item)
            # if no namespace defined the use the group name for it
            if item_name_space == "null":
                item_name_space = item

            # Extract Multiplicity
            multiplicity = curPrj.GetDefCompGrpMultiplicity(comp, item)

            if multiplicity == "null":
                multiplicity = "1"

            # evaluate nr of names count
            counts = curPrj.MultiplicityDecode(multiplicity,
                                               max_prj_item_nr_of)
            item_max_mult = counts[1]
            items_nr_of = item_max_mult

            # insert at least one item by namespace
            if items_nr_of <= 0:
                items_nr_of = 1

            # Insert generated Group Names
            item_cnt = 0
            while items_inserted <= items_nr_of:
                # for i in range(items_nr_of):
                # find unique name
                while True:
                    if item_cnt > 0:
                        # insert count at end of namespace based names
                        item_n = str(item_name_space + "_" + str(item_cnt))
                    else:
                        # first name is with no counting at the end
                        item_n = item_name_space
                    item_cnt += 1
                    # detect if unique

                    if item_n not in item_list:
                        # insert if unique
                        item_list.append(item_n)
                        items_inserted += 1
                        break
                    elif item_n in prj_item_list:
                        if item_n not in item_names_list:
                            items_inserted += 1

        # Update Combo list
        grp_name_cb.Clear()
        for item in item_list:
            grp_name_cb.Append(item)
        # update selected text value
        grp_name_cb.SetValue(grp_in)

        return

    def UpdateCnlSrcComboBox(self,
                             cnl_name_cb,
                             comp,
                             grp,
                             cnl_in="null",
                             ovr=True):
        """Update Component Selector"""
        # TODO colorer for existing group
        curPrj.LoadCompConfigFile(comp)
        prj_item_list = curPrj.GetPrjCompGrpCnlList(comp, grp)

        # print("===================")
        # print(comp)
        # print(grp)
        # print(prj_item_list)

        prj_item_nr_of = len(prj_item_list)
        max_prj_item_nr_of = 5

        # Insert new group item
        item_list = ["< new >"]

        # Insert  Existing Component Groups
        items_inserted = 0
        for item in prj_item_list:
            item_list.append(item)
            items_inserted += 1

        #go through definitions
        # for item in def_item_list:
        item = grp
        # Extract predefined group names
        item_names_list = curPrj.GetDefCompCnlNames(comp, grp)
        # print("======= NL ============")
        # print(item_names_list)

        # if there are predefined names
        if item_names_list == "null":
            item_names_list = []

        # insert Predefined Group Names
        for item_name in item_names_list:
            if item_name not in item_list:
                items_inserted += 1
                item_list.append(str(item_name))
            elif item_name in prj_item_list:
                items_inserted += 1

        # Extract Namespace
        item_name_space = curPrj.GetDefCompCnlNameSpace(comp, grp)
        # print("======= NS ============")
        # print(item_name_space)
        # if no namespace defined the use the group name for it
        if item_name_space == "null":
            item_name_space = item

        # Extract Multiplicity
        multiplicity = curPrj.GetDefCompCnlMultiplicity(comp, grp)
        # print("======= ML ============")
        # print(multiplicity)

        if multiplicity == "null":
            multiplicity = "1"
        # print(multiplicity)

        # evaluate nr of names count
        counts = curPrj.MultiplicityDecode(multiplicity, max_prj_item_nr_of)
        item_max_mult = counts[1]
        items_nr_of = item_max_mult

        # insert at least one item by namespace
        if items_nr_of <= 0:
            items_nr_of = 1
        # print(items_nr_of)
        # print(items_inserted)

        # Insert generated Group Names
        item_cnt = 0
        while items_inserted <= items_nr_of:
            # for i in range(items_nr_of):
            # find unique name
            while True:
                if item_cnt > 0:
                    # insert count at end of namespace based names
                    item_n = str(item_name_space + "_" + str(item_cnt))
                else:
                    # first name is with no counting at the end
                    item_n = item_name_space
                item_cnt += 1
                # detect if unique

                if item_n not in item_list:
                    # insert if unique
                    item_list.append(item_n)
                    items_inserted += 1
                    break
                elif item_n in prj_item_list:
                    items_inserted += 1

        # Update Combo list
        if ovr:
            cnl_name_cb.Clear()
        for item in item_list:
            cnl_name_cb.Append(item)
        # update selected text value
        if ovr:
            cnl_name_cb.SetValue(cnl_in)

        return

    def UpdateSrcLinkComboBox(self, link_name_cb, comp, grp, link_in="null"):
        """Update Link Selector."""

        #extract dependency ist
        dep_comp = curPrj.GetPrjCompGrpDep(comp, grp)
        print(dep_comp)
        dep_comp_grp_list = curPrj.GetPrjCompGrpList(dep_comp)

        print(dep_comp)

        link_name_cb.Clear()

        # Insert  dependency Channels
        for dep_grp in dep_comp_grp_list:
            self.UpdateCnlSrcComboBox(link_name_cb,
                                      dep_comp,
                                      dep_grp,
                                      link_in,
                                      ovr=False)

        link_name_cb.SetValue(link_in)

        return

    def UpdateDepSrcComboBox(self,
                             item_name_cb,
                             comp,
                             grp,
                             Item_name_in="null"):
        """Update Dependencyes combobox."""
        item_list = []
        #extract dependency from component
        prj_item_comp = curPrj.GetPrjCompGrpDep(comp, grp)
        # insert it
        item_list.append(prj_item_comp)

        # extract dependencyes from definition
        curPrj.LoadCompConfigFile(comp)
        item_names_list = curPrj.GetDefCompDepList(comp)

        # collect dependencyes from definitions
        for item in item_names_list:
            if item not in item_list:
                item_list.append(item)

        # Update combobox
        item_name_cb.Clear()
        for item in item_list:
            item_name_cb.Append(item)

        item_name_cb.SetValue(Item_name_in)

        return

    def UpdatePushSrcComboBox(self,
                              item_name_cb,
                              comp,
                              grp,
                              Item_name_in="null"):
        """Update Dependencyes combobox."""
        item_list = []
        #extract Push  from component
        prj_item_comp = curPrj.GetPrjCompGrpPush(comp, grp)
        # insert it
        print(prj_item_comp)
        item_list.append(prj_item_comp)

        # TODO not form definitions but from dependency
        # extract push  from definition
        curPrj.LoadCompConfigFile(comp)
        item_names_list = curPrj.GetDefCompDepList(comp)
        # collect Push  from definitions
        for dep_item in item_names_list:
            curPrj.LoadCompConfigFile(dep_item)
            push_list = curPrj.GetDefCompPushList(dep_item)
            for item in push_list:
                if item not in item_list:
                    item_list.append(item)

        # Update combobox
        item_name_cb.Clear()
        for item in item_list:
            item_name_cb.Append(item)

        item_name_cb.SetValue(Item_name_in)

        return

    def UpdatePullSrcComboBox(self,
                              item_name_cb,
                              comp,
                              grp,
                              Item_name_in="null"):
        """Update Dependencyes combobox."""
        item_list = []
        #extract dependency from component
        prj_item_comp = curPrj.GetPrjCompGrpPull(comp, grp)
        # insert it
        item_list.append(prj_item_comp)

        # TODO not form definitions but from dependency
        # extract push  from definition
        curPrj.LoadCompConfigFile(comp)
        item_names_list = curPrj.GetDefCompDepList(comp)
        # collect Push  from definitions
        for dep_item in item_names_list:
            curPrj.LoadCompConfigFile(dep_item)
            push_list = curPrj.GetDefCompPushList(dep_item)
            for item in push_list:
                if item not in item_list:
                    item_list.append(item)

        # Update combobox
        item_name_cb.Clear()
        for item in item_list:
            item_name_cb.Append(item)

        item_name_cb.SetValue(Item_name_in)

        return

    def UpdatePushDstComboBox(self, item_name_cb, comp):
        """Update Dependencyes combobox."""
        item_list = []

        # extract push  from definition
        curPrj.LoadCompConfigFile(comp)
        item_names_list = curPrj.GetDefCompPushList(comp)
        print(comp)
        print(item_names_list)

        # collect Push  from definitions
        for item in item_names_list:
            if item not in item_list:
                item_list.append(item)

        item_name_in = "null"
        if len(item_names_list) > 0:
            item_name_in = item_names_list[0]
        # Update combobox
        item_name_cb.Clear()
        for item in item_list:
            item_name_cb.Append(item)

        item_name_cb.SetValue(item_name_in)

        return

    def UpdatePullDstComboBox(self, item_name_cb, comp):
        """Update Dependencyes combobox."""
        item_list = []

        # extract push  from definition
        curPrj.LoadCompConfigFile(comp)
        item_names_list = curPrj.GetDefCompPullList(comp)

        # collect Push  from definitions
        for item in item_names_list:
            if item not in item_list:
                item_list.append(item)

        item_name_in = "null"
        if len(item_names_list) > 0:
            item_name_in = item_names_list[0]

        # Update combobox
        item_name_cb.Clear()
        for item in item_list:
            item_name_cb.Append(item)

        item_name_cb.SetValue(item_name_in)

        return

    def GetSelectedListCtrlItem(self, item_list):
        """Return selected item in the list."""
        result = "null"
        item_ref = self.GetSelectedListCtrlItemRef(item_list)
        if item_ref != "null":
            result = item_list.GetItemText(item_ref)
        return result

    def GetSelectedListCtrlItemRef(self, item_list):
        """Return selected item in the list."""
        result = "null"
        list_size = item_list.GetItemCount()
        if list_size > 0:
            result = item_list.GetFirstSelected()
            if result == -1:
                result = item_list.GetTopItem()
        return result

    def UpdateProjectCompList(self, item_list):
        """Show component on Panel."""
        sel_pre = self.GetSelectedListCtrlItem(item_list)
        ref_pre = self.GetSelectedListCtrlItemRef(item_list)
        comp_prj_list = curPrj.GetProjectCompList()

        item_list.DeleteAllItems()
        # Groups Iterate
        index = 0
        for comp in comp_prj_list:
            # Insert component in list
            item_list.InsertItem(index, comp)
            # Color Mark component in the project
            color = curPrj.GetCompStatusColor(comp)
            item_list.SetItemTextColour(index, color)

            index += 1

        sel_post = self.GetSelectedListCtrlItem(item_list)
        ref_post = self.GetSelectedListCtrlItemRef(item_list)
        if sel_pre in comp_prj_list:
            sel_ref = ref_pre
            sel_comp = sel_pre
        else:
            sel_ref = ref_post
            sel_comp = sel_post
        if (sel_ref != "null"):
            item_list.Select(int(sel_ref))

        return sel_comp

    def UpdateGroupListSrc(self, comp):
        """Show Groups Source on Panel."""
        return self.UpdateGroupTreeList(comp, self.cnl_tree_src)

    def UpdateGroupListDst(self, comp):
        """Show Groups destination on Panel."""
        return self.UpdateGroupTreeList(comp, self.cnl_tree_dst)

    def UpdateGroupTreeList(self, comp, item_tree_list):
        """Show Groups on Panel."""

        # global curPrj
        grp_list = curPrj.GetPrjCompGrpList(comp)
        item_tree_list.DeleteAllItems()
        root = item_tree_list.GetRootItem()
        # Groups Iterate
        for grp in grp_list:
            child = item_tree_list.AppendItem(root, grp)
            cnl_list = curPrj.GetPrjCompGrpCnlList(comp, grp)
            for cnl in cnl_list:
                cnl_item = item_tree_list.AppendItem(child, cnl)
                # Show Link
                cnl_link = curPrj.GetPrjGrpCnlLink(comp, grp, cnl)
                item_tree_list.SetItemText(cnl_item, 1, cnl_link)
                # Show Dependency
                res = curPrj.GetPrjCompGrpDep(comp, grp)
                item_tree_list.SetItemText(cnl_item, 2, res)
                # Show Push
                res = curPrj.GetPrjCompGrpPush(comp, grp)
                item_tree_list.SetItemText(cnl_item, 3, res)
                # Show Pull
                res = curPrj.GetPrjCompGrpPull(comp, grp)
                item_tree_list.SetItemText(cnl_item, 4, res)
            item_tree_list.Expand(child)
        item = item_tree_list.GetFirstItem()
        item_tree_list.Select(item)
        # print("UpdateGrpTree")
        if len(grp_list) > 0:
            sel_grp = item_tree_list.GetItemText(item, 0)
            # print("1")
        else:
            sel_grp = "null"
            # print("2")

        # print(sel_grp)

        return sel_grp

    def GetTreeLevel(self, tree, item):
        # first level back
        tmp_grp_item = tree.GetItemParent(item)
        # second Level Back
        tmp_root_item = self.cnl_tree_src.GetItemParent(tmp_grp_item)
        if tmp_root_item.IsOk():
            return "Channel"
        else:
            return "Group"

    def GetGrpTreeSel(self, group_tree, sel_item):
        # first level back
        tmp_grp_item = group_tree.GetItemParent(sel_item)
        # second Level Back
        tmp_root_item = group_tree.GetItemParent(tmp_grp_item)
        if tmp_root_item.IsOk():
            cnl_item = sel_item
            grp_item = group_tree.GetItemParent(cnl_item)
            cnl_name = group_tree.GetItemText(cnl_item)
        else:
            grp_item = sel_item
            cnl_item = group_tree.GetFirstChild(sel_item)
            if cnl_item.IsOk:
                cnl_name = group_tree.GetItemText(cnl_item)
            else:
                cnl_name = "null"
                cnl_item = "null"

        selDict = {}
        selDict["Channel"] = cnl_name
        selDict["Group"] = group_tree.GetItemText(grp_item)
        selDict["Link"] = group_tree.GetItemText(cnl_item, 1)
        selDict["Dependency"] = group_tree.GetItemText(cnl_item, 2)
        selDict["Push"] = group_tree.GetItemText(cnl_item, 3)
        selDict["Pull"] = group_tree.GetItemText(cnl_item, 4)

        return selDict

    def OnCompSrcSelected(self, event):
        """Call Action when component in list is selected."""
        sel_comp = event.GetText()
        self.activeCompSrc = sel_comp
        self.UpdateGroupListSrc(sel_comp)
        self.BuildDependencyTree(sel_comp)
        # if autofill
        auto_fill = self.auto_src_cb.GetValue()
        if auto_fill:
            self.UpdateCompComboBox(self.comp_name_cb, self.activeCompSrc)

            comp_name = self.activeCompSrc
            root = self.cnl_tree_src.GetRootItem()
            grp_item = self.cnl_tree_src.GetFirstChild(root)

            if grp_item.IsOk():
                selDict = self.GetGrpTreeSel(self.cnl_tree_src, grp_item)

                self.UpdateGrpSrcComboBoxSet(sel_comp, selDict)

    def OnCompDstSelected(self, event):
        """Call Action when component in destination list is selected."""
        sel_comp = event.GetText()
        self.activeCompDst = sel_comp
        self.UpdateGroupListDst(sel_comp)
        self.BuildDependencyTree(sel_comp)
        # if autofill
        auto_fill = self.auto_dst_cb.GetValue()
        if auto_fill:
            self.UpdateCompComboBox(self.dep_name_cb, self.activeCompDst)

            comp_name = self.activeCompDst
            root = self.cnl_tree_dst.GetRootItem()
            grp_item = self.cnl_tree_dst.GetFirstChild(root)

            if grp_item.IsOk():
                selDict = self.GetGrpTreeSel(self.cnl_tree_dst, grp_item)

                self.UpdateGrpDstComboBoxSet(sel_comp, selDict)

        # comp = event.GetText()
        # self.activeCompDst = comp
        # self.UpdateGroupListDst(comp)
        # self.dep_name_cb.SetValue(comp)

    def OnCompGrpSrcSelected(self, event):
        """Call Action when component in list is selected."""
        grp_item = event.GetItem()
        print("selectGrp >>")

        auto_fill = self.auto_src_cb.GetValue()
        if auto_fill:
            if grp_item.IsOk():
                selDict = self.GetGrpTreeSel(self.cnl_tree_src, grp_item)

                self.UpdateGrpSrcComboBoxSet(self.activeCompSrc, selDict)

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
        """Build dependency tree entry."""
        # Clear the tree
        self.comp_tree_dep.DeleteAllItems()
        # Init tree root
        root = self.comp_tree_dep.AddRoot(comp)
        # Start Tree building
        self.BuildTreeDependency(root, comp)
        # Expand the dependency tree
        self.comp_tree_dep.ExpandAll()

    def BuildTreeDependency(self, parent, comp):
        """Build dependency tree recurency."""
        # load selected component configuration
        curPrj.LoadCompConfigFile(comp)
        # Extrect componet dependencies
        dep_list = curPrj.GetDefCompDepList(comp)
        for comp_it in dep_list:
            # if it is not the parent comp then it is a child
            if str(comp_it) != str(comp):
                # Insert child in the tree
                child = self.comp_tree_dep.AppendItem(parent, comp_it)
                # Color Mark component in the project
                color = curPrj.GetCompStatusColor(comp_it)
                self.comp_tree_dep.SetItemTextColour(child, color)
                # Go recurrently through children
                self.BuildTreeDependency(child, comp_it)
                # Expand the dependency tree
                self.comp_tree_dep.ExpandAll()


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
        self.build_panel = ProjectBuilderPanel(nb)
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
        fileNum = 1 - wx.ID_FILE1
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