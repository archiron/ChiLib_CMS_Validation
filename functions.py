#! /usr/bin/env python
#-*-coding: utf-8 -*-

from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
argv.remove( '-b-' )

import os,sys,subprocess, shutil

if sys.version_info >= (3, 0):
    sys.stdout.write("Python 3.x\n")
else:
    sys.stdout.write("Python 2.x\n")

try:
  from httplib import HTTPSConnection
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

import re
import numpy as np
import concurrent.futures

from graphicFunctions import *

def getDataSet(tab_files):
    # tt[0] : dataset
    # tt[1] : RELEASE
    # tt[2] : GlobalTag
    i = 0
    temp = []
    for t in tab_files:
        tt = explode_item(t)
        #print(tt)
        temp.append(tt[0])
        i += 1
    temp = sorted(set(temp), reverse=False)
    return temp

def explode_item(item):
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

def analyzeDTS(text):
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

def checkRecompInName(name):
    if re.search('recomp', name):
        return True
    else:
        return False

def shortHistoName(elem):
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

def testExtension(histoName, histoPrevious):
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

def createDatasetFolder(folder):
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

def createDatasetFolder2(): # for pngs
    if not os.path.exists('pngs'): # create folder
        os.makedirs('pngs') # create pngs folder
    return

def createDatasetFolder3(): # for Decision Box
    if not os.path.exists('DBox'): # create folder
        os.makedirs('DBox') # create pngs folder
    return

def deleteDatasetFolder3(): # for Decision Box
    import shutil
    if os.path.exists('DBox'): # create folder
        shutil.rmtree('DBox')
    return

# calculate the difference of s0
def getDifference_1(s0,e0,s1,e1):
    s0 = np.asarray(s0) # if not this, ind is returned as b_00x instead of int value
    s1 = np.asarray(s1) # if not this, ind is returned as b_00x instead of int value
    e0 = np.asarray(e0) # if not this, ind is returned as b_00x instead of int value
    e1 = np.asarray(e1) # if not this, ind is returned as b_00x instead of int value
    diff_max = 0.
    mask = []
    N = len(s0)
    for i in range(0, N):
        a1 = s0[i] - e0[i]
        b1 = s1[i] + e1[i]
        a2 = s0[i] + e0[i]
        b2 = s1[i] - e1[i]
        ab1 = a1 - b1
        ab2 = b2 - a2
        #print(i)
        if (s0[i] > s1[i]):
            if (ab1 > 0.):
                mask.append(0)
                if (np.abs(ab1) > diff_max):
                    diff_max = np.abs(ab1)
                    #print('ab1[%d] : %f' % (i, diff_max))
            elif (ab1 <= 0.):
                mask.append(1)
        elif (s0[i] < s1[i]):
            if (ab2 > 0.):
                mask.append(0)
                if (np.abs(ab2) > diff_max):
                    diff_max = np.abs(ab2)
                    #print('ab2[%d] : %f' % (i, diff_max))
            elif (ab2 <= 0.):
                mask.append(1)
        elif (s0[i] == s1[i]):
            #diff = 0.
            mask.append(1)
    #print('diff max : %f' % diff_max)
    return diff_max, mask

# calculate the difference of s0
def getDifference_2(s0,e0,s1,e1):
    s0 = np.asarray(s0) # if not this, ind is returned as b_00x instead of int value
    s1 = np.asarray(s1) # if not this, ind is returned as b_00x instead of int value
    e0 = np.asarray(e0) # if not this, ind is returned as b_00x instead of int value
    e1 = np.asarray(e1) # if not this, ind is returned as b_00x instead of int value
    diff_max = 0.
    mask = []
    N = len(s0)
    for i in range(0, N):
        a1 = s0[i] - e0[i]
        b1 = s1[i] + e1[i]
        a2 = s0[i] + e0[i]
        b2 = s1[i] - e1[i]
        ab1 = a1 - b1
        ab2 = b2 - a2
        #print(i)
        if ((s0[i] + s1[i]) != 0.):
            #print('so[%d] + s1[%d] = %f' % (i,i,s0[i] + s1[i]))
            if (s0[i] > s1[i]):
                if (ab1 > 0.):
                    mask.append(0)
                    if (np.abs(ab1) > diff_max):
                        diff_max = np.abs(ab1)
                        #print('ab1[%d] : %f' % (i, diff_max))
                elif (ab1 <= 0.):
                    mask.append(1)
            elif (s0[i] < s1[i]):
                if (ab2 > 0.):
                    mask.append(0)
                    if (np.abs(ab2) > diff_max):
                        diff_max = np.abs(ab2)
                        #print('ab2[%d] : %f' % (i, diff_max))
                elif (ab2 <= 0.):
                    mask.append(1)
            elif (s0[i] == s1[i]):
                #diff = 0.
                mask.append(1)
        #else:
            #print('so[%d] + s1[%d] = %f' % (i,i,s0[i] + s1[i]))
    #print('diff max : %f' % diff_max)
    return diff_max, mask

