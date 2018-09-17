
clear
#take arguments as start and end for loop iteration
start=$1
end=$2

#declare variables to use with loops
declare -i ii
declare -i st
declare -i en


for ((c=$start; c<=$end; c++))
do
ii=c+1
mv Hoeganaes$c.csv _Hoeganaes$ii.csv  #this adds one to the Heat number on the file name
done	


st=start+1
en=end+1


for ((cc=$st; cc<=$en; cc++))

do
mv _Hoeganaes$cc.csv Hoeganaes$cc.csv  #this is just to remove the _
done
