#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys
import urllib2

class cms_env:
    def __init__(self): 
        # os.getenv is equivalent, and can also give a default value instead of `None`
        self.CMSSWBASE = os.getenv('CMSSW_BASE', "CMSSW_BASE")
        self.CMSSWBASECMSSWRELEASEBASE = os.getenv('CMSSW_RELEASE_BASE', "CMSSW_RELEASE_BASE")
        self.CMSSWBASECMSSWVERSION = os.getenv('CMSSW_VERSION', "CMSSW_VERSION")

    def getCMSSWBASE(self):
        CMSSWBASE = os.getenv('CMSSW_BASE', "CMSSW_BASE")
        return CMSSWBASE
		
    def getCMSSWBASECMSSWRELEASEBASE(self):
        return self.CMSSWBASECMSSWRELEASEBASE
		
    def getCMSSWBASECMSSWVERSION(self):
        return self.CMSSWBASECMSSWVERSION
		
    def cmsAll(self):
        cmsAll="<strong>CMSSW_BASE</strong> : " + self.getCMSSWBASE()
        cmsAll+="<br /><strong>CMSSW_RELEASE_BASE</strong> : " + self.getCMSSWBASECMSSWRELEASEBASE()
        cmsAll+="<br /><strong>CMSSW_VERSION</strong> : " + self.getCMSSWBASECMSSWVERSION()
        return cmsAll

    def eosText(self):
        eosText = 'eos ls /eos/cms/store/relval/' 
        return eosText

    def eosFind(self):
        eosFind="http://cms-project-relval.web.cern.ch/cms-project-relval/relval_stats/"
        return eosFind

    def eosArch_1(self):
        eosArch_1="eos ls /eos/cms/store/group/phys_egamma/"
        return eosArch_1

    def liste_datasets(self):
        liste_datasets = ['RelValSingleElectronPt10_UP15', 'RelValSingleElectronPt1000_UP15', 'RelValSingleElectronPt35_UP15', 'RelValQCD_Pt_80_120_13', 'RelValTTbar_13', 'RelValZEE_13']
        return liste_datasets

    def liste_datasets_miniAOD(self):
        return self.liste_datasets()

    def liste_datasets_fast(self):
        liste_fast = ['RelValTTbar_13', 'RelValZEE_13']
        return liste_fast

    def liste_datasets_pu(self):
        return self.liste_fast()

    def liste_type(self):
        liste_type = ['GEN-SIM-RECO', 'MINIAODSIM', 'GEN-SIM-DIGI-RECO']
        return liste_type

    def liste_tab(self):
        list_tab = ['liste_datasets', 'liste_datasets_miniAOD', 'liste_datasets_fast']
        return list_tab
        
    def dictionnaire(self):
        dictionnaire = {}
        #dictionnaire["liste_datasets"] = ['RelValSingleElectronPt10_UP15', 'RelValSingleElectronPt1000_UP15', 'RelValSingleElectronPt35_UP15', 'RelValQCD_Pt_80_120_13', 'RelValTTbar_13', 'RelValZEE_13']
        #dictionnaire["liste_datasets_miniAOD"] = ['RelValSingleElectronPt10_UP15', 'RelValSingleElectronPt1000_UP15', 'RelValSingleElectronPt35_UP15', 'RelValQCD_Pt_80_120_13', 'RelValTTbar_13', 'RelValZEE_13']
        dictionnaire["liste_datasets"] = ['RelValSingleElectronPt10', 'RelValSingleElectronPt1000', 'RelValSingleElectronPt35', 'RelValQCD_Pt_80_120_13', 'RelValTTbar_13', 'RelValZEE_13']
        dictionnaire["liste_datasets_miniAOD"] = ['RelValSingleElectronPt10', 'RelValSingleElectronPt1000', 'RelValSingleElectronPt35', 'RelValQCD_Pt_80_120_13', 'RelValTTbar_13', 'RelValZEE_13']
        dictionnaire["liste_datasets_fast"] = ['RelValTTbar_13', 'RelValZEE_13']
        return dictionnaire

