cd /d %~dp0
Start /B "CobaltStrike4.5" "../../env/jdk11/bin/javaw.exe" "-Dfile.encoding=UTF-8" "-XX:ParallelGCThreads=4" "-XX:+AggressiveHeap" "-XX:+UseParallelGC" "-javaagent:patch.jar" "-javaagent:CSAgent.jar=CSAgent.properties" "-Duser.language=en" "-jar" "cobaltstrike.jar"

