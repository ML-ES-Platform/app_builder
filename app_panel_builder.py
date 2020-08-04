
"""GUI - Project Builder Panel."""
import wx

class ProjectBuilderPanel(wx.Panel):
    """Panel for component list and the references in the project and git."""
    def __init__(self, parent, curPrj, panel_color):
        """Init Component list Panel."""
        self.parent = parent
        self.curPrj = curPrj
        self.activeCompSrc = "null"
        self.activeCompDst = "null"
        self.activeGrpSrc = "null"
        self.activeGrpDst = "null"
        self.activeCnlSrc = "null"
        self.activeCnlDst = "null"

        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(panel_color)
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
        comp = self.curPrj.activeComponent
        self.UpdateGroupListSrc(comp)
        self.UpdateGroupListDst(comp)

    def OnEnterWindow(self, event):
        self.UpdateCompList()
        comp = self.curPrj.activeComponent
        self.UpdateGroupListSrc(comp)
        self.UpdateGroupListDst(comp)

    def OnAddCompBtnClicked(self, event):
        comp_name = self.comp_name_cb.GetValue()
        self.curPrj.activeComponent = comp_name
        self.curPrj.AddPrjComp(comp_name)
        # self.curPrj.SetPrjCompName(comp_name, comp_name)
        self.UpdatePanel()

    def OnAddGroupBtnClicked(self, event):
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        self.curPrj.AddPrjCompGrp(comp_name, grp_name)
        # self.curPrj.SetPrjCompGrpName(comp_name, grp_name, grp_name)
        self.UpdateCompList()
        return

    def OnAddChannelBtnClicked(self, event):
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        cnl_name = self.cnl_name_cb.GetValue()
        self.curPrj.AddPrjCompGrpCnl(comp_name, grp_name, cnl_name)
        self.UpdateCompList()
        return

    def OnAddLinkBtnClicked(self, event):
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        cnl_name = self.cnl_name_cb.GetValue()
        link_name = self.link_name_cb.GetValue()
        self.curPrj.AddPrjCompGrpCnlLink(comp_name, grp_name, cnl_name, link_name)
        self.UpdateCompList()
        return

    def OnAddDepBtnClicked(self, event):
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        dep_name = self.dep_name_cb.GetValue()
        self.curPrj.SetPrjCompGrpDep(comp_name, grp_name, dep_name)
        self.UpdateCompList()
        return

    def OnAddPushBtnClicked(self, event):
        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        push_name = self.push_name_cb.GetValue()
        self.curPrj.SetPrjCompGrpPush(comp_name, grp_name, push_name)
        self.UpdateCompList()
        return

    def OnAddPullBtnClicked(self, event):

        comp_name = self.comp_name_cb.GetValue()
        grp_name = self.grp_name_cb.GetValue()
        pull_name = self.pull_name_cb.GetValue()
        self.curPrj.SetPrjCompGrpPull(comp_name, grp_name, pull_name)
        print(self.curPrj.JSON_project)
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
        comp_list = self.curPrj.GetAllCompList()
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
        self.curPrj.LoadCompConfigFile(comp)
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
        """Update Component Selector"""
        # TODO colorer for existing group
        self.curPrj.LoadCompConfigFile(comp)
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
        counts = self.curPrj.MultiplicityDecode(multiplicity, max_prj_item_nr_of)
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
        print(dep_comp)
        dep_comp_grp_list = self.curPrj.GetPrjCompGrpList(dep_comp)

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
        prj_item_comp = self.curPrj.GetPrjCompGrpDep(comp, grp)
        # insert it
        item_list.append(prj_item_comp)

        # extract dependencyes from definition
        self.curPrj.LoadCompConfigFile(comp)
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
        print(prj_item_comp)
        item_list.append(prj_item_comp)

        # TODO not form definitions but from dependency
        # extract push  from definition
        self.curPrj.LoadCompConfigFile(comp)
        item_names_list = self.curPrj.GetDefCompDepList(comp)
        # collect Push  from definitions
        for dep_item in item_names_list:
            self.curPrj.LoadCompConfigFile(dep_item)
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
        self.curPrj.LoadCompConfigFile(comp)
        item_names_list = self.curPrj.GetDefCompDepList(comp)
        # collect Push  from definitions
        for dep_item in item_names_list:
            self.curPrj.LoadCompConfigFile(dep_item)
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
        self.curPrj.LoadCompConfigFile(comp)
        item_names_list = self.curPrj.GetDefCompPushList(comp)
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
        self.curPrj.LoadCompConfigFile(comp)
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
        self.curPrj.LoadCompConfigFile(comp)
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

