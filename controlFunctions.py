#!/usr/bin/env python
# coding: utf-8

################################################################################
# controlFunctions : a tool with all functions used in the KSTools environment
# for egamma AutoEncoder/KS validation comparison                              
#
# MUST be launched with the cmsenv cmd after a cmsrel cmd !!
#                                                                              
# Arnaud Chiron-Turlay LLR - arnaud.chiron@llr.in2p3.fr                        
#                                                                              
################################################################################

import os

from os import listdir
from os.path import isfile, join

def checkFolderName(folderName):
    if folderName[-1] != '/':
        folderName += '/'
    return folderName

'''    # create folder 
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except OSError as e:
            if e.errno != errno.EEXIST: # the folder did not exist
                raise  # raises the error again
        print('Creation of %s release folder\n' % folder)
    else:
        print('Folder %s already created\n' % folder)
'''

def checkFolder(folder):
    if not os.path.exists(folder): # create folder
        os.makedirs(folder) # create reference folder
    else: # folder already created
        print('%s already created.' % folder)
    return

def changeColor(color):
    # 30:noir ; 31:rouge; 32:vert; 33:orange; 34:bleu; 35:violet; 36:turquoise; 37:blanc
    # other references at https://misc.flogisoft.com/bash/tip_colors_and_formatting
    if (color == 'black'):
        return '[30m'
    elif (color == 'red'):
        return '[31m'
    elif (color == 'green'):
        return '[32m'
    elif (color == 'orange'):
        return '[33m'
    elif (color == 'blue'):
        return '[34m'
    elif (color == ''):
        return '[35m'
    elif (color == 'purple'):
        return '[36m'
    elif (color == 'turquoise'):
        return '[37m'
    elif (color == 'lightyellow'):
        return '[93m'
    else:
        return '[30m'

def colorText(sometext, color):
    return '\033' + changeColor(color) + sometext + '\033[0m'

def getListFiles(path, ext='root'):
    # use getListFiles(str path_where_the_files_are, str 'ext')
    # ext can be root, txt, png, ...
    # default is root
    ext = '.' + ext
    #print('path : %s' % path)
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    onlyfiles = [f for f in onlyfiles if f.endswith(ext)] # keep only root files
    #print(onlyfiles)
    return onlyfiles

def getBranches(t_p, branchPath):
    b = []
    source = open(branchPath, "r")
    for ligne in source:
        if t_p in ligne:
            #print(ligne)
            tmp = ligne.split(" ", 1)
            #print(tmp[0].replace(t_p + "/", ""))
            b.append(tmp[0].replace(t_p + "/", ""))
    source.close()
    return b

def getKeysName(t_p, branchPath):
    b = []
    key = ''
    tmp = []
    source = open(branchPath, "r")
    for line in source:
        if line in ['\n', '\r\n']: # blank line
            if ( (len(key) != 0) and (len(tmp) != 0) ):
                b.append([key, tmp])
                key = ''
                tmp = []
        else: # line not empty
            if t_p in line:
                aaa = line.split(' ')
                bbb = []
                for elem in aaa:
                    if elem != '':
                        bbb.append(elem)
                line = bbb[0].split('/')[1].replace(t_p, '')
                name = line.split(' ')[0]
                tmp.append([name, bbb[3]]) 
            else:
                key = line
    source.close()
    return b

def cleanBranches(branches):
    #if (branches[i] == 'h_ele_seedMask_Tec'): # temp (pbm with nan)
    #if re.search('OfflineV', branches[i]): # temp (pbm with nbins=81 vs nbins=80)
    toBeRemoved = ['h_ele_seedMask_Tec'] # , 'h_ele_convRadius', 'h_ele_PoPtrue_golden_barrel', 'h_ele_PoPtrue_showering_barrel'
    for ele in toBeRemoved:
        if ele in branches:
            branches.remove(ele)

def reduceBranch(branch):
    shn = branch.replace("h_", "").replace("ele_", "").replace("scl_", "").replace("bcl_", "")
    return shn

def optimizeBranches(tmp_branches):
    #tmp_branches = np.asarray(tmp_branches)
    nb_branches = len(tmp_branches)
    print('nb branches : %d' % nb_branches)
    t0 = tmp_branches[0]
    print(t0)
    for i in range(1,nb_branches):
        #print(i)
        t1 = tmp_branches[i]
        for item in t0:
            if (t1.count(item) == 0):
                print('%s not in t1' % item)
                t0.remove(item)
        print('{:d} : '.format(i), t0)
    print(len(t0))
    return t0

def change_nbFiles(nbFiles_computed, nbFiles):
    if (nbFiles_computed != nbFiles):
        print('the number of computed files (' + '{:d}'.format(nbFiles_computed) + ') is different from the pre supposed number (' + '{:d}'.format(nbFiles) + ').')
        print('switching to the computed number ({:d}).'.format(nbFiles_computed))
        return nbFiles_computed
    else:
        return nbFiles