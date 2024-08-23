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
        #histo_name = histo_names[0]
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

    def shortHistoName_0(self, elem):
        short_histo_name = elem.replace("h_", "")
        if "ele_" in short_histo_name:
            short_histo_name = short_histo_name.replace("ele_", "")
        if "scl_" in short_histo_name:
            short_histo_name = short_histo_name.replace("scl_", "")
        if "bcl_" in short_histo_name:
            short_histo_name = short_histo_name.replace("bcl_", "")
        return short_histo_name

    def createDatasetFolder(self, folder, ext):
        # checking ext
        if ((ext != "gifs") or (ext != "pngs")) :
            ext = 'gifs'
        if not os.path.exists(folder): # create folder
            os.makedirs(folder) # create reference folder
            os.chdir(folder)
            # create gifs/pngs folders
            os.makedirs(ext) # create gifs folder for pictures
            os.chdir('../')
        else: # folder already created
            os.chdir(folder)
            if (ext == 'gifs'):
                self.createGifDatasetFolder()
            else: # pngs
                self.createPngDatasetFolder()
            os.chdir('../')
        return

    def createGifDatasetFolder(self):
        if not os.path.exists('gifs'): #
            # create gifs folders
            os.makedirs('gifs') # create gifs folder for pictures
        return

    def createPngDatasetFolder(self): # for pngs
        if not os.path.exists('pngs'): # create folder
            os.makedirs('pngs') # create pngs folder
        return

    def createDBoxDatasetFolder(self): # for Decision Box
        if not os.path.exists('DBox'): # create folder
            os.makedirs('DBox') # create pngs folder
        return

    def deleteDBoxDatasetFolder(self): # for Decision Box
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

        #print('dataset name : {:s}'.format(dataSetsName))
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

    def testForDataSetsFile2(self, tmp_path, type, dataSetsName): # only for dev !!!
        # also get the tree path part (tp_rel, tp_ref) for root files :
        # folder location for those files : HistosConfigFiles/
        # ElectronMcSignalValidator
        # ElectronMcSignalValidatorMiniAOD
        # ElectronMcSignalValidatorPt1000
        # ElectronMcFakeValidator

        print('dataset name : {:s}'.format(dataSetsName))
        #print('type : {:s}'.format(type))
        t_rel = tmp_path + 'ElectronMcSignalHistos.txt'
        t_ref = t_rel
        tp_rel = 'ElectronMcSignalValidator'
        tp_ref = tp_rel
        if ( 'Pt1000' in type[0] ):
            t_rel = tmp_path + 'ElectronMcSignalHistosPt1000.txt'
            t_ref = t_rel
            tp_rel = 'ElectronMcSignalValidatorPt1000'
            tp_ref = tp_rel
        elif ( 'Fake' in type[0] ):
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

    def createDefinitionsFile(self, datas, fileName):
        '''
        gedGsfElectrons ZEE_14
        RECO
        12_0_0_pre6
        DQM_V0001_R000000001__RelValZEE_14__CMSSW_12_0_0_pre6-120X_mcRun3_2021_realistic_v4-v1__DQMIO.root
        RECO
        12_0_0_pre4
        DQM_V0001_R000000001__RelValZEE_14__CMSSW_12_0_0_pre4-120X_mcRun3_2021_realistic_v2-v1__DQMIO.root
        CMSSW_12_0_0_pre6
        CMSSW_12_0_0_pre4
        https://hypernews.cern.ch/HyperNews/CMS/get/relval/16218.html
        config_target.txt
        '''
        if ( fileName ):
            wp_defs = open(fileName, 'w') # definitions for PHP page
            print('\n\t ==== ' + fileName + ' ====\n')
        else:
            wp_defs = open('definitions.txt', 'w') # definitions for PHP page
            print('\n\t ==== definitions.txt ====\n')
        for elem in datas:
            print(elem)
            wp_defs.write(elem + "\n")
        print('\n\t ==== definitions.txt ====\n')
        wp_defs.close()
        return

    def createWebPageLite(input_rel_file, input_ref_file, path_1, path_2, cnv, webdir): # simplified version of createWebPage()
        print('Start creating web pages')
        print(input_rel_file)
        print(input_ref_file)
        f_rel = ROOT.TFile(input_rel_file)
        h1 = getHisto(f_rel, path_1)
        h1.ls()
    
        f_ref = ROOT.TFile(input_ref_file)
        h2 = getHisto(f_ref, path_2)
        h2.ls()
    
        CMP_CONFIG = '../HGCTPGValidation/data/HGCALTriggerPrimitivesHistos.txt'
        CMP_TITLE = ' HGCAL Trigger Primitives Validation '
        CMP_RED_FILE = input_rel_file
        CMP_BLUE_FILE = input_ref_file
        CMP_INDEX_FILE_DIR = webdir + '/index.html'
    
        MEM_REP_REF = './MemoryReport_ref.log'
        MEM_REP_TEST = './MemoryReport_test.log'
    
        shutil.copy2('../HGCTPGValidation/data/img/up.gif', webdir+ '/img')
        shutil.copy2('../HGCTPGValidation/data/img/point.gif', webdir+ '/img')
        image_up = './img/up.gif'
        image_point = './img/point.gif'
        f = open(CMP_CONFIG, 'r')
        fmemref = open(MEM_REP_REF, 'r')
        fmemtest = open(MEM_REP_TEST, 'r')
    
        wp = open(CMP_INDEX_FILE_DIR, 'w') # web page
        wp.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">\n")
        wp.write("<html>\n")
        wp.write("<head>\n")
        wp.write("<meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\" />\n")
        wp.write("<title> " + CMP_TITLE + " </title>\n") #option -t dans OvalFile
        wp.write("</head>\n")
        wp.write("<a NAME=\"TOP\"></a>")
        wp.write("<h1><a href=\"../\"><img border=0 width=\"22\" height=\"22\" src=\"img/up.gif\" alt=\"Up\"/></a>&nbsp; " + CMP_TITLE + " </h1>\n" ) # option -t dans OvalFile
        
        # here you can add some text such as GlobalTag for release & reference.
        wp.write("<br>\n")
    
        if (f_ref == 0):
            wp.write("<p>In all plots below, there was no reference histograms to compare with")
            wp.write(", and the " + CMP_RED_FILE + " histograms are in red.") # new release red in OvalFile
        else:
            wp.write("<p>In all plots below")
            wp.write(", the <b><font color='red'> " + CMP_RED_FILE + " </font></b> histograms are in red") # new release red in OvalFile
            wp.write(", and the <b><font color='blue'> " + CMP_BLUE_FILE + " </font></b> histograms are in blue.") # ref release blue in OvalFile
        wp.write(" Some more details") # 
        wp.write(", <a href=\"" + CMP_CONFIG + "\">specification</a> of histograms") # histos list .txt file
        wp.write(", <a href=\"gifs/\">images</a> of histograms" + "." )
        wp.write("</p>\n")

        # filling the title array & dict
        histoArray_0 = {}
        titlesList = [] # need with python < 3.7. dict does not keep the correct order of the datasets histograms
        key = ""
        tmp = []
        for line in f:
            print('line = ', line)
            if ( len(line) == 1 ): # len == 0, empty line
                if ( ( len(key) != 0 ) and ( len(tmp) != 0) ): 
                    histoArray_0[key] = tmp
                    key = ""
                    tmp = []
            else: # len <> 0
                if ( len(key) == 0 ):
                    key = line # get title
                    titlesList.append(line)
                else:
                    tmp.append(line) # histo name
        # end of filling the title array & dict
        f.close()
        wp.write( "<table border=\"1\" cellpadding=\"5\" width=\"100%\">" )
    
        for i in range(0, len(titlesList)):
            if ( i % 5  == 0 ):
                wp.write( "\n<tr valign=\"top\">" )
            textToWrite = ""
            wp.write( "\n<td width=\"10\">\n<b> " + titlesList[i] + "</b>" )
            titles = titlesList[i].split()
            if len(titles) > 1 :
                titleShortName = titles[0] + "_" + titles[1]
            else:
                titleShortName = titles[0]
            wp.write( "&nbsp;&nbsp;" + "<a href=\"#" + titleShortName + "\">" ) # write group title
            wp.write( "<img width=\"18\" height=\"15\" border=\"0\" align=\"center\" src=" + image_point + " alt=\"Top\"/>" + "<br><br>" )
            textToWrite += "</a>"
            histoPrevious = ""
            numLine = 0
            
            for elem in histoArray_0[titlesList[i]]:
                otherTextToWrite = ""
                histo_names = elem.split("/")
                histoShortNames = histo_names[0]
                short_histo_names = histoShortNames.split(" ")
                histo_name = short_histo_names[0].strip().replace('\n', ' ').replace('\r', '')
                print('!!!!! histo_name = ',histo_name)
                short_histo_name = histo_name.replace("h_", "")
                if "ele_" in short_histo_name:
                    short_histo_name = short_histo_name.replace("ele_", "")
                if "scl_" in short_histo_name:
                    short_histo_name = short_histo_name.replace("scl_", "")
                if "bcl_" in short_histo_name:
                    short_histo_name = short_histo_name.replace("bcl_", "")
                   
                otherTextToWrite += "<a href=\"#" + short_histo_name + "\"><font color=\'blue\'>" + short_histo_name + "</font></a>" + "&nbsp;\n"
                    
                otherTextToWrite += "<br>"
                otherTextToWrite = otherTextToWrite.replace("<br><br>", "<br>")

                textToWrite += otherTextToWrite
            textReplace = True
            while textReplace :
                textToWrite = textToWrite.replace("<br><br>", "<br>")
                if ( textToWrite.count('<br><br>') >= 1 ):
                    textReplace = True
                else:
                    textReplace = False
            if ( textToWrite.count("</a><br><a") >= 1 ):
                    textToWrite = textToWrite.replace("</a><br><a", "</a><a")
            wp.write( textToWrite )
                    
            wp.write( "</td>" )
            if ( i % 5 == 4 ):
                wp.write( "</tr>" )
      
        wp.write( "</table>\n" )
        wp.write( "<br>" )
        
        wp.write( "<table border=\"0\" cellpadding=\"5\" width=\"100%\">" )
        for i in range(0, len(titlesList)):
            wp.write( "\n<tr valign=\"top\">" )
            wp.write( "\n<td><a href=\"#TOP\"><img width=\"18\" height=\"18\" border=\"0\" align=\"middle\" src=" + image_up + " alt=\"Top\"/></a></td>\n" )
            titles = titlesList[i].split()
            if len(titles) > 1 :
                titleShortName = titles[0] + "_" + titles[1]
            else:
                titleShortName = titles[0]
            wp.write( "\n<td>\n<b> " )
            wp.write( "<a id=\"" + titleShortName + "\" name=\"" + titleShortName + "\"></a>" )
            wp.write( titlesList[i] + "</b></td>" )
            wp.write( "</tr><tr valign=\"top\">" )
            for elem in histoArray_0[titlesList[i]]:
                if ( elem != "endLine" ):
                    histo_names = elem.split("/")
                    histoShortNames = histo_names[0]
                    short_histo_names = histoShortNames.split(" ")
                    histo_name = short_histo_names[0].strip().replace('\n', ' ').replace('\r', '')
                    short_histo_name = histo_name.replace("h_", "")
                    if "ele_" in short_histo_name:
                        short_histo_name = short_histo_name.replace("ele_", "")
                    if "scl_" in short_histo_name:
                        short_histo_name = short_histo_name.replace("scl_", "")
                    if "bcl_" in short_histo_name:
                        short_histo_name = short_histo_name.replace("bcl_", "")
                
                    histo_2 = h2.Get(histo_name)
                    histo_1 = h1.Get(histo_name)
                    gif_name = webdir + '/' + histo_name + ".gif"
                    gif_name_index = histo_name + ".gif"
                    createPicture2(histo_1, histo_2, "1", "1", gif_name, cnv, "lin")
                    # Make histo in log
                    #if (histo_1.GetMaximum() > 0 and histo_1.GetMinimum() >= 0):
                    #    gif_name_log = webdir + '/' + histo_name + "_log.gif"
                    #    gif_name_log_index = histo_name + "_log.gif"
                    #    createPicture2(histo_1, histo_2, "1", "1", gif_name_log, cnv, "log")

                    wp.write( "\n<td><a href=\"#TOP\"><img width=\"18\" height=\"18\" border=\"0\" align=\"middle\" src=" + image_up + " alt=\"Top\"/></a></td>\n" )
                    wp.write( "<td>" )
                    wp.write( "<a id=\"" + short_histo_name + "\" name=\"" + short_histo_name + "\"></a>" )
                    wp.write( "<a href=\"" + gif_name_index + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + gif_name_index + "\"></a>" )
                    # For histo in log
                    #if (histo_1.GetMaximum() > 0 and histo_1.GetMinimum() >= 0):
                    #    wp.write( "</td><td><a href=\"" + gif_name_log_index + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + gif_name_log_index + "\"></a>" )
                    wp.write( "</td></tr><tr valign=\"top\">" )
    
        wp.write( "<h2>" + "Memory Report" + "</h2>\n" )
        with open(MEM_REP_REF) as file:
            for line in file.readlines():
                wp.write(line)
 
        with open(MEM_REP_TEST) as file:
            for line in file.readlines():
                wp.write("<p>Datatest => " + line)

        wp.write( "</tr></table>\n" )
        wp.close()
        
        return
    
    def createWebPageLite2(input_rel_file, input_ref_file, path_1, path_2, cnv, webdir): # simplified version of createWebPage()/GevSeq()
        print('Start creating web pages')
        print(input_rel_file)
        print(input_ref_file)
        f_rel = ROOT.TFile(input_rel_file)
        h1 = getHisto(f_rel, path_1)
        h1.ls()
    
        f_ref = ROOT.TFile(input_ref_file)
        h2 = getHisto(f_ref, path_2)
        h2.ls()
    
        CMP_CONFIG = '../HGCTPGValidation/data/HGCALTriggerPrimitivesHistos.txt'
        CMP_TITLE = ' HGCAL Trigger Primitives Validation '
        CMP_RED_FILE = input_rel_file
        CMP_BLUE_FILE = input_ref_file
    
        shutil.copy2('../HGCTPGValidation/data/img/up.gif', webdir+ '/img')
        shutil.copy2('../HGCTPGValidation/data/img/point.gif', webdir+ '/img')
    
        # RELEASE/REFERENCE : CMSSW_12_1_0_pre3
        # ShortRelease/shortReference : 12_1_0_pre3
        datas = []
        datas.append(CMP_TITLE) # LINE 7
        datas.append('RECO')
        datas.append(shortRelease)
        datas.append(CMP_RED_FILE) # LINE 8
        datas.append('RECO')
        datas.append(shortReference)
        datas.append(CMP_BLUE_FILE) # LINE 9
        if (f_ref == 0):
            datas.append(release)
            datas.append(release)
        else:
            datas.append(release)
            datas.append(reference)
        if (Validation_reference != ""):
            datas.append(Validation_reference) # wiki page which reference the comparison. Can be null ('none').
        else:
            datas.append('none')
        datas.append(CMP_CONFIG)
        tl.createDefinitionsFile(datas)
       
        # filling the title array & dict
        histoArray_0 = {}
        titlesList = [] # need with python < 3.7. dict does not keep the correct order of the datasets histograms
        key = ""
        tmp = []
        for line in f:
            print('line = ', line)
            if ( len(line) == 1 ): # len == 0, empty line
                if ( ( len(key) != 0 ) and ( len(tmp) != 0) ): 
                    histoArray_0[key] = tmp
                    key = ""
                    tmp = []
            else: # len <> 0
                if ( len(key) == 0 ):
                    key = line # get title
                    titlesList.append(line)
                else:
                    tmp.append(line) # histo name
        # end of filling the title array & dict
        f.close()
        
        wp.write( "<table border=\"0\" cellpadding=\"5\" width=\"100%\">" )
        for i in range(0, len(titlesList)):
            for elem in histoArray_0[titlesList[i]]:
                if ( elem != "endLine" ):
                    short_histo_name, short_histo_names, histo_positions = tl.shortHistoName(elem)
                    histo_name = short_histo_names[0].strip().replace('\n', ' ').replace('\r', '')
                    histo_2 = h2.Get(histo_name)
                    histo_1 = h1.Get(histo_name)
                    gif_name = webdir + '/' + histo_name + ".gif"
                    createPicture2(histo_1, histo_2, "1", "1", gif_name, cnv, "lin")
                    # Make histo in log
                    #if (histo_1.GetMaximum() > 0 and histo_1.GetMinimum() >= 0):
                    #    gif_name_log = webdir + '/' + histo_name + "_log.gif"
                    #    gif_name_log_index = histo_name + "_log.gif"
                    #    createPicture2(histo_1, histo_2, "1", "1", gif_name_log, cnv, "log")

    
        ## the following lines will be automaticly integrated in to the genericIndex.php file.
        #wp.write( "<h2>" + "Memory Report" + "</h2>\n" )
        #with open(MEM_REP_REF) as file:
        #    for line in file.readlines():
        #        wp.write(line)
 
        #with open(MEM_REP_TEST) as file:
        #    for line in file.readlines():
        #        wp.write("<p>Datatest => " + line)

        
        return
    
