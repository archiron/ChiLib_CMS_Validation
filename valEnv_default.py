#! /usr/bin/env python
#-*-coding: utf-8 -*-

################################################################################
# GevSeqDev: a tool to generate Release Comparison                              
#
#
#                                                                              
# Arnaud Chiron-Turlay LLR - arnaud.chiron@llr.in2p3.fr                        
#                                                                              
################################################################################

import os,sys
from defEnv import *

class env_default:
    localWorkDir = os.getcwd() + '/'
    sys.path.append(localWorkDir) # path where you work

    def __init__(self):
        self.CMSSWBASE = os.getenv('CMSSW_BASE', "CMSSW_BASE") # donne le repertoire de travail
        self.CMSSWBASECMSSWRELEASEBASE = os.getenv('CMSSW_RELEASE_BASE', "CMSSW_RELEASE_BASE") # donne la release et l'architecture
        self.CMSSWBASECMSSWVERSION = os.getenv('CMSSW_VERSION', "CMSSW_VERSION") # donne la release (CMSSW_7_1_0 par exemple)

    def getCMSSWBASE(self):
        CMSSWBASE = os.getenv('CMSSW_BASE', "CMSSW_BASE")
        return CMSSWBASE

    def workDir(self): # GevSeq.py
        workDir =  self.localWorkDir # '/afs/cern.ch/work/a/archiron/private/CMSSW_10_6_1_patch1_ValELE/src' # the path where you are
        return workDir

    def tmpPath(self): # defaultqV.py
        tmpPath = self.localWorkDir + tmp_path
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

    def KS_path_local(self):
        KS_path_local = '/eos/project/c/cmsweb/www/egamma/validation/Electrons/Store/KS_Curves/'
        return KS_path_local

    def KS_path_web(self):
        KS_path_web = 'http://cms-egamma.web.cern.ch/validation/Electrons/Store/KS_Curves/'
        return KS_path_web

    def web_URL (self):
        web_URL = 'http://cms-egamma.web.cern.ch/validation/Electrons/'
        return web_URL

    def KS_Path(self): # defaultqV.py
        KS_Path = []
        KS_Path.append(self.KS_path_local())
        KS_Path.append(self.KS_path_web())
        KS_Path.append(self.web_URL())
        return KS_Path
