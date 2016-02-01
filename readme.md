`conv_enc.py` is a stripped-down python (2.7) sub/perm network encryptor invoked with a single command. 

A bash function `e` calls the script. The following is placed in .bashrc (if conv_enc.py is located in the home directory):

e () {
	python $HOME/conv_enc.py $@
}

conv_enc.py takes two and only two arguments: action and filename. 

A properly formulated invocation is as follows:

	$ e e filename
	
		*or*
	
	$ e d filename

The first `e` invokes the bash function and calls the python script. 

The second character ('e' or 'd') facilitates encryption or decryption, respectively. 

Without the bash function, the script is run from its location as:
	
	$ python conv_enc.py e filename

The script prompts for a password.   

For encryption, file contents are serialized, encrypted, and saved as a dictionary whose key is the file name. 
The original file name and extension are thus encoded into the file, and will facilitate opening the file with the appropriate program at a later date. 

For decryption, the reverse sub/perm network is executed, resulting in a json-encoded document that will be opened from a 
subprocess call in the default application for opening files of that type. Without an extension on the original file, that file may not be opened properly. 

After opening the decrypted file, the shell process waits for a command to remove the new file (or not). 