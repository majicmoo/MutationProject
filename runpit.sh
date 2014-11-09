#java -cp /c/Users/Megan/Documents/MutationProject/pitjars/*:/c/Users/Megan/workspace/testProject/jar/junit.jar:/c/Users/Megan/workspace/testProject/src:. \
#org.pitest.mutationtest.commandline.MutationCoverageReport \
#--reportDir /c/Users/Megan/Documents/MutationProject/mutationreports \
#--sourceDirs /c/Users/Megan/workspace/testProject/src \
#--targetClasses Temp \
#--targetTests TempTest


#run waw

echo "compile waw"
javac -cp /c/Users/Megan/Documents/MutationProject/jumblejars/*:/c/Users/Megan/Documents/WAW-Assessment4/Game/lib/jars/*:/c/Users/Megan/Documents/WAW-Assessment4/Game/src:/c/Users/Megan/Documents/WAW-Assessment4/Game/lib/natives:. -d /c/Users/Megan/Documents/WAW-Assessment4/Game/src /c/Users/Megan/Documents/WAW-Assessment4/Game/src/stateContainer/Game.java

echo "compile tests"
javac -cp /c/Users/Megan/Documents/MutationProject/jumblejars/*:/c/Users/Megan/Documents/WAW-Assessment4/Game/lib/jars/*:/c/Users/Megan/Documents/WAW-Assessment4/Game/src:/c/Users/Megan/Documents/WAW-Assessment4/Game/lib/natives:. -d /c/Users/Megan/Documents/WAW-Assessment4/Game/src /c/Users/Megan/Documents/WAW-Assessment4/Game/src/unitTests/*.java

#echo "run waw"
#java -Djava.library.path="/c/Users/Megan/Documents/WAW-Assessment4/Game/lib/natives" -cp /c/Users/Megan/Documents/MutationProject/jumblejars/*:/c/Users/Megan/Documents/WAW-Assessment4/Game/lib/jars/*:/c/Users/Megan/Documents/WAW-Assessment4/Game/src:/c/Users/Megan/Documents/WAW-Assessment4/Game/lib/natives:. stateContainer.Game


echo "run pit"
java -Djava.library.path="/c/Users/Megan/Documents/WAW-Assessment4/Game/lib/natives" -cp /c/Users/Megan/Documents/MutationProject/jumblejars/*:/c/Users/Megan/Documents/WAW-Assessment4/Game/lib/jars/*:/c/Users/Megan/Documents/WAW-Assessment4/Game/src:/c/Users/Megan/Documents/WAW-Assessment4/Game/lib/natives:/c/Users/Megan/workspace/testProject/jar/junit.jar:. \  
org.pitest.mutationtest.commandline.MutationCoverageReport \
--reportDir /c/Users/Megan/Documents/MutationProject/mutationreports \
--sourceDirs /c/Users/Megan/Documents/WAW-Assessment4/Game/src \
--targetClasses competitve.*, coop.*, events.*, logicClasses.*, res.*, stateContainer.*, states.*, util.* \
--targetTests unitTests.*