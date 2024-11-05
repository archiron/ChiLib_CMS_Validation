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

from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
argv.remove( '-b-' )

import os,sys, shutil # ,subprocess
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

from graphicFunctions import Graphic
from fonctions import Tools

# create the index.html web page for the validation comparison.
# Do not confuse with DBwebPage into the DecisionBox class.
def createWebPage(arg):
    # arg = ((self, str(webFolder), release, reference, relrefVT[0], relrefVT[1], shortRelease, shortReference, b, datasets[b], rel_ref[b], validation[7][b]) for b in range(0, N))
    #print('createWebPage')

    #print('arg', arg)
    from DecisionBox import DecisionBox
    from valEnv_default import env_default
    valEnv_d = env_default()
    DB = DecisionBox()
    gr = Graphic()
    tl = Tools()

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
    tl.createDatasetFolder(arg[1] + dataSetFolder) # need absolute path for concurrent folder creation
    os.chdir(arg[1] + dataSetFolder) # going to dataSetFolder
    # get config files
    it1 = env_default().tmpPath() + 'ElectronMcSignalHistos.txt'
    it2 = it1
    tp_1 = 'ElectronMcSignalValidator'
    tp_2 = 'ElectronMcSignalValidator'

    relrefVT = [arg[4], arg[5]]
    (it1, it2, tp_1, tp_2) = tl.testForDataSetsFile(env_default().tmpPath(), relrefVT, dts)
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
    h1 = gr.getHisto(f_rel, tp_1)

    input_ref_file = env_default().workDir() + '/DATA/' + str(arg[10][1])
    #input_ref_file = workDir + '/DATA/' + str(arg[10][1])
    if not os.path.isfile(input_ref_file): # the ref root file does not exist
        print('%s does not exist' % input_ref_file)
        exit()
    else:
        print(input_ref_file)
    f_ref = ROOT.TFile(input_ref_file)
    h2 = gr.getHisto(f_ref, tp_2)
    #print("CMP_CONFIG[%d] = %s\n" % (arg[8], CMP_CONFIG))
    print("input_rel_file[%d] = %s" % (arg[8], input_rel_file))
    print("input_ref_file[%d] = %s" % (arg[8], input_ref_file))
    print('index.html[' + str(arg[8]) + '] :' + arg[1] + dataSetFolder + '/index.html')

    #wp = open(arg[1] + dataSetFolder + '/index.html', 'w') # web page
    wp_Files = []
    wp_index = open(arg[1] + dataSetFolder + '/index.html', 'w') # web page
    wp_Files.append(wp_index)
    if (DB_flag == True):
        tl.createDatasetFolder3() # create DBox folder
        print('DB_flag = True')
    else:
        tl.deleteDatasetFolder3()  # delete DBox folder
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
                short_histo_name, short_histo_names, histo_positions = tl.shortHistoName(elem)

                [after, before, common] = tl.testExtension(short_histo_name, histoPrevious)

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

                short_histo_name, short_histo_names, histo_positions = tl.shortHistoName(elem)
                gif_name = "gifs/" + short_histo_names[0] + ".gif"
                png_name = "pngs/" + short_histo_names[0] + ".png" # for DB yellow curves
                png_cumul_name = "pngs/" + short_histo_names[0] + "_cum.png" # for DB yellow curves
                #gif_name = arg[1] + dataSetFolder + "/gifs/" + short_histo_names[0] + ".gif"

                # creating shortHistoName file in DBox folder
                if DB_flag:
                    fHisto = open('DBox/' + short_histo_name + '.txt', 'w') # web page
                    fHisto.write('<table border="1" bordercolor=green cellpadding="2" style="margin-left:auto;margin-right:auto">' + '\n')

                if tl.checkRecompInName(short_histo_names[0]): #
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
                gr.PictureChoice(histo_1, histo_2, histo_positions[1], histo_positions[2], gif_name, arg[0], arg[8], c_recomp)
                if ycFlag:
                    tl.createDatasetFolder2()
                    gr.PictureChoice_DB(histo_1, histo_2, histo_positions[1], histo_positions[2], png_name, arg[0], 0, yellowCurves)
                    gr.PictureChoice_DB3(histo_1, histo_2, histo_positions[1], histo_positions[2], png_cumul_name, arg[0], 0, yellowCurvesCum)

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