# calculate the difference of s0
def getDifference_3(s0,e0,s1,e1):
    s0 = np.asarray(s0) # if not this, ind is returned as b_00x instead of int value
    s1 = np.asarray(s1) # if not this, ind is returned as b_00x instead of int value
    e0 = np.asarray(e0) # if not this, ind is returned as b_00x instead of int value
    e1 = np.asarray(e1) # if not this, ind is returned as b_00x instead of int value
    diff_max = 0.
    mask = []
    N = len(s0)
    for i in range(1, N-1):
        a1 = s0[i] - e0[i]
        b1 = s1[i] + e1[i]
        a2 = s0[i] + e0[i]
        b2 = s1[i] - e1[i]
        ab1 = a1 - b1
        ab2 = b2 - a2
        #print(i)
        if (s0[i] > s1[i]):
            if (ab1 > 0.):
                mask.append(0)
                if (np.abs(ab1) > diff_max):
                    diff_max = np.abs(ab1)
                    #print('ab1[%d] : %f' % (i, diff_max))
            elif (ab1 <= 0.):
                mask.append(1)
        elif (s0[i] < s1[i]):
            if (ab2 > 0.):
                mask.append(0)
                if (np.abs(ab2) > diff_max):
                    diff_max = np.abs(ab2)
                    #print('ab2[%d] : %f' % (i, diff_max))
            elif (ab2 <= 0.):
                mask.append(1)
        elif (s0[i] == s1[i]):
            #diff = 0.
            mask.append(1)
    #else:
        #print('so[%d] + s1[%d] = %f' % (i,i,s0[i] + s1[i]))
    #print('diff max : %f' % diff_max)
    return diff_max, mask

# get a coefficient from an array of integers 0/1
def getCoeff(m0):
    coeff = np.asarray(m0).mean()
    return coeff

def setColor(coeff):
    tmp = str("%6.4f" % coeff)
    if(coeff <= 0.35):
        text = "<font color=\'red\'><b>" + tmp + "</b></font>"
    elif(coeff <= 0.75):
        text = "<font color=\'blue\'><b>" + tmp + "</b></font>"
    else:
        text = "<font color=\'green\'><b>" + tmp + "</b></font>"
    #print("%6.4f : %s" % (coeff, text))
    return text

