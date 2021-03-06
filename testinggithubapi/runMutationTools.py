import os
import subprocess
import shutil
import stat  # needed for file stat


def rem_shut(*args):
    func, path, _ = args  # onerror returns a tuple containing function, path and     exception info
    os.chmod(path, stat.S_IWRITE)
    os.remove(path)


class RunMutationTools(object):

    def __init__(self, project, path_cloned_repos):
        self.project = project
        self.path_cloned_repos = path_cloned_repos

    def clone_repo(self):
        # create folder to clone into
        max_file_number = 0
        for files in os.walk(self.path_cloned_repos):
            temp = map(int, files[1])
            if len(temp) > 0:
                max_file_number = max(temp)
            break
        os.makedirs(self.path_cloned_repos+"\\"+str(max_file_number+1))
        print self.path_cloned_repos+"\\"+str(max_file_number+1)
        # clone repo
        print "DEBUG: Cloning", self.project.name, "into", self.path_cloned_repos+"\\"+str(max_file_number+1)
        subprocess.call("git clone "+self.project.clone+" "+self.path_cloned_repos+"\\"+str(max_file_number+1),
                        shell=True)
        return self.path_cloned_repos+"\\"+str(max_file_number+1)
        #pass

    # def remove_readonly(func, path, excinfo):
    #     os.chmod(path, stat.S_IWRITE)
    #     func(path)

    def run_mvn(self, current_file):
        pom = self.find_pom(current_file)
        print "DEBUG: Running tests for ", current_file
        print "mvn -f " + pom + " test"
        #checkoutput if mvn tests fail delete folder

        try:
            temp = subprocess.check_output("mvn -f " + pom + " test", shell=True)
            temp = temp.split("\n")
            num = '1234567890'
            tests_run, failures, errors, skipped = 0,0,0,0
            for i in temp:
                if "Tests run:" in i:
                    i=i.split(",")
                    tests_run, failures, errors, skipped = int("".join([c for c in i[0] if c in num])),\
                                                           int("".join([c for c in i[1] if c in num])),\
                                                           int("".join([c for c in i[2] if c in num])),\
                                                           int("".join([c for c in i[3] if c in num]))
            print "Tests run:", tests_run, "\n", "Failures:", failures, "\n", "Errors:", errors, "\n", \
                "Skipped:", skipped

            if tests_run == 0:
                print "DEBUG: No tests run"
                print "DEBUG: Deleting", current_file
                shutil.rmtree(current_file, onerror=rem_shut)

            if failures > 0:
                print "DEBUG: Test suite not green"
                print "DEBUG: Deleting", current_file
                shutil.rmtree(current_file, onerror=rem_shut)

            print "DEBUG: Test Successful"
            return True
        except subprocess.CalledProcessError:
            print "DEBUG: Test Failed"
            print "DEBUG: Deleting", current_file
            shutil.rmtree(current_file, onerror=rem_shut)
            return False

    def find_pom(self, current_file):
        print "DEBUG: Locating pom.xml"
        for root, dirnames, files in os.walk(current_file):
            for i in files:
                if i == 'pom.xml':
                    self.project.pom_location = root+"\\"+i
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
        print "*******************************************"
        return self.run_mvn(current_file)