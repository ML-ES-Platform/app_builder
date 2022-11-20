"""Example  docstrings."""
# module: configuration Generator

from graphviz import Digraph
import json


class AppGenerator:
    def CfgHeadGen(self, jsonFile, headerFile):
        """Generate component configuration Header."""
        #
        with open(jsonFile, mode='r', encoding='utf-8') as read_file:
            JSON_object = json.load(read_file)
            if "ProjectName" in JSON_object:
                applicationName = JSON_object["ProjectName"]
            else:
                applicationName = "Project"

            if "Description" in JSON_object:
                appDescription = JSON_object["Description"]
            else:
                appDescription = "ES Platform based Project"

            f_head = open(headerFile, mode='w', encoding='utf-8')
            f_head.write("/**\n")
            f_head.write(" * @file " + applicationName + "_cfg_gen.h\n")
            f_head.write(" * @author your name (you@domain.com)\n")
            f_head.write(" * @brief \n")
            f_head.write(" * @version 0.1\n")
            f_head.write(" * @date 2020-06-12\n")
            f_head.write(" * \n")
            f_head.write(" * @copyright Copyright (c) 2020\n")
            f_head.write(" * \n")
            f_head.write(" */\n")

            f_head.write("#ifndef _" + applicationName.upper() + "_CONFIG_H_\n")
            f_head.write("#define _" + applicationName.upper() + "_CONFIG_H_\n")
            f_head.write("\n")
            f_head.write("#include \"./PLF/platform_config.h\"\n")
            f_head.write("\n")

            linkComps = JSON_object["Components"]
            for comp in linkComps:

                # Ignore generation of the component on ignore setting = true
                if "Ignore" in linkComps[comp]:
                    if linkComps[comp]["Ignore"] == "true":
                        continue

                # Override the name of the component if defined by "Name"
                if "Name" in linkComps[comp]:
                    componentName = linkComps[comp]["Name"]
                else:
                    componentName = str(comp)

                # Components Groups
                if "Groups" in linkComps[comp]:

                    # no generation if no groups in component identified
                    if len(linkComps[comp]["Groups"]) == 0:
                        continue
                    
                    # Override the default configuration by defining <Component>__CONFIG symbol
                    f_head.write("#define " + componentName.upper() + "_CONFIG" + "\n")

                    linkGroup = linkComps[comp]["Groups"]
                    for grp in linkGroup:

                        # Ignore generation of the group on ignore setting = true
                        if "Ignore" in linkGroup[grp]:
                            if linkGroup[grp]["Ignore"] == "true":
                                continue

                        # Override the name of the group if defined by "Name"
                        if "Name" in linkGroup[grp]:
                            groupName = linkGroup[grp]["Name"]
                        else:
                            groupName = str(grp)


                        discipline = "SW"
                        if "Discipline" in linkGroup[grp]:
                            discipline = linkGroup[grp]["Discipline"]

                        # do not generate channels config in HEADER for non SW discupline
                        if discipline != "SW" :
                            continue

                        # Channels
                        if "Channels" in linkGroup[grp]:

                            # no generation if no channels in group identified
                            if len(linkGroup[grp]["Channels"]) == 0:
                                continue

                            f_head.write("enum " + groupName.upper() +
                                        "_Cnl_IdType {")
                            linkChannels = linkGroup[grp]["Channels"]
                            for cnl in linkChannels:
                                f_head.write(cnl + ", ")
                            f_head.write(groupName.upper() +
                                        "_CHANNEL_NR_OF};\n")

                        # Defines
                        if "Defines" in linkGroup[grp]:
                            linkDefines = linkGroup[grp]["Defines"]
                            for cnl in linkDefines:
                                f_head.write("#define " + cnl + " " +
                                            str(linkDefines[cnl]) + "\n")
                                            
                # Components Paths in project
                if "Path" in linkComps[comp]:
                    linkPath = linkComps[comp]["Path"]
                    f_head.write("#include \"" + str(linkPath) +
                                    str(componentName) + ".h\"\n")

                f_head.write("\n")

        f_head.write("Std_ReturnType " + applicationName + "_config(void);\n")

        f_head.write("\n")
        f_head.write("#endif // _" + applicationName.upper() + "_CONFIG_H_\n")
        f_head.close()

    def CfgSrcGen(self, jsonFile, srcFile):
        """Generate component configuration Source file."""
        #
        with open(jsonFile, mode='r', encoding='utf-8') as read_file:
            JSON_object = json.load(read_file)

            if "ProjectName" in JSON_object:
                applicationName = JSON_object["ProjectName"]
            else:
                applicationName = "Project"

            if "Description" in JSON_object:
                appDescription = JSON_object["Description"]
            else:
                appDescription = "ES Platform based Project"

            linkComps = JSON_object["Components"]

            f_src = open(srcFile, mode='w', encoding='utf-8')
            f_src.write("\
/**\n\
* @file " + applicationName + "_cfg_gen.cpp\n\
* @author your name (you@domain.com)\n\
* @brief \n\
* @version 0.1\n\
* @date 2020-06-12\n\
* \n\
* @copyright Copyright (c) 2020\n\
* \n\
*/\n\
\n\
#include \"" + applicationName + "_cfg_gen.h\"\n\
\n")