def createWebPage(arg):
    # arg = ((self, str(webFolder), release, reference, relrefVT[0], relrefVT[1], shortRelease, shortReference, b, datasets[b], rel_ref[b], validation[7][b]) for b in range(0, N))
    #print('createWebPage')

    #print('arg', arg)
    from DecisionBox import DecisionBox
    from valEnv_default import env_default
    valEnv_d = env_default()
    DB = DecisionBox()

    print('arg : ', arg)
    '''print('webFolder ', arg[1])
    print('release ', arg[2])
    print('reference ', arg[3])
    print('relValType ', arg[4])
    print('refValType ', arg[5])
    print('short release ', arg[6])
    print('short reference ', arg[7])
    print('b ', arg[8])
    print('finalList[%d], %s ' % (arg[7], arg[9]))
    print('rel_ref[%d], %s ' % (arg[7], arg[10]))
    '''
    print('Decision Box flag : %s', arg[11])
    dts = arg[9]
    print('dataset : %s' % dts)
    DB_flag = arg[11]
    dataSetFolder = str(arg[4] + '-' + arg[5] + '_' + dts + '_par')
    createDatasetFolder(arg[1] + dataSetFolder) # need absolute path for concurrent folder creation
    os.chdir(arg[1] + dataSetFolder) # going to dataSetFolder
    # get config files
    it1 = env_default().tmpPath() + 'ElectronMcSignalHistos.txt'
    it2 = it1
    tp_1 = 'ElectronMcSignalValidator'
    tp_2 = 'ElectronMcSignalValidator'

    relrefVT = [arg[4], arg[5]]
    (it1, it2, tp_1, tp_2) = testForDataSetsFile(env_default().tmpPath(), relrefVT, dts)
    print("config file for target : %s" % it1)
    print("config file for reference : %s" % it2)
    print("tree path for target : %s" % tp_1)
    print("tree path for reference : %s" % tp_2)
    shutil.copy2(it1, arg[1] + dataSetFolder + '/config_target.txt')
    shutil.copy2(it2, arg[1] + dataSetFolder + '/config_reference.txt')

    # create gifs pictures & web page
    CMP_CONFIG = 'config_target.txt'
    CMP_TITLE = 'gedGsfElectrons ' + dts

    f = open(arg[1] + dataSetFolder + '/' + CMP_CONFIG, 'r')
    input_rel_file = env_default().workDir() + '/DATA/' + str(arg[10][0])
    #input_rel_file = workDir + '/DATA/' + str(arg[10][0])
    if not os.path.isfile(input_rel_file): # the ref root file does not exist
        print('%s does not exist' % input_rel_file)
        exit()
    else:
        print(input_rel_file)
    f_rel = ROOT.TFile(input_rel_file)
    h1 = getHisto(f_rel, tp_1)

    input_ref_file = env_default().workDir() + '/DATA/' + str(arg[10][1])
    #input_ref_file = workDir + '/DATA/' + str(arg[10][1])
    if not os.path.isfile(input_ref_file): # the ref root file does not exist
        print('%s does not exist' % input_ref_file)
        exit()
    else:
        print(input_ref_file)
    f_ref = ROOT.TFile(input_ref_file)
    h2 = getHisto(f_ref, tp_2)
    #print("CMP_CONFIG[%d] = %s\n" % (arg[8], CMP_CONFIG))
    print("input_rel_file[%d] = %s" % (arg[8], input_rel_file))
    print("input_ref_file[%d] = %s" % (arg[8], input_ref_file))
    print('index.html[' + str(arg[8]) + '] :' + arg[1] + dataSetFolder + '/index.html')

    #wp = open(arg[1] + dataSetFolder + '/index.html', 'w') # web page
    wp_Files = []
    wp_index = open(arg[1] + dataSetFolder + '/index.html', 'w') # web page
    wp_Files.append(wp_index)
    if (DB_flag == True):
        createDatasetFolder3() # create DBox folder
        print('DB_flag = True')
    else:
        deleteDatasetFolder3()  # delete DBox folder
    #stop

    extWrite("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">\n", wp_Files)
    extWrite("<html>\n", wp_Files)
    extWrite("<head>\n", wp_Files)
    extWrite("<meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\" />\n", wp_Files)
    extWrite("<title> " + CMP_TITLE + " </title>\n", wp_Files) #option -t dans OvalFile
    extWrite("</head>\n", wp_Files)
    extWrite("<a NAME=\"TOP\"></a>", wp_Files)
    extWrite("<h1><a href=\"../\"><img border=0 width=\"22\" height=\"22\" src=\"../../../../img/up.gif\" alt=\"Up\"/></a>&nbsp; " + CMP_TITLE + " </h1>\n" , wp_Files) # option -t dans OvalFile

    extWrite("<b><font color='red'> " + arg[4] + " " + arg[6] + " </font></b>", wp_Files)
    extWrite(" : " + str(arg[10][0]) , wp_Files)
    extWrite("<br>\n", wp_Files)
    extWrite("<b><font color='blue'> " + arg[5] + " " + arg[7] + " </font></b>", wp_Files)
    extWrite(" : " + str(arg[10][1]) , wp_Files)
    extWrite("<br>\n", wp_Files)

    if (f_ref == 0):
        extWrite("<p>In all plots below, there was no reference histograms to compare with", wp_Files)
        extWrite(", and the " + arg[2] + " histograms are in red.", wp_Files) # new release red in OvalFile
    else:
        extWrite("<p>In all plots below", wp_Files)
        extWrite(", the <b><font color='red'> " + arg[2] + " </font></b> histograms are in red", wp_Files) # new release red in OvalFile
        extWrite(", and the <b><font color='blue'> " + arg[3] + " </font></b> histograms are in blue.", wp_Files) # ref release blue in OvalFile
    extWrite(" Some more details", wp_Files) #
    extWrite(", <a href=\"" + CMP_CONFIG + "\">specification</a> of histograms", wp_Files) # .txt file
    extWrite(", <a href=\"gifs/\">images</a> of histograms" + "." , wp_Files) #
    extWrite("</p>\n", wp_Files)

    # remplissage tableau titres et dict
    histoArray_0 = {}
    titlesList = [] # need with python < 3.7. dict does not keep the correct order of the datasets histograms
    key = ""
    tmp = []
    for line in f:
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
                t1 = line.split("/")
                t2 = str(t1[1])
                short_positions = t2.split()
                if ( short_positions[3] == '1' ): # be careful it is '1' and not 1 (without quote)
                    tmp.append("endLine")

    # fin remplissage tableau titres et dict
    f.close()
    extWrite( "<table border=\"1\" cellpadding=\"5\" width=\"100%\">" , wp_Files)

    # ecriture du tableau general
    firstFlag= True
    for i in range(0, len(titlesList)):
        if ( i % 5  == 0 ):
            extWrite( "\n<tr valign=\"top\">" , wp_Files)
        textToWrite = ""
        extWrite( "\n<td width=\"10\">\n<b> " + titlesList[i] + "</b>" , wp_Files)
        titles = titlesList[i].split() # explode(" ", $clefs[$i])
        if len(titles) > 1 :
            titleShortName = titles[0] + "_" + titles[1]
        else:
            titleShortName = titles[0]
        extWrite( "&nbsp;&nbsp;" + "<a href=\"#" + titleShortName + "\">" , wp_Files) # write group title
        extWrite( "<img width=\"18\" height=\"15\" border=\"0\" align=\"center\" src=" + env_default().imagePoint() + " alt=\"Top\"/>" + "<br><br>" , wp_Files)
        textToWrite += "</a>"
        histoPrevious = ""
        numLine = 0

        for elem in histoArray_0[titlesList[i]]:
            otherTextToWrite = ""

            if ( elem == "endLine" ):
                otherTextToWrite += "<br>"
            else: # no endLine
                short_histo_name, short_histo_names, histo_positions = shortHistoName(elem)

                [after, before, common] = testExtension(short_histo_name, histoPrevious)

                if ( histo_positions[3] == "0" ):
                    if ( numLine == 0 ):
                        otherTextToWrite += "<a href=\"#" + short_histo_name + "\"><font color=\'green\'>" + short_histo_name + "</font></a>" + "&nbsp;\n"
                        common = short_histo_name
                        numLine += 1
                    else: # $numLine > 0
                        if ( after == "" ):
                            otherTextToWrite += "<a href=\"#" + short_histo_name + "\"><font color=green>" + before + "</font></a>" + "&nbsp;\n"
                        else: # $after != ""
                            otherTextToWrite += "<a href=\"#" + short_histo_name + "\"><font color=green>" + after + "</font></a>" + "&nbsp;\n"
                        common = before
                else: # histo_positions[3] == "1"
                    if ( numLine == 0 ):
                        otherTextToWrite += "<a href=\"#" + short_histo_name + "\"><font color=grey>" + short_histo_name + "</font></a>" + "&nbsp;\n"
                        common = short_histo_name
                    else: # $numLine > 0
                        if ( after == "" ):
                            otherTextToWrite += "<a href=\"#" + short_histo_name + "\"><font color=blue>" + before + "</font></a>" + "&nbsp;\n"
                        else: # after != ""
                            otherTextToWrite += "<a href=\"#" + short_histo_name + "\"><font color=blue>" + after + "</font></a>" + "&nbsp;\n"
                    numLine = 0

                histoPrevious = common
                if ( histo_positions[4] == "1" ):
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
        extWrite( textToWrite , wp_Files)

        extWrite( "</td>" , wp_Files)
        if ( i % 5 == 4 ):
            extWrite( "</tr>" , wp_Files)
            firstFlag = False
        else:
            firstFlag = True

    # fin ecriture du tableau general
    if firstFlag:
        extWrite( "</tr>" , wp_Files)
    extWrite( "</table>\n" , wp_Files)
    extWrite( "<br>" , wp_Files)

    lineFlag = True
    extWrite( "<table border=\"0\" cellpadding=\"5\" width=\"100%\">" , wp_Files)
    # ecriture des histos
    for i in range(0, len(titlesList)):
        extWrite( "\n<tr valign=\"top\">" , wp_Files)
        extWrite( "\n<td><a href=\"#\"><img width=\"18\" height=\"18\" border=\"0\" align=\"middle\" src=" + env_default().imageUp() + " alt=\"Top\"/></a></td>\n" , wp_Files)
        titles = titlesList[i].split()
        if len(titles) > 1 :
            titleShortName = titles[0] + "_" + titles[1]
        else:
            titleShortName = titles[0]
        extWrite( "\n<td>\n<b> " , wp_Files)
        extWrite( "<a id=\"" + titleShortName + "\" name=\"" + titleShortName + "\"></a>" , wp_Files)
        extWrite( titlesList[i] + "</b></td>" , wp_Files)
        extWrite( "</tr>" , wp_Files)
        for elem in histoArray_0[titlesList[i]]:
            if ( elem != "endLine" ):
                if ( lineFlag ):
                    extWrite( "\n<tr valign=\"top1\">" , wp_Files)

                short_histo_name, short_histo_names, histo_positions = shortHistoName(elem)
                gif_name = "gifs/" + short_histo_names[0] + ".gif"
                png_name = "pngs/" + short_histo_names[0] + ".png" # for DB yellow curves
                png_cumul_name = "pngs/" + short_histo_names[0] + "_cum.png" # for DB yellow curves
                #gif_name = arg[1] + dataSetFolder + "/gifs/" + short_histo_names[0] + ".gif"

                # creating shortHistoName file in DBox folder
                if DB_flag:
                    fHisto = open('DBox/' + short_histo_name + '.txt', 'w') # web page
                    fHisto.write('<table border="1" bordercolor=green cellpadding="2" style="margin-left:auto;margin-right:auto">' + '\n')

                if checkRecompInName(short_histo_names[0]): #
                    histo_name_recomp = short_histo_names[0].replace("_recomp", "")
                    #short_histo_names[0] = histo_name_recomp
                    gif_name = "gifs/" + histo_name_recomp + "_recomp.gif"
                    png_name = "pngs/" + histo_name_recomp + "_recomp.png" # for DB yellow curves
                    png_cumul_name = "pngs/" + histo_name_recomp + "_cum__recomp.png" # for DB yellow curves
                    histo_1 = h2.Get(short_histo_names[0]) #
                    histo_2 = h1.Get(histo_name_recomp) #
                    c_recomp = 1
                else: # without recomp
                    histo_1 = h1.Get(short_histo_names[0]) # without recomp
                    histo_2 = h2.Get(short_histo_names[0]) # without recomp
                    c_recomp = 0

                ycFlag = False
                if DB_flag:
                    KS_reference_release = arg[0].KS_reference_release
                    KS_Path1 = valEnv_d.KS_Path()[1] + KS_reference_release
                    KS_Path0 = valEnv_d.KS_Path()[0] + KS_reference_release
                    KS_values_1 = DB.decisionBox1(short_histo_names[0], histo_1, histo_2, KS_Path0)
                    KS_values_2 = DB.decisionBox2(short_histo_names[0], histo_1, histo_2, KS_Path0)
                    KS_values_3 = DB.decisionBox3(short_histo_names[0], histo_1, histo_2, KS_Path0)
                    if (len(KS_values_1) > 5):
                        #yellowCurves = [ KS_values_1[5], KS_values_2[2], KS_values_3[2] ]
                        #yellowCurvesCum = [ KS_values_1[6], KS_values_2[3], KS_values_3[3] ]
                        yellowCurves = [KS_values_1[5]]
                        yellowCurvesCum = [KS_values_1[6]]
                        ycFlag = True

                print('ycFlag : %s : %s' % (short_histo_names[0], ycFlag))
                PictureChoice(histo_1, histo_2, histo_positions[1], histo_positions[2], gif_name, arg[0], arg[8], c_recomp)
                if ycFlag:
                    createDatasetFolder2()
                    PictureChoice_DB(histo_1, histo_2, histo_positions[1], histo_positions[2], png_name, arg[0], 0, yellowCurves)
                    PictureChoice_DB3(histo_1, histo_2, histo_positions[1], histo_positions[2], png_cumul_name, arg[0], 0, yellowCurvesCum)

                    percentage = 0.05
                    if ( KS_values_1[4] >= percentage ):
                        color = 'green'
                        DB_picture = env_default().imageOK()
                    else:
                        color = 'red'
                        DB_picture = env_default().imageKO()

                #stop
                if ( lineFlag ):
                    extWrite( "\n<td><a href=\"#\"><img width=\"18\" height=\"18\" border=\"0\" align=\"middle\" src=" + env_default().imageUp() + " alt=\"Top\"/></a></td>\n" , wp_Files)
                if (  histo_positions[3] == "0" ):
                    extWrite( "<td>" , wp_Files)
                    extWrite( "<a id=\"" + short_histo_name + "\" name=\"" + short_histo_name + "\"" , wp_Files)
                    extWrite( " href=\"" + gif_name + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + gif_name + "\"></a>" , wp_Files)
                    extWrite( " </td>\n", wp_Files)
                    # insert here the decision box
                    if DB_flag:
                        KS_V = [KS_values_1, KS_values_2, KS_values_3]
                        # KS_V = [KS_values_1]
                        Names = [short_histo_name, gif_name, short_histo_names[0], png_name, png_cumul_name]
                        DB.webPage(fHisto, Names, KS_V, DB_picture, arg[0].webURL, arg[0].shortWebFolder, dataSetFolder, valEnv_d.KS_Path()[0], KS_Path1, ycFlag)
                    lineFlag = False
                else: # line_sp[3]=="1"
                    extWrite( "<td>" , wp_Files)
                    extWrite( "<a id=\"" + short_histo_name + "\" name=\"" + short_histo_name + "\"" , wp_Files)
                    extWrite( " href=\"" + gif_name + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + gif_name + "\"></a>" , wp_Files)
                    extWrite( "</td>" , [wp_index])
                    if DB_flag:
                        KS_V = [KS_values_1, KS_values_2, KS_values_3]
                        # KS_V = [KS_values_1]
                        Names = [short_histo_name, gif_name, short_histo_names[0], png_name, png_cumul_name]
                        DB.webPage(fHisto, Names, KS_V, DB_picture, arg[0].webURL, arg[0].shortWebFolder, dataSetFolder, valEnv_d.KS_Path()[0], KS_Path1, ycFlag)
                    extWrite( "\n</tr>", wp_Files ) # close the histo names loop
                    lineFlag = True

                if DB_flag:
                    extWrite("</table>\n", [fHisto])
                    fHisto.close()
    # fin ecriture des histos
    extWrite( "</table>\n" , wp_Files)

    #wp.close()
    wp_index.close()
    if DB_flag:
        #print('appel generateExplanation pour %s' % dts)
        DB.generateExplanation2()
    #else:
        #print('pas appel generateExplanation pour %s' % dts)

    os.chdir('../') # back to the final folder.

    return 0

def extWrite(text, fileList): #
    for f in fileList:
        f.write(text)
    return

def testForDataSetsFile(tmp_path, type, dataSetsName):
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
