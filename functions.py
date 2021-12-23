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

import os,sys # , shutil,subprocess
import re

if sys.version_info >= (3, 0):
    sys.stdout.write("Python 3.x\n")
else:
    sys.stdout.write("Python 2.x\n")

try:
  from httplib import HTTPSConnection # not used ?
except ImportError:
  from http.client import HTTPSConnection

try:
    import urllib2
    from urllib2  import AbstractHTTPHandler
    from urllib2 import build_opener, Request
except ImportError:
    import urllib
    from urllib.request  import AbstractHTTPHandler
    from urllib.request import build_opener
    from urllib.request import Request

class quickRD_Tools:
    def __init__(self):
        pass

    def getDataSet(self, tab_files): # used with quickRD (quick Root Down)
        # tt[0] : dataset
        # tt[1] : RELEASE
        # tt[2] : GlobalTag
        i = 0
        temp = []
        for t in tab_files:
            tt = self.explode_item(t)
            temp.append(tt[0])
            i += 1
        temp = sorted(set(temp), reverse=False)
        return temp

    def explode_item(self, item): # used by getDataSet
        # initial file name : DQM_V0001_R000000001__RelValTTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1__DQMIO.root
        # prefix in DQM_V0001_R000000001__ removed : RelValTTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1__DQMIO.root
        # suffix in __DQMIO.root removed : RelVal
        # new prefix in RelVal removed : TTbar_13__CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
        # splitting with __ : TTbar_13 CMSSW_7_4_0_pre8-PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1
        # splitting second term with - : TTbar_13 CMSSW_7_4_0_pre8 PUpmx50ns_MCRUN2_74_V6_gs_pre7-v1

        temp_item = item[22:] # DQM_V0001_R000000001__ removed
        temp_item = temp_item[:-12] # __DQMIO.root removed
        temp_item = temp_item[6:] # RelVal removed
        temp_item = temp_item.split('__')
        temp_item2 = temp_item[1].split('-', 1)
        temp_item = [ temp_item[0] ]
        for it in temp_item2:
            temp_item.append(it)

        return temp_item

    def analyzeDTS(self, text): # used with quickRD (quick Root Down)
        tmp = text.split(',')
        tmp2 = []
        for item in tmp:
            try:
                tmp_tmp = int(item)
            except:
                print("Something went wrong with %s" % item)
            else:
                tmp2.append(tmp_tmp)
        return tmp2

class Tools:
    def __init__(self):
        pass

    def checkRecompInName(self, name): # no more used
        if re.search('recomp', name):
            return True
        else:
            return False

    def testExtension(self, histoName, histoPrevious): # no more used
        after = "" # $histoName
        common = ""

        if '_' in histoName:
            afters = histoName.split('_')
            before = afters[0]
            nMax = len(afters)

            if ( afters[nMax - 1] == "endcaps" ):
                after = "endcaps"
                for i in range(1, nMax-1):
                    before += "_" + afters[i]
            elif ( afters[nMax - 1] == "barrel" ):
                after = "barrel"
                for i in range(1, nMax-1):
                    before += "_" + afters[i]
            else:
                if ( histoPrevious == "" ):
                    before = histoName
                    after = ""
                    common = histoName
                else:
                    avant =  afters[0]
                    after = ""
                    for i in range(1, nMax-1):
                        avant += "_" + afters[i]
                        if avant == histoPrevious:
                            before = avant
                            common = histoPrevious
                            break
                    for j in range(nMax-1, nMax):
                        after += "_" + afters[j]
                    after = after[1:]

        else: # no _ in histoName
            before = histoName
            common = histoName

        return [after, before, common]

    def shortHistoName(self, elem):
        histo_names = elem.split("/")
        histo_name = histo_names[0]
        histoShortNames = histo_names[1]
        histo_pos = histoShortNames
        histo_positions = histo_pos.split()
        short_histo_names = histoShortNames.split(" ")
        short_histo_name = short_histo_names[0].replace("h_", "")
        if "ele_" in short_histo_name:
            short_histo_name = short_histo_name.replace("ele_", "")
        if "scl_" in short_histo_name:
            short_histo_name = short_histo_name.replace("scl_", "")
        if "bcl_" in short_histo_name:
            short_histo_name = short_histo_name.replace("bcl_", "")
        return short_histo_name, short_histo_names, histo_positions

    def createDatasetFolder(self, folder):
        if not os.path.exists(folder): # create folder
            os.makedirs(folder) # create reference folder
            os.chdir(folder)
            # create gifs folders
            os.makedirs('gifs') # create gifs folder for pictures
            os.chdir('../')
        else: # folder already created
            os.chdir(folder)
            if not os.path.exists('gifs'): #
                # create gifs folders
                os.makedirs('gifs') # create gifs folder for pictures
            os.chdir('../')
        return

    def createDatasetFolder2(self): # for pngs
        if not os.path.exists('pngs'): # create folder
            os.makedirs('pngs') # create pngs folder
        return

    def createDatasetFolder3(self): # for Decision Box
        if not os.path.exists('DBox'): # create folder
            os.makedirs('DBox') # create pngs folder
        return

    def deleteDatasetFolder3(self): # for Decision Box
        import shutil
        if os.path.exists('DBox'): # create folder
            shutil.rmtree('DBox')
        return

    def extWrite(self, text, fileList): #
        for f in fileList:
            f.write(text)
        return

    def testForDataSetsFile(self, tmp_path, type, dataSetsName):
        # also get the tree path part (tp_rel, tp_ref) for root files :
        # folder location for those files : HistosConfigFiles/
        # ElectronMcSignalValidator
        # ElectronMcSignalValidatorMiniAOD
        # ElectronMcSignalValidatorPt1000
        # ElectronMcFakeValidator

        t_rel = tmp_path + 'ElectronMcSignalHistos.txt'
        t_ref = t_rel
        tp_rel = 'ElectronMcSignalValidator'
        tp_ref = tp_rel
        if ( re.search('Pt1000', dataSetsName) ):
            t_rel = tmp_path + 'ElectronMcSignalHistosPt1000.txt'
            t_ref = t_rel
            tp_rel = 'ElectronMcSignalValidatorPt1000'
            tp_ref = tp_rel
        elif ( re.search('QCD', dataSetsName) ):
            t_rel = tmp_path + 'ElectronMcFakeHistos.txt'
            t_ref = t_rel
            tp_rel = 'ElectronMcFakeValidator'
            tp_ref = tp_rel
        else: # general
            if type[0] == 'RECO': # RECO
                if type[1] == 'miniAOD': # RECO vs miniAOD
                    t_rel = tmp_path + 'ElectronMcSignalHistosMiniAOD.txt' # we have only miniAOD histos to compare.
                    t_ref = tmp_path + 'ElectronMcSignalHistosMiniAOD.txt'
                    tp_rel = 'ElectronMcSignalValidator'
                    tp_ref = 'ElectronMcSignalValidatorMiniAOD'
                else: # RECO vs RECO
                    t_rel = tmp_path + 'ElectronMcSignalHistos.txt'
                    t_ref = t_rel
                    tp_rel = 'ElectronMcSignalValidator'
                    tp_ref = 'ElectronMcSignalValidator'
            elif type[0] == 'miniAOD': # miniAOD vs miniAOD
                t_rel = tmp_path + 'ElectronMcSignalHistosMiniAOD.txt'
                t_ref = t_rel
                tp_rel = 'ElectronMcSignalValidatorMiniAOD'
                tp_ref = tp_rel
        return [t_rel, t_ref, tp_rel, tp_ref]

