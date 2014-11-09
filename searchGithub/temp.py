from requests import *
from urllib2 import *
import json
from StringIO import *


def searchGithub(keyword, maxsize, minsize, language, sortby, orderby):
    # keyword: search keyword
    # maxsize: maximum size of repository
    # minsize: minimum size of repository
    # language: main language of repository
    # sortby: what you want to sort repos by (stars /forks / updated)
    # orderby: order sort by ascending or descending (asc/desc)
    if language != "java" and language != "python" and language != "ruby" and language != "c":
        #Check language is valid
        return False
    #create search url
    start = 'https://api.github.com/search/repositories?'
    search_keyword = "q="+keyword
    search_languange = 'language:'+language
    sort = "sort="+sortby
    order = "order="+orderby
    size= "size:"+str(minsize) +".."+str(maxsize)
    search_string = start + search_keyword + "+"+ search_languange + "&" + sort + "&" + order + "&"+ size
    print search_string
    # return dictionary of results from search inquiry
    return json.load(StringIO(urlopen(Request(search_string)).read()))

def searchRepoForJunitTests(repo,language):
    # search repository (given by repo) for junit tests
    start = "https://api.github.com/search/code"
    keyword = "?q=junit"
    language_search = "language:"+language
    repo_search = "+repo:"+repo
    search_string = start + keyword + "+in:file+" + language_search + repo_search
    print search_string
    return json.load(StringIO(urlopen(Request(search_string)).read()))

def run_search():
    # search Github for java projects with keyword test
    search_dico = searchGithub("test",30000,0, "java", "stars", "desc")
    # store repository's which use junit
    repository_storage = []
    search_counter = 0
    while len(repository_storage) < 20:
        # search through found repository's and see if they contain files which contain junit
        # If they do store to repository_storage
        repo_name= search_dico["items"][search_counter]["full_name"]
        if searchRepoForJunitTests(repo_name, "java")["total_count"] > 0:
            repository_storage += [search_dico["items"][search_counter]]
        search_counter +=1
    for i in repository_storage:
        print i


## testing things
#code_search_dico = searchRepoForJunitTests("Rory1994/WAW-Assessment4", "java")
run_search()

#notes
# dictionary contains total_count items incomplete_results