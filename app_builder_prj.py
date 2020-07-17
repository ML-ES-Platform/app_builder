
import json
import os
import git

class AppBuilderProject():
    def __init__(self,x):
        self.prjDir = ""
        self.prjFileName = ""
        self.compsFileName = ""
        self.compsUrl = ""
        self.compsDir = ""
        self.compDefaultPath = "null"
        x = '{ }'
        self.JSON_object = json.loads(x)
        self.JSON_platform = json.loads(x)


    def newProjectFile(self, pathname):

        self.openProjectFile(pathname)

        x = '{ "FileName" : "' + self.prjFileName +'"}'
        self.JSON_object = json.loads(x)

        self.saveProjectFile()


    def openProjectFile(self, pathname):
        """Open the Json Project configuration File."""
        with open(pathname, 'r') as file:

            self.prjDir = os.path.dirname(pathname).replace("\\", "/")
            print(self.prjDir)

            self.prjFileName = os.path.basename(pathname).replace("\\", "/")
            print(self.prjFileName)
    
            self.JSON_object = json.load(file)


    def saveProjectFile(self):
        """Save the Json Project configuration File."""

        filePath = self.prjDir + "/" + self.prjFileName
        with open(filePath, 'w') as file:
            json.dump(self.JSON_object, file, indent=4)


    def GenerateTree (self):

        filePath = self.prjDir + "/" + self.prjFileName

        with open( filePath, "r") as read_file:

            JSON_Open_object = json.load(read_file)

            if "Components" in JSON_Open_object:
                linkComps = JSON_Open_object["Components"]
                for comp in linkComps:
                    componentName = linkComps[comp]
                    if "Path" in linkComps[comp]:
                        compPath = linkComps[comp]["Path"]
                        compDir = str(self.prjDir +"/" + compPath)
                        if not os.path.exists(compDir):
                            os.makedirs(compDir)
                        if "git" in linkComps[comp]:
                            gitUrl = linkComps[comp]["git"]
                            print("====================")
                            print(compDir)
                            print(gitUrl)

                            git.Repo.clone_from(gitUrl,compDir)

    def UpdateComponents(self, compsUrl, compsDir):

        resp = requests.get(compsUrl)
        filename = compsUrl.split("/")[-1]

        if not os.path.exists(compsDir):
            os.makedirs(compsDir)

        # print(curPrj.prjDir + "\\"+curPrj.compsDir+"\\" + filename)
        # print(resp.text)

        open(compsDir + "\\" + filename, 'w').write(resp.text)

    def getPlatformCompName(self, comp):
        """Extract platform component Name."""
        result = "null"
        if "Components" in self.JSON_platform:
            dictComps = self.JSON_platform["Components"]
            if comp in dictComps:
                result = comp
                if "Name" in dictComps[comp]:
                    result = dictComps[comp]["Name"]
        return result

    def getPlatformCompPath(self, comp):
        """Extract  platform component path."""
        result = "null"
        if "Components" in self.JSON_platform:
            dictComps = self.JSON_platform["Components"]
            if comp in dictComps:
                #TBD result = compDefaultPath
                if "Path" in dictComps[comp]:
                    result = dictComps[comp]["Path"]

        return result

    def getPlatformCompGit(self, comp):
        """Extract platform component git."""
        result = "null"
        if "Components" in self.JSON_platform:
            dictComps = self.JSON_platform["Components"]
            if comp in dictComps:
                if "git" in dictComps[comp]:
                    result = dictComps[comp]["git"]
        return result

    def getPlatformPathSet(self, comp):
        """Extract component path set."""
        pathSet = None

        if "Components" in self.JSON_platform:
            dictComps = self.JSON_platform["Components"]
            if comp in dictComps:
                pathSet = {}
                pathSet["Name"] = self.getPlatformCompName(comp)
                pathSet["git"] = self.getPlatformCompGit(comp)
                pathSet["Path"] = self.getPlatformCompPath(comp)
        return pathSet


    def getPlatformPathList(self):
        """Extract component list and the references in a panel."""
        with open( self.prjDir + "/" + self.compsDir + "/" +self.compsFileName, "r") as read_file:
            self.JSON_platform = json.load(read_file)

        comp_list = None
        if "Components" in self.JSON_platform:
            comp_list = {}
            linkComps = self.JSON_platform["Components"]
            for comp in linkComps:
                comp_list[comp] = self.getPlatformPathSet(comp)

        return comp_list



    def getComponentList(self):
        """Return the component list in the project."""
        comp_list = []
        if "Components" in self.JSON_object:
            linkComps = self.JSON_object["Components"]
            for comp in linkComps:
                #print ("Comp ->" +comp +" : " +linkComps[comp] +" *")
                comp_list.insert(0, comp)
        # self.comp_list.SortItems(self.CompareFunction)

        return comp_list
    def getCompName(self, comp):
        """Extract component name."""
        result = "null"
        if "Components" in self.JSON_object:
            dictComps = self.JSON_object["Components"]
            if comp in dictComps:
                result = comp
                if "Name" in dictComps[comp]:
                    result = dictComps[comp]["Name"]
        return result

    def getCompPath(self, comp):
        """Extract component path."""
        result = "null"
        if "Components" in self.JSON_object:
            dictComps = self.JSON_object["Components"]
            if comp in dictComps:
                #TBD result = compDefaultPath
                if "Path" in dictComps[comp]:
                    result = dictComps[comp]["Path"]

        return result

    def getCompGit(self, comp):
        """Extract component git."""
        result = "null"
        if "Components" in self.JSON_object:
            dictComps = self.JSON_object["Components"]
            if comp in dictComps:
                if "git" in dictComps[comp]:
                    result = dictComps[comp]["git"]
        return result
                        
    def getGroupList(self, comp):
        """Return the component group list in the project."""
        grp_list = []
        if "Components" in self.JSON_object:
            dictComps = self.JSON_object["Components"]
            if comp in dictComps:
                if "Groups" in dictComps[comp]:
                    dictGrp = dictComps[comp]["Groups"]
                    for grp in dictGrp:
                        grp_list.insert(0, grp)
        return grp_list

    def getGroupCnlList(self, comp, grp):
        """Return the component group channel list in the project."""
        cnl_list = []
        if "Components" in self.JSON_object:
            dictComps = self.JSON_object["Components"]
            if comp in dictComps:
                if "Groups" in dictComps[comp]:
                    dictGrp = dictComps[comp]["Groups"]
                    if grp in dictGrp:
                        if "Channels" in dictGrp[grp]:
                            dictCnl = dictGrp[grp]["Channels"]
                            print(dictCnl)
                            for cnl in dictCnl:
                                cnl_list.insert(0, cnl)
        return cnl_list

    def getGroupCnlLink(self, comp, grp, cnl):
        """Return the component group channel list in the project."""
        result = "null"
        if "Components" in self.JSON_object:
            dictComps = self.JSON_object["Components"]
            if comp in dictComps:
                if "Groups" in dictComps[comp]:
                    dictGrp = dictComps[comp]["Groups"]
                    if grp in dictGrp:
                        if "Channels" in dictGrp[grp]:
                            dictCnl = dictGrp[grp]["Channels"]
                            if cnl in dictCnl:
                                result = dictCnl[cnl]
        return result
    
    def addProjectCompFromPlatform(self, comp):
        
        componetFilePath = self.prjDir + "/" + self.compsDir + "/" + self.compsFileName
        projectFilePath = self.prjDir + "/" + self.prjFileName

        print("componetFilePath : X")
        print(componetFilePath)

        with open(componetFilePath, "r") as read_file:
            JSON_CompList = json.load(read_file)

        print("self.compsFileName:")
        print(self.compsFileName)

        print("JSON_CompList:")
        print(JSON_CompList)

        if "Components" not in self.JSON_object:
            self.JSON_object["Components"] = {}

        JSON_Comps = self.JSON_object["Components"]

        if comp not in JSON_Comps:

            if comp in JSON_CompList["Components"]:
                JSON_Comps[comp] = JSON_CompList["Components"][comp]
                print("TRUE :")
            else:
                JSON_Comps[comp] = {"Name": comp}
                print("FALSE :")

        with open(projectFilePath, 'w') as file:
            json.dump(self.JSON_object, file, indent=4)

            file.close()

        return