# ////
            for comp in linkComps:

                # Ignore generation of the component on ignore setting = true
                if "Ignore" in linkComps[comp]:
                    if linkComps[comp]["Ignore"] == "true":
                        continue

                # Override the name of the component if defined by "Name"
                if "Name" in linkComps[comp]:
                    componentName = linkComps[comp]["Name"]
                else:
                    componentName = str(comp)


                # Components Groups
                if "Groups" in linkComps[comp]:

                    # no generation if no groups in component identified 
                    if len(linkComps[comp]["Groups"]) == 0:
                        continue

                    linkGroup = linkComps[comp]["Groups"]

                    for grp in linkGroup:

                        # Ignore generation of the group on ignore setting = true
                        if "Ignore" in linkGroup[grp]:
                            if linkGroup[grp]["Ignore"] == "true":
                                continue

                        # Override the name of the group if defined by "Name"
                        if "Name" in linkGroup[grp]:
                            groupName = linkGroup[grp]["Name"]
                        else:
                            groupName = str(grp)

                        # discipline = "SW"
                        # if "Discipline" in linkGroup[grp]:
                        #     discipline = linkGroup[grp]["Discipline"]
                        # if discipline != "SW" :
                        #     continue

                        # Channels
                        if "Channels" in linkGroup[grp]:

                            # no generation if no channels in group identified
                            if len(linkGroup[grp]["Channels"]) == 0:
                                continue

                            f_src.write("Std_ChannelIdType " + groupName.upper() +
                                        "_Group[")                                
                            f_src.write(groupName.upper() +
                                        "_CHANNEL_NR_OF] = {")
                            linkChannels = linkGroup[grp]["Channels"]
                            cnl_str = ""
                            for cnl in linkChannels:
                                cnl_str = cnl_str + cnl + ", "
                            if cnl_str.endswith(', '):
                                cnl_str = cnl_str[:-2]                                
                            f_src.write(cnl_str)
                            f_src.write("};\n\n")




            # ///////////////////////////////////

            f_src.write("\
Std_ReturnType " + applicationName + "_config(void)\n\
{\n\
    Serial.begin(115200);\n\
    Serial.println(\"" + appDescription + "\");\n\
    Std_ReturnType error = E_OK;\n")


            for comp in linkComps:

                # Ignore generation of the component on ignore setting = true
                if "Ignore" in linkComps[comp]:
                    if linkComps[comp]["Ignore"] == "true":
                        continue

                # Override the name of the component if defined by "Name"
                if "Name" in linkComps[comp]:
                    componentName = linkComps[comp]["Name"]
                else:
                    componentName = str(comp)


                # Components Groups
                if "Groups" in linkComps[comp]:

                    # no generation if no groups in component identified 
                    if len(linkComps[comp]["Groups"]) == 0:
                        continue

                    linkGroup = linkComps[comp]["Groups"]

                    for grp in linkGroup:

                        # Ignore generation of the group on ignore setting = true
                        if "Ignore" in linkGroup[grp]:
                            if linkGroup[grp]["Ignore"] == "true":
                                continue

                        # Override the name of the group if defined by "Name"
                        if "Name" in linkGroup[grp]:
                            groupName = linkGroup[grp]["Name"]
                        else:
                            groupName = str(grp)


                        discipline = "SW"
                        if "Discipline" in linkGroup[grp]:
                            discipline = linkGroup[grp]["Discipline"]
                        if discipline != "SW" :
                            continue

                        # Parent
                        parentChannelStr = ""
                        if "Parent" in linkGroup[grp]:
                            parentChannelStr = linkGroup[grp][
                                "Parent"] + ", "

                        # Channels
                        if "Channels" in linkGroup[grp]:

                            # no generation if no channels in group identified
                            if len(linkGroup[grp]["Channels"]) == 0:
                                continue

                            f_src.write("\n")
                            linkChannels = linkGroup[grp]["Channels"]

                            for cnl in linkChannels:
                                if (linkChannels[cnl] != "null"):
                                    f_src.write("\
    error += " + componentName.upper() + "_ChannelSetup(" +
                                                parentChannelStr + cnl +
                                                ", " + linkChannels[cnl] +
                                                ");\n")
                            # Pull
                            if "Pull" in linkGroup[grp]:

                                f_src.write("\n")
                                linkChannels = linkGroup[grp]["Channels"]

                                for cnl in linkChannels:
                                    if (linkChannels[cnl] != "null"):
                                        f_src.write(
                                            "\
    error += " + componentName.upper() + "_SetPullMethod(" +
                                            # parentChannelStr + 
                                            cnl + ", " +
                                            linkGroup[grp]["Pull"] +
                                            ");\n")

                            # Push
                            if "Push" in linkGroup[grp]:

                                f_src.write("\n")
                                linkChannels = linkGroup[grp]["Channels"]

                                for cnl in linkChannels:
                                    if (linkChannels[cnl] != "null"):
                                        f_src.write(
                                            "\
    error += " + componentName.upper() + "_SetPushMethod(" +
                                            # parentChannelStr +
                                            cnl + ", " +
                                            linkGroup[grp]["Push"] +
                                            ");\n")

                            f_src.write("\
    Serial.print(\""+" Group: " + groupName + " configured - Error : \");\n\
    Serial.println(error);\n")

                f_src.write("\n")

        f_src.write("    return error;\n")
        f_src.write("}\n")
        f_src.close()

    # def DotGenSelf(self):
    #     self.DotGen(self.JSON_project, "test.dot")

    def DotGen(self, JSON_object, dotFile):
        """Generate project Linkage dot."""
        #
        dot = Digraph(comment='arm 6-dof demo')

        # with open(jsonFile, mode='r', encoding='utf-8') as read_file:
        # JSON_object = json.load(read_file)

        applicationName = ""

        if "ProjectName" in JSON_object:
            applicationName = JSON_object["ProjectName"]
        else:
            applicationName = "Noname Project"

        # if "Components" not in JSON_object:
        #     return "null"

        layer_cluster = {
            "null" : []
        }
          

        linkComps = JSON_object["Components"]
        for comp in linkComps:

            # Ignore generation of the component on ignore setting = true
            if "Ignore" in linkComps[comp]:
                if linkComps[comp]["Ignore"] == "true":
                    continue

            cluster_name = "null"

            component_name = linkComps[comp]
            if "Domain" in linkComps[comp]:
                cluster_name = linkComps[comp]["Domain"]

            # print(cluster_name)
            # print(comp)

            if cluster_name not in layer_cluster:
                layer_cluster[cluster_name] = []

            layer_cluster[cluster_name].append(comp)



        for cluster_item in layer_cluster:

            cluster_name = str(cluster_item)

            with dot.subgraph(name="cluster_" + cluster_name) as cl_node:
                if cluster_name != "null":
                    cl_node.attr(color='blue')
                    cl_node.node_attr['style'] = 'filled'                   
                    cl_node.attr(label=cluster_name)
                    # cl_node.node(str("x"+cluster_name))

                for component_name in layer_cluster[cluster_name]:
                    if cluster_name == "null":
                        cl_node = dot
                        # dot.node(str("x"+component_name))

                    with cl_node.subgraph(name="cluster_" + str(component_name)) as comp_node:
                        comp_node.attr(color='blue')
                        comp_node.node_attr['style'] = 'filled'
                        comp_node.attr(label=component_name)
                        # comp_node.node(str("x"+component_name))


                        # Components Groups
                        if "Groups" in linkComps[component_name]:
                            if len(linkComps[component_name]["Groups"]) == 0:
                                continue


                            linkGroup = linkComps[component_name]["Groups"]

                            for grp in linkGroup:

                                # Ignore generation of the group on ignore setting = true
                                if "Ignore" in linkGroup[grp]:
                                    if linkGroup[grp]["Ignore"] == "true":
                                        continue
                                    
                                # Override the name of the group if defined by "Name"
                                if "Name" in linkGroup[grp]:
                                    groupName = linkGroup[grp]["Name"]
                                else:
                                    groupName = str(grp)


                                # Channels
                                if "Channels" in linkGroup[grp]:

                                    # no generation if no channels in group identified
                                    if len(linkGroup[grp]["Channels"]) == 0:
                                        continue

                                    linkChannels = linkGroup[grp]["Channels"]

                                    for el in linkChannels:
                                        # NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
                                        #       so that Graphviz recognizes it as a special cluster subgraph
                                        # with dot.subgraph(name="cluster_" + comp) as c:
                                        # comp_node.attr(color='blue')
                                        # comp_node.node_attr['style'] = 'filled'
                                        # comp_node.attr(label=comp)
                                        comp_node.node(el)
                                        # print(el)
                                        src = el
                                        dst = linkChannels[el]
                                        # if "Pull" in linkGroup[grp]:
                                        #     dst = el
                                        #     src = linkChannels[el]
                                        if linkChannels[el] != "null":
                                            dot.edge(src, dst)




        # print(layer_cluster)

        dot.render(dotFile, view=True)
        # dot.render('test-output/round-table.gv', view=True)
        print(dot.source)

        # g = Digraph('G', filename='cluster.gv')
        # g.view()

        print(" Diagram for "+ applicationName + "generated ")

        return


        linkComps = JSON_object["Components"]
        for comp in linkComps:

            component_name = linkComps[comp]

            if (component_name != "null"):

                # Components Groups
                if "Groups" in linkComps[comp]:
                    linkGroup = linkComps[comp]["Groups"]
                    for grp in linkGroup:
                        groupName = str(linkGroup[grp])

                        # Channels
                        if "Channels" in linkGroup[grp]:
                            linkChannels = linkGroup[grp]["Channels"]
                            for el in linkChannels:
                                # NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
                                #       so that Graphviz recognizes it as a special cluster subgraph
                                with dot.subgraph(name="cluster_" + comp) as c:
                                    c.attr(color='blue')
                                    c.node_attr['style'] = 'filled'
                                    c.attr(label=comp)
                                    c.node(el)
                                print(el)
                                src = el
                                dst = linkChannels[el]
                                if linkChannels[el] != "null":
                                    dot.edge(src, dst)
                # Components Groups
                if "Features" in linkComps[comp]:
                    linkGroup = linkComps[comp]["Features"]
                    for ftr in linkGroup:
                        groupName = str(linkGroup[ftr])

                        # Channels
                        if "Channels" in linkGroup[ftr]:
                            linkChannels = linkGroup[ftr]["Channels"]
                            for el in linkChannels:
                                # NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
                                #       so that Graphviz recognizes it as a special cluster subgraph
                                with dot.subgraph(name="cluster_" + comp) as c:
                                    c.attr(color='blue')
                                    c.node_attr['style'] = 'filled'
                                    c.attr(label=comp)
                                    c.node(ftr)
                                print(el)
                                src = ftr
                                dst = el
                                dot.edge(src, dst)

        dot.render(dotFile, view=True)
        # dot.render('test-output/round-table.gv', view=True)
        print(dot.source)

        # g = Digraph('G', filename='cluster.gv')
        # g.view()
