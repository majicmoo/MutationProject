import os
import subprocess
import glob
from project import Project

class RunMutationTools(object):

    def __init__(self):
        self.project = None
        self.path_cloned_repos = None


    def clone_repo(self):
        #clone repo
        #subprocess.call("git clone "+self.project.clone, shell=True)
        pass

    def find_classpath(self):
        #find classpath
        for root, dirnames, files in os.walk(os.getcwd() + "/" + self.project.name):
            for i in dirnames:
                if self.is_src(i):
                    self.project.src = root + "/"+ i
                    # "DEBUG: src is", self.project.src
            for fname in files:
                if fname == ".classpath":
                    print "DEBUG:" , fname, "is classpath"
                    self.project.classpath = os.path.join(root,fname)
        if self.project.classpath == "":
            # find src, libs, jars
            print "DEBUG: Classpath not found"

    def find_jars(self):
        pass

    def find_main(self):
        for root, dirnames, files in os.walk(os.getcwd() + "/" + self.project.name):
            for fname in files:
                if self.is_java(fname):
                    if self.is_main(root,fname):
                        print "DEBUG: main class found:", fname
                        self.project.main = fname
        print "DEBUG: Main is", self.project.main

    def is_main(self, root, fname):
        #print str(root)+"/" +"/"+ fname
        #print "DEBUG: Reading:", root,fname
        f = open(root+"/"+ fname, 'r')
        for i in f.readlines():
            #print "DEBUG: "+ fname + " line:" + i
            #if "main" in i:
            #    print i
            if "public static void main" in i:
                f.close()
                return True
        f.close()
        return False

    def is_java(self, fname):
        # Return true if file ends with .java
        f = fname.split(".")
        if f[-1] == "java":
            print fname
            return True

    def is_src(self, directory):
        if directory == "src":
            return True

    def compile_repo(self):
        #compilie repository
        subprocess.call("javac -cp " + self.project.classpath + self.project.main, shell=True)
        #compitle tests
        subprocess.call("java -cp " + self.project.classpath + self.project.main, shell=True)

    def setup_repo(self, test_jars):
        # Clone repo
        print "DEBUG: Cloning", self.project.name ,"into", self.path_cloned_repos
        self.clone_repo()
        # Find classpath
        self.find_classpath()
        # Find main
        self.find_main()
        # Compile tests and program
        self.project.classpath += ":" + str(test_jars)
        self.compile_repo()

    def run_jumble(self, project, path_cloned_repos):
        self.project = project
        self.path_cloned_repos = path_cloned_repos
        jumble_jar_path ="C:\Users\Megan\Documents\MutationProject\jumblejars\*"
        self.setup_repo(jumble_jar_path)
        #run jumble on project
        subprocess.call("java -jar "+self.project.pclasspath+self.project.main, shell=True)

    def run_pit(self, project, path_cloned_repos):
        self.project = project
        self.path_cloned_repos = path_cloned_repos
        pit_jar_path = ""
        mutation_reports = ""
        target_classes = ""
        tests = ""
        self.setup_repo(pit_jar_path)
        subprocess.call("java -cp "+ self.project.classpath +
                        "\ org.pitest.mutationtest.commandline.MutationCoverageReport \ "
                        "--reportDir " + mutation_reports + " \ --sourceDirs" + self.project.src +
                        " \ --targetClasses " + target_classes + "--targetTests " + tests, shell=True)

    def run_mujava(self, repo_url, repo_name, path_cloned_repos):
        classpath, main = self.setup_repo(self, repo_url, repo_name, path_cloned_repos)

