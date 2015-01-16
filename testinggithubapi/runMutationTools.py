import os
import subprocess
import shutil
import glob
from project import Project

class RunMutationTools(object):

    def __init__(self, project, path_cloned_repos):
        self.project = project
        self.path_cloned_repos = path_cloned_repos

    def clone_repo(self):
        # create folder to clone into
        max_file_number = 0
        for files in os.walk(self.path_cloned_repos):
            temp = map(int, files[1])
            if len(temp)>0:
                max_file_number = max(temp)
            break
        os.makedirs(self.path_cloned_repos+"\\"+str(max_file_number+1))
        print self.path_cloned_repos+"\\"+str(max_file_number+1)
        # clone repo
        print "DEBUG: Cloning", self.project.name ,"into", self.path_cloned_repos+"\\"+str(max_file_number+1)
        subprocess.call("git clone "+self.project.clone+" "+self.path_cloned_repos+"\\"+str(max_file_number+1), shell=True)
        return self.path_cloned_repos+"\\"+str(max_file_number+1)
        #pass

    def run_mvn(self, current_file):
        test_success = False
        pom = self.find_pom(current_file)
        print "DEBUG: Running tests for ", current_file
        print "mvn -f "+ pom +" test"
        #checkoutput if mvn tests fail delete folder

        try:
            subprocess.check_output("mvn -f "+pom +" test", shell=True)
            print "DEBUG: Test Successful"
            return True
        except subprocess.CalledProcessError:
            print "DEBUG: Test Failed"
            print "DEBUG: Deleting", current_file
            #shutil.rmtree(current_file)
            return False


    def find_pom(self, current_file):
        print "DEBUG: Locating pom.xml"
        for root, dirnames, files in os.walk(current_file):
            for i in files:
                if i == 'pom.xml':
                    return root+"\\"+i

    def run_pit(self, pom):
        # Run Pit
        # Add plugin to build plugins in pom

        # mvn -f pom org.pitest-maven:mutationCoverage
        pass

    def setup_repo(self):
        # Clone repo
        current_file = self.clone_repo()
        # run tests
        return self.run_mvn(current_file)

