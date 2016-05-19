# clone

## what is clone

	make same files in two dirs

## the difference between 'cp -r'

	'clone' is a selective 'cp -r' 

## how to run
	
	1. clone.py Clone [run the specified Clone file]
	2. clone.py [run the ./Clone file]

## Clone format
 
a demo

	\# this is a comments
	from_dir : /home/a    
	to_dir  : /home/b	\#clone from_dir to to_dir
	omit_dir :	[bak]	\#a list
	omit_file :	[test.py, @*.pyc$]	\#a list, @ indicate regular expression

