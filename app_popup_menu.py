"""GUI - Project popup menu collection."""
import wx
import app_builder_prj as ES_project

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
        # window.comp_panel.UpdatePlatformComptList()


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
