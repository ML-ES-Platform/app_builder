"""Project management module."""
import json
import os
import git
import app_builder_gen as gen


class AppBuilderProject(gen.AppGenerator):
    """Application builder project manager."""

    def __init__(self, x):
        """Init the manager instance."""
        self.prjContentChanged = False
        self.cbChangedParent = "null"

        self.platformUrl = "none"
        self.platformDir = "none"
        self.platformFileName = "none"
        self.headerFile = "none"
        self.srcFile = "none"
        self.dotFile = "none"
        self.compDefaultPath = "none"
        self.JSON_project = {}
        self.JSON_platform = {}
        self.JSON_config = {}
        self.JSON_comp_config = {}
        self.activeComponent = "none"
        self.activeGroup = "none"
        self.activeChannel = "none"
        # self.SetProjectFileName("none")
        # self.SetProjectHomeDir("none")
        self.prjContentChanged = False

    def NewProjectFile(self, pathname):
        """Create a new project instance."""
        self.JSON_project = {}
        self.SetProjectFilePath(pathname)
        # self.SaveProjectFile()

    def LoadProjectFile(self, pathname):
        """Open the Json Project configuration File."""
        with open(pathname, 'r') as file:
            self.JSON_project = json.load(file)
            self.SetProjectFilePath(pathname)
            file.close()
        filePath = self.GetProjectFilePath()
        self.prjContentChanged = False

    def SaveProjectFile(self):
        """Save the Json Project configuration File."""
        filePath = self.GetProjectFilePath()
        with open(filePath, 'w') as file:
            json.dump(self.JSON_project, file, indent=4)
            file.close

    def LoadCompConfigFile(self, comp):
        """Load component configuration file."""
        result = False
        prjDir = self.GetProjectHomeDir()
        compDir = self.GetPlatformCompPath(comp)
        configFileName = (prjDir + "/" + compDir + "/" +
                          "config.json").replace("//", "/")
        try:
            with open(configFileName, 'r') as file:
                self.JSON_config = json.load(file)
                result = True
        except IOError:
            print("Cannot open file '%s'." % configFileName)
            result = False

        return result

    def LoadCompDefinitions(self):
        """Load all component definitions registered in platform."""
        plf_comp_list = self.GetPlatformCompList()
        # print(plf_comp_list)
        self.JSON_comp_config["Components"] = {}
        for comp in plf_comp_list:
            if self.LoadCompConfigFile(comp):
                # self.JSON_comp_config = self.merge_two_dicts(self.JSON_comp_config, self.JSON_config) 
                self.JSON_comp_config["Components"][comp] = self.JSON_config["Components"][comp]

        # print(self.JSON_comp_config)
    


    def LoadPlatformFile(self):
        """Extract component list and the references in a panel."""
        platformFilePath = self.GetProjectHomeDir(
        ) + "/" + self.platformDir + "/" + self.platformFileName

        with open(platformFilePath, "r") as read_file:
            self.JSON_platform = json.load(read_file)

    def UpdatePlatform(self, platformUrl, platformDir):
        """Update Platform configuration from the git."""
        resp = requests.get(platformUrl)
        filename = platformUrl.split("/")[-1]

        if not os.path.exists(platformDir):
            os.makedirs(platformDir)

        open(platformDir + "\\" + filename, 'w').write(resp.text)

    # --------------------------

    def SetValueByKeyList(self, JSON_object, key_list, value):
        """Set a value by given key list."""
        result = "null"
        if len(key_list) > 0:
            key = key_list[-1]
            new_keylist = key_list[:-1]
            objRef = self.GetValueByKeyList(JSON_object, new_keylist)
            if objRef != "null":
                objRef[key] = value
                result = objRef
                self.prjContentChanged = True
                self.OnProjectChangedCallback()
        return result

    def OnProjectChangedCallback(self):
        """React on write access in the project content."""
        if self.cbChangedParent == "null":
            print("the Changed call back is not set")
        else:
            self.cbChangedParent.OnProjectChanged()

    def AddObjectByKeylist(self, JSON_object, key_list):
        """Add an empty object to a location defined by a keylist."""
        # TODO think about recursive
        # result = "null"
        empty_dict = {}  # don't use previous, should be a new assignment
        result = self.GetValueByKeyList(JSON_object, key_list)
        if result == "null":
            result = self.SetValueByKeyList(JSON_object, key_list, empty_dict)
        return result

    # --------------------------
    def GetValueByKeyList(self, JSON_object, key_list):
        """Extract a value following a keylist."""
        result = "null"
        resultRef = JSON_object
        for key in key_list:
            if key in resultRef:
                resultRef = resultRef[key]
            else:
                resultRef = "null"
                break
        result = resultRef
        return result

    # --------------------------
    def GetValueListByKeyList(self, JSON_object, key_list):
        """Extract a list of values following the same keylist."""
        result = []
        resultRef = JSON_object
        for key in key_list:
            if key in resultRef:
                resultRef = resultRef[key]
            else:
                resultRef = "null"
                break
        if resultRef != "null":
            for item in resultRef:
                result.append(item)

        return result

    def GetDefCompByKey(self, comp, key):
        """Extract a configuration from component definition by a key."""
        key_list = ["Components", comp, key]
        result = self.GetValueByKeyList(self.JSON_comp_config, key_list)
        return result

    def GetDefCompName(self, comp):
        """Test the component Name exists in definitions."""
        if comp not in JSON_comp_config["Components"]:
            comp = "null"
        
        return comp

    def GetDefCompGit(self, comp):
        return GetDefCompByKey(self, comp, "git")

    def GetDefCompPath(self, comp):
        return GetDefCompByKey(self, comp, "Path")

    def GetDefCompGrpList(self, comp):
        key_list = ["Components", comp, "Groups"]
        result = self.GetValueListByKeyList(self.JSON_comp_config, key_list)
        return result

    def GetDefCompGrpCnlList(self, comp, grp):
        key_list = ["Components", comp, "Groups", grp, "Channels", "Names"]
        result = self.GetValueListByKeyList(self.JSON_comp_config, key_list)
        return result

    def GetDefCompAllListByKey(self, comp, key):
        result = []
        grp_list = self.GetDefCompGrpList(comp)
        for grp in grp_list:
            key_list = ["Components", comp, "Groups", grp, key]
            result += self.GetValueListByKeyList(self.JSON_comp_config, key_list)
        return result

    def GetDefCompDepList(self, comp):
        return self.GetDefCompAllListByKey(comp, "Dependency")

    def GetDefCompDefineList(self, comp):
        return self.GetDefCompAllListByKey(comp, "Defines")

    def GetDefCompPullList(self, comp):
        return self.GetDefCompAllListByKey(comp, "Pull")

    def GetDefCompPushList(self, comp):
        return self.GetDefCompAllListByKey(comp, "Push")

    def GetDefCompGrpByKey(self, comp, grp, key):
        key_list = ["Components", comp, "Groups", grp, key]
        result = self.GetValueByKeyList(self.JSON_comp_config, key_list)
        return result

    def GetDefCompGrpListByKey(self, comp, grp, key):
        key_list = ["Components", comp, "Groups", grp, key]
        result = self.GetValueListByKeyList(self.JSON_comp_config, key_list)
        return result

    def GetDefCompGrpName(self, comp, grp):
        key_list = ["Components", comp, "Groups", grp]
        result = self.GetValueByKeyList(self.JSON_comp_config, key_list)
        return result

    def GetDefCompGrpMultiplicity(self, comp, grp):
        return self.GetDefCompGrpByKey(comp, grp, "Multiplicity")

    def MultiplicityDecode(self, multiplicity, max_mult=5):
        """Decode Multiplicity string."""
        counts = [0, 0]
        str_counts = multiplicity.split("-")

        mapper = lambda x: -1 if x == '*' else int(x)

        if len(str_counts) > 0:
            counts[0] = mapper(str_counts[0])

        if len(str_counts) == 1:
            counts[1] = mapper(str_counts[0])

        if len(str_counts) > 1:
            counts[1] = mapper(str_counts[1])

        if counts[0] == -1:
            counts = [0, max_mult]
        elif counts[1] == -1:
            counts[1] = max_mult

        return counts

    def GetDefCompGrpNameSpace(self, comp, grp):
        return self.GetDefCompGrpByKey(comp, grp, "NameSpace")

    def GetDefCompGrpNames(self, comp, grp):
        return self.GetDefCompGrpByKey(comp, grp, "Names")

    def GetDefCompGrpDepList(self, comp, grp):
        return self.GetDefCompGrpListByKey(comp, grp, "Dependency")

    def GetDefCompGrpDefList(self, comp, grp):
        return self.GetDefCompGrpListByKey(comp, grp, "Defines")

    def GetDefCompGrpPullList(self, comp, grp):
        return self.GetDefCompGrpListByKey(comp, grp, "Pull")

    def GetDefCompGrpPushList(self, comp, grp):
        return self.GetDefCompGrpListByKey(comp, grp, "Push")

    def GetDefCompCnlByKey(self, comp, grp, key):
        key_list = ["Components", comp, "Groups", grp, "Channels", key]
        result = self.GetValueByKeyList(self.JSON_comp_config, key_list)
        return result

    def GetDefCompCnlNameSpace(self, comp, grp):
        return self.GetDefCompCnlByKey(comp, grp, "NameSpace")

    def GetDefCompCnlNames(self, comp, grp):
        return self.GetDefCompCnlByKey(comp, grp, "Names")

    def GetDefCompCnlMultiplicity(self, comp, grp):
        return self.GetDefCompCnlByKey(comp, grp, "Multiplicity")

    def GetPlatformComp(self, comp):
        """Return the component if it exists."""
        if comp in self.JSON_platform["Components"]:
            result = comp
        else:
            result = "null"

        return result

    def GetPlatformCompList(self):
        """Return the component list in the project."""
        key_list = ["Components"]
        result = self.GetValueListByKeyList(self.JSON_platform, key_list)
        return result

    def GetPlatformCompDepList(self):
        """Return the component list in the project."""
        comp_list = []
        plf_comp_list = self.GetPlatformCompList()
        for comp in plf_comp_list:
            # self.LoadCompConfigFile(comp)
            item_list = self.GetDefCompDepList(comp)
            for item in item_list:
                if item not in comp_list:
                    if item !="null":
                        comp_list.append(item)
        return comp_list

    def GetAllCompList(self):
        plf_comp_list = self.GetPlatformCompList()
        # print(plf_comp_list)
        plf_comp_dep_list = self.GetPlatformCompDepList()
        # print(plf_comp_dep_list)
        prj_comp_list = self.GetProjectCompList()
        # print(prj_comp_list)
        prj_comp_dep_list = self.GetProjectCompDepList()
        # print(prj_comp_dep_list)
        comp_list = self.GetUniqueList(plf_comp_list + plf_comp_dep_list +
                                       prj_comp_list + prj_comp_dep_list)
        # print(comp_list)
        return comp_list

    def GetPlatformCompCfgByKey(self, comp, key):
        """Extract platform component Name."""
        result = "null"
        key_list = ["Components", comp, key]
        result = self.GetValueByKeyList(self.JSON_platform, key_list)
        return result

    def GetPlatformCompPath(self, comp):
        """Extract  platform component path."""
        return self.GetPlatformCompCfgByKey(comp, "Path")

    def GetPlatformCompGit(self, comp):
        """Extract platform component git."""
        return self.GetPlatformCompCfgByKey(comp, "git")

    def GetPlatformPathSet(self, comp):
        """Extract component path set."""
        pathSet = None
        comp_list = self.GetProjectCompList()
        if comp in comp_list:
            pathSet = {}
            pathSet["git"] = self.GetPlatformCompGit(comp)
            pathSet["Path"] = self.GetPlatformCompPath(comp)
        return pathSet

    def GetPlatformPathList(self):
        """Extract component list and the references in a panel."""
        comp_list = None
        if "Components" in self.JSON_platform:
            comp_list = {}
            linkComps = self.JSON_platform["Components"]
            for comp in linkComps:
                comp_list[comp] = self.GetPlatformPathSet(comp)

        return comp_list

    def GetGroupDict(self, comp, grp):
        result = "null"
        if "Components" in self.JSON_project:
            dictComps = self.JSON_project["Components"]
            if comp in dictComps:
                if "Groups" in dictComps[comp]:
                    dictGrp = dictComps[comp]["Groups"]
                    if grp in dictGrp:
                        result = dictGrp[grp]
        return result

    def SetProjectFileName(self, pathname):
        """Set project File Name."""
        filename = os.path.basename(pathname).replace("\\", "/")
        key_list = ["FileName"]
        result = self.SetValueByKeyList(self.JSON_project, key_list, filename)
        return filename

    def SetProjectHomeDir(self, pathname):
        """Set project File Name."""
        homeDir = os.path.dirname(pathname).replace("\\", "/")
        key_list = ["HomeDir"]
        result = self.SetValueByKeyList(self.JSON_project, key_list, homeDir)
        return homeDir

    def SetProjectFilePath(self, pathname):
        """Set project File Path."""
        fileName = self.SetProjectFileName(pathname)
        homeDir = self.SetProjectHomeDir(pathname)
        filePath = homeDir + "/" + fileName
        return filePath

    def GetProjectFileName(self):
        """Get project File Name."""
        key_list = ["FileName"]
        result = self.GetValueByKeyList(self.JSON_project, key_list)
        return result

    def GetProjectHomeDir(self):
        """Get project Home Directory."""
        key_list = ["HomeDir"]
        result = self.GetValueByKeyList(self.JSON_project, key_list)
        return result

    def GetProjectFilePath(self):
        """Return project File Path."""
        homeDir = self.GetProjectHomeDir()
        fileName = self.GetProjectFileName()
        filePath = homeDir + "/" + fileName
        return filePath

    def GetProjectCompList(self):
        """Return the component list in the project."""
        key_list = ["Components"]
        result = self.GetValueListByKeyList(self.JSON_project, key_list)
        return result

    def GetDefCompList(self):
        """Return the component list in the project."""
        key_list = ["Components"]
        result = self.GetValueListByKeyList(self.JSON_comp_config, key_list)
        return result




    def GetPrjCompAllDepList(self, comp):
        dep_list = []
        grp_list = self.GetPrjCompGrpList(comp)
        for grp in grp_list:
            dep = self.GetPrjCompGrpDep(comp, grp)
            if dep != "null":
                dep_list.append(dep)
        return dep_list


    def GetProjectCompDepList(self):
        """Return the component dependency list in the project."""
        comp_list = []
        prj_comp_list = self.GetProjectCompList()
        for comp in prj_comp_list:
            item_list = self.GetPrjCompAllDepList(comp)
            for item in item_list:
                if item not in comp_list:
                    if item != "null":
                        comp_list.append(item)
        return comp_list




        key_list = ["Components"]
        result = self.GetValueListByKeyList(self.JSON_project, key_list)
        return result

    def AddPrjComp(self, comp):
        """Add component object."""

        key_list = ["Components"]
        result = self.AddObjectByKeylist(self.JSON_project, key_list)

        key_list = ["Components", comp]
        result = self.AddObjectByKeylist(self.JSON_project, key_list)

        return result

    def AddPrjCompGrp(self, comp, grp):
        """Add component object."""

        key_list = ["Components", comp]
        result = self.GetValueByKeyList(self.JSON_project, key_list)
        if result != "null":
            key_list = ["Components", comp, "Groups"]
            result = self.AddObjectByKeylist(self.JSON_project, key_list)

            key_list = ["Components", comp, "Groups", grp]
            result = self.AddObjectByKeylist(self.JSON_project, key_list)

        return result

    def AddPrjCompGrpCnl(self, comp, grp, cnl):
        """Add component object."""

        key_list = ["Components", comp, "Groups", grp]
        result = self.GetValueByKeyList(self.JSON_project, key_list)
        if result != "null":
            key_list = ["Components", comp, "Groups", grp, "Channels"]
            result = self.AddObjectByKeylist(self.JSON_project, key_list)

            key_list = ["Components", comp, "Groups", grp, "Channels", cnl]
            result = self.SetValueByKeyList(self.JSON_project, key_list,
                                            "null")

        return result

    def GetUniqueList(self, in_list):
        """Extract unique list"""
        out_list = []
        for item in in_list:
            if item not in out_list:
                out_list.append(item)
        return out_list

    def GetCompStatusColor(self, comp):
        """Extract color according to the comp availability status """

        plf_comp_list = self.GetPlatformCompList()
        plf_comp_dep_list = self.GetPlatformCompDepList()
        prj_comp_list = self.GetProjectCompList()
        prj_comp_dep_list = self.GetProjectCompDepList()
        def_comp_list = self.GetDefCompList()

        # New component
        color = "red"  # red
        # Platform component

 
        if comp in plf_comp_list:
            color = "navy"  # blue
            # Installed Platform component
            if comp in prj_comp_list:
                color = "forest green"
            # UN Installed Platform component
            if comp not in def_comp_list:
                color = "purple"
        else:
            #referenced in definition but not in component list
            if comp in plf_comp_dep_list:
                color = "violet red"

            #referenced in components but not in component list
            if comp in prj_comp_dep_list:
                color = "sienna"
        


        return color

    def AddPrjCompGrpCnlLink(self, comp, grp, cnl, link):
        """Add component object."""

        key_list = ["Components", comp, "Groups", grp, "Channels", cnl]
        result = self.SetValueByKeyList(self.JSON_project, key_list, link)

        return result

    def SetPrjCompCfgByKey(self, comp, key, value):
        """Extract platform component Name."""
        key_list = ["Components", comp, key]
        result = self.SetValueByKeyList(self.JSON_project, key_list, value)
        return result

    def SetPrjCompGrpCfgByKey(self, comp, grp, key, value):
        """Extract platform component Name."""
        key_list = ["Components", comp, "Groups", grp, key]
        result = self.SetValueByKeyList(self.JSON_project, key_list, value)
        return result

    def SetPrjCompGrpDep(self, comp, grp, value):
        """Add component name."""
        return self.SetPrjCompGrpCfgByKey(comp, grp, "Dependency", value)

    def SetPrjCompGrpPush(self, comp, grp, value):
        """Add component name."""
        return self.SetPrjCompGrpCfgByKey(comp, grp, "Push", value)

    def SetPrjCompGrpPull(self, comp, grp, value):
        """Add component name."""
        return self.SetPrjCompGrpCfgByKey(comp, grp, "Pull", value)

    def GetPrjCompCfgByKey(self, comp, key):
        """Extract platform component Name."""
        key_list = ["Components", comp, key]
        result = self.GetValueByKeyList(self.JSON_project, key_list)
        return result

    def GetPrjCompName(self, comp):
        """Return the component if exists in the project."""
        if comp in self.JSON_project["Components"]:
            result = comp
        else:
            result = "null"
        return result

    def GetPrjCompObj(self, comp):
        """Return the component if exists in the project."""
        if comp in self.JSON_project["Components"]:
            result = self.JSON_project["Components"][comp]
        else:
            result = "null"
        return result

    def GetPrjCompPath(self, comp):
        """Extract component path."""
        return self.GetPrjCompCfgByKey(comp, "Path")

    def GetPrjCompGit(self, comp):
        """Extract component git."""
        return self.GetPrjCompCfgByKey(comp, "git")

    def GetPrjCompGrpList(self, comp):
        """Return the component group list in the project."""
        key_list = ["Components", comp, "Groups"]
        result = self.GetValueListByKeyList(self.JSON_project, key_list)
        return result

    def GetPrjCompGrpCfgByKey(self, comp, grp, key):
        """Extract platform component Name."""
        result = "null"
        key_list = ["Components", comp, "Groups", grp, key]
        result = self.GetValueByKeyList(self.JSON_project, key_list)
        return result

    def GetPrjCompGrpPush(self, comp, grp):
        """Extract Group Push method."""
        return self.GetPrjCompGrpCfgByKey(comp, grp, "Push")

    def GetPrjCompGrpPull(self, comp, grp):
        """Extract Group Push method."""
        return self.GetPrjCompGrpCfgByKey(comp, grp, "Pull")

    def GetPrjCompGrpDep(self, comp, grp):
        """Extract Group Push method."""
        return self.GetPrjCompGrpCfgByKey(comp, grp, "Dependency")

    def GetPrjCompGrpCnlList(self, comp, grp):
        """Return the component group channel list in the project."""
        key_list = ["Components", comp, "Groups", grp, "Channels"]
        result = self.GetValueListByKeyList(self.JSON_project, key_list)
        return result

    def GetPrjGrpCnlLink(self, comp, grp, cnl):
        """Return the component group channel list in the project."""
        key_list = ["Components", comp, "Groups", grp, "Channels", cnl]
        result = self.GetValueByKeyList(self.JSON_project, key_list)
        return result

    def AddProjectCompFromPlatform(self, comp):

        componetFilePath = self.GetProjectHomeDir(
        ) + "/" + self.platformDir + "/" + self.platformFileName
        projectFilePath = self.GetProjectFilePath()
        # with open(componetFilePath, "r") as read_file:
        #     JSON_CompList = json.load(read_file)
        JSON_CompList = self.JSON_platform
        if "Components" not in self.JSON_project:
            self.JSON_project["Components"] = {}
        JSON_Comps = self.JSON_project["Components"]
        if comp not in JSON_Comps:
            if comp in JSON_CompList["Components"]:
                JSON_Comps[comp] = JSON_CompList["Components"][comp]
            else:
                JSON_Comps[comp] = {}
        # with open(projectFilePath, 'w') as file:
        #     json.dump(self.JSON_project, file, indent=4)
        #     file.close()

    def GenProjectConfig(self):
        """Handle Config Generate Action."""
        jsonFile = self.GetProjectFilePath()
        headerFile = self.GetProjectFilePath() + "_cfg_gen.h"
        srcFile = self.GetProjectFilePath() + "_cfg_gen.cpp"
        self.CfgHeadGen(jsonFile, headerFile)
        self.CfgSrcGen(jsonFile, srcFile)

    def GenProjectDot(self):
        """Handle Dot Generate Action."""
        jsonFile = self.GetProjectFilePath()
        index = 0
        while True:
            if index == 0:
                prefix = ""
            else:
                prefix = "_"+str(index)
            dotFile = self.GetProjectFilePath().split(".")[0]+prefix + ".gv"
            # dotFile = self.GetProjectFilePath()+prefix + ".dot"
            if not os.path.isfile(dotFile):
                break
            index+=1


        self.DotGen(self.JSON_project, dotFile)
        # self.DotGen(jsonFile, dotFile)

    def GenProjectTree(self):
        """Handle Project Tree Generate Action."""
        if "Components" in self.JSON_project:
            linkComps = JSON_Open_object["Components"]
            for comp in linkComps:
                componentName = linkComps[comp]
                if "Path" in linkComps[comp]:
                    compPath = linkComps[comp]["Path"]
                    compDir = str(self.GetProjectHomeDir() + "/" + compPath)
                    if not os.path.exists(compDir):
                        os.makedirs(compDir)
                    if "git" in linkComps[comp]:
                        gitUrl = linkComps[comp]["git"]

                        git.Repo.clone_from(gitUrl, compDir)
