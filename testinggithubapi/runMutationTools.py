import os
import subprocess
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
        #pass

    def run_mvn(self):
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

    def setup_repo(self):
        # Clone repo
        self.clone_repo()
        # Find classpath
        # self.find_classpath()
        # # Find main
        # self.find_main()
        # # Compile tests and program
        # self.project.classpath += ":" + str(test_jars)
        # self.compile_repo()

