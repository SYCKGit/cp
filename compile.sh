#!/bin/sh
if [ ! -d $1 ]
then
    echo "Problem directory does not exist"
    return 0
fi
PREVWD=$PWD
cln $1
if [ ! -d zdist ]
then
    mkdir zdist
fi
g++ $1/$1.cpp -o zdist/$1 -Wall ${@:2}
if [ $? != 0 ]
then
    return 1
fi
cd $1
trap "cd $PREVWD" SIGINT
sudo $PREVWD/zdist/$1 < $1.in > $1.out
if [ -f $1.out ]
then
    cat $1.out
    code -r $1.out
fi
cd $PREVWD