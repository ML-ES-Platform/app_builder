"""Example  docstrings."""
# module: configuration Generator

from graphviz import Digraph
import json

class AppGenerator:
    def CfgHeadGen(self, jsonFile, headerFile):
        """Generate component configuration Header."""
        #
        with open(jsonFile, "r") as read_file:
            JSON_object = json.load(read_file)
            applicationName = JSON_object["ProjectName"]
            appDescription = JSON_object["Description"]

            f_head = open(headerFile, "w")
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
            f_head.write("#include \"platform_config.h\"\n")
            f_head.write("\n")

            linkComps = JSON_object["Components"]
            for comp in linkComps:

                componentName = linkComps[comp]

                if (componentName != "null"):
                    f_head.write("#define " + componentName.upper() + "_CONFIG" +
                                "\n")

                    # Components Groups
                    if "Groups" in linkComps[comp]:

                        linkGroup = linkComps[comp]["Groups"]
                        for grp in linkGroup:
                            groupName = str(linkGroup[grp])

                            # Channels
                            if "Channels" in linkGroup[grp]:
                                f_head.write("enum " + groupName.upper() +
                                            "_IdType {")
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


    def CfgSrcGen(jsonFile, srcFile):
        """Generate component configuration Source file."""
        #
        with open(jsonFile, "r") as read_file:
            JSON_object = json.load(read_file)
            applicationName = JSON_object["ProjectName"]
            appDescription = JSON_object["Description"]

            f_src = open(srcFile, "w")
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
    \n\
    Std_ReturnType " + applicationName + "_config(void)\n\
    {\n\
        Serial.begin(115200);\n\
        Serial.println(\"" + appDescription + "\");\n\
        Std_ReturnType error = E_OK;\n")

            linkComps = JSON_object["Components"]
            for comp in linkComps:

                componentName = linkComps[comp]

                if (componentName != "null"):
                    # Components Groups
                    if "Groups" in linkComps[comp]:
                        linkGroup = linkComps[comp]["Groups"]
                        for grp in linkGroup:
                            groupName = str(linkGroup[grp])

                            # Parent
                            parentChannelStr = ""
                            if "Parent" in linkGroup[grp]:
                                parentChannelStr = linkGroup[grp]["Parent"] + ", "

                            # Channels
                            if "Channels" in linkGroup[grp]:

                                f_src.write("\n")
                                linkChannels = linkGroup[grp]["Channels"]

                                for el in linkChannels:
                                    if (linkChannels[el] != "null"):
                                        f_src.write("\
        error += " + componentName.upper() + "_ChannelSetup(" + parentChannelStr +
                                                    el + ", " + linkChannels[el] +
                                                    ");\n")
                                # Pull
                                if "Pull" in linkGroup[grp]:

                                    f_src.write("\n")
                                    linkChannels = linkGroup[grp]["Channels"]

                                    for el in linkChannels:
                                        if (linkChannels[el] != "null"):
                                            f_src.write("\
        error += " + componentName.upper() + "_SetPullMethod(" + parentChannelStr +
                                                        el + ", " +
                                                        linkGroup[grp]["Pull"] +
                                                        ");\n")

                                # Push
                                if "Push" in linkGroup[grp]:

                                    f_src.write("\n")
                                    linkChannels = linkGroup[grp]["Channels"]

                                    for el in linkChannels:
                                        if (linkChannels[el] != "null"):
                                            f_src.write("\
        error += " + componentName.upper() + "_SetPushMethod(" + parentChannelStr +
                                                        el + ", " +
                                                        linkGroup[grp]["Push"] +
                                                        ");\n")

                                f_src.write("\
        Serial.print(\"" + groupName.upper() + " configured - Error : \");\n\
        Serial.println(error);\n")

                    f_src.write("\n")

        f_src.write("    return error;\n")
        f_src.write("}\n")
        f_src.close()


    def DotGenSelf(self):
        self.DotGen(self.JSON_project, "test.dot")

    def DotGen(self, JSON_object, dotFile):
        """Generate project Linkage dot."""
        #
        dot = Digraph(comment='arm 6-dof demo')

        # with open(jsonFile, "r") as read_file:
        # JSON_object = json.load(read_file)
        if "ProjectName" in JSON_object:
            applicationName = JSON_object["ProjectName"]
        else:
            applicationName = "Noname Project"

        # if "Components" not in JSON_object:
        #     return "null"

        linkComps = JSON_object["Components"]
        for comp in linkComps:

            componentName = linkComps[comp]

            if (componentName != "null"):

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
                                with dot.subgraph( name="cluster_" + comp) as c:
                                    c.attr(color='blue')
                                    c.node_attr['style'] = 'filled'
                                    c.attr(label=comp)
                                    c.node(el)
                                print(el)
                                src = el
                                dst = linkChannels[el]
                                if linkChannels[el] != "null":
                                    dot.edge(src, dst)


        dot.render(dotFile, view=True)
        # dot.render('test-output/round-table.gv', view=True)
        print(dot.source)

        # g = Digraph('G', filename='cluster.gv')
            # g.view()
