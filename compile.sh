#!/bin/sh
if [ ! -d $1 ]
then
    echo "Problem directory does not exist"
    return 0
fi
PREVWD=$PWD
cln $1
g++ $1/$1.cpp -o $1/$1 -Wall
if [ $? != 0 ]
then
    return 1
fi
cd $1
sudo ./$1
if [ -f $1.out ]
then
    cat $1.out
fi
cd $PREVWD