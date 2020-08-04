import json
import os
import git
import app_builder_gen as gen

class AppBuilderProject(gen.AppGenerator):
    def __init__(self, x):
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
        self.activeComponent = "none"
        self.activeGroup = "none"
        self.activeChannel = "none"
        self.SetProjectFileName("none")
        self.SetProjectHomeDir("none")
        self.prjContentChanged = False
        self.OnProjectChangedCallback = "null"

    def NewProjectFile(self, pathname):

        self.JSON_project = {}
        self.SetProjectFilePath(pathname)
        self.SaveProjectFile()

    def LoadProjectFile(self, pathname):
        """Open the Json Project configuration File."""
        with open(pathname, 'r') as file:
            self.JSON_project = json.load(file)
            self.SetProjectFilePath(pathname)
            file.close()
        filePath = self.GetProjectFilePath()

    def SaveProjectFile(self):
        """Save the Json Project configuration File."""
        filePath = self.GetProjectFilePath()
        with open(filePath, 'w') as file:
            json.dump(self.JSON_project, file, indent=4)
            file.close

    def LoadCompConfigFile(self, comp):
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

    def LoadPlatformFile(self):
        """Extract component list and the references in a panel."""
        platformFilePath = self.GetProjectHomeDir(
        ) + "/" + self.platformDir + "/" + self.platformFileName

        with open(platformFilePath, "r") as read_file:
            self.JSON_platform = json.load(read_file)

    def UpdatePlatform(self, platformUrl, platformDir):

        resp = requests.get(platformUrl)
        filename = platformUrl.split("/")[-1]

        if not os.path.exists(platformDir):
            os.makedirs(platformDir)

        open(platformDir + "\\" + filename, 'w').write(resp.text)

    # --------------------------

    def SetValueByKeyList(self, JSON_object, key_list, value):
        result = "null"
        if len(key_list) > 0:
            key = key_list[-1]
            new_keylist = key_list[:-1]
            objRef = self.GetValueByKeyList(JSON_object, new_keylist)
            if objRef != "null":
                objRef[key] = value
                result = objRef
                self.prjContentChanged
                if self.OnProjectChangedCallback != "null"
                    self.OnProjectChangedCallback()
        return result

    def AddObjectByKeylist(self, JSON_object, key_list):
        # TODO think about recursive
        # result = "null"
        empty_dict = {}  # don't use previous, should be a new assignment
        result = self.GetValueByKeyList(JSON_object, key_list)
        if result == "null":
            result = self.SetValueByKeyList(JSON_object, key_list, empty_dict)
        return result

    # --------------------------
    def GetValueByKeyList(self, JSON_object, key_list):
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

    def GetValueListByKey(self, JSON_object, key_list):
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
        key_list = ["Components", comp, key]
        result = self.GetValueByKeyList(self.JSON_config, key_list)
        return result

    def GetDefCompName(self, comp):
        return comp

    def GetDefCompGit(self, comp):
        return GetDefCompByKey(self, comp, "git")

    def GetDefCompPath(self, comp):
        return GetDefCompByKey(self, comp, "Path")

    def GetDefCompGrpNameList(self, comp):
        result = []
        if "Components" in self.JSON_config:
            dictComps = self.JSON_config["Components"]
            if comp in dictComps:
                if "Groups" in dictComps[comp]:
                    dictGrp = dictComps[comp]["Groups"]
                    for grp in dictGrp:
                        name = str(grp)
                        result.append(name)
        return result

    def GetDefCompGrpList(self, comp):
        key_list = ["Components", comp, "Groups"]
        result = self.GetValueListByKey(self.JSON_config, key_list)
        return result

    def GetDefCompGrpCnlList(self, comp, grp):
        key_list = ["Components", comp, "Groups", grp, "Channels", "Names"]
        result = self.GetValueListByKey(self.JSON_config, key_list)
        return result

    def GetDefCompAllListByKey(self, comp, key):
        result = []
        grp_list = self.GetDefCompGrpList(comp)
        for grp in grp_list:
            key_list = ["Components", comp, "Groups", grp, key]
            result += self.GetValueListByKey(self.JSON_config, key_list)
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
        result = self.GetValueByKeyList(self.JSON_config, key_list)
        return result

    def GetDefCompGrpListByKey(self, comp, grp, key):
        key_list = ["Components", comp, "Groups", grp, key]
        result = self.GetValueListByKey(self.JSON_config, key_list)
        return result

    def GetDefCompGrpName(self, comp, grp):
        key_list = ["Components", comp, "Groups", grp]
        result = self.GetValueByKeyList(self.JSON_config, key_list)
        return result

    def GetDefCompGrpMultiplicity(self, comp, grp):
        return self.GetDefCompGrpByKey(comp, grp, "Multiplicity")

    def MultiplicityDecode(self, multiplicity, max_mult = 5):
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
        return self.GetDefCompGrpListByKey(comp, grp, "Dependency" )

    def GetDefCompGrpDefList(self, comp, grp):
        return self.GetDefCompGrpListByKey(comp, grp, "Defines")

    def GetDefCompGrpPullList(self, comp, grp):
        return self.GetDefCompGrpListByKey(comp, grp, "Pull")

    def GetDefCompGrpPushList(self, comp, grp):
        return self.GetDefCompGrpListByKey(comp, grp, "Push")

    def GetDefCompCnlByKey(self, comp, grp, key):
        key_list = ["Components", comp, "Groups", grp, "Channels", key]
        result = self.GetValueByKeyList(self.JSON_config, key_list)
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
        result = self.GetValueListByKey(self.JSON_platform, key_list)
        return result

    def GetAllCompList(self):
        comp_plf_list = self.GetPlatformCompList()
        comp_prj_list = self.GetProjectCompList()
        comp_list = self.GetUniqueList(comp_plf_list + comp_prj_list)
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
        result = self.GetValueListByKey(self.JSON_project, key_list)
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

        comp_plf_list = self.GetPlatformCompList()
        comp_prj_list = self.GetProjectCompList()

        # New component
        color = "red" # red
        # Platform component
        if comp in comp_plf_list:
            color = "navy"   # blue
            # Installed Platform component
            if comp in comp_prj_list:
                color = "forest green"
            # UN Installed Platform component
            if self.LoadCompConfigFile(comp) == False:
                color = "purple"
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

    def GetPrjCompName(self,comp):
        """Return the component if exists in the project."""
        if comp in self.JSON_project["Components"]:
            result = comp
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
        result = self.GetValueListByKey(self.JSON_project, key_list)
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
        result = self.GetValueListByKey(self.JSON_project, key_list)
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
        dotFile = self.GetProjectFilePath() + ".dot"
        self.DotGen(self.JSON_project, "test.dot" )
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

