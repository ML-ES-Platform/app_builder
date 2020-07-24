import json
import os
import git


class AppBuilderProject():
    def __init__(self, x):
        self.platformUrl = ""
        self.platformDir = ""
        self.platformFileName = ""
        self.prjDir = ""
        self.prjFileName = ""
        self.headerFile = ""
        self.srcFile = ""
        self.dotFile = ""
        self.compDefaultPath = "null"
        x = '{ }'
        self.JSON_project = json.loads(x)
        self.JSON_platform = json.loads(x)
        self.JSON_config = json.loads(x)
        self.activeComponent = ""
        self.activeGroup = ""
        self.activeChannel = ""

    def SetProjectFilePath(self, pathname):
        """Set project File Path."""
        self.prjDir = os.path.dirname(pathname).replace("\\", "/")
        self.prjFileName = os.path.basename(pathname).replace("\\", "/")

    def GetProjectFilePath(self):
        """Return project File Path."""
        filePath = self.prjDir + "/" + self.prjFileName
        return filePath

    def GetProjectDir(self):
        return self.prjDir

    def NewProjectFile(self, pathname):

        self.SetProjectFilePath(pathname)
        x = '{ "FileName" : "' + self.prjFileName + '"}'
        self.JSON_project = json.loads(x)
        self.SaveProjectFile()

    def LoadProjectFile(self, pathname):
        """Open the Json Project configuration File."""
        with open(pathname, 'r') as file:
            self.SetProjectFilePath(pathname)
            self.JSON_project = json.load(file)
            file.close()

    def SaveProjectFile(self):
        """Save the Json Project configuration File."""
        # filePath = self.prjDir + "/" + self.prjFileName
        filePath = self.GetProjectFilePath()
        with open(filePath, 'w') as file:
            json.dump(self.JSON_project, file, indent=4)
            file.close

    def LoadCompConfigFile(self, comp):
        result = False
        prjDir = self.GetProjectDir()
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
        with open(self.prjDir + "/" + self.platformDir + "/" + self.platformFileName,
                  "r") as read_file:
            self.JSON_platform = json.load(read_file)
    

    def UpdatePlatform(self, platformUrl, platformDir):

        resp = requests.get(platformUrl)
        filename = platformUrl.split("/")[-1]

        if not os.path.exists(platformDir):
            os.makedirs(platformDir)

        open(platformDir + "\\" + filename, 'w').write(resp.text)

    # --------------------------
    def GetValueByKey(self, JSON_object, key_list):
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
        result = self.GetValueByKey(self.JSON_config, key_list)
        return result

    def GetDefCompName(self, comp):
        return GetDefCompByKey(self, comp, "Name")

    def GetDefCompGit(self, comp):
        return GetDefCompByKey(self, comp, "git")

    def GetDefCompPath(self, comp):
        return GetDefCompByKey(self, comp, "git")

    def GetDefCompGrpNameList(self, comp):
        result = []
        if "Components" in self.JSON_config:
            dictComps = self.JSON_config["Components"]
            if comp in dictComps:
                if "Groups" in dictComps[comp]:
                    dictGrp = dictComps[comp]["Groups"]
                    for grp in dictGrp:
                        name = str(grp)
                        if "Name" in dictGrp[grp]:
                            name = dictGrp[grp]["Name"]
                            # if dep not in result
                        result.append(name)
        return result

    def GetDefCompGrpList(self, comp):
        key_list = ["Components", comp, "Groups"]
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
        return self.GetDefCompAllListByKey(comp, "Dependencies")

    def GetDefCompDefineList(self, comp):
        return self.GetDefCompAllListByKey(comp, "Defines")

    def GetDefCompPullList(self, comp):
        return self.GetDefCompAllListByKey(comp, "Pull")

    def GetDefCompPushList(self, comp):
        return self.GetDefCompAllListByKey(comp, "Push")

    def GetDefCompGrpByKey(self, comp, grp, key):
        key_list = ["Components", comp, "Groups", grp, key]
        result = self.GetValueByKey(self.JSON_config, key_list)
        return result

    def GetDefCompGrpListByKey(self, comp, grp, key):
        key_list = ["Components", comp, "Groups", grp, key]
        result = self.GetValueListByKey(self.JSON_config, key_list)
        return result

    def GetDefCompGrpName(self, comp, grp):
        return self.GetDefCompGrpByKey(comp, grp, "Name")

    def GetDefCompGrpMultiplicity(self, comp, grp):
        return self.GetDefCompGrpByKey(comp, grp, "Multiplicity")

    def GetDefCompGrpNamespace(self, comp, grp):
        return self.GetDefCompGrpByKey(comp, grp, "NameSpace")

    def GetDefCompGrpDepList(self, comp, grp):
        return self.GetDefCompGrpListByKey(comp, grp, "Dependencies")

    def GetDefCompGrpDefList(self, comp, grp):
        return self.GetDefCompGrpListByKey(comp, grp, "Defines")

    def GetDefCompGrpPullList(self, comp, grp):
        return self.GetDefCompGrpListByKey(comp, grp, "Pull")

    def GetDefCompGrpPushList(self, comp, grp):
        return self.GetDefCompGrpListByKey(comp, grp, "Push")

    def GetDefCompCnlByKey(self, comp, grp, key):
        key_list = ["Components", comp, "Groups", grp, "Channels", key]
        result = self.GetValueByKey(self.JSON_config, key_list)
        return result

    def GetDefCompCnlNameSpace(self, comp, grp):
        return self.GetDefCompCnlByKey(comp, grp, "NameSpace")

    def GetDefCompCnlMultiplicity(self, comp, grp):
        return self.GetDefCompCnlByKey(comp, grp, "Multiplicity")

    def GetPlatformCompList(self):
        """Return the component list in the project."""
        key_list = ["Components"]
        result = self.GetValueListByKey(self.JSON_platform, key_list)
        return result

    def GetPlatformCompCfgByKey(self, comp, key):
        """Extract platform component Name."""
        result = "null"
        key_list = ["Components", comp, key]
        result = self.GetValueByKey(self.JSON_platform, key_list)
        return result

    def GetPlatformCompName(self, comp):
        """Extract platform component Name."""
        return self.GetPlatformCompCfgByKey(comp, "Name")

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
            pathSet["Name"] = self.GetPlatformCompName(comp)
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

    def GetProjectCompList(self):
        """Return the component list in the project."""
        key_list = ["Components"]
        result = self.GetValueListByKey(self.JSON_project, key_list)
        return result


    def GetPrjCompCfgByKey(self, comp, key):
        """Extract platform component Name."""
        result = "null"
        key_list = ["Components", comp, key]
        result = self.GetValueByKey(self.JSON_project, key_list)
        return result

    def GetPrjCompName(self, comp):
        """Extract component name."""
        return self.GetPrjCompCfgByKey(comp, "Name")

    def GetPrjCompPath(self, comp):
        """Extract component path."""
        return self.GetPrjCompCfgByKey(comp, "Path")

    def GetPrjCompGit(self, comp):
        """Extract component git."""
        return self.GetPrjCompCfgByKey(comp, "git")

    def GetPrjGrpList(self, comp):
        """Return the component group list in the project."""
        key_list = ["Components", comp, "Groups"]
        result = self.GetValueListByKey(self.JSON_project, key_list)
        return result

    def GetPrjCompGrpCfgByKey(self, comp, grp, key):
        """Extract platform component Name."""
        result = "null"
        key_list = ["Components", comp, "Groups", grp, key]
        result = self.GetValueByKey(self.JSON_project, key_list)
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


    def GetPrjGrpCnlList(self, comp, grp):
        """Return the component group channel list in the project."""
        key_list = ["Components", comp, "Groups",grp,"Channels"]
        result = self.GetValueListByKey(self.JSON_project, key_list)
        return result

    def GetPrjGrpCnlLink(self, comp, grp, cnl):
        """Return the component group channel list in the project."""
        key_list = ["Components", comp, "Groups",grp,"Channels",cnl]
        result = self.GetValueByKey(self.JSON_project, key_list)
        return result

    def AddProjectCompFromPlatform(self, comp):

        componetFilePath = self.prjDir + "/" + self.platformDir + "/" + self.platformFileName
        projectFilePath = self.prjDir + "/" + self.prjFileName
        # with open(componetFilePath, "r") as read_file:
        #     JSON_CompList = json.load(read_file)
        if "Components" not in self.JSON_project:
            self.JSON_project["Components"] = {}
        JSON_Comps = self.JSON_project["Components"]
        if comp not in JSON_Comps:
            if comp in JSON_CompList["Components"]:
                JSON_Comps[comp] = JSON_CompList["Components"][comp]
            else:
                JSON_Comps[comp] = {"Name": comp}
        # with open(projectFilePath, 'w') as file:
        #     json.dump(self.JSON_project, file, indent=4)
        #     file.close()

    def AddGroup(self, comp, grp):
        if "Components" in self.JSON_project:
            dictComps = self.JSON_project["Components"]
            if comp in dictComps:
                if "Groups" not in dictComps[comp]:
                    dictComps[comp] = {}
                dictGrp = dictComps[comp]["Groups"]
                if grp not in dictGrp:
                    dictGrp[grp] = {"Name": str(grp)}

    def GenProjectConfig(self):
        """Handle Config Generate Action."""
        jsonFile = self.prjDir + "/" + self.prjFileName
        headerFile = self.prjDir + "/" + self.prjFileName + "_cfg_gen.h"
        srcFile = self.prjDir + "/" + self.prjFileName + "_cfg_gen.cpp"
        app_builder_gen.CfgHeadGen(jsonFile, headerFile)
        app_builder_gen.CfgSrcGen(jsonFile, srcFile)

    def GenProjectDot(self):
        """Handle Dot Generate Action."""
        jsonFile = self.prjDir + "/" + self.prjFileName
        dotFile = self.prjDir + "/" + self.prjFileName + ".dot"
        app_builder_gen.DotGen(jsonFile, dotFile)

    def GenProjectTree(self):
        """Handle Project Tree Generate Action."""
        if "Components" in self.JSON_project:
            linkComps = JSON_Open_object["Components"]
            for comp in linkComps:
                componentName = linkComps[comp]
                if "Path" in linkComps[comp]:
                    compPath = linkComps[comp]["Path"]
                    compDir = str(self.prjDir + "/" + compPath)
                    if not os.path.exists(compDir):
                        os.makedirs(compDir)
                    if "git" in linkComps[comp]:
                        gitUrl = linkComps[comp]["git"]

                        git.Repo.clone_from(gitUrl, compDir)
