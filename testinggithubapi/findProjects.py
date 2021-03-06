GITHUB_API = 'https://api.github.com'
MAX_ITEMS = 30  # max number of items on each page in github
SLEEP_TIME = 60  # Time between API accesses when reached rate limit
ACCEPTED_STATUS_CODE = 200  # Status code of successful access to API
NUMBER_OF_MAVEN_FILES = 1  # How many maven files you wish to find
CLONED_REPOS_PATH = "C:\Users\Megan\Documents\MutationProject\\testinggithubapi\clonedrepos"
MAX_JUNIT_TESTS = 40
MIN_JUNIT_TESTS = 0

from project import Project
from runMutationTools import RunMutationTools
import time
from authenticate import Authenticate
import requests


class FindProjects(object):

    def __init__(self):
        # languages accepted
        self.languages = ["python", "java", "ruby", "c"]
        self.count_github_access = 0

    def search_github(self, keyword, maxsize, minsize, language, sortby,
                      orderby, number_of_projects, username, password):
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
        start = GITHUB_API + '/search/repositories?'
        search_keyword = "q=" + keyword
        search_language = 'language:' + language
        sort = "sort=" + sortby
        order = "order=" + orderby
        size = "size:" + str(minsize) + ".." + str(maxsize)
        pagination = 2
        #Search for projects
        search_string = start + search_keyword + "+" + size + "+" + search_language + "&" + sort + "&" + order
        # store dictionary of results from search inquiry
        while True:
            temp = requests.get(search_string, auth=(username, password))
            #print 'DEBUG: Status',temp.status_code
            if temp.status_code == ACCEPTED_STATUS_CODE:
                print "DEBUG: Requesting", search_string
                #search_dico = json.load(requests.get(search_string, auth=(username, password)).json())
                search_dico = temp.json()
                break
            else:
                print "DEBUG: sleep", SLEEP_TIME, "seconds"
                time.sleep(SLEEP_TIME)
                continue
        # search through found repository's and see if they contain files which contain junit
        # If they do store to repository_storage
        repository_storage = []
        search_counter = 0
        #print len(search_dico["items"])
        while len(repository_storage) < number_of_projects:
            print search_counter
            if search_counter >= MAX_ITEMS:
                #print "REACH MAX SEARCHS PAGE+1"
                while True:
                    temp = requests.get(search_string+'&page='+str(pagination), auth=(username, password))
                    #print 'DEBUG: Status',temp.status_code
                    if temp.status_code == ACCEPTED_STATUS_CODE:
                        search_dico = temp.json()
                        pagination += 1
                        search_counter = 0
                        break
                    else:
                        print "DEBUG sleep:", SLEEP_TIME, "seconds"
                        time.sleep(SLEEP_TIME)
                        continue
            #print search_counter
            repo_name = search_dico["items"][search_counter]["full_name"]

            search_for_mvn = self.search_for_mvn(repo_name, username, password)["total_count"]
            if search_for_mvn == NUMBER_OF_MAVEN_FILES:
                search_for_junit = self.search_repo_for_junit_tests(repo_name, "java",
                                                                    username, password)["total_count"]
                if search_for_junit < MAX_JUNIT_TESTS and search_for_junit > MIN_JUNIT_TESTS:
                    temp_project = Project(search_dico["items"][search_counter])
                    print "*******************************************"
                    if RunMutationTools(temp_project, CLONED_REPOS_PATH).setup_repo():
                        print "*******************************************"
                        repository_storage.append(temp_project)
            search_counter += 1
            #print "PAGE NUMBER:", pagination
            #print "ENDED ON:", search_string+'&page='+str(pagination)
        return repository_storage

    def search_repo_for_junit_tests(self, repo, language, username, password):
        # search repository (given by repo) for junit tests
        start = "https://api.github.com/search/code"
        keyword = "?q=junit"
        language_search = "language:"+language
        repo_search = "+repo:"+repo
        search_string = start + keyword + "+in:file+" + language_search + repo_search

        while True:
            print 'DEBUG: requesting', search_string
            temp = requests.get(search_string, auth=(username, password))
            #print 'status code', temp.status_code
            if temp.status_code == ACCEPTED_STATUS_CODE:
                return temp.json()
            else:
                print "DEBUG sleep:", SLEEP_TIME, "seconds"
                time.sleep(SLEEP_TIME)
                continue


    def search_for_mvn(self, repo, username, password):
        start = "https://api.github.com/search/code?q=project+"
        filename = "filename:.xml+pom"
        repo_search = "+repo:"+repo
        search_string = start + filename + repo_search

        while True:
            print 'DEBUG: requesting', search_string
            temp = requests.get(search_string, auth=(username, password))
            #print 'status code', temp.status_code
            if temp.status_code == ACCEPTED_STATUS_CODE:
                return temp.json()
            else:
                print "DEBUG sleep:", SLEEP_TIME, "seconds"
                time.sleep(SLEEP_TIME)
                continue

###############################################################################
test = Authenticate()
username, password = test.doAuthenticate()

## testing things
#code_search_dico = searchRepoForJunitTests("Rory1994/WAW-Assessment4", "java")
findProjects = FindProjects()
temp_repo = findProjects.search_github("", 10000, 0, "java", "forks", "desc", 6, username, password)
for i in temp_repo:
    print "Name:", i.name, i.url
    #RunMutationTools(i, CLONED_REPOS_PATH).setup_repo()
    #a.run_jumble(i, "C:\Users\Megan\Documents\clonedRepos")
#print "temp", temp_repo