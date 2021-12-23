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

import sys
import re
from authentication import *

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

class networkFunctions:
    def __init__(self):
        self.toto = "network class"

    def list_search_0(self):

        # on fera la fonction par un appel a cmd_fetchall(options)
        # ou options regroupera option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run

        ## Define options
        option_is_from_data = "mc" # mc ou data
        option_regexp = '_RelValTTbar_13' # str( self.lineedit4.text() ) to be removed
        option_mthreads = 3
        option_dry_run = True # False for loading files

        option_regexp = ''
        (liste_releases_0) = self.cmd_fetch_0(option_is_from_data, option_regexp, option_mthreads, option_dry_run)

        temp_0 = []
        for item in liste_releases_0:
            # find if some elements are empty or not. if no -> append
            tt = self.list_search_1(item[0:-1])
            if (len(tt) > 0):
                temp_0.append(item[0:-1])

        return temp_0

    def list_search_1(self, my_choice_0):

        # on fera la fonction par un appel a cmd_fetchall(options)
        # ou options regroupera option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run

        ## Define options
        option_is_from_data = "mc" # mc ou data
        option_release = str( my_choice_0 )
        option_dry_run = True # False for loading files

        option_regexp = ''
        (liste_releases_1) = self.cmd_fetch_1(option_is_from_data, option_release, option_regexp, option_dry_run)

        temp_1 = []
        if ( len(liste_releases_1) > 0 ):
            for item in liste_releases_1:
                temp_1.append(item)

        return temp_1

    def list_search(self): # used with Projet_CheckRootFiles/
        # on fera la fonction par un appel a cmd_fetchall(options)
        # ou options regroupera option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run

        ## Define options
        option_is_from_data = "mc" # mc ou data
        option_release_1 = str(self.lineedit1.text()) # self.cmsenv.getCMSSWBASECMSSWVERSION()
        option_regexp = '_RelValTTbar_13' # str( self.lineedit4.text() ) to be removed
        option_mthreads = 3
        option_dry_run = True # False for loading files
        self.gccs = 'Full' # 'Fast' 'PU'

        # get collections list to do (Pt35, Pt10, TTbar, .... if checked)

        self.rel_list = []

        for items in self.coll_list:
            print("ITEMS : ", items)
            option_regexp = str( items ) + '__'
            if ( self.gccs != 'Full' ):
                option_regexp += ',' + str(self.gccs)
            (liste_fichiers_1) = cmd_fetch(option_is_from_data, option_release_1, option_regexp, option_mthreads, option_dry_run)
            self.rel_list += liste_fichiers_1

        return

    def cmd_fetch_0(self, option_is_from_data, option_regexp, option_mthreads, option_dry_run):

        ## Define options
        # option_is_from_data = "mc"
        # option_regexp = 'TTbar,PU,25'
        # option_mthreads = 3
        # option_dry_run = True

        try:
            from authentication import X509CertOpen
        except ImportError:
            from authentication import X509CertOpen

        def auth_wget(url, chunk_size=1048576):
            from os.path import basename, isfile
            """Returns the content of specified URL, which requires authentication.
            If the content is bigger than 1MB, then save it to file.
            """
            opener = build_opener(X509CertOpen())
            url_file = opener.open(Request(url))
            size = int(url_file.headers["Content-Length"])

            if size < 1048576:   # if File size < 1MB
                filename = basename(url)    #still download
                readed = url_file.read()    ## and then check if its not an empty dir (parent directory)
                if filename != '':
                    outfile = open(filename, 'wb')  #then write File to local system
                    outfile.write(readed)
                return readed

            filename = basename(url)
            #file_id = selected_files.index(filename)

            if isfile("./%s" % filename):
                return

            file = open(filename, 'wb')
            chunk = url_file.read(chunk_size)
            while chunk:
                file.write(chunk)
                chunk = url_file.read(chunk_size)
            file.close()

        ## Use options
        relvaldir = "RelVal"
        if option_is_from_data == 'data':
            relvaldir = "RelValData"
        base_url = 'https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/'
        filedir_url = base_url + relvaldir + '/' # + releasedir + '/'
        filedir_html = auth_wget(filedir_url)

        file_list_re = re.compile(r"<a href='[-./\w]*'>([-./\w]*)<")
        all_files = file_list_re.findall( filedir_html.decode('utf-8') )[1:]  # list of file names

        ### Fetch the files, using multi-processing
        file_res = [re.compile(r) for r in option_regexp.split(',') ]

        selected_files = [f for f in all_files if all([r.search(f) for r in file_res])]

        if option_dry_run:
            return selected_files

        return

    def cmd_fetch_1(self, option_is_from_data, option_release, option_regexp, option_dry_run):
        #from urllib2 import build_opener, Request

        ## Define options
        # option_is_from_data = "mc"
        # option_regexp = 'TTbar,PU,25'
        # option_mthreads = 3
        # option_dry_run = True

        try:
            from Utilities.RelMon.authentication import X509CertOpen
        except ImportError:
            from authentication import X509CertOpen

        def auth_wget(url, chunk_size=2097152):
            from os.path import basename #, isfile
            """Returns the content of specified URL, which requires authentication.
            If the content is bigger than 1MB, then save it to file.
            """
            # NOTE 2097152 instead of 1048576 is needed because CMSSW_7_1_X > 1 MB
            opener = build_opener(X509CertOpen())
            url_file = opener.open(Request(url))
            size = int(url_file.headers["Content-Length"])

            if size < 2097152:   # if File size < 2MB
                filename = basename(url)    #still download
                readed = url_file.read()    ## and then check if its not an empty dir (parent directory)
                if filename != '':
                    outfile = open(filename, 'wb')  #then write File to local system
                    outfile.write(readed)
                return readed

            filename = basename(url)
            #file_id = selected_files.index(filename)

            file = open(filename, 'wb')
            chunk = url_file.read(chunk_size)
            while chunk:
                file.write(chunk)
                chunk = url_file.read(chunk_size)
            file.close()

        ## Use options
        relvaldir = "RelVal"
        if option_is_from_data == 'data':
            relvaldir = "RelValData"

        releasedir = option_release
        base_url = 'https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/'
        filedir_url = base_url + relvaldir + '/'  + releasedir + '/'
        filedir_html = auth_wget(filedir_url)

        file_list_re = re.compile(r"<a href='[-./\w]*'>([-./\w]*)<")
        all_files = file_list_re.findall( filedir_html.decode('utf-8') )[1:]  # list of file names

        ### Fetch the files, using multi-processing
        file_res = [re.compile(r) for r in option_regexp.split(',') ]

        selected_files = [f for f in all_files if all([r.search(f) for r in file_res])]

        if option_dry_run:
            return selected_files

        return

    def cmd_fetch(self, option_is_from_data, option_release, option_regexp, option_mthreads, option_dry_run): # used with Projet_CheckRootFiles/

        ## Define options
        # option_is_from_data = "mc" # mc ou data
        # option_regexp = 'TTbar,PU,25'
        # option_mthreads = 3
        # option_dry_run = True

        try:
            from Utilities.RelMon.authentication import X509CertOpen
        except ImportError:
            from authentication import X509CertOpen

        def auth_wget(url, chunk_size=1048576):
            """Returns the content of specified URL, which requires authentication.
            If the content is bigger than 1MB, then save it to file.
            """
            opener = build_opener(X509CertOpen())
            url_file = opener.open(Request(url))
            size = int(url_file.headers["Content-Length"])

            if size < 1048576:   # if File size < 1MB
                filename = basename(url)    #still download
                readed = url_file.read()    ## and then check if its not an empty dir (parent directory)
                if filename != '':
                    outfile = open(filename, 'wb')  #then write File to local system
                    outfile.write(readed)
                return readed

            filename = basename(url)
            file_id = selected_files.index(filename)

            if isfile("./%s" % filename):
                print('%d. Exists on disk. Skipping.' % (file_id +1))
                return

            print('%d. Downloading...' % (file_id +1))
            file = open(filename, 'wb')
            # progress = 0
            chunk = url_file.read(chunk_size)
            while chunk:
                file.write(chunk)
                # progress += chunk_size
                chunk = url_file.read(chunk_size)
            print('%d.  Done.' % (file_id +1))
            file.close()

        ## Use options
        relvaldir = "RelVal"
        if option_is_from_data == 'data':
            relvaldir = "RelValData"
        print("relvaldir : ", relvaldir)
        release = re.findall('(CMSSW_\d*_\d*_)\d*(?:_[\w\d]*)?', option_release)
        if not release:
            parser.error('No such CMSSW release found. Please check the ``--release`` commandline option value.')
        releasedir = release[0] + "x"
        base_url = 'https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/'
        filedir_url = base_url + relvaldir + '/' + releasedir + '/'
        filedir_html = auth_wget(filedir_url)

        file_list_re = re.compile(r"<a href='[-./\w]*'>([-./\w]*)<")
        all_files = file_list_re.findall(filedir_html)[1:]  # list of file names

        ### Fetch the files, using multi-processing
        print("cmd_fetch : ", option_regexp.split(',') + [option_release])
        file_res = [re.compile(r) for r in option_regexp.split(',') + [option_release]]

        selected_files = [f for f in all_files if all([r.search(f) for r in file_res])]

        print('Downloading files:')
        for i, name in enumerate(selected_files):
            print('%d. %s' % (i+1, name))

        if option_dry_run:
            print("done")
            return selected_files

        return

    def cmd_load_files(self, files_array, folder):

        ## Define options
        option_mthreads = 1 # 2
        print('cmd_load_files : %d thread(s)' % option_mthreads)
        print(folder)
        ## Use options
        relvaldir = 'RelVal'

        base_url = 'https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/'
        filedir_url = base_url + relvaldir + '/' + folder + '/'

        self.cmd_fetch_2(option_mthreads, filedir_url, files_array)

        return

    def cmd_fetch_2(self, option_mthreads, filedir_url, selectedFilesList):
        #import re, sys, os

        from multiprocessing import Pool # , Queue, Process
        #from Queue import Empty
        #from os.path import basename, isfile
        #from optparse import OptionParser
        #from urllib2 import build_opener, Request

        try:
            from Utilities.RelMon.authentication import X509CertOpen
        except ImportError:
            from authentication import X509CertOpen

        def auth_wget2(url, chunk_size=2097152):
            from os.path import basename, isfile
            from optparse import OptionParser
            """Returns the content of specified URL, which requires authentication.
            If the content is bigger than 1MB, then save it to file.
            """

            opener = build_opener(X509CertOpen())
            url_file = opener.open(Request(url))
            filename = basename(url)

            if isfile("./%s" % filename):
                print('%s. Exists on disk. Skipping.' % (filename))
                return
            file = open(filename, 'wb')
            chunk = url_file.read(chunk_size)
            while chunk:
                file.write(chunk)
                chunk = url_file.read(chunk_size)
            print('\rDownloaded: %s  ' % (filename,))
            file.close()

        ## Use options
        for i, name in enumerate(selectedFilesList):
            print('%d. %s' % (i+1, name))
            auth_wget2(filedir_url + name)

        #pool = Pool(option_mthreads)
        #pool.map(auth_wget2, [filedir_url + name for name in selectedFilesList])

        #pool.terminate()
        #pool.join()

        return

