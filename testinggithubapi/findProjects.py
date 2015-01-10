from requests import *
import urllib2
from urllib2 import *
import json
from StringIO import *
from project import Project
from runMutationTools import RunMutationTools
import time
from retrying import retry
import requests
from urlparse import urljoin

class FindProjects(object):

    def __init__(self):
        # languages accepted
        self.languages = ["python", "java", "ruby", "c"]
        self.count_github_access = 0

    def searchGithub(self, keyword, maxsize, minsize, language, sortby, orderby):
        # keyword: search keyword
        # maxsize: maximum size of repository
        # minsize: minimum size of repository
        # language: main language of repository
        # sortby: what you want to sort repos by (stars /forks / updated)
        # orderby: order sort by ascending or descending (asc/desc)

        if language not in self.languages:
            #Check language is valid
            print "DEBUG: language", language, "is not valid"
            return False

        #create search url
        start = 'https://api.github.com/search/repositories?'
        search_keyword = "q="+keyword
        search_language = 'language:'+language
        sort = "sort="+sortby
        order = "order="+orderby
        size= "size:"+str(minsize) +".."+str(maxsize)

        #Search for projects
        search_string = start + search_keyword + "+" + size + "+" + search_language + "&" + sort + "&" + order


        # store dictionary of results from search inquiry
        while True:
            try:
                print "DEBUG: Requesting", search_string
                search_dico = json.load(StringIO(urlopen(Request(search_string)).read()))
                break
            except urllib2.HTTPError:
                print "DEBUG: sleep 30"
                time.sleep(30)

        # search through found repository's and see if they contain files which contain junit
        # If they do store to repository_storage
        repository_storage = []
        search_counter = 0
        print len(search_dico["items"])
        while len(repository_storage) < 10:
            try:
                print search_counter
                repo_name= search_dico["items"][search_counter]["full_name"]
                #search_for_junit = self.searchRepoForJunitTests(repo_name, "java")["total_count"]
                #if search_for_junit < 40 and search_for_junit > 0:
                #    repository_storage.append(Project(search_dico["items"][search_counter]))

                search_for_mvn = self.search_for_mvn(repo_name)["total_count"]
                if search_for_mvn == 2:
                    repository_storage.append(Project(search_dico["items"][search_counter]))

                search_counter +=1
            except:
                pass
        return repository_storage

    def searchRepoForJunitTests(self, repo, language):
        # search repository (given by repo) for junit tests
        start = "https://api.github.com/search/code"
        keyword = "?q=junit"
        language_search = "language:"+language
        repo_search = "+repo:"+repo
        search_string = start + keyword + "+in:file+" + language_search + repo_search

        while True:
            try:
                print "DEBUG: Requesting" ,search_string
                temp = json.load(StringIO(urlopen(Request(search_string)).read()))
                print temp
                return temp
            except urllib2.HTTPError:
                print "DEBUG sleep:", 30, "seconds"
                time.sleep(30)
                continue


       # print "DEBUG: Requesting" ,search_string
        #return json.load(StringIO(urlopen(Request(search_string)).read()))
        '''
        temp=  self.retrySearch(search_string)
        print temp
        return temp'''

    def search_for_mvn(selfself, repo,):
        start = "https://api.github.com/search/code?q=project+"
        filename = "filename:pom.xml"
        repo_search = "+repo:"+repo
        search_string=start+filename+repo_search

        while True:
            try:
                print "DEBUG: Requesting" ,search_string
                temp = json.load(StringIO(urlopen(Request(search_string)).read()))
                print temp
                return temp
            except urllib2.HTTPError:
                print "DEBUG sleep:", 30, "seconds"
                time.sleep(30)
                continue




    def retry_if_result_none(self, result):
        return result is None

    @retry(retry_on_result=retry_if_result_none)
    def retrySearch(self, search_string):
        print 'trying'
        try:
            print "DEBUG: Requesting" ,search_string
            temp = json.load(StringIO(urlopen(Request(search_string)).read()))
            print temp
            return temp
        except urllib2.HTTPError:
            print "DEBUG sleep:", 30, "seconds"
            time.sleep(30)

## testing things
#code_search_dico = searchRepoForJunitTests("Rory1994/WAW-Assessment4", "java")
findProjects = FindProjects()
temp_repo = findProjects.searchGithub("",10000,0, "java", "forks", "desc")
a = RunMutationTools()
for i in temp_repo:
    print "Name:",i.name, i.url
    #a.run_jumble(i, "C:\Users\Megan\Documents\clonedRepos")
#print "temp", temp_repo





# Notes
# dictionary contains total_count items incomplete_results