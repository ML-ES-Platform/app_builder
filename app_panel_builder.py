"""GUI - Project Builder Panel."""
import wx


class ProjectBuilderPanel(wx.Panel):
    """Panel for component list and the references in the project and git."""
    def __init__(self, parent, curPrj, panel_color):
        """Init Component list Panel."""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(panel_color)

        self.parent = parent
        self.curPrj = curPrj
        self.activeCompSrc = "null"
        self.activeCompDst = "null"
        self.activeGrpSrc = "null"
        self.activeGrpDst = "null"
        self.activeCnlSrc = "null"
        self.activeCnlDst = "null"


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

        # Link destination component List
        self.comp_list_dst = wx.ListCtrl(self, style=wx.LC_REPORT)
        linkSrcSizer.Add(self.comp_list_dst, 0, wx.ALL | wx.EXPAND, 3)
        self.comp_list_dst.InsertColumn(0, " Destination Component", width=150)
        self.comp_list_dst.Bind(wx.EVT_LIST_ITEM_SELECTED,
                                self.OnCompDstSelected)

        # Destination Channel List

        self.cnl_tree_dst = wx.dataview.TreeListCtrl(self,
                                                     size=(150, -1),
                                                     style=wx.LC_REPORT)
        linkSrcSizer.Add(self.cnl_tree_dst, 0, wx.ALL | wx.EXPAND, 3)
        self.cnl_tree_dst.AppendColumn('Channel', width=100)
        self.cnl_tree_dst.Bind(wx.dataview.EVT_TREELIST_SELECTION_CHANGED,
                               self.OnCompGrpDstSelected)

        build_tree_sizer.Add(linkSrcSizer, 1, wx.ALL | wx.EXPAND, 3)
        # build dependency tree Sizer ==================================
        dependencySizer = wx.BoxSizer(wx.HORIZONTAL)

        autoFillSizer = wx.BoxSizer(wx.VERTICAL)


        # Auto fill from Source tree
        autoFillSrcSizer = wx.BoxSizer(wx.VERTICAL)

        self.auto_tree_freeze_cb = wx.CheckBox(self, wx.ID_ANY, u"Freeze Tree")
        autoFillSrcSizer.Add(self.auto_tree_freeze_cb, 0, wx.ALL, 10)


        self.fill_src_btn = wx.Button(self, -1, 'Fill settings')
        autoFillSrcSizer.Add(self.fill_src_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.fill_src_btn.Bind(wx.EVT_BUTTON, self.OnAddGroupBtnClicked)
        self.auto_src_cb = wx.CheckBox(self, wx.ID_ANY, u"Auto fill Source")
        self.auto_src_cb.Bind(wx.EVT_CHECKBOX, self.onAutoSrcChecked)

        autoFillSrcSizer.Add(self.auto_src_cb, 0, wx.ALL, 5)

        autoFillSizer.Add(autoFillSrcSizer, 0, wx.ALL | wx.EXPAND, 3)

        # Auto fill from destination tree
        autoFillTreeSizer = wx.BoxSizer(wx.VERTICAL)
        self.dep_add_btn = wx.Button(self, -1, 'Fill settings')
        autoFillTreeSizer.Add(self.dep_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.dep_add_btn.Bind(wx.EVT_BUTTON, self.OnAddDepBtnClicked)
        self.auto_tree_cb = wx.CheckBox(self, wx.ID_ANY, u"Auto fill Tree")
        self.auto_tree_cb.Bind(wx.EVT_CHECKBOX, self.onAutoTreeChecked)

        autoFillTreeSizer.Add(self.auto_tree_cb, 0, wx.ALL, 5)
        # self. = wx.Button(self, -1, 'Fill settings')
        # .Add(self., 0, wx.ALL | wx.EXPAND, 3)
        # self..Bind(wx.EVT_BUTTON, self.)
        autoFillSizer.Add(autoFillTreeSizer, 0, wx.ALL | wx.EXPAND, 3)

        # Auto fill from destination tree
        autoFillDstSizer = wx.BoxSizer(wx.VERTICAL)
        self.fill_dst_btn = wx.Button(self, -1, 'Fill settings')
        autoFillDstSizer.Add(self.fill_dst_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.fill_dst_btn.Bind(wx.EVT_BUTTON, self.OnCompDstSelected)
        self.auto_dst_cb = wx.CheckBox(self, wx.ID_ANY, u"Auto fill Dest.")
        self.auto_dst_cb.Bind(wx.EVT_CHECKBOX, self.onAutoDstChecked)

        autoFillDstSizer.Add(self.auto_dst_cb, 0, wx.ALL, 5)
        autoFillSizer.Add(autoFillDstSizer, 0, wx.ALL | wx.EXPAND, 3)

        dependencySizer.Add(autoFillSizer, 0, wx.ALL | wx.EXPAND, 3)

        # dependency component List
        self.comp_tree_dep = wx.TreeCtrl(self, wx.ID_ANY, wx.DefaultPosition,
                                         wx.Size(150, 150))
        self.comp_tree_dep.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged,
                                self.comp_tree_dep)

        dependencySizer.Add(self.comp_tree_dep, 1, wx.ALL | wx.EXPAND, 3)

        # build Edit / Add Sizer ==================================
        editSizer = wx.GridSizer(rows=4, cols=2, hgap=0, vgap=0)

        # Bind Section
        editBindSizer = wx.BoxSizer(wx.VERTICAL)

        self.comp_add_btn = wx.Button(self, -1, 'Bind')
        editBindSizer.Add(self.comp_add_btn, 0, wx.ALL, 3)
        self.comp_add_btn.Bind(wx.EVT_BUTTON, self.OnAddBindBtnClicked)
        editSizer.Add(editBindSizer, 0, wx.ALL | wx.EXPAND, 0)

        # Component Section
        editCompSizer = wx.BoxSizer(wx.VERTICAL)
        self.comp_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Component')
        editCompSizer.Add(self.comp_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        comp_name_cb_choices = []
        self.comp_name_cb = wx.ComboBox(self, wx.ID_ANY, u"none",
                                        wx.DefaultPosition, wx.DefaultSize,
                                        comp_name_cb_choices, 0)
        editCompSizer.Add(self.comp_name_cb, 0, wx.ALL | wx.EXPAND, 5)
        self.comp_name_cb.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.OnCompNameDown)
        self.comp_add_btn = wx.Button(self, -1, 'Add Component')
        editCompSizer.Add(self.comp_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.comp_add_btn.Bind(wx.EVT_BUTTON, self.OnAddCompBtnClicked)
        editSizer.Add(editCompSizer, 0, wx.ALL | wx.EXPAND, 0)

        # Group Section
        editGrpSizer = wx.BoxSizer(wx.VERTICAL)
        self.grp_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Group')
        editGrpSizer.Add(self.grp_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        grp_name_cb_choices = []
        self.grp_name_cb = wx.ComboBox(self, wx.ID_ANY, u"none",
                                       wx.DefaultPosition, wx.DefaultSize,
                                       grp_name_cb_choices, 0)
        editGrpSizer.Add(self.grp_name_cb, 0, wx.ALL, 5)
        self.grp_add_btn = wx.Button(self, -1, 'Add Group')
        editGrpSizer.Add(self.grp_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.grp_add_btn.Bind(wx.EVT_BUTTON, self.OnAddGroupBtnClicked)
        editSizer.Add(editGrpSizer, 0, wx.ALL | wx.EXPAND, 0)

        # Dependency section
        editDepSizer = wx.BoxSizer(wx.VERTICAL)
        self.dep_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Dependency')
        editDepSizer.Add(self.dep_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        dep_name_cb_choices = []
        self.dep_name_cb = wx.ComboBox(self, wx.ID_ANY, u"none",
                                       wx.DefaultPosition, wx.DefaultSize,
                                       dep_name_cb_choices, 0)
        editDepSizer.Add(self.dep_name_cb, 0, wx.ALL, 5)
        self.dep_add_btn = wx.Button(self, -1, 'Add Dependency')
        editDepSizer.Add(self.dep_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.dep_add_btn.Bind(wx.EVT_BUTTON, self.OnAddDepBtnClicked)
        editSizer.Add(editDepSizer, 0, wx.ALL | wx.EXPAND, 0)

        # Channel Section
        editCnlSizer = wx.BoxSizer(wx.VERTICAL)
        self.cnl_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Channel')
        editCnlSizer.Add(self.cnl_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        cnl_name_cb_choices = []
        self.cnl_name_cb = wx.ComboBox(self, wx.ID_ANY, u"none",
                                       wx.DefaultPosition, wx.DefaultSize,
                                       cnl_name_cb_choices, 0)
        editCnlSizer.Add(self.cnl_name_cb, 0, wx.ALL, 5)
        self.cnl_add_btn = wx.Button(self, -1, 'Add Channel')
        editCnlSizer.Add(self.cnl_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.cnl_add_btn.Bind(wx.EVT_BUTTON, self.OnAddChannelBtnClicked)
        editSizer.Add(editCnlSizer, 0, wx.ALL | wx.EXPAND, 0)

        # Channel Link section
        editLinkSizer = wx.BoxSizer(wx.VERTICAL)
        self.link_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Link')
        editLinkSizer.Add(self.link_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        link_name_cb_choices = []
        self.link_name_cb = wx.ComboBox(self, wx.ID_ANY, u"none",
                                        wx.DefaultPosition, wx.DefaultSize,
                                        link_name_cb_choices, 0)
        editLinkSizer.Add(self.link_name_cb, 0, wx.ALL, 5)
        self.link_add_btn = wx.Button(self, -1, 'Add Link')
        editLinkSizer.Add(self.link_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.link_add_btn.Bind(wx.EVT_BUTTON, self.OnAddLinkBtnClicked)
        editSizer.Add(editLinkSizer, 0, wx.ALL | wx.EXPAND, 0)

        # Push Section
        editPushSizer = wx.BoxSizer(wx.VERTICAL)
        self.push_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Push')
        editPushSizer.Add(self.push_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        push_name_cb_choices = []
        self.push_name_cb = wx.ComboBox(self, wx.ID_ANY, u"none",
                                        wx.DefaultPosition, wx.DefaultSize,
                                        push_name_cb_choices, 0)
        editPushSizer.Add(self.push_name_cb, 0, wx.ALL, 5)
        self.push_add_btn = wx.Button(self, -1, 'Add Push')
        editPushSizer.Add(self.push_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.push_add_btn.Bind(wx.EVT_BUTTON, self.OnAddPushBtnClicked)
        editSizer.Add(editPushSizer, 0, wx.ALL | wx.EXPAND, 0)

        # Pull Section
        editPullSizer = wx.BoxSizer(wx.VERTICAL)
        self.pull_name_lbl = wx.StaticText(self, wx.ID_ANY, 'Pull')
        editPullSizer.Add(self.pull_name_lbl, 0, wx.ALL | wx.EXPAND, 3)
        pull_name_cb_choices = []
        self.pull_name_cb = wx.ComboBox(self, wx.ID_ANY, u"none",
                                        wx.DefaultPosition, wx.DefaultSize,
                                        pull_name_cb_choices, 0)
        editPullSizer.Add(self.pull_name_cb, 0, wx.ALL, 5)
        self.pull_add_btn = wx.Button(self, -1, 'Add Pull')
        editPullSizer.Add(self.pull_add_btn, 0, wx.ALL | wx.EXPAND, 3)
        self.pull_add_btn.Bind(wx.EVT_BUTTON, self.OnAddPullBtnClicked)
        editSizer.Add(editPullSizer, 0, wx.ALL | wx.EXPAND, 0)

        dependencySizer.Add(editSizer, 0, wx.ALL, 3)

        build_tree_sizer.Add(dependencySizer, 1, wx.ALL | wx.EXPAND, 3)
        # build comp Name Sizer ==================================
        linkDstSizer = wx.BoxSizer(wx.HORIZONTAL)
        # build comp Name Sizer

        # build_tree_sizer.Add(linkDstSizer, 1, wx.ALL | wx.EXPAND, 3)

        top_sizer.Add(build_tree_sizer, 1, wx.ALL | wx.EXPAND, 3)

        self.SetSizer(top_sizer)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.UpdateCompList()
        comp = self.curPrj.activeComponent
        self.UpdateGroupListSrc(comp)
        self.UpdateGroupListDst(comp)

    def OnEnterWindow(self, event):
        """Handle enter into panel event."""
        self.UpdateCompList()
        comp = self.curPrj.activeComponent
        self.UpdateGroupListSrc(self.activeCompSrc)
        self.UpdateGroupListDst(self.activeCompDst)

    def onAutoSrcChecked(self, event):
        """Handle auto fill destination checkbox."""
        cb = event.GetEventObject()
        # # print cb.GetLabel(),' is clicked',cb.GetValue()
        # self.auto_src_cb.SetValue(True)
        # self.auto_dst_cb.SetValue(False)
        # self.auto_tree_cb.SetValue(False)
        return

    def onAutoDstChecked(self, event):
        """Handle auto fill destination checkbox."""
        # cb = event.GetEventObject()
        # # print cb.GetLabel(),' is clicked',cb.GetValue()
        # self.auto_src_cb.SetValue(False)
        # self.auto_dst_cb.SetValue(True)
        # self.auto_tree_cb.SetValue(False)
        return

    def onAutoTreeChecked(self, event):
        """Handle auto fill tree checkbox."""
        # cb = event.GetEventObject()
        # # print cb.GetLabel(),' is clicked',cb.GetValue()
        # self.auto_src_cb.SetValue(False)
        # self.auto_dst_cb.SetValue(False)
        # self.auto_tree_cb.SetValue(True)
        return

    def GetActiveComp(self, comp_list):
        """Return the selected item as component from given ListCtrl."""
        comp = self.GetSelectedListCtrlItem(comp_list)
        return comp

    def GetActiveGrp(self, group_tree):
        """Return the selected item as component from given ListCtrl."""
        result = "null"
        sel_item = self.GetSelectedTreeCtrlItemRef(group_tree)
        if sel_item != "null":
            # first level back
            tmp_grp_item = group_tree.GetItemParent(sel_item)
            # second Level Back
            if tmp_grp_item.IsOk():
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

                result = selDict

        return result

    def SetActiveComp(self, comp_list, comp):
        """Select a component in a given ListCtrl."""

        item = self.GetListCtrlItemByText(comp, comp_list)
        if item != "null":
            sel_item = comp_list.GetFirstSelected()
            comp_list.Select(sel_item,0)
            comp_list.Select(item)

        return item

    def OnAddBindBtnClicked(self, event):
        """Handle 'Bind' button for Channels from selected GUI Lists."""
        comp_src = self.GetActiveComp(self.comp_list_src)
        selDict = self.GetActiveGrp(self.cnl_tree_src)

        grp_src = selDict["Group"]
        cnl_src = selDict["Channel"]

        comp_dst = self.GetActiveComp(self.comp_list_dst)
        selDict = self.GetActiveGrp(self.cnl_tree_dst)

        grp_dst = selDict["Group"]
        cnl_dst = selDict["Channel"]

        print("Src", comp_src, " ,", grp_src, " ,", cnl_src)
        print("Dst", comp_dst, " ,", grp_dst, " ,", cnl_dst)

        self.curPrj.SetPrjCompGrpDep(comp_src, grp_src, comp_dst)
        self.curPrj.AddPrjCompGrpCnlLink(comp_src, grp_src, cnl_src, cnl_dst)

        self.UpdatePanel()

    def OnAddCompBtnClicked(self, event):
        """Handle 'Add Component' Button."""
        comp_name = self.comp_name_cb.GetValue()
        self.curPrj.activeComponent = comp_name
        self.curPrj.AddPrjComp(comp_name)
        # self.curPrj.SetPrjCompName(comp_name, comp_name)
        self.UpdatePanel()

    def OnAddGroupBtnClicked(self, event):
        """Handle 'Add Group' Button."""
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        self.curPrj.AddPrjCompGrp(comp_name, grp_name)
        # self.curPrj.SetPrjCompGrpName(comp_name, grp_name, grp_name)
        self.UpdateCompList()
        return

    def OnAddChannelBtnClicked(self, event):
        """Handle 'Add Channel' Button."""
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        cnl_name = self.cnl_name_cb.GetValue()
        self.curPrj.AddPrjCompGrpCnl(comp_name, grp_name, cnl_name)
        self.UpdateCompList()
        return

    def OnAddLinkBtnClicked(self, event):
        """Handle 'Add Link' Button."""
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        cnl_name = self.cnl_name_cb.GetValue()
        link_name = self.link_name_cb.GetValue()
        self.curPrj.AddPrjCompGrpCnlLink(comp_name, grp_name, cnl_name,
                                         link_name)
        self.UpdateCompList()
        return

    def OnAddDepBtnClicked(self, event):
        """Handle 'Add Dependency' Button."""
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        dep_name = self.dep_name_cb.GetValue()
        self.curPrj.SetPrjCompGrpDep(comp_name, grp_name, dep_name)
        self.UpdateCompList()
        return

    def OnAddPushBtnClicked(self, event):
        """Handle 'Add Push' Button."""
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        push_name = self.push_name_cb.GetValue()
        self.curPrj.SetPrjCompGrpPush(comp_name, grp_name, push_name)
        self.UpdateCompList()
        return

    def OnAddPullBtnClicked(self, event):
        """Handle 'Add Pull' Button."""
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        pull_name = self.pull_name_cb.GetValue()
        self.curPrj.SetPrjCompGrpPull(comp_name, grp_name, pull_name)
        # print(self.curPrj.JSON_project)
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
        sel_comp_src = self.UpdateProjectCompList(self.comp_list_src)

        self.UpdateCompComboBox(self.comp_name_cb, sel_comp_src)

        sel_grp = self.UpdateGroupListSrc(sel_comp_src)

        sel_comp_dst = self.UpdateProjectCompList(self.comp_list_dst)
        self.UpdateGroupListDst(sel_comp_dst)

    def OnCompNameDown(self, event):
        # self.UpdateCompComboBox(self.comp_name_cb, self.activeCompSrc)
        return

    def UpdateCompComboBox(self, comp_name_cb, comp="null"):
        """Update Component Selector."""
        comp_list = self.curPrj.GetAllCompList()
        comp_name_cb.Clear()
        index = comp_name_cb.Append("< new >")
        for item in comp_list:
            index = comp_name_cb.Append(item)

        comp_name_cb.SetValue(comp)

        return

    def UpdateGrpSrcComboBoxSet(self, comp_name, selDict):
        """Update combobox affected by source selection."""
        self.activeGrpSrc = selDict["Group"]
        self.activeCnlSrc = selDict["Channel"]

        self.UpdateGrpSrcComboBox(self.grp_name_cb, comp_name,
                                  selDict["Group"])
        self.UpdateCnlSrcComboBox(self.cnl_name_cb, comp_name,
                                  selDict["Group"], selDict["Channel"])
        self.UpdateSrcLinkComboBox(self.link_name_cb, comp_name,
                                   selDict["Group"], selDict["Link"])
        self.UpdateDepSrcComboBox(self.dep_name_cb, comp_name,
                                  selDict["Group"], selDict["Dependency"])
        self.UpdatePushSrcComboBox(self.push_name_cb, comp_name,
                                   selDict["Group"], selDict["Push"])
        self.UpdatePullSrcComboBox(self.pull_name_cb, comp_name,
                                   selDict["Group"], selDict["Pull"])

        return

    def UpdateGrpDstComboBoxSet(self, comp_name, selDict):
        """Update combobox affected by destination selection."""
        self.activeGrpDst = selDict["Group"]
        self.activeCnlDst = selDict["Channel"]

        self.UpdateCnlSrcComboBox(self.link_name_cb, comp_name,
                                  selDict["Group"], selDict["Channel"])

        return

    def UpdateGrpSrcComboBox(self, grp_name_cb, comp, grp_in="null"):
        """Update Group Selector."""
        # self.curPrj.LoadCompConfigFile(comp)
        prj_item_list = self.curPrj.GetPrjCompGrpList(comp)
        def_item_list = self.curPrj.GetDefCompGrpList(comp)

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
            item_names_list = self.curPrj.GetDefCompGrpNames(comp, item)
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
            item_name_space = self.curPrj.GetDefCompGrpNameSpace(comp, item)
            # if no namespace defined the use the group name for it
            if item_name_space == "null":
                item_name_space = item

            # Extract Multiplicity
            multiplicity = self.curPrj.GetDefCompGrpMultiplicity(comp, item)

            if multiplicity == "null":
                multiplicity = "1"

            # evaluate nr of names count
            counts = self.curPrj.MultiplicityDecode(multiplicity,
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
        """Update Component Selector."""
        # TODO colorer for existing group
        # self.curPrj.LoadCompConfigFile(comp)
        prj_item_list = self.curPrj.GetPrjCompGrpCnlList(comp, grp)

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
        item_names_list = self.curPrj.GetDefCompCnlNames(comp, grp)
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
        item_name_space = self.curPrj.GetDefCompCnlNameSpace(comp, grp)
        # print("======= NS ============")
        # print(item_name_space)
        # if no namespace defined the use the group name for it
        if item_name_space == "null":
            item_name_space = item

        # Extract Multiplicity
        multiplicity = self.curPrj.GetDefCompCnlMultiplicity(comp, grp)
        # print("======= ML ============")
        # print(multiplicity)

        if multiplicity == "null":
            multiplicity = "1"
        # print(multiplicity)

        # evaluate nr of names count
        counts = self.curPrj.MultiplicityDecode(multiplicity,
                                                max_prj_item_nr_of)
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
        dep_comp = self.curPrj.GetPrjCompGrpDep(comp, grp)
        # print(dep_comp)
        dep_comp_grp_list = self.curPrj.GetPrjCompGrpList(dep_comp)

        # print(dep_comp)

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
        prj_item_comp = self.curPrj.GetPrjCompGrpDep(comp, grp)
        # insert it
        item_list.append(prj_item_comp)

        # extract dependencyes from definition
        # self.curPrj.LoadCompConfigFile(comp)
        item_names_list = self.curPrj.GetDefCompDepList(comp)

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
        prj_item_comp = self.curPrj.GetPrjCompGrpPush(comp, grp)
        # insert it
        # print(prj_item_comp)
        item_list.append(prj_item_comp)

        # TODO not form definitions but from dependency
        # extract push  from definition
        # self.curPrj.LoadCompConfigFile(comp)
        item_names_list = self.curPrj.GetDefCompDepList(comp)
        # collect Push  from definitions
        for dep_item in item_names_list:
            # self.curPrj.LoadCompConfigFile(dep_item)
            push_list = self.curPrj.GetDefCompPushList(dep_item)
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
        prj_item_comp = self.curPrj.GetPrjCompGrpPull(comp, grp)
        # insert it
        item_list.append(prj_item_comp)

        # TODO not form definitions but from dependency
        # extract push  from definition
        # self.curPrj.LoadCompConfigFile(comp)
        item_names_list = self.curPrj.GetDefCompDepList(comp)
        # collect Push  from definitions
        for dep_item in item_names_list:
            # self.curPrj.LoadCompConfigFile(dep_item)
            push_list = self.curPrj.GetDefCompPushList(dep_item)
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
        # self.curPrj.LoadCompConfigFile(comp)
        item_names_list = self.curPrj.GetDefCompPushList(comp)
        # print(comp)
        # print(item_names_list)

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
        # self.curPrj.LoadCompConfigFile(comp)
        item_names_list = self.curPrj.GetDefCompPullList(comp)

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
        """Return selected item in the list ctrl."""
        result = "null"
        item_ref = self.GetSelectedListCtrlItemRef(item_list)
        if item_ref != "null":
            result = item_list.GetItemText(item_ref)
        return result

    def GetSelectedListCtrlItemRef(self, item_list):
        """Return selected item in the list ctrl."""
        result = "null"
        list_size = item_list.GetItemCount()
        if list_size > 0:
            result = item_list.GetFirstSelected()
            if result == -1:
                result = item_list.GetTopItem()
        return result

    def GetSelectedTreeCtrlItem(self, item_tree):
        """Return selected item in the tree ctrl."""
        result = "null"
        item_ref = self.GetSelectedTreeCtrlItemRef(item_tree)
        if item_ref != "null":
            result = item_tree.GetItemText(item_ref)
        return result

    def GetSelectedTreeCtrlItemRef(self, item_tree):
        """Return selected item in the tree ctrl."""
        result = "null"
        item_ref = item_tree.GetSelection()
        if item_ref.IsOk():
            result = item_ref
        return result

    def UpdateProjectCompList(self, item_list):
        """Show component on Panel."""
        # extract actual component Name before update
        sel_pre = self.GetSelectedListCtrlItem(item_list)
        ref_pre = self.GetSelectedListCtrlItemRef(item_list)

        comp_prj_list = self.curPrj.GetProjectCompList()

        item_list.DeleteAllItems()
        # Components Iterate
        index = 0
        for comp in comp_prj_list:
            # Insert component in list
            item_list.InsertItem(index, comp)
            # Color Mark component in the project
            color = self.curPrj.GetCompStatusColor(comp)
            item_list.SetItemTextColour(index, color)

            index += 1

        ref_post = self.GetListCtrlItemByText(sel_pre, item_list)
        if (ref_post != "null"):
            item_list.Select(ref_post)
            item_list.EnsureVisible(ref_post)
            sel_pre = item_list.GetItemText(ref_post)
        else:
            sel_pre = "null"

        return sel_pre


    def UpdateGroupListSrc(self, comp):
        """Show Groups Source on Panel."""
        return self.UpdateGroupSrcTreeList(comp, self.cnl_tree_src)

    def UpdateGroupListDst(self, comp):
        """Show Groups destination on Panel."""
        return self.UpdateGroupDstTreeList(comp, self.cnl_tree_dst)

    def GetTreeCtrlItemByText(self, search_text, tree_ctrl_instance):
        """Return the item by given test as name."""
        retval = "null"

        item = tree_ctrl_instance.GetFirstItem()

        while item.IsOk():
            print(tree_ctrl_instance.GetItemText(item))
            if tree_ctrl_instance.GetItemText(item) == search_text:
                retval = item
                break
            item = tree_ctrl_instance.GetNextItem(item)
        return retval

    def GetListCtrlItemByText(self, search_text, list_ctrl_instance):
        """Return the item by given test as name."""
        retval = "null"

        item = list_ctrl_instance.FindItem(0, search_text)

        if item != -1:
            # print(list_ctrl_instance.GetItemText(item))
            retval = item
            # retval = list_ctrl_instance.GetItem(item)

        return retval

    def UpdateGroupSrcTreeList(self, comp, item_tree_list):
        """Show Groups on Panel."""
        # extract actual component Name before update
        sel_pre = self.GetSelectedTreeCtrlItem(item_tree_list)

        # global curPrj
        grp_list = self.curPrj.GetPrjCompGrpList(comp)
        item_tree_list.DeleteAllItems()
        root = item_tree_list.GetRootItem()
        # Groups Iterate
        for grp in grp_list:
            child = item_tree_list.AppendItem(root, grp)
            cnl_list = self.curPrj.GetPrjCompGrpCnlList(comp, grp)
            for cnl in cnl_list:
                cnl_item = item_tree_list.AppendItem(child, cnl)
                # Show Link
                cnl_link = self.curPrj.GetPrjGrpCnlLink(comp, grp, cnl)
                item_tree_list.SetItemText(cnl_item, 1, cnl_link)
                # Show Dependency
                res = self.curPrj.GetPrjCompGrpDep(comp, grp)
                item_tree_list.SetItemText(cnl_item, 2, res)
                # Show Push
                res = self.curPrj.GetPrjCompGrpPush(comp, grp)
                item_tree_list.SetItemText(cnl_item, 3, res)
                # Show Pull
                res = self.curPrj.GetPrjCompGrpPull(comp, grp)
                item_tree_list.SetItemText(cnl_item, 4, res)
            item_tree_list.Expand(child)
        item = item_tree_list.GetFirstItem()
        item_tree_list.Select(item)
        if len(grp_list) > 0:
            sel_grp = item_tree_list.GetItemText(item, 0)
        else:
            sel_grp = "null"
        ref_post = self.GetTreeCtrlItemByText(sel_pre, item_tree_list)

        if (ref_post != "null"):
            item_tree_list.Select(ref_post)
            item_tree_list.EnsureVisible(ref_post)
        return sel_grp

    def UpdateGroupDstTreeList(self, comp, item_tree_list):
        """Show Groups on Panel."""
        # extract actual component Name before update
        sel_pre = self.GetSelectedTreeCtrlItem(item_tree_list)

        # global curPrj
        grp_list = self.curPrj.GetPrjCompGrpList(comp)
        item_tree_list.DeleteAllItems()
        root = item_tree_list.GetRootItem()
        # Groups Iterate
        for grp in grp_list:
            child = item_tree_list.AppendItem(root, grp)
            cnl_list = self.curPrj.GetPrjCompGrpCnlList(comp, grp)
            for cnl in cnl_list:
                cnl_item = item_tree_list.AppendItem(child, cnl)
            item_tree_list.Expand(child)
        item = item_tree_list.GetFirstItem()
        item_tree_list.Select(item)

        if len(grp_list) > 0:
            sel_grp = item_tree_list.GetItemText(item, 0)
        else:
            sel_grp = "null"

        ref_post = self.GetTreeCtrlItemByText(sel_pre, item_tree_list)
        if (ref_post != "null"):
            item_tree_list.Select(ref_post)
            item_tree_list.EnsureVisible(ref_post)

        return sel_grp

    def GetTreeLevel(self, tree, item):
        """Extract item tree level - Group or Channel."""
        # first level back
        tmp_grp_item = tree.GetItemParent(item)
        # second Level Back
        tmp_root_item = self.cnl_tree_src.GetItemParent(tmp_grp_item)
        if tmp_root_item.IsOk():
            return "Channel"
        else:
            return "Group"

    def GetGrpTreeSelSrc(self, group_tree, sel_item):
        """Extract Group settings collection dict."""
        # first level back
        tmp_grp_item = group_tree.GetItemParent(sel_item)
        # second Level Back
        if tmp_grp_item.IsOk():
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

    def GetGrpTreeSelDst(self, group_tree, sel_item):
        """Extract Group settings collection dict."""
        # first level back
        tmp_grp_item = group_tree.GetItemParent(sel_item)
        # second Level Back
        if tmp_grp_item.IsOk():
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

        return selDict

    def OnCompSrcSelected(self, event):
        """Call Action when component in list is selected."""
        sel_comp = event.GetText()
        self.activeCompSrc = sel_comp
        self.UpdateGroupListSrc(self.activeCompSrc)
        tree_freeze = self.auto_tree_freeze_cb.GetValue()
        if not tree_freeze:
            self.BuildDependencyTree(self.activeCompSrc)
        # if autofill
        auto_fill = self.auto_src_cb.GetValue()
        if auto_fill:
            self.UpdateCompComboBox(self.comp_name_cb, sel_comp)

            comp_name = sel_comp
            root = self.cnl_tree_src.GetRootItem()
            grp_item = self.cnl_tree_src.GetFirstChild(root)

            if grp_item.IsOk():
                selDict = self.GetGrpTreeSelSrc(self.cnl_tree_src, grp_item)

                self.UpdateGrpSrcComboBoxSet(sel_comp, selDict)

    def OnCompDstSelected(self, event):
        """Call Action when component in destination list is selected."""
        sel_comp = event.GetText()
        self.activeCompDst = sel_comp
        self.UpdateGroupListDst(self.activeCompDst)

        # if autofill
        auto_fill = self.auto_dst_cb.GetValue()
        if auto_fill:
            self.UpdateCompComboBox(self.dep_name_cb, self.activeCompDst)

            comp_name = self.activeCompDst
            root = self.cnl_tree_dst.GetRootItem()
            grp_item = self.cnl_tree_dst.GetFirstChild(root)

            if grp_item.IsOk():
                selDict = self.GetGrpTreeSelDst(self.cnl_tree_dst, grp_item)

                self.UpdateGrpDstComboBoxSet(sel_comp, selDict)

        # comp = event.GetText()
        # self.activeCompDst = comp
        # self.UpdateGroupListDst(comp)
        # self.dep_name_cb.SetValue(comp)

    def OnCompGrpSrcSelected(self, event):
        """Call Action when component in list is selected."""
        sel_item = event.GetItem()
        # print("selectGrp >>")

        auto_fill = self.auto_src_cb.GetValue()
        if auto_fill:
            if sel_item.IsOk():
                selDict = self.GetGrpTreeSelSrc(self.cnl_tree_src, sel_item)

                self.UpdateGrpSrcComboBoxSet(self.activeCompSrc, selDict)

    def OnCompGrpDstSelected(self, event):
        """Call Action when component in list is selected."""
        sel_item = event.GetItem()

        auto_fill = self.auto_dst_cb.GetValue()
        if auto_fill:
            if sel_item.IsOk():
                selDict = self.GetGrpTreeSelDst(self.cnl_tree_dst, sel_item)

                self.UpdateGrpDstComboBoxSet(self.activeCompDst, selDict)

    def OnSelChanged(self, event):
        """Handle Bulder tree selection."""
        sel_item = event.GetItem()
        comp = self.comp_tree_dep.GetItemText(sel_item)
        auto_fill = self.auto_tree_cb.GetValue()

        if auto_fill:
            if sel_item.IsOk():
                self.SetActiveComp(self.comp_list_src, comp)
                dep_list = self.curPrj.GetPrjCompAllDepList(comp)
                print(dep_list)
                dep_list += self.curPrj.GetDefCompDepList(comp)
                print(dep_list)
                if len(dep_list) >0 :
                    self.SetActiveComp(self.comp_list_dst, dep_list[0])

        print("OnSelChanged:   ",
              self.comp_tree_dep.GetItemText(event.GetItem()))

    def BuildDependencyTree(self, comp):
        """Build dependency tree entry."""
        # Clear the tree
        self.comp_tree_dep.DeleteAllItems()
        # Init tree root
        root = self.comp_tree_dep.AddRoot(comp)
        # Start Tree building
        self.BuildTreeDependency(root, comp)
        # Expand the dependency tree

    def BuildTreeDependency(self, parent, comp):
        """Build dependency tree recurency."""
        # Extrect componet dependencies
        dep_list = self.curPrj.GetDefCompDepList(comp)
        for comp_it in dep_list:
            # if it is not the parent comp then it is a child
            if str(comp_it) != str(comp):
                # Insert child in the tree
                child = self.comp_tree_dep.AppendItem(parent, comp_it)
                # Color Mark component in the project
                color = self.curPrj.GetCompStatusColor(comp_it)
                self.comp_tree_dep.SetItemTextColour(child, color)
                # Go recurrently through children
                self.BuildTreeDependency(child, comp_it)
                # Expand the dependency tree
                self.comp_tree_dep.ExpandAll()

    def BuildConfigTree(self, comp):
        """Build dependency tree entry."""
        # Clear the tree
        self.comp_tree_dep.DeleteAllItems()
        # Init tree root
        root = self.comp_tree_dep.AddRoot(comp)
        # Start Tree building
        self.BuildTreeDependency(root, comp)
        # Expand the dependency tree

    def BuildTreeConfig(self, parent, comp):
        """Build dependency tree recurency."""
        # load selected component configuration
        # self.curPrj.LoadCompConfigFile(comp)
        # Extrect componet dependencies
        def_dep_list = self.curPrj.GetDefCompDepList(comp)
        prj_dep_list = self.curPrj.GetPrjCompAllDepList(comp)
        dep_list = self.curPrj.GetUniqueList(def_dep_list + prj_dep_list)

        # Color Mark component in the project
        color = self.curPrj.GetCompStatusColor(comp)
        self.comp_tree_dep.SetItemTextColour(parent, color)
        self.comp_tree_dep.SetItemBackgroundColour(parent, "gray")
        grp_list = self.curPrj.GetPrjCompGrpList(comp)
        for grp_it in grp_list:
            #  Add group instance in tree
            child_grp = self.comp_tree_dep.AppendItem(parent, grp_it)
            self.comp_tree_dep.SetItemBackgroundColour(child_grp, "light gray")

            # Add channel instances in tree
            cnl_list = self.curPrj.GetPrjCompGrpCnlList(comp, grp_it)
            child_cnl = self.comp_tree_dep.AppendItem(child_grp, str(cnl_list))
            for cnl_it in cnl_list:
                self.comp_tree_dep.AppendItem(child_cnl, str(cnl_it))

            # Add Dependencies instancies in the list
            grp_dep = self.curPrj.GetPrjCompGrpDep(comp, grp_it)
            #  If dependency is not defined in the group
            if grp_dep == "null":
                grp_dep_def_list = self.curPrj.GetDefCompDepList(comp)
                grp_dep += str(grp_dep_def_list)
                # Insert child in the tree
                child_dep = self.comp_tree_dep.AppendItem(child_grp, grp_dep)
                # insert dependency list form definition
                for dep_it in grp_dep_def_list:
                    self.comp_tree_dep.AppendItem(child_dep, str(dep_it))
            else:
                child_dep = self.comp_tree_dep.AppendItem(child_grp, grp_dep)

            # Add Dependencies instancies in the list
            grp_dep = self.curPrj.GetPrjCompGrpDep(comp, grp_it)
            #  If dependency is not defined in the group
            if grp_dep == "null":
                grp_dep_def_list = self.curPrj.GetDefCompDepList(comp)
                grp_dep += str(grp_dep_def_list)
                # Insert child in the tree
                child_dep = self.comp_tree_dep.AppendItem(child_grp, grp_dep)
                # insert dependency list form definition
                for dep_it in grp_dep_def_list:
                    self.comp_tree_dep.AppendItem(child_dep, str(dep_it))
            else:
                child_dep = self.comp_tree_dep.AppendItem(child_grp, grp_dep)

        # if it is not the parent comp then it is a child
            if grp_dep != comp:
                # Go recurrently through children
                self.BuildTreeConfig(child_dep, grp_dep)
                # Expand the dependency tree

            self.comp_tree_dep.Expand(child_grp)

        if self.curPrj.GetPrjCompObj(comp) != "null":
            self.comp_tree_dep.Expand(parent)
