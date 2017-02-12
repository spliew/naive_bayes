#!/bin/sh
mkdir gunosyInText
for class in `seq 1 8`
do
	sqlite3 database.db "SELECT REPLACE(title, char(10), '') AS title, REPLACE(content, char(10), '') AS content FROM NEWS WHERE category=$class" > .tmp.txt
	nkf --ic=UTF-8 --oc=EUC-JP .tmp.txt > $class.txt
	mv $class.txt gunosyInText
done
