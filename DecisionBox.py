#! /usr/bin/env python
#-*-coding: utf-8 -*-

import os,sys

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

import numpy as np

import os.path
from os import path

from functions import Tools #.extWrite

################################################################################
# GevSeqDev: a tool to generate Release Comparison                              
#
#
#                                                                              
# Arnaud Chiron-Turlay LLR - arnaud.chiron@llr.in2p3.fr                        
#                                                                              
################################################################################

class DecisionBox:
    def __init__(self):
        self.toto = 1.2

    # calculate the difference of s0
    def getDifference_1(self, s0,e0,s1,e1):
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
            if (s0[i] > s1[i]):
                if (ab1 > 0.):
                    mask.append(0)
                    if (np.abs(ab1) > diff_max):
                        diff_max = np.abs(ab1)
                elif (ab1 <= 0.):
                    mask.append(1)
            elif (s0[i] < s1[i]):
                if (ab2 > 0.):
                    mask.append(0)
                    if (np.abs(ab2) > diff_max):
                        diff_max = np.abs(ab2)
                elif (ab2 <= 0.):
                    mask.append(1)
            elif (s0[i] == s1[i]):
                mask.append(1)
        return diff_max, mask

    # calculate the difference of s0
    def getDifference_2(self, s0,e0,s1,e1):
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
            if ((s0[i] + s1[i]) != 0.):
                if (s0[i] > s1[i]):
                    if (ab1 > 0.):
                        mask.append(0)
                        if (np.abs(ab1) > diff_max):
                            diff_max = np.abs(ab1)
                    elif (ab1 <= 0.):
                        mask.append(1)
                elif (s0[i] < s1[i]):
                    if (ab2 > 0.):
                        mask.append(0)
                        if (np.abs(ab2) > diff_max):
                            diff_max = np.abs(ab2)
                    elif (ab2 <= 0.):
                        mask.append(1)
                elif (s0[i] == s1[i]):
                    mask.append(1)
        return diff_max, mask

    # calculate the difference of s0
    def getDifference_3(self, s0,e0,s1,e1):
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
            if (s0[i] > s1[i]):
                if (ab1 > 0.):
                    mask.append(0)
                    if (np.abs(ab1) > diff_max):
                        diff_max = np.abs(ab1)
                elif (ab1 <= 0.):
                    mask.append(1)
            elif (s0[i] < s1[i]):
                if (ab2 > 0.):
                    mask.append(0)
                    if (np.abs(ab2) > diff_max):
                        diff_max = np.abs(ab2)
                elif (ab2 <= 0.):
                    mask.append(1)
            elif (s0[i] == s1[i]):
                mask.append(1)
        return diff_max, mask

    # get a coefficient from an array of integers 0/1
    def getCoeff(self, m0):
        coeff = np.asarray(m0).mean()
        return coeff

    def getHistoValues(self, histo):
        i=0
        s0 = []
        e0 = []
        for entry in histo:
            s0.append(entry)
            e0.append(histo.GetBinError(i))
            i += 1
        # we eliminate the under/overflow values
        s0 = s0[1:-1]
        e0 = e0[1:-1]
        return s0, e0

    def diffMAXKS(self, s0,s1, sum0, sum1):
        s0 = np.asarray(s0) # if not this, ind is returned as b_00x instead of int value
        s1 = np.asarray(s1)
        N = len(s0)
        v0 = 0.
        v1 = 0.
        sDKS = []
        for i in range(0, N):
            t0 = s0[i]/sum0
            t1 = s1[i]/sum1
            v0 += t0
            v1 += t1
            sDKS.append(np.abs(v1 - v0))
        v = max(sDKS)
        ind = sDKS.index(v)
        return v, ind

    def integralpValue(self, abscisses, ordonnees, x):
        v = 0.0
        N = len(abscisses)
        if (x <= abscisses[0]) :
            x = 0. # ttl integral
            for i in range(0, N-1):
                v += (abscisses[i+1] - abscisses[i]) * ordonnees[i]
        elif (x >= abscisses[N-1]):
            v = 0. # null integral
        else: # general case
            ind = 0
            for i in range(0, N):
                if (np.floor(x/abscisses[i]) == 0):
                    ind = i
                    break
            #print('ind : %d' % ind)
            v = (abscisses[ind] - x) * ordonnees[ind-1]
            for i in range(ind, N-1):
                v += (abscisses[i+1] - abscisses[i]) * ordonnees[i]
        return v

    # major function to be called (ref is GevSeq.py)
    def decisionBox1(self, histoName, h1, h2, KS_path_local, shortRel):
        s0, e0 = self.getHistoValues(h1)
        s1, e1 = self.getHistoValues(h2)
        new_entries = h1.GetEntries()
        ref_entries = h2.GetEntries()
        d_max_1, r_mask_1 = self.getDifference_1(s0, e0, s1, e1)
        d_max_2, r_mask_2 = self.getDifference_2(s0, e0, s1, e1) # same as above without couples (0., 0.)
        d_max_3, r_mask_3 = self.getDifference_3(s0, e0, s1, e1) # same as above without couples first & end (0., 0.) couple.
        coeff_1 = self.getCoeff(r_mask_1)
        coeff_2 = self.getCoeff(r_mask_2)
        coeff_3 = self.getCoeff(r_mask_3)

        # Kolmogorov - Smirnov
        diffKS = 0.
        pValue = -1.
        I_Max = 1.
        fileName = KS_path_local + '-' + shortRel + '/histo_' + histoName + '_KScurve1.txt'
        fileExist = path.exists(fileName)
        #if ( fileExist and (os.path.getsize(fileName) != 0)):
        if ( fileExist):
            wKS = open(fileName, 'r')
            l1 = wKS.readline().rstrip('\n\r')
            l2 = wKS.readline().rstrip('\n\r')
            l3 = wKS.readline().rstrip('\n\r')
            l4 = wKS.readline().rstrip('\n\r')
            l5 = wKS.readline().rstrip('\n\r') # yellow curve
            l6 = wKS.readline().rstrip('\n\r') # cumulative yellow curve
            #print(histoName, ' : ', l1, type(l1),' - ',l1.split(',')[0], type(l1.split(',')[0]))
            I_Max = float(l1.split(',')[0])
            count = []
            division = []
            yellowCurve = []
            yellowCurveCum = []
            for elem in l3.split(' '):
                count.append(float(elem))
            for elem in l4.split(' '):
                division.append(float(elem))
            for elem in l5.split(' '):
                yellowCurve.append(float(elem))
            for elem in l6.split(' '):
                yellowCurveCum.append(float(elem))

            wKS.close()
            # Get the Kolmogoroff-Smirnov diff. for reference curve (s0) vs test curve (s1)
            diffKS, ind_pos_max = self.diffMAXKS(s0, s1, new_entries, ref_entries)
            # Get the p-Value for ref/test curves
            pValue = self.integralpValue(division, count, diffKS)
            yellowCurve = np.asarray(yellowCurve)
            yellowCurveCum = np.asarray(yellowCurveCum)
            return coeff_1, coeff_2, coeff_3, diffKS, pValue/I_Max, yellowCurve, yellowCurveCum # return normalized pValue
        else:
            print('no file name : %s' % fileName)
            return coeff_1, coeff_2, coeff_3, diffKS, pValue/I_Max # return normalized pValue

    def decisionBox2(self, histoName, h1, h2, KS_path_local, shortRel):
        s0, e0 = self.getHistoValues(h1)
        s1, e1 = self.getHistoValues(h2)
        new_entries = h1.GetEntries()
        ref_entries = h2.GetEntries()

        # Kolmogorov - Smirnov
        diffKS = 0.
        pValue = -1.
        I_Max = 1.
        fileName = KS_path_local + '-' + shortRel + '/histo_' + histoName + '_KScurve2.txt'
        fileExist = path.exists(fileName)
        if ( fileExist ):
            wKS = open(fileName, 'r')
            l1 = wKS.readline().rstrip('\n\r')
            l2 = wKS.readline().rstrip('\n\r')
            l3 = wKS.readline().rstrip('\n\r')
            l4 = wKS.readline().rstrip('\n\r')
            l5 = wKS.readline().rstrip('\n\r') # yellow curve
            l6 = wKS.readline().rstrip('\n\r') # cumulative yellow curve
            I_Max = float(l1.split(',')[0])

            count = []
            division = []
            yellowCurve = []
            yellowCurveCum = []
            for elem in l3.split(' '):
                count.append(float(elem))
            for elem in l4.split(' '):
                division.append(float(elem))
            for elem in l5.split(' '):
                yellowCurve.append(float(elem))
            for elem in l6.split(' '):
                yellowCurveCum.append(float(elem))

            wKS.close()
            # Get the Kolmogoroff-Smirnov diff. for reference curve (s0) vs test curve (s1)
            diffKS, ind_pos_max = self.diffMAXKS(s0, s1, new_entries, ref_entries)
            # Get the p-Value for ref/test curves
            pValue = self.integralpValue(division, count, diffKS)
            yellowCurve = np.asarray(yellowCurve)
            yellowCurveCum = np.asarray(yellowCurveCum[1:-1])
            return diffKS, pValue/I_Max, yellowCurve, yellowCurveCum # return normalized pValue
        else:
            return diffKS, pValue/I_Max # return normalized pValue

    def decisionBox3(self, histoName, h1, h2, KS_path_local, shortRel):
        s0, e0 = self.getHistoValues(h1)
        s1, e1 = self.getHistoValues(h2)
        new_entries = h1.GetEntries()
        ref_entries = h2.GetEntries()

        # Kolmogorov - Smirnov
        diffKS = 0.
        pValue = -1.
        I_Max = 1.
        fileName = KS_path_local + '-' + shortRel + '/histo_' + histoName + '_KScurve3.txt'
        fileExist = path.exists(fileName)
        if ( fileExist ):
            wKS = open(fileName, 'r')
            l1 = wKS.readline().rstrip('\n\r')
            l2 = wKS.readline().rstrip('\n\r')
            l3 = wKS.readline().rstrip('\n\r') # count
            l4 = wKS.readline().rstrip('\n\r') # division
            l5 = wKS.readline().rstrip('\n\r') # yellow curve : must be "new" curve
            l6 = wKS.readline().rstrip('\n\r') # cumulative yellow curve
            I_Max = float(l1.split(',')[0])

            count = []
            division = []
            yellowCurve = []
            yellowCurveCum = []
            for elem in l3.split(' '):
                count.append(float(elem))
            for elem in l4.split(' '):
                division.append(float(elem))
            for elem in l5.split(' '):
                yellowCurve.append(float(elem))
            for elem in l6.split(' '):
                yellowCurveCum.append(float(elem))

            wKS.close()
            # Get the Kolmogoroff-Smirnov diff. for reference curve (s0) vs test curve (s1)
            diffKS, ind_pos_max = self.diffMAXKS(s0, s1, new_entries, ref_entries)
            # Get the p-Value for ref/test curves
            pValue = self.integralpValue(division, count, diffKS)
            yellowCurve = np.asarray(yellowCurve)
            yellowCurveCum = np.asarray(yellowCurveCum[1:-1])
            return diffKS, pValue/I_Max, yellowCurve, yellowCurveCum # return normalized pValue
        else:
            return diffKS, pValue/I_Max # return normalized pValue

    def setColor(self, coeff):
        tmp = str("%6.4f" % coeff)
        if(coeff <= 0.35):
            text = "<font color=\'red\'><b>" + tmp + "</b></font>"
        elif(coeff <= 0.75):
            text = "<font color=\'blue\'><b>" + tmp + "</b></font>"
        else:
            text = "<font color=\'green\'><b>" + tmp + "</b></font>"
        #print("%6.4f : %s" % (coeff, text))
        return text

    def generateExplanation(self): # 1 line
        # creating shortHistoName file in DBox folder
        fExplain = open('DBox/explanation.html', 'w')  # web page
        fExplain.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\">\n")
        fExplain.write("<html>\n")
        fExplain.write("<head>\n")
        fExplain.write("<meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\" />\n")
        fExplain.write("<title> Some explanations </title>\n")  # option -t dans OvalFile
        fExplain.write("</head>\n")

        fExplain.write('<table border="1" bordercolor=green cellpadding="2" style="margin-left:auto;margin-right:auto">' + '\n')
        fExplain.write("<tr>\n")
        fExplain.write("<td colspan=3 style=\"text-align:center\"><br>")
        fExplain.write("<b>Some explanations</b>")
        fExplain.write("<br><br></td>\n")
        fExplain.write("</tr>\n")
        fExplain.write("<tr>\n")
        fExplain.write("<td><br>")
        fExplain.write("First we generate an average curve bin to bin from the mean of all the histograms.<br>")
        fExplain.write("Each of the 3 curves of the histogram on the left place represent the classical comparison of the histograms with the average curve added.<br>")
        fExplain.write("We have the new histo curve in <b><font color=\"red\">red</font></b>, ")
        fExplain.write("the reference one in <b><font color=\"blue\">blue</font></b> ")
        fExplain.write("and the average curve in <b><font color=\"green\">green</font></b><br>")
        fExplain.write("<br><br></td>\n")
        fExplain.write("<td><br>")
        fExplain.write("Here its a summary of the p-Values for the 3 cases explained below.<br>")
        fExplain.write("The first value (diff. max.) represents the maximum of difference between the 2 histograms curves.")
        fExplain.write("<br><br></td>\n")
        fExplain.write("<td><br>")
        fExplain.write("On the right, we have 3 graphs.<br>")
        fExplain.write("The first one represents the cumulatives curves of the 3 curves from the left histogram.<br>")
        fExplain.write("The second graph represents the difference curve between the 2 (new and reference) cumulatives curves of the left histogram.<br>")
        fExplain.write("The last graph represents the difference curve between the new curve and the average curve of the left histogram.")
        fExplain.write("<br><br></td>\n")
        fExplain.write("</tr>\n")
        fExplain.write("\n")
        fExplain.write("\n</table>\n")
        fExplain.write("<br>\n")
        fExplain.write("<table border=\"1\" bordercolor=\"blue\" cellpadding=\"2\" style=\"margin-left:auto;margin-right:auto\">\n")
        fExplain.write("<tr>\n") # line 0
        fExplain.write("<th scope=\"col\"><br>KS curves<br><br></th>\n")
        fExplain.write("</tr>\n")
        fExplain.write("<tr>\n")
        fExplain.write( "<td><br>")
        fExplain.write("For the first graph, we use all the references histograms and compare each cumulated curve with all the others. ")
        fExplain.write( "<br><br></td>\n")
        fExplain.write("</tr>\n")
        fExplain.write("<tr>\n")
        fExplain.write( "<td><br>")
        fExplain.write("For the second graph, we choose a random histogram as reference and compare its cumulated curve with each cumulated curve of all the others. ")
        fExplain.write( "<br><br></td>\n")
        fExplain.write("</tr>\n")
        fExplain.write("<tr>\n")
        fExplain.write( "<td><br>")
        fExplain.write("For the third graph, we took the histogram to be validated and compare its cumulated curve with each other cumulated curve of all the others histograms. ")
        fExplain.write( "<br><br></td>\n")
        fExplain.write("</tr>\n")
        fExplain.write("<tr><td></td></tr>\n")
        fExplain.write("<tr>\n")
        fExplain.write( "<td><br>")
        fExplain.write("<br>For each comparison, we take the maximum value of the difference. <br>")
        fExplain.write("For the 3 graphs, we took the max difference written above in the central box, ")
        fExplain.write("and display it with the following color code : <br>")
        fExplain.write("if the value is included into the x-axis limits, the max. difference corresponding to the p-Value is displayed as a <b><font color=\"green\">green</font></b> line, <br>")
        fExplain.write("and if the value is lesser or greater than the x-axis limits, then the corresponding line is in <b><font color=\"red\">red</font></b>.")
        fExplain.write( "<br><br></td>\n")
        fExplain.write("</tr>\n")
        fExplain.write("</table>\n")
        fExplain.close()
        return

    def DBwebPage(self, fHisto, Names, KS_V, DB_picture, webURL, shortWebFolder, dataSetFolder, KS_Path0, KS_Path, ycFlag, shortRelease):
        tool = Tools()
        explanationName = "/DBox/explanation.html"
        gif_name = Names[1]

        short_histo_names = Names[2]
        png_name = Names[3]
        png_cumul_name = Names[4]
        KS_Picture = []
        KS_fileExist = []
        KS_valid = False
        png_Picture = False
        png_fileExist = False
        png_valid = False
        pngCum_Picture = False
        pngCum_fileExist = False
        pngCum_valid = False
        for i in range(0,3):
            picture = 'KS-ttlDiff_' + str(i+1) + '_' + short_histo_names + '.png'
            KS_Picture.append(KS_Path + '-' + shortRelease + '/' + picture)
            KS_fileExist.append(path.exists(KS_Path0 + '-' + shortRelease + '/' + picture))
            KS_valid = KS_valid or KS_fileExist[i]
        if ycFlag:
            png_Picture = png_name.split('.')[0] + str(0) + '.png'
            png_fileExist = path.exists(png_Picture)
            png_valid = png_valid or png_fileExist
            pngCum_Picture = png_cumul_name.split('.')[0] + str(0) + '.png'
            pngCum_fileExist = path.exists(pngCum_Picture)
            pngCum_valid = pngCum_valid or pngCum_fileExist

        # write the KS reference release used.
        fHisto.write("<tr>\n")
        fHisto.write("<td colspan=3 style=\"text-align:center\">\n")
        fHisto.write("<br><b>Kolmogorov-Smirnov reference release used : <font color=\"red\">%s</font></b>\n" % KS_Path.split('/')[-1])
        fHisto.write("<br><br></td>\n")
        fHisto.write("</tr>\n")
        fHisto.write("<br>\n")
        fHisto.write("<tr>\n")
        fHisto.write("<th scope=\"col\">Comparison with average curve</th>\n")
        fHisto.write("<th scope=\"col\">KS Values</th>\n")
        fHisto.write("<th scope=\"col\">cumulatives & differences curves</th>\n")
        fHisto.write("</tr>\n")
        fHisto.write("<tr>")
        fHisto.write("<td>")
        if (png_valid and png_fileExist):
            fHisto.write("<div><a href=\"" + png_Picture + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + png_Picture + "\"></a></div>")
        else: # no png file (yellow curve)
            fHisto.write("<div><a href=\"" + gif_name + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + gif_name + "\"></a></div>")
        fHisto.write("</td>\n")
        KS_val_1 = KS_V[0]
        KS_val_2 = KS_V[1]
        KS_val_3 = KS_V[2]

        fHisto.write("<td>")
        fHisto.write(" <p><b>confiance : </b></p><p>coeff 1 : %6.4f<br>coeff 2 : %6.4f<br>coeff 3 : %6.4f</p>\n" % (KS_val_1[0], KS_val_1[1], KS_val_1[2]))
        fHisto.write(" <p>diff. max. : %6.4f</p>" % (KS_val_1[3]))
        if (KS_val_1[4] != -1.):
            pv1 = KS_val_1[4]
        else:
            pv1 = -1.0
        if ( KS_val_2[1] != -1. ):
            pv2 = KS_val_2[1]
        else:
            pv2 = -1.0
        if ( KS_val_3[1] != -1. ):
            pv3 = KS_val_3[1]
        else:
            pv3 = -1.0
        fHisto.write(" \n<p><b>KS 1 : </b> pValue : %6.4f</p>" % (pv1))
        fHisto.write("   <p><b>KS 2 : </b> pValue : %6.4f</p>" % (pv2))
        fHisto.write("   <p><b>KS 3 : </b> pValue : %6.4f</p>" % (pv3))
        fHisto.write("\n<div><a href=\"" + DB_picture + "\"><img border=\"0\" class=\"image\" width=\"40\" src=\"" + DB_picture + "\"></a></div>")
        fHisto.write("</td>\n")

        fHisto.write( "<td>")
        if (pngCum_valid and pngCum_fileExist):
            tool.extWrite( "<div><a href=\"" + pngCum_Picture + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + pngCum_Picture + "\"></a></div>", [fHisto] )
        fHisto.write( "</td>\n")
        fHisto.write("</tr>")

        fHisto.write("\n</table>\n")
        fHisto.write("\n")
        fHisto.write("<br>\n")
        fHisto.write("<table border=\"1\" bordercolor=\"blue\" cellpadding=\"2\" style=\"margin-left:auto;margin-right:auto\">\n")
        fHisto.write("<tr>\n")
        urlPath = webURL + shortWebFolder + '/' + dataSetFolder + explanationName
        fHisto.write("<th scope=\"col\"> <a href=\"" + urlPath + ">Explanations</a> </th>\n")
        fHisto.write("<th scope=\"col\">Kolmogorov-Smirnov curves</th>\n")
        fHisto.write("</tr>\n")

        fHisto.write("<tr>\n")
        fHisto.write( "<th scope=\"row\">p-Value 1 : %6.4f</th>\n" % pv1)
        fHisto.write( "<td>")
        if (KS_valid and KS_fileExist[0]):
            tool.extWrite( "<div><a href=\"" + KS_Picture[0] + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + KS_Picture[0] + "\"></a></div>", [fHisto] )
        fHisto.write( "</td>\n")
        fHisto.write("</tr>\n")#
        fHisto.write("<tr>\n")
        fHisto.write( "<th scope=\"row\">p-Value 2 : %6.4f</th>\n" % pv2)
        fHisto.write( "<td>")
        if (KS_valid and KS_fileExist[1]):
            tool.extWrite( "<div><a href=\"" + KS_Picture[1] + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + KS_Picture[1] + "\"></a></div>", [fHisto] )
        fHisto.write( "</td>\n")
        fHisto.write("</tr>\n")#
        fHisto.write("<tr>\n")
        fHisto.write( "<th scope=\"row\">p-Value 3 : %6.4f</th>\n" % pv3)
        fHisto.write( "<td>")
        if (KS_valid and KS_fileExist[2]):
            tool.extWrite( "<div><a href=\"" + KS_Picture[2] + "\"><img border=\"0\" class=\"image\" width=\"440\" src=\"" + KS_Picture[2] + "\"></a></div>", [fHisto] )
        fHisto.write( "</td>\n")
        fHisto.write("</tr>\n")#
        return

