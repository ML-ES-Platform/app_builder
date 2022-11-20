import app_builder_prj as app_prj

curPrj = app_prj.AppBuilderProject("")


def GetSelectedTreePath(tree_list):
    tree_path = []

    item_ref = tree_list.GetSelection()

    while True:
        if item_ref.IsOk():
            result = tree_list.GetItemText(item_ref)
            tree_path.insert(0, result)
            print(result)
            item_ref = tree_list.GetItemParent(item_ref)
            if item_ref == tree_list.GetRootItem():
                break
        else:
            break

    return tree_path


def ShowCompDef(JSON_object, tree_list, comp):
    tree_list.DeleteAllItems()
    root_item = tree_list.GetRootItem()
    child_item = tree_list.AppendItem(root_item, comp)
    key_list = ["Components", comp]
    ShowRecurrentCompDef(JSON_object, tree_list, child_item, key_list)


def ShowRecurrentCompDef(JSON_object, tree_list, parent_item, key_list):
    item_list = curPrj.GetValueListByKeyList(JSON_object, key_list)
    # print(item_list)
    for item in item_list:
        item_key_list = key_list + [item]
        child_item = tree_list.AppendItem(parent_item, item)
        item_val = curPrj.GetValueByKeyList(JSON_object, item_key_list)
        # print(type(item_val))
        if type(item_val) == list:
            tree_list.SetItemText(child_item, 1, str(item_val))
            for list_item in item_val:
                tree_list.AppendItem(child_item, list_item)

        elif type(item_val) == dict:
            item_val = curPrj.GetValueListByKeyList(JSON_object, item_key_list)
            tree_list.SetItemText(child_item, 1, str(item_val))
            ShowRecurrentCompDef(JSON_object, tree_list, child_item,
                                 item_key_list)
        else:
            tree_list.SetItemText(child_item, 1, str(item_val))

        tree_list.Expand(child_item)
    tree_list.Expand(parent_item)

    return
