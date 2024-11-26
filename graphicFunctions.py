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

import re
import numpy as np

from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
#ROOT.gErrorIgnoreLevel = ROOT.kWarning # remove info like : Info in <TCanvas::Print>: gif file gifs/h_ele_vertexPhi.gif has been created
# Print, Info, Warning, Error, Break, SysError and Fatal.
ROOT.gErrorIgnoreLevel = ROOT.kFatal # ROOT.kBreak
argv.remove( '-b-' )

from ROOT import kWhite, kBlue, kBlack, kRed, gStyle, TCanvas, gPad 

class Graphic:
    def __init__(self):
        self.toto = 1.2

    def initRoot(self):
        self.initRootStyle()

    def initRootStyle(self):
        gStyle.SetCanvasBorderMode(1)
        gStyle.SetCanvasColor(kWhite)
        gStyle.SetCanvasDefH(600)
        gStyle.SetCanvasDefW(800)
        gStyle.SetCanvasDefX(0)
        gStyle.SetCanvasDefY(0)
        gStyle.SetPadBorderMode(1)
        gStyle.SetPadColor(kWhite)
        gStyle.SetPadGridX(False)
        gStyle.SetPadGridY(False)
        gStyle.SetGridColor(0)
        gStyle.SetGridStyle(3)
        gStyle.SetGridWidth(1)
        gStyle.SetOptStat(1)
        gStyle.SetPadTickX(1)
        gStyle.SetPadTickY(1)
        gStyle.SetHistLineColor(1)
        gStyle.SetHistLineStyle(0)
        gStyle.SetHistLineWidth(2)
        gStyle.SetEndErrorSize(2)
        gStyle.SetErrorX(0.)
        gStyle.SetTitleColor(1, "XYZ")
        gStyle.SetTitleFont(32, "XYZ")
        gStyle.SetTitleX(0) # ne fonctionne pas avec les gds titres
        gStyle.SetTextAlign(13)
        gStyle.SetTitleX(0)
        gStyle.SetTitleAlign(13)
        gStyle.SetTitleStyle(3002)
        gStyle.SetTitleFillColor(18)
        gStyle.SetTitleXOffset(1.0)
        gStyle.SetTitleYOffset(1.0)
        gStyle.SetLabelOffset(0.005, "XYZ") # numeric label
        gStyle.SetTitleSize(0.05, "XYZ")
        gStyle.SetTitleFont(22,"X")
        gStyle.SetTitleFont(22,"Y")
        gStyle.SetTitleBorderSize(2)
        gStyle.SetPadBottomMargin(0.13) # 0.05
        gStyle.SetPadLeftMargin(0.15)
        gStyle.SetMarkerStyle(21)
        gStyle.SetMarkerSize(0.8)
        gStyle.SetOptTitle(2)
        gStyle.SetPadRightMargin(0.20)
        gStyle.cd()

    def getHisto(self, file, tp):
        #t1 = file.Get("DQMData")
        #t2 = t1.Get("Run 1")
        #t3 = t2.Get("EgammaV")
        #t4 = t3.Get("Run summary")
        #t5 = t4.Get(tp)
        path = 'DQMData/Run 1/EgammaV/Run summary/' + tp
        t_path = file.Get(path)
        return t_path # t5

    def getHistoConfEntry(self, h1):
        d = 1

        if ( h1.InheritsFrom("TH2") ):
            #print('TH2')
            d = 1
        elif ( h1.InheritsFrom("TProfile") ):
            #print('TProfile')
            d = 0
        elif ( h1.InheritsFrom("TH1")): # TH1
            #print('TH1')
            d = 1
        else:
            print("don't know")

        return d

    def RenderHisto(self, histo):
        if ("ELE_LOGY" in histo.GetOption() and histo.GetMaximum() > 0):
            self.cnv.SetLogy(1)
        histo_name_flag = 1 # use 0 to switch off
        if ( histo.InheritsFrom("TH2") ):
            gStyle.SetPalette(1)
            gStyle.SetOptStat(110+histo_name_flag)
        elif ( histo.InheritsFrom("TProfile") ):
            gStyle.SetOptStat(110+histo_name_flag)
        else: # TH1
            gStyle.SetOptStat(111110+histo_name_flag)

    def fill_Snew(self, histo):
        s_new = []
        for entry in histo:
            s_new.append(entry)
        s_new = np.asarray(s_new)
        s_new = s_new[1:-1]
        return s_new

    def fill_Snew2(self, d, histo):
        s_new = []
        ii = 0
        if (d==1):
            for entry in histo:
                s_new.append(entry)
        else:
            for entry in histo:
                if ((histo.GetBinEntries(ii) == 0.) and (entry == 0.)):
                    s_new.append(0.)
                elif ((histo.GetBinEntries(ii) == 0.) and (entry != 0.)):
                    s_new.append(1.e38)
                    print('========================================',ii,entry,histo.GetBinEntries(ii))
                else:
                    s_new.append(entry/histo.GetBinEntries(ii))
                ii+=1
        s_new = np.asarray(s_new)
        s_new = s_new[1:-1]
        return s_new

    def PictureChoice(self, histo1, histo2, scaled, err, filename, id):
        if (histo1):
            v_h1 = 1
        else:
            v_h1 = 0
        if (histo2):
            v_h2 = 1
        else:
            v_h2 = 0

        if ( (v_h1 + v_h2) == 0): # no histos at all
            return
        if ( (v_h1 * v_h2) == 0 ): # only one histo
            print('PictureChoice : One histo')
            self.createSinglePicture(histo1, histo2, scaled, err, filename, id, v_h1, v_h2)
        else: # two histos
            if( histo1.InheritsFrom("TH1F") ):
                #print('PictureChoice : TH1F')
                self.createPicture2(histo1, histo2, scaled, err, filename, id)
            elif ( histo1.InheritsFrom("TProfile") ):
                #print('PictureChoice : TProfile')
                self.createPicture2(histo1, histo2, scaled, err, filename, id)
            else:
                #print('PictureChoice : inherit from nothing')
                self.createPicture(histo1, histo2, scaled, err, filename, id)
            
    def PictureChoice2(self, args):
        # args = histo_1, histo_2, histo_positions[1], histo_positions[2], gif_name, args[0], args[8]
        h1 = args[0]
        h2 = args[1]
        scaled = args[2]
        err = args[3]
        filename = args[4]
        self = args[5]
        id = args[6]

        if (h1):
            v_h1 = 1
        else:
            v_h1 = 0
        if (h2):
            v_h2 = 1
        else:
            v_h2 = 0

        if ( (v_h1 + v_h2) == 0): # no histos at all
            return
        if ( (v_h1 * v_h2) == 0 ): # only one histo
             self.createSinglePicture(h1, h2, scaled, err, filename, id, v_h1, v_h2)
        else: # two histos
            if(h1.InheritsFrom("TH1F")):
                self.createPicture2(self, h1, h2, scaled, err, filename, id)
            elif ( h1.InheritsFrom("TProfile") ):
                self.createPicture2(self, h1, h2, scaled, err, filename, id)
            else:
                self.createPicture2(self, h1, h2, scaled, err, filename, id)
            
    def PictureChoice_DB(self, histo1, histo2, scaled, err, filename0, id, s0):
        # s0 : yellow curve tuple
        i = 0
        for elem in s0:
            if(histo1.InheritsFrom("TH1F")):
                # create png files
                tmp = filename0.split('.')
                filename = tmp[0] + str(i) + '.png'
                self.createPicture3(histo1, histo2, scaled, err, filename, id, elem)
        #elif ( histo1.InheritsFrom("TProfile") ):
        #    self.createPicture2(histo1, histo2, scaled, err, filename, id)
        #else:
        #    self.createPicture(histo1, histo2, scaled, err, filename, id)
            i += 1
        return

    def PictureChoice_DB2(self, histo1, histo2, scaled, err, filename0, id, s0):
        # s0 : yellow cumulative curve tuple
        i = 0
        for elem in s0:
            if(histo1.InheritsFrom("TH1F")):
                # create png files
                tmp = filename0.split('.')
                filename = tmp[0] + str(i) + '.png'
                #createCumulPicture(self, histo1, histo2, filename, id, elem)
                self.createCumulPicture2(histo1, histo2, filename, id, elem, i)
        #elif ( histo1.InheritsFrom("TProfile") ):
        #    self.createPicture2(histo1, histo2, scaled, err, filename, id)
        #else:
        #    self.createPicture(histo1, histo2, scaled, err, filename, id)
            i += 1
        return

    def PictureChoice_DB3(self, histo1, histo2, scaled, err, filename0, id, s0):
        # s0 : yellow cumulative curve tuple
        i = 0
        for elem in s0:
            # create png files
            tmp = filename0.split('.')
            filename = tmp[0] + str(i) + '.png'
            self.createCumulPicture3(histo1, histo2, filename, id, elem)
            i += 1
        return

    def createSinglePicture(self, histo1, histo2, scaled, err, filename, id, v_h1, v_h2):
        if (v_h1):
            print('histo1 OK')
            textToAdd = 'no reference (NULL), same as new histo'
            histo2 = histo1
        else:
            print('histo1 KO')
        if (v_h2):
            print('histo2 OK')
            textToAdd = 'no new histo (NULL), same as reference'
            histo1 = histo2
        else:
            print('histo2 KO')

        new_entries = histo1.GetEntries() # ttl # of bins (9000 in general)
        ref_entries = histo2.GetEntries()
        self.cnv = TCanvas(str(id), "canvas")
        #print(filename)

        histo2c = histo2.Clone()
        if ((scaled =="1") and (new_entries != 0) and (ref_entries != 0)):
            rescale_factor = new_entries / ref_entries
            histo2c.Scale(rescale_factor)
        if (histo2c.GetMaximum() > histo1.GetMaximum()):
            histo1.SetMaximum(histo2c.GetMaximum() * 1.1)
        
        self.cnv.SetCanvasSize(960, 900)
        self.cnv.Clear()
        self.cnv.SetFillColor(10)
        
        pad1 = ROOT.TPad(str(id), "pad1", 0, 0.25, 1.0, 1.0) # ,0,0,0
        pad1.SetBottomMargin(0.05)
        pad1.Draw()
        pad1.cd()
        
        if err == "1":
            newDrawOptions ="E1 P"
        else:
            newDrawOptions = "hist"
        
        histo1.SetStats(1)
        histo1.Draw(newDrawOptions) # 
        self.RenderHisto(histo1)
        if ("ELE_LOGY" in histo1.GetOption() and histo1.GetMaximum() > 0):
            if (re.search('etaEff_all', filename) or re.search('ptEff_all', filename)):
                print('accord')
                pad1.SetLogy(0)
            else:
                pad1.SetLogy(1)
        gPad.Update()
        statBox1 = histo1.GetListOfFunctions().FindObject("stats")
        statBox1.SetTextColor(kRed)    
        gPad.Update()
        histo2c.Draw("sames hist") # ""  same
        histo2c.SetStats(1)
        self.RenderHisto(histo2c)
        if ("ELE_LOGY" in histo2c.GetOption() and histo2c.GetMaximum() > 0):
            if (re.search('etaEff_all', filename) or re.search('ptEff_all', filename)):
                print('accord')
                pad1.SetLogy(0)
            else:
                pad1.SetLogy(1)
        self.cnv.Update()
        statBox2 = histo2c.GetListOfFunctions().FindObject("stats")
        statBox2.SetTextColor(kBlue)
        y1 = statBox1.GetY1NDC()
        y2 = statBox1.GetY2NDC()
        statBox2.SetY1NDC(2*y1-y2)
        statBox2.SetY2NDC(y1)

        newDrawOptions = "sames "
        if err == "1":
            newDrawOptions += "E1 P"
        else:
            newDrawOptions += "hist"
        histo1.Draw(newDrawOptions)
        histo2c.Draw("sames hist")
        
        t = ROOT.TText() # .45,.95, textToAdd
        #t.setNDC()
        t.SetTextAlign(22)
        t.SetTextColor(kRed+2)
        t.SetTextFont(43)
        t.SetTextSize(40)
        t.SetTextAngle(45)
        #t.Draw()
        t.DrawTextNDC(.5,.5, textToAdd)

        self.cnv.cd()
        pad2 = ROOT.TPad(str(id), "pad2", 0, 0.05, 1.00, 0.25) # ,0,0,0
        pad2.SetTopMargin(0.025)
        pad2.SetBottomMargin(0.2)
        pad2.SetGridy()
        pad2.Draw()
        pad2.cd()
        
        histo3 = histo1.Clone("histo3")
        histo3.SetLineColor(kBlack)
        histo3.SetMaximum(2.)
        histo3.SetMinimum(0.)
        histo3.SetStats(0)
        histo3.Sumw2() ########
        histo3.Divide(histo2)
        histo3.SetMarkerStyle(21)
        histo3.Draw("ep")
        
        histo1.SetMarkerColor(kRed)
        histo1.SetLineWidth(3) 
        histo1.SetLineColor(kRed)
        histo1.GetYaxis().SetTitleSize(25)
        histo1.GetYaxis().SetTitleFont(43)
        histo1.GetYaxis().SetTitleOffset(2.00)
        
        histo2c.SetLineColor(kBlue)
        histo2c.SetMarkerColor(kBlue)
        histo2c.SetLineWidth(3)
        
        histo3.SetTitle("")
        # Y axis ratio plot settings
        histo3.GetYaxis().SetTitle("ratio h1/h2 ")
        histo3.GetYaxis().SetNdivisions(505)
        histo3.GetYaxis().SetTitleSize(20)
        histo3.GetYaxis().SetTitleFont(43)
        histo3.GetYaxis().SetTitleOffset(1.55)
        histo3.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
        histo3.GetYaxis().SetLabelSize(15)
        # X axis ratio plot settings
        histo3.GetXaxis().SetTitleSize(20)
        histo3.GetXaxis().SetTitleFont(43)
        histo3.GetXaxis().SetTitleOffset(4.)
        histo3.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
        histo3.GetXaxis().SetLabelSize(15)

        self.cnv.Draw()
        self.cnv.Update()

        self.cnv.SaveAs(filename)
        
        return
        
    def createPicture(self, histo1, histo2, scaled, err, filename, id):
        new_entries = histo1.GetEntries()
        ref_entries = histo2.GetEntries()
        self.cnv = TCanvas(str(id), "canvas")
        print('createPicture')

        histo2c = histo2.Clone()
        if (scaled and (new_entries != 0) and (ref_entries != 0)):
            rescale_factor = new_entries / ref_entries
            histo2c.Scale(rescale_factor)
        if (histo2c.GetMaximum() > histo1.GetMaximum()):
            histo1.SetMaximum(histo2c.GetMaximum() * 1.1)
        
        self.cnv.SetCanvasSize(960, 600)
        self.cnv.Clear()
        histo2c.Draw()
        self.cnv.Update()

        self.cnv.Clear()
        histo1.Draw()
        self.cnv.Update()

        self.cnv.Clear()
        histo1.Draw()
        histo1.SetMarkerColor(kRed)
        histo1.SetLineWidth(3)
        histo1.SetStats(1)
        self.RenderHisto(histo1)
        gPad.Update()
        statBox1 = histo1.GetListOfFunctions().FindObject("stats")
        histo1.SetLineColor(kRed)
        histo1.SetMarkerColor(kRed)
        statBox1.SetTextColor(kRed)
        gPad.Update()
        histo2c.Draw()
        histo2c.SetLineWidth(3)
        histo2c.SetStats(1)
        self.RenderHisto(histo2c)
        self.cnv.Update()
        statBox2 = histo2c.GetListOfFunctions().FindObject("stats")
        histo2c.SetLineColor(kBlue)
        histo2c.SetMarkerColor(kBlue)
        statBox2.SetTextColor(kBlue)
        y1 = statBox1.GetY1NDC()
        y2 = statBox1.GetY2NDC()
        statBox2.SetY1NDC(2*y1-y2)
        statBox2.SetY2NDC(y1)
        histo1.Draw()
        histo2c.Draw("histsames")
        self.cnv.Draw()
        self.cnv.Update()
        
        self.cnv.SaveAs(filename)

        return
        
    def createPicture2(self, histo1, histo2, scaled, err, filename, id):
        new_entries = histo1.GetEntries() # ttl # of bins (9000 in general)
        ref_entries = histo2.GetEntries()
        self.cnv = TCanvas(str(id), "canvas")

        histo2c = histo2.Clone()
        histo3 = histo1.Clone("histo3")
        if ((scaled =="1") and (new_entries != 0) and (ref_entries != 0)):
            rescale_factor = new_entries / ref_entries
            histo2c.Scale(rescale_factor)
        if (histo2c.GetMaximum() > histo1.GetMaximum()):
            histo1.SetMaximum(histo2c.GetMaximum() * 1.1)
        
        self.cnv.SetCanvasSize(960, 900)
        self.cnv.Clear()
        self.cnv.SetFillColor(10)
        self.cnv.SetBorderMode(1)
        
        pad1 = ROOT.TPad(str(id), "pad1", 0, 0.25, 1.0, 1.0) # ,0,0,0
        pad1.SetBottomMargin(0.05)
        pad1.Draw()
        pad1.cd()
        
        if err == "1":
            newDrawOptions ="E1 P"
        else:
            newDrawOptions = "hist"
        
        histo1.SetStats(1)
        histo1.Draw(newDrawOptions) # 
        histo1.SetLineStyle(0)
        histo1.SetLineWidth(2)

        self.RenderHisto(histo1)
        if ("ELE_LOGY" in histo1.GetOption() and histo1.GetMaximum() > 0):
            if (re.search('etaEff_all', filename) or re.search('ptEff_all', filename)):
                print('accord')
                pad1.SetLogy(0)
            else:
                pad1.SetLogy(1)
        gPad.Update()
        
        statBox1 = histo1.GetListOfFunctions().FindObject("stats")
        statBox1.SetTextColor(kRed)
        statBox1.SetBorderSize(2)
        #statBox1.SetFillColor(kGray)
        statBox1.SetFillColorAlpha(18, 0.35) # https://root.cern.ch/doc/master/classTAttFill.html
        statBox1.SetY2NDC(0.995)
        statBox1.SetY1NDC(0.755)
        statBox1.SetX2NDC(0.995)
        statBox1.SetX1NDC(0.795)

        gPad.Update()
        histo2c.Draw("sames hist") # ""  same
        histo2c.SetStats(1)
        self.RenderHisto(histo2c)
        if ("ELE_LOGY" in histo2c.GetOption() and histo2c.GetMaximum() > 0):
            if (re.search('etaEff_all', filename) or re.search('ptEff_all', filename)):
                print('accord')
                pad1.SetLogy(0)
            else:
                pad1.SetLogy(1)
        self.cnv.Update()
        statBox2 = histo2c.GetListOfFunctions().FindObject("stats")
        statBox2.SetTextColor(kBlue)
        y1 = statBox1.GetY1NDC()
        y2 = statBox1.GetY2NDC()
        statBox2.SetY1NDC(2*y1-y2)
        statBox2.SetY2NDC(y1)
        statBox2.SetBorderSize(2)
        statBox2.SetFillColorAlpha(18, 0.35)
        statBox2.SetX2NDC(0.995)
        statBox2.SetX1NDC(0.795)

        newDrawOptions = "sames "
        if err == "1":
            newDrawOptions += "E1 P"
        else:
            newDrawOptions += "hist"
        histo1.Draw(newDrawOptions)
        histo2c.Draw("sames hist")
        
        self.cnv.cd()
        pad2 = ROOT.TPad(str(id), "pad2", 0, 0.05, 1.00, 0.26) # ,0,0,0
        pad2.SetTopMargin(0.025)
        pad2.SetBottomMargin(0.3)
        pad2.SetBorderMode(0)
        pad2.SetGridy()
        pad2.Draw()
        pad2.cd()
        
        d1 = self.getHistoConfEntry(histo3)
        d2 = self.getHistoConfEntry(histo2c)
        if ((d1 + d2) == 0): # TProfiles
            histo3r = histo3.ProjectionX()
            histo2cr = histo2c.ProjectionX()
        else:
            histo3r = histo3
            histo2cr = histo2c
        #histo3.Divide(histo2) # divide by the original nb of events
        #histo3.Divide(histo2c) # divide by the scaled nb of events
        histo3r.Divide(histo2cr) # divide by the scaled nb of events
        histo3r.SetLineColor(kBlack)
        histo3r.SetMaximum(2.)
        histo3r.SetMinimum(0.)
        histo3r.SetStats(0)
        histo3r.Sumw2()
        histo3r.SetMarkerStyle(21)
        histo3r.Draw("ep")
        
        histo1.SetMarkerColor(kRed)
        histo1.SetLineWidth(3) 
        histo1.SetLineColor(kRed)
        histo1.GetYaxis().SetTitleSize(25)
        histo1.GetYaxis().SetTitleFont(43)
        histo1.GetYaxis().SetTitleOffset(2.00)
        histo1.GetZaxis().SetTitleSize(0.05)
        histo1.SetMarkerStyle(21)
        histo1.SetMarkerSize(0.8)
        
        histo2c.SetLineColor(kBlue)
        histo2c.SetMarkerColor(kBlue)
        histo2c.SetLineWidth(3)
        
        histo3r.SetTitle("")
        # Y axis ratio plot settings
        histo3r.GetYaxis().SetTitle("ratio h1/h2 ")
        histo3r.GetYaxis().SetNdivisions(505)
        histo3r.GetYaxis().SetTitleSize(20)
        histo3r.GetYaxis().SetTitleFont(43)
        histo3r.GetYaxis().SetTitleOffset(1.55)
        histo3r.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
        histo3r.GetYaxis().SetLabelSize(15)
        # X axis ratio plot settings
        histo3r.GetXaxis().SetTitleSize(20)
        histo3r.GetXaxis().SetTitleFont(43)
        histo3r.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
        histo3r.GetXaxis().SetLabelSize(15)

        self.cnv.Draw()
        self.cnv.Update()

        #self.cnv.SaveAs(filename)
        self.cnv.Print(filename)
        self.cnv.Close()
        
        return
            
    def createPicture2b(self, histo1, histo2, filename, id):
        self.cnv = TCanvas(str(id), "canvas")

        print('call to histo2 Clone')
        histo2c = histo2.Clone()
        print('call to histo1 Clone')
        histo3 = histo1.Clone()
        print('end Cloning')

        self.cnv.SetCanvasSize(960, 900)
        self.cnv.Clear()
        self.cnv.SetFillColor(10)

        pad1 = ROOT.TPad(str(id), "pad1", 0, 0.25, 1.0, 1.0) # ,0,0,0
        pad1.SetBottomMargin(0.05)
        pad1.Draw()
        pad1.cd()
        
        newDrawOptions = "hist"
        histo2.SetStats(1)
        histo2.Draw(newDrawOptions) # 
        
        self.cnv.Draw()
        self.cnv.Update()

        self.cnv.SaveAs(filename)
        self.cnv.Close()
        
        return

    def createPicture3(self, histo1, histo2, scaled, err, filename, id, s0):
        # same as createPicture2 but with yellowCurve
        new_entries = histo1.GetEntries()
        ref_entries = histo2.GetEntries()
        self.cnv = TCanvas(str(id), "canvas")
        
        histo2c = histo2.Clone()
        if ((scaled =="1") and (new_entries != 0) and (ref_entries != 0)):
            rescale_factor = new_entries / ref_entries
            histo2c.Scale(rescale_factor)
        if (histo2c.GetMaximum() > histo1.GetMaximum()):
            histo1.SetMaximum(histo2c.GetMaximum() * 1.1)
        
        self.cnv.SetCanvasSize(960, 900)
        self.cnv.Clear()
        self.cnv.SetFillColor(10)
        self.cnv.SetBorderMode(1)
        
        pad1 = ROOT.TPad(str(id), "pad1", 0, 0.25, 1.0, 1.0) # ,0,0,0
        pad1.SetBottomMargin(0.05)
        pad1.Draw()
        pad1.cd()
        
        if err == "1":
            newDrawOptions ="E1 P"
        else:
            newDrawOptions = "hist"
        
        histo1.SetStats(1)
        histo1.Draw(newDrawOptions) # 
        histo1.SetLineStyle(0)
        histo1.SetLineWidth(2)

        self.RenderHisto(histo1)
        if ("ELE_LOGY" in histo1.GetOption() and histo1.GetMaximum() > 0):
            pad1.SetLogy(1)
        gPad.Update()

        statBox1 = histo1.GetListOfFunctions().FindObject("stats")
        statBox1.SetTextColor(kRed)    
        statBox1.SetBorderSize(2)
        #statBox1.SetFillColor(kGray)
        statBox1.SetFillColorAlpha(18, 0.35) # https://root.cern.ch/doc/master/classTAttFill.html
        statBox1.SetY2NDC(0.995)
        statBox1.SetY1NDC(0.755)
        statBox1.SetX2NDC(0.995)
        statBox1.SetX1NDC(0.795)

        gPad.Update()
        histo2c.Draw("sames hist") # ""  same
        histo2c.SetStats(1)
        self.RenderHisto(histo2c)
        if ("ELE_LOGY" in histo2c.GetOption() and histo2c.GetMaximum() > 0):
            pad1.SetLogy(1)
        self.cnv.Update()
        statBox2 = histo2c.GetListOfFunctions().FindObject("stats")
        statBox2.SetTextColor(kBlue)
        y1 = statBox1.GetY1NDC()
        y2 = statBox1.GetY2NDC()
        statBox2.SetY1NDC(2*y1-y2)
        statBox2.SetY2NDC(y1)
        statBox2.SetBorderSize(2)
        statBox2.SetFillColorAlpha(18, 0.35)
        statBox2.SetX2NDC(0.995)
        statBox2.SetX1NDC(0.795)

        newDrawOptions = "sames "
        if err == "1":
            newDrawOptions += "E1 P"
        else:
            newDrawOptions += "hist"
        histo1.Draw(newDrawOptions)
        histo2c.Draw("sames hist")
        
        # yellow curve
        # only whith TH1F
        # need to rescale
        # rom https://root.cern.ch/root/htmldoc/guides/users-guide/Histograms.html
        nbX = histo1.GetXaxis().GetNbins()
        xmin = histo1.GetXaxis().GetXmin()
        xmax = histo1.GetXaxis().GetXmax()
        yC = ROOT.TH1F("average curve", "curve", nbX, xmin, xmax)
        i = 1
        yC.SetBinContent(0, 0.)
        for elem in s0:
            yC.SetBinContent(i, elem)
            i+=1
        yC.SetBinContent(i, 0.)
        yC.SetLineColor(kGreen-2) # kYellow
        yC.SetStats(1)
        yC.Draw(newDrawOptions) # sames hist
        self.RenderHisto(yC)
        self.cnv.Update()
        statBox3 = yC.GetListOfFunctions().FindObject("stats")    
        #if (statBox3):
        #    print("statBox3 OK")
        #else:
        #    print("statBox3 KO")
        statBox3.SetTextColor(kGreen-2) # kYellow
        y1 = statBox1.GetY1NDC()
        y2 = statBox1.GetY2NDC()
        y3 = statBox2.GetY1NDC()
        #y4 = statBox2.GetY2NDC()
        statBox3.SetY1NDC(3*y1-2*y2)
        statBox3.SetY2NDC(y3)
        statBox3.SetBorderSize(2)
        statBox3.SetFillColorAlpha(18, 0.35)
        statBox3.SetX2NDC(0.995)
        statBox3.SetX1NDC(0.795)
        yC.Draw("sames hist") # 

        self.cnv.cd()
        pad2 = ROOT.TPad(str(id), "pad2", 0, 0.05, 1.0, 0.26) # ,0,0,0
        pad2.SetTopMargin(0.025)
        pad2.SetBottomMargin(0.3)
        pad2.SetGridy()
        pad2.Draw()
        pad2.cd()
        
        histo3 = histo1.Clone("histo3")
        histo3.SetLineColor(kBlack)
        histo3.SetMaximum(2.)
        histo3.SetStats(0)
        histo3.Sumw2() ########
        histo3.Divide(histo2c)
        histo3.SetMarkerStyle(21)
        histo3.Draw("ep")
        
        histo1.SetMarkerColor(kRed)
        histo1.SetLineWidth(3) 
        histo1.SetLineColor(kRed)
        histo1.GetYaxis().SetTitleSize(25)
        histo1.GetYaxis().SetTitleFont(43)
        histo1.GetYaxis().SetTitleOffset(2.00)
        histo1.GetZaxis().SetTitleSize(0.05)
        histo1.SetMarkerStyle(21)
        histo1.SetMarkerSize(0.8)
        
        histo2c.SetLineColor(kBlue)
        histo2c.SetMarkerColor(kBlue)
        histo2c.SetLineWidth(3)
        
        histo3.SetTitle("")
        # Y axis ratio plot settings
        histo3.GetYaxis().SetTitle("ratio h1/h2 ")
        histo3.GetYaxis().SetNdivisions(505)
        histo3.GetYaxis().SetTitleSize(20)
        histo3.GetYaxis().SetTitleFont(43)
        histo3.GetYaxis().SetTitleOffset(1.55)
        histo3.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
        histo3.GetYaxis().SetLabelSize(15)
        # X axis ratio plot settings
        histo3.GetXaxis().SetTitleSize(20)
        histo3.GetXaxis().SetTitleFont(43)
        histo3.GetXaxis().SetTitleOffset(4.)
        histo3.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
        histo3.GetXaxis().SetLabelSize(15)
    
        self.cnv.Draw()
        self.cnv.Update()

        self.cnv.SaveAs(filename)
        
        return
            
    def createCumulPicture3(self, histo1, histo2, filename, id, s0):
        #import numpy as np
        new_entries = histo1.GetEntries()
        ref_entries = histo2.GetEntries()
        self.cnv = TCanvas(str(id), "canvas")
        # print('len : s0=%d, new_entries=%d, ref_entries=%d' %(len(s0), (new_entries), (ref_entries))) # temp

        sumNew = 0.
        sumRef = 0.
        cumulNew = []
        cumulRef = []
        t_new = []
        t_ref = []

        for entry in histo1:
            t_new.append(entry)

        for entry in histo2:
            t_ref.append(entry)

        t_new = t_new[1:-1]
        t_ref = t_ref[1:-1]

        for elem in t_new:
            sumNew += elem
            cumulNew.append(sumNew)
        for elem in t_ref:
            sumRef += elem
            cumulRef.append(sumRef)
        
        # TEMPORARY test
        if ( len(cumulNew) != len(cumulRef)):
            print('pbm with array size [%d, %d]' % (len(cumulNew), len(cumulRef)))
            return
        
        #print('cumul rel : %f - sum rel : %f' % (sumNew, new_entries))
        #print('cumul ref : %f - sum ref : %f' % (sumRef, ref_entries))
        #print('len : s0=%d, cumulNew=%d, cumulRef=%d' %(len(s0), len(cumulNew), len(cumulRef))) # temp
        cumulNew = np.asarray(cumulNew) / new_entries
        cumulRef = np.asarray(cumulRef) / ref_entries
        #print('len cumul new/ref : %d/%d - len s0 : %d' % (len(cumulNew), len(cumulRef), len(s0)))
        diff1 = np.abs(cumulNew - cumulRef)
        diff2 = np.abs(s0 - cumulNew)
        #print('diff 1 : %f - diff 2 : %f' % (np.max(diff1), np.max(diff2)))

        self.cnv.SetCanvasSize(960, 900)
        self.cnv.Clear()
        self.cnv.SetFillColor(10)

        #pad1 = ROOT.TPad(str(id), "pad1", 0, 0.5, 1, 1.0)  # 0, 0.25, 1, 1.0
        pad1 = ROOT.TPad(str(id), "pad1", 0, 0.65, 1, 1.0)  #
        # pad1.SetBottomMargin(0.05)
        pad1.Draw()
        pad1.cd()
        pad1.SetLogy(1)

        newDrawOptions = "sames hist"

        # yellow curve only whith TH1F
        # need to rescale
        # rom https://root.cern.ch/root/htmldoc/guides/users-guide/Histograms.html
        nbX = histo1.GetXaxis().GetNbins()
        xmin = histo1.GetXaxis().GetXmin()
        xmax = histo1.GetXaxis().GetXmax()
        #print('nbX : %d' % nbX)

        newC = ROOT.TH1F("new curve", "cumulatives curves", nbX, xmin, xmax)
        refC = ROOT.TH1F("ref curve", "cumulatives curves", nbX, xmin, xmax)
        yC = ROOT.TH1F("average curve", "cumulatives curves", nbX, xmin, xmax)
        newC.SetLineColor(kRed)
        refC.SetLineColor(kBlue)
        yC.SetLineColor(kGreen - 2)

        newC.SetBinContent(0, elem)
        i = 1
        for elem in cumulNew:
            newC.SetBinContent(i, elem)
            i += 1
        newC.SetBinContent(i, elem)
        refC.SetBinContent(0, elem)
        i = 1
        for elem in cumulRef:
            refC.SetBinContent(i, elem)
            i += 1
        refC.SetBinContent(i, elem)
        yC.SetBinContent(0, elem)
        i = 1
        for elem in s0:
            yC.SetBinContent(i, elem)
            i += 1
        yC.SetBinContent(i, elem)

        newC.SetStats(1)
        newC.Draw(newDrawOptions)  # sames hist
        gPad.Update()
        statBox1 = newC.GetListOfFunctions().FindObject("stats")
        statBox1.SetTextColor(kRed)
        statBox1.SetFillColorAlpha(18, 0.35) # https://root.cern.ch/doc/master/classTAttFill.html
        statBox1.SetY2NDC(0.995)
        statBox1.SetY1NDC(0.755)
        statBox1.SetX2NDC(0.995)
        statBox1.SetX1NDC(0.795)
        gPad.Update()
        refC.Draw(newDrawOptions)  # sames hist
        refC.SetStats(1)
        self.cnv.Update()
        statBox2 = refC.GetListOfFunctions().FindObject("stats")
        statBox2.SetTextColor(kBlue)
        y1 = statBox1.GetY1NDC()
        y2 = statBox1.GetY2NDC()
        statBox2.SetY1NDC(2 * y1 - y2)
        statBox2.SetY2NDC(y1)
        statBox2.SetBorderSize(2)
        statBox2.SetFillColorAlpha(18, 0.35)
        statBox2.SetX2NDC(0.995)
        statBox2.SetX1NDC(0.795)
        newC.Draw(newDrawOptions)  # sames hist
        refC.Draw(newDrawOptions)  # sames hist

        yC.SetLineColor(kGreen - 2)
        yC.SetStats(1)
        yC.Draw(newDrawOptions)  # sames hist
        self.cnv.Update()
        statBox3 = yC.GetListOfFunctions().FindObject("stats")
        statBox3.SetTextColor(kGreen - 2)
        y1 = statBox1.GetY1NDC()
        y2 = statBox1.GetY2NDC()
        y3 = statBox2.GetY1NDC()
        y4 = statBox2.GetY2NDC()
        statBox3.SetY1NDC(3 * y1 - 2 * y2)
        statBox3.SetY2NDC(y3)
        statBox3.SetBorderSize(2)
        statBox3.SetFillColorAlpha(18, 0.35)
        statBox3.SetX2NDC(0.995)
        statBox3.SetX1NDC(0.795)
        yC.Draw("sames hist")  #

        self.cnv.cd()
        pad2 = ROOT.TPad(str(id), "pad2", 0, 0.33, 1.0, 0.65)  #
        # pad2.SetTopMargin(0.05)
        # pad2.SetBottomMargin(0.2)
        pad2.SetGridy()
        pad2.Draw()
        pad2.cd()

        diffC = ROOT.TH1F("diff. of curves", "diff. between new and ref. curves", nbX, xmin, xmax)

        diffC.SetBinContent(0, elem)
        i = 1
        vMax = 0.
        for elem in diff1:
            diffC.SetBinContent(i, elem)
            i += 1
        diffC.SetBinContent(i, elem)
        diffC.SetMarkerStyle(3)
        diffC.SetMarkerColor(kBlue)
        diffC.Draw("lp")  #

        self.cnv.Update()

        self.cnv.cd()
        pad3 = ROOT.TPad(str(id), "pad3", 0, 0.0, 1.0, 0.33)  # 0, 0.05, 1, 0.25
        # pad3.SetTopMargin(0.05)
        # pad3.SetBottomMargin(0.2)
        pad3.SetGridy()
        pad3.Draw()
        pad3.cd()

        diffD = ROOT.TH1F("diff. of cumul. curves", "new and average cumul. curves diff.", nbX, xmin, xmax)

        diffD.SetBinContent(0, elem)
        i = 1
        for elem in diff2:
            diffD.SetBinContent(i, elem)
            i += 1
        diffD.SetBinContent(i, elem)

        diffD.SetMarkerStyle(3)
        diffD.SetMarkerColor(kGreen)
        diffD.Draw("lp")  #

        self.cnv.Draw()
        self.cnv.Update()

        self.cnv.SaveAs(filename)

        return

    def createHistoPicture(self, histo1, filename):
        # draw a filled histogram & save it into a file.
        cnv = TCanvas(str(id), "canvas")
        print('createPicture')

        cnv.SetCanvasSize(960, 600)

        cnv.Clear()
        histo1.Draw()
        histo1.SetLineWidth(3)
        histo1.SetStats(1)
        #RenderHisto(histo1)
        gPad.Update()
        statBox1 = histo1.GetListOfFunctions().FindObject("stats")
        histo1.SetLineColor(kBlack)
        histo1.SetMarkerColor(kRed)
        statBox1.SetTextColor(kBlue)
        statBox1.SetFillStyle(0);
        statBox1.SetY1NDC(0.800)
        statBox1.SetFillColorAlpha(18, 0.35) # https://root.cern.ch/doc/master/classTAttFill.html
        statBox1.SetY2NDC(0.995)
        statBox1.SetY1NDC(0.755)
        statBox1.SetX2NDC(0.995)
        statBox1.SetX1NDC(0.795)
        gPad.Update()

        cnv.Draw()
        cnv.Update()
        
        cnv.SaveAs(filename)

        return

    def getCurveTailPos(self, histo1, histo2):
        t_histo1 = []
        t_histo2 = []
        for entry in histo1:
            t_histo1.append(entry)
        t_histo1 = t_histo1[1:-1]
        for entry in histo2:
            t_histo2.append(entry)
        t_histo2 = t_histo2[1:-1]

        ymin = min(t_histo1)
        ymax = max(t_histo1)
        if min(t_histo2) < ymin:
            ymin = min(t_histo2)
        if max(t_histo2) > ymax:
            ymax = max(t_histo2)

        pos = 0.
        N = len(t_histo1)
        nPos = int(N / 5)
        print('nPos : %d / nLen : %d' % (nPos, N))
        for i in range(N-nPos, N):
            pos += t_histo1[i]
        pos /= nPos
        print('mean position : %f' % pos)
        print('min - max : %f - %f' % (ymin, ymax))
        relativePos = (pos - ymin) / (ymax - ymin)
        print('relative position : %f' % relativePos)
        return relativePos

    def createCumulPicture(self, histo1, histo2, filename, id, s0):
        #new_entries = histo1.GetEntries()
        #ref_entries = histo2.GetEntries()
        self.cnv = TCanvas(str(id), "canvas")
        
        sumNew = 0.
        sumRef = 0.
        cumulNew = []
        cumulRef = []
        for entry in histo1:
            sumNew += entry
            cumulNew.append(sumNew)
        for entry in histo2:
            sumRef += entry
            cumulRef.append(sumRef)
        #print(sumNew, sumRef)
        cumulNew = np.asarray(cumulNew) / sumNew
        cumulRef = np.asarray(cumulRef) / sumRef
        
        self.cnv.SetCanvasSize(960, 900)
        self.cnv.Clear()
        self.cnv.SetFillColor(10)
        
        pad1 = ROOT.TPad(str(id), "pad1", 0, 0.25, 1, 1.0) # ,0,0,0
        pad1.SetBottomMargin(0.05)
        pad1.Draw()
        pad1.cd()
        pad1.SetLogy(1)
        
        newDrawOptions = "sames hist"
        
        # yellow curve only whith TH1F
        # need to rescale
        # rom https://root.cern.ch/root/htmldoc/guides/users-guide/Histograms.html
        nbX = histo1.GetXaxis().GetNbins()
        xmin = histo1.GetXaxis().GetXmin()
        xmax = histo1.GetXaxis().GetXmax()
        #print('nbX : %d' % nbX)

        newC = ROOT.TH1F("new curve", "curve", nbX, xmin, xmax)
        refC = ROOT.TH1F("ref curve", "curve", nbX, xmin, xmax)
        yC = ROOT.TH1F("average curve", "curve", nbX, xmin, xmax)
        newC.SetLineColor(kRed)
        refC.SetLineColor(kBlue)
        yC.SetLineColor(kGreen-2) # kYellow
        
        i = 0
        for elem in cumulNew:
            newC.SetBinContent(i, elem)
            i+=1
        i = 0
        for elem in cumulRef:
            refC.SetBinContent(i, elem)
            i+=1
        i = 1 # because of nb of bin in s0
        for elem in s0:
            yC.SetBinContent(i, elem)
            i+=1
        
        newC.SetStats(1)
        newC.Draw(newDrawOptions) # sames hist
        gPad.Update()
        statBox1 = newC.GetListOfFunctions().FindObject("stats")
        #if (statBox1):
        #    print("statBox1 OK")
        #else:
        #    print("statBox1 KO")
        statBox1.SetTextColor(kRed)
        statBox1.SetBorderSize(2)
        statBox1.SetFillColorAlpha(18, 0.35)
        statBox1.SetX2NDC(0.995)
        statBox1.SetX1NDC(0.795)
        gPad.Update()
        refC.Draw(newDrawOptions) # sames hist
        refC.SetStats(1)
        self.cnv.Update()
        statBox2 = refC.GetListOfFunctions().FindObject("stats")
        #if (statBox2):
        #    print("statBox2 OK")
        #else:
        #    print("statBox2 KO")
        statBox2.SetTextColor(kBlue)
        y1 = statBox1.GetY1NDC()
        y2 = statBox1.GetY2NDC()
        statBox2.SetY1NDC(2*y1-y2)
        statBox2.SetY2NDC(y1)
        statBox2.SetBorderSize(2)
        statBox2.SetFillColorAlpha(18, 0.35)
        statBox2.SetX2NDC(0.995)
        statBox2.SetX1NDC(0.795)
        newC.Draw(newDrawOptions) # sames hist
        refC.Draw(newDrawOptions) # sames hist

        yC.SetLineColor(kGreen-2) # kYellow
        yC.SetStats(1)
        yC.Draw(newDrawOptions) # sames hist
        self.cnv.Update()
        statBox3 = yC.GetListOfFunctions().FindObject("stats")    
        #if (statBox3):
        #    print("statBox3 OK")
        #else:
        #    print("statBox3 KO")
        statBox3.SetTextColor(kGreen-2) # kYellow, kGreen is similar to light green, 8 is dark green
        y1 = statBox1.GetY1NDC()
        y2 = statBox1.GetY2NDC()
        y3 = statBox2.GetY1NDC()
        #y4 = statBox2.GetY2NDC()
        statBox3.SetY1NDC(3*y1-2*y2)
        statBox3.SetY2NDC(y3)
        statBox3.SetBorderSize(2)
        statBox3.SetFillColorAlpha(18, 0.35)
        statBox3.SetX2NDC(0.995)
        statBox3.SetX1NDC(0.795)
        yC.Draw("sames hist") # 

        self.cnv.Draw()
        self.cnv.Update()

        self.cnv.SaveAs(filename)
        
        return
            
    def createCumulPicture2(self, histo1, histo2, filename, id, s0):
        #new_entries = histo1.GetEntries()
        #ref_entries = histo2.GetEntries()
        self.cnv = TCanvas(str(id), "canvas")
        #print('len : s0=%d, new_entries=%d, ref_entries=%d' %(len(s0), (new_entries), (ref_entries))) # temp
        
        sumNew = 0.
        sumRef = 0.
        cumulNew = []
        cumulRef = []
        diff = []
        for entry in histo1:
            sumNew += entry
            cumulNew.append(sumNew)
        for entry in histo2:
            sumRef += entry
            cumulRef.append(sumRef)
        #print(sumNew, sumRef)
        #print('len : s0=%d, cumulNew=%d, cumulRef=%d' %(len(s0), len(cumulNew), len(cumulRef))) # temp
        cumulNew = np.asarray(cumulNew) / sumNew
        cumulRef = np.asarray(cumulRef) / sumRef
        if ( k == 2 ):
            diff = np.abs(cumulNew - cumulRef)
        else:
            diff = np.abs(s0 - cumulRef[1:-1])
        
        self.cnv.SetCanvasSize(960, 900)
        self.cnv.Clear()
        self.cnv.SetFillColor(10)
        
        pad1 = ROOT.TPad(str(id), "pad1", 0, 0.5, 1, 1.0) # 0, 0.25, 1, 1.0
        #pad1.SetBottomMargin(0.05)
        pad1.Draw()
        pad1.cd()
        pad1.SetLogy(1)
        
        newDrawOptions = "sames hist"
        
        # yellow curve only whith TH1F
        # need to rescale
        # rom https://root.cern.ch/root/htmldoc/guides/users-guide/Histograms.html
        nbX = histo1.GetXaxis().GetNbins()
        xmin = histo1.GetXaxis().GetXmin()
        xmax = histo1.GetXaxis().GetXmax()
        #print('nbX : %d' % nbX)

        newC = ROOT.TH1F("new curve", "curve", nbX, xmin, xmax)
        refC = ROOT.TH1F("ref curve", "curve", nbX, xmin, xmax)
        yC = ROOT.TH1F("average curve", "curve", nbX, xmin, xmax)
        newC.SetLineColor(kRed)
        refC.SetLineColor(kBlue)
        yC.SetLineColor(kGreen-2)
        
        i = 0
        for elem in cumulNew:
            newC.SetBinContent(i, elem)
            i+=1
        i = 0
        for elem in cumulRef:
            refC.SetBinContent(i, elem)
            i+=1
        i = 1
        for elem in s0:
            yC.SetBinContent(i, elem)
            i+=1
        
        newC.SetStats(1)
        newC.Draw(newDrawOptions) # sames hist
        gPad.Update()
        statBox1 = newC.GetListOfFunctions().FindObject("stats")
        #if (statBox1):
        #    print("statBox1 OK")
        #else:
        #    print("statBox1 KO")
        statBox1.SetTextColor(kRed)
        statBox1.SetFillColorAlpha(18, 0.35) # https://root.cern.ch/doc/master/classTAttFill.html
        statBox1.SetX2NDC(0.995)
        statBox1.SetX1NDC(0.795)
        gPad.Update()
        refC.Draw(newDrawOptions) # sames hist
        refC.SetStats(1)
        self.cnv.Update()
        statBox2 = refC.GetListOfFunctions().FindObject("stats")
        #if (statBox2):
        #    print("statBox2 OK")
        #else:
        #    print("statBox2 KO")
        statBox2.SetTextColor(kBlue)
        y1 = statBox1.GetY1NDC()
        y2 = statBox1.GetY2NDC()
        statBox2.SetY1NDC(2*y1-y2)
        statBox2.SetY2NDC(y1)
        statBox2.SetBorderSize(2)
        statBox2.SetFillColorAlpha(18, 0.35)
        statBox2.SetX2NDC(0.995)
        statBox2.SetX1NDC(0.795)
        newC.Draw(newDrawOptions) # sames hist
        refC.Draw(newDrawOptions) # sames hist

        yC.SetLineColor(kGreen-2)
        yC.SetStats(1)
        yC.Draw(newDrawOptions) # sames hist
        self.cnv.Update()
        statBox3 = yC.GetListOfFunctions().FindObject("stats")    
        #if (statBox3):
        #    print("statBox3 OK")
        #else:
        #    print("statBox3 KO")
        statBox3.SetTextColor(kGreen-2)
        y1 = statBox1.GetY1NDC()
        y2 = statBox1.GetY2NDC()
        y3 = statBox2.GetY1NDC()
        y4 = statBox2.GetY2NDC()
        statBox3.SetY1NDC(3*y1-2*y2)
        statBox3.SetY2NDC(y3)
        statBox3.SetBorderSize(2)
        statBox3.SetFillColorAlpha(18, 0.35)
        statBox3.SetX2NDC(0.995)
        statBox3.SetX1NDC(0.795)
        yC.Draw("sames hist") # 

        self.cnv.cd()
        pad2 = ROOT.TPad(str(id), "pad2", 0, 0.0, 1.0, 0.5) # 0, 0.05, 1, 0.25
        pad2.SetTopMargin(0.05)
        #pad2.SetBottomMargin(0.2)
        pad2.SetGridy()
        pad2.Draw()
        pad2.cd()
        
        diffC = ROOT.TH1F("diff. of cumul. curves", "curve", nbX, xmin, xmax)
        
        i = 0
        for elem in diff:
            diffC.SetBinContent(i, elem)
            i+=1
        
        diffC.SetMarkerStyle(3)
        diffC.SetMarkerColor(kBlue)
        #diffC.SetLineColor(kGreen-2)
        diffC.Draw("lp") #
        
        self.cnv.Draw()
        self.cnv.Update()

        self.cnv.SaveAs(filename)
        
        return


