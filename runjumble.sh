#Compile on Linux
#javac -cp Documents/MutationProject/jumblejars/*:Documents/WAW-Assessment4/Game/lib/jars/*:Documents/WAW-Assessment4/Game/src:Documents/WAW-Assessment4/Game/lib/natives:. -d Documents/WAW-Assessment4/Game/src Documents/WAW-Assessment4/Game/src/stateContainer/Game.java 

#Run Game on Linux
#java -Djava.library.path="Documents/WAW-Assessment4/Game/lib/natives" -cp .:Documents/WAW-Assessment4/Game/lib/jars/*:Documents/WAW-Assessment4/Game/src stateContainer.Game

#Mutation test on Linux
#java -jar Documents/MutationProject/jumblejars/* --classpath=. "Documents/WAW-Assessment4/Game/lib/jars/*:Documents/WAW-Assessment4/Game/src:Documents/WAW-Assessment4/Game/lib/natives/*:."

#Run Game on Windows
#java -Djava.library.path="Documents/WAW-Assessment4/Game/lib/natives" -cp .:Documents/WAW-Assessment4/Game/lib/jars/*:Documents/WAW-Assessment4/Game/bin:Documents/WAW-Assessment4/Game/src stateContainer.Game

#Compile tempProject on Windows
echo "compiling main"
javac -cp .:/c/Users/Megan/workspace/testProject/jar/junit.jar:/c/Users/Megan/workspace/testProject/src:/c/Users/Megan/Documents/MutationProject/jumblejars/* -sourcepath /c/Users/Megan/workspace/testProject/src /c/Users/Megan/workspace/testProject/src/Temp.java

echo "compiling tests"
javac -cp .:/c/Users/Megan/workspace/testProject/jar/junit.jar:/c/Users/Megan/workspace/testProject/src:/c/Users/Megan/Documents/MutationProject/jumblejars/*  -sourcepath /c/Users/Megan/workspace/testProject/src/ /c/Users/Megan/workspace/testProject/src/TempTest.java  -verbose

echo " "
#Run tempProject on Windows -Linux cmd
echo "running main"
java -cp /c/Users/Megan/workspace/testProject src.Temp

#echo "running tests"
#java -cp ./workspace/testProject/src tempProjectTest.Temp_Test

#Mutation test on Windows
echo " "
echo "jumble"
java -jar /c/Users/Megan/Documents/MutationProject/jumblejars/* --classpath=. src/Temp
