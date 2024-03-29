source ~/.bash_aliases
if [ -d $1 ] && [[ $2 != "-f" ]]
then
    echo "Directory already exists"
else
    if [ -d $1 ]
    then
        cln $1
        rm $1/$1.in
    else
        mkdir $1
    fi
    touch $1/$1.in
    python3 make.py $@
    code -r $1/$1.cpp
    code -r $1/$1.in
fi