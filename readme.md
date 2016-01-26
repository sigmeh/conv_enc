`e.py` is a stripped-down python sub/perm network encryptor invoked with a single command. 

A bash function `e` calls the script. The following is placed in .bashrc (if e.py is located in the home directory):

e () {
	python $HOME/e.py $@
}

e.py takes two and only two arguments: action and filename. 

A properly formulated invocation is as follows:

	$ e e filename
	
		*or*
	
	$ e d filename

The first `e` invokes the bash function and calls the python script. 

The second character ('e' or 'd') facilitates encryption or decryption, respectively. 

The script prompts for a password. 

The document is encrypted/decrypted and saved (temporarily). 

The option to continue allows replacement of the original file with the new file, deleting the "temporary" new file
(and effectively removing the original file).

If aborting the process, the name of the newly created file is displayed. Neither file is deleted. 