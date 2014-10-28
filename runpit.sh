java -cp Documents/pitjars/*:Documents/WAW-Assessment4/Game/lib/jars/*:. \
org.pitest.mutationtest.commandline.MutationCoverageReport \
--reportDir Documents/mutationreports \
--targetClasses competitve.*, coop.*, events.*, logicClasses.*, res.*, stateContainer.*, states.*, util.* \
--targetTests unitTests.*
--sourceDirs Documents/WAW-Assessment4/Game/src/
