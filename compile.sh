#!/bin/sh
if [ ! -d $1 ]
then
    echo "Problem directory does not exist"
    return 0
fi
PREVWD=$PWD
cln $1
if [ ! -d dist ]
then
    mkdir dist
fi
g++ $1/$1.cpp -o dist/$1 -Wall
if [ $? != 0 ]
then
    return 1
fi
cd $1
sudo $PREVWD/dist/$1
if [ -f $1.out ]
then
    cat $1.out
    code -r $1.out
fi
cd $PREVWD