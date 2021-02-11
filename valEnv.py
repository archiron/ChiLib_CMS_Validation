#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys
from default import *
from config import *

class env:
    localWorkDir = os.getcwd()
    sys.path.append(localWorkDir) # path where you work

    def __init__(self):
        self.CMSSWBASE = os.getenv('CMSSW_BASE', "CMSSW_BASE") # donne le repertoire de travail
        self.CMSSWBASECMSSWRELEASEBASE = os.getenv('CMSSW_RELEASE_BASE', "CMSSW_RELEASE_BASE") # donne la release et l'architecture
        self.CMSSWBASECMSSWVERSION = os.getenv('CMSSW_VERSION', "CMSSW_VERSION") # donne la release (CMSSW_7_1_0 par exemple)

    def getCMSSWBASE(self):
        CMSSWBASE = os.getenv('CMSSW_BASE', "CMSSW_BASE")
        return CMSSWBASE

    def workDir(self): # Gev[2/Seq].py
        workDir =  self.localWorkDir # '/afs/cern.ch/work/a/archiron/private/CMSSW_10_6_1_patch1_ValELE/src' # the path where you are
        return workDir

    def tmpPath(self): # defaultqV.py
        tmpPath = tmp_path # '/eos/project/c/cmsweb/www/egamma/validation/Electrons/GUI/Projet_Validations-PortableDev/HistosConfigFiles/'
        return tmpPath

    def imageUp(self): # defaultqV.py
        imageUp = image_up # "http://cms-egamma.web.cern.ch/validation/Electrons/img/up.gif"
        return imageUp

    def imagePoint(self): # defaultqV.py
        imagePoint = image_point # "http://cms-egamma.web.cern.ch/validation/Electrons/img/point.gif"
        return imagePoint

    def imageOK(self): # defaultqV.py
        imageOK = image_OK # "http://cms-egamma.web.cern.ch/validation/Electrons/img/OK.gif"
        return imageOK

    def imageKO(self): # defaultqV.py
        imageKO = image_KO # "http://cms-egamma.web.cern.ch/validation/Electrons/img/KO.gif"
        return imageKO

    def KS_Path(self): # defaultqV.py
        KS_Path = []
        KS_Path.append(KS_path_local)
        KS_Path.append(KS_path_web)
        return KS_Path

    def rel(self): # config.py
        rel = release
        return rel

    def ref(self): # config.py
        ref = reference
        return ref

    def relExtent(self): # config.py
        relExtent = rel_extent
        return relExtent

    def refExtent(self): # config.py
        refExtent = ref_extent
        return refExtent

    def choiceT(self): # config.py
        choiceT = choice
        return choiceT

    def repoExt(self): # config.py
        repoExt = web_repo
        return repoExt

    def webFolder(self): # always after rel & ref
        if ( self.refExtent() != '' ):
            webFolder = self.choiceT() + '_' + self.ref() + "_" + self.refExtent()
        else:
            webFolder = self.choiceT() + '_' + self.ref()
        if ( self.relExtent() != '' ):
            webFolder = self.rel() + "_" + self.relExtent() + "_DQM_" + self.repoExt()[1] + webFolder
        else:
            webFolder = self.rel() + "_DQM_" + self.repoExt()[1] + webFolder
        webFolder = self.repoExt()[0] + webFolder + '/'
        return webFolder

    def redRel(self): # config.py
        redRel = red_release
        return redRel

    def blueRef(self): # config.py
        blueRef = blue_reference
        return blueRef

    def dataSets(self): # config.py
        dataSets = datasets
        return dataSets

    def relrefVT(self): # config.py
        relrefVT = relrefValType
        return relrefVT

    def relFiles(self): # config.py
        relFiles = rel_files
        return relFiles

    def refFiles(self): # config.py
        refFiles = ref_files
        return refFiles

    def DB_Flag(self): # config.py
        DB_Flag = DB_flag
        return DB_Flag
