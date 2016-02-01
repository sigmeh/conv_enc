#!/usr/bin/env python
# -*- coding: utf-8 -*-
#	For conv_enc.py in $HOME, and function `e` in .bashrc as:
#		e () {python $HOME/conv_enc.py $@} 
#	formulate shell commands as:
#			$ e e filename
#			$ e d filename
#			to encrypt/decrypt respectively
import sys,os,getpass,random,subprocess,math,json
def sub_zero(sub_num):
	sub_zero = list('0123456789')	
	for i in range(len(sub_num)):	#iteratively substitute zeroes for values in sub_zero to prevent large numbers of zeroes appearing together
		if sub_num[i] == '0':
			sub_num[i] = sub_zero[i%len(sub_zero)]
	return ''.join(sub_num)
def sub_doc(doc,sub,pw,pw_num,action):#generate substituted doc based on sub list
	if sub == 's2':
		pw_num = sorted(pw_num)
	sub = [x for x in ''.join([str(pw_num[i]**pw_num[i+1]) for i in range(len(pw)-1)])]	#generate long digit list from password
	sub = sub_zero(sub)	#reduce number of zeros and obfuscate
	sub = [int(sub[i:i+3]) for i in range(len(sub)) if len(sub[i:i+3])==3]	#generate list of 3-digit numbers by slicing sub11	
	doc = ''.join([unichr(ord(doc[i])^sub[i%len(sub)]) for i in range(len(doc))])
	return doc
def perm_doc(doc,perm,pw,pw_num,action):		#generate permuted doc based on perm list
	if perm == 'p1':
		set_size = len(doc)/100; num_set_sizes = 1; bs = 100
	elif perm == 'p2':
		set_size = 100; num_set_sizes = len(doc)/set_size; bs = 1
	iter = float(sum(pw_num[:len(pw)/2]))/sum(pw_num[len(pw)/2:]) 	#generate iterator
	if iter < 1: iter = 1/iter			#make iter > 1
	iter = int(iter*100)/100.			#round to two decimal places
	n = iter; map = []; new_doc = ''
	while len(map) < set_size:
		digit = int(set_size/2.*(1.+math.sin(n)))	#generate map values until map is filled
		if digit not in map:						#add unique values to map
			map.append(digit)
		n+=iter
	if action == 'e':
		for i in range(num_set_sizes):		
			for j in range(len(map)):
				new_doc += doc[i*set_size+map[j]*bs:i*set_size+map[j]*bs+bs]
	elif action == 'd':
		new_set = ['']*set_size			
		for i in range(num_set_sizes):
			for j in range(len(map)):
				new_set[map[j]] = doc[i*set_size+j*bs:i*set_size+j*bs+bs]
			new_doc += ''.join(new_set)
	return new_doc
def sub_perm(actions,doc,pw,pw_num,action):	#orchestrate sub/perm pathway navigation
	for i in actions:
		if i[0] == 's':
			doc = sub_doc(doc,i,pw,pw_num,action)	#substitution
		elif i[0] == 'p':
			doc = perm_doc(doc,i,pw,pw_num,action)	#permutation
	return doc
def get_file(action,file):		#open file 	
	with open(file,'r') as f:
		if action == 'e':	#encrypt
			return json.dumps({file:f.read()},encoding='latin1')
		else:				#decrypt
			return f.read().decode('utf8')
def quit():
	print; print 'Exiting...';print;sys.exit()
def main():
	print;print '### conv_enc ###'
	if len(sys.argv) != 3: print 'program \"e\" takes two arguments';quit()	#ensure correct number of args
	if sys.argv[1] not in list('ed'): print '2nd arg must be \"e\" or \"d\"';quit() 	#2nd arg must be e or d	
	if not os.path.exists(sys.argv[2]): print 'file \"'+sys.argv[2]+'\" not found';quit()	#file must exist		
	action = sys.argv[1]; file = sys.argv[2]	#parse bash input			
	doc = get_file(action,file)		#open file
	pw = getpass.getpass('pw: ')	#enter password
	pw_num = [ord(i) for i in pw]
	s_chain = ''.join([str(int(9*random.random())) for x in range(5)])	#random value for filename save	
	if action == 'e':
		doc += ''.join([unichr(int(random.random()*100)) for x in range(100-(len(doc)%100))]) 	#generate padding to block size (integer number of 100s)
		doc = sub_perm(['s1','p1','s2','p2'],doc,pw,pw_num,action)	#encrypt with sub/perm network
		filename = raw_input('Enter filename to save encrypted file: ') 
		with open(filename,'w') as f:	#save encrypted file
			f.write(doc.encode('utf8'))
		ask_remove = ''
		while ask_remove not in list ('ynq'):
			ask_remove = raw_input('Remove old file? (y n q): ')
		if ask_remove == 'y':
			subprocess.Popen(['rm '+file],shell=True)	#remove old (unencrypted) file
		quit()
	elif action == 'd':
		doc = sub_perm(['p2','s2','p1','s1'],doc,pw,pw_num,action)	#decrypt doc; sub/perm in reverse
		for i in range(len(doc)-1,-1,-1):	#remove padding
			if doc[i] == '}':	#all padding after final '}'
				doc = doc[0:i+1]
				break
		file_dict = json.loads(str(doc))	#json-decode data as dictionary
		filename = list(file_dict.iterkeys())[0]	#get embedded filename
		with open(s_chain+filename,'w') as f:	#save decrypted file with rand# + original filename
			f.write(file_dict[list(file_dict.iterkeys())[0]].encode('latin1'))
		open_file = ''
		while open_file not in list('ynq'):	#ask to open file
			open_file = raw_input('Open decrypted file? (y n q): ')
		if open_file == 'q': quit()	
		if open_file == 'y':
		#if open_file in list('nq'): quit()
			show_file=subprocess.Popen(['open '+s_chain+filename],stdout=subprocess.PIPE,shell=True)	#open file
		ask_remove = ''
		while ask_remove not in list('ynq'):	#ask to remove file after use
			ask_remove = raw_input('Decrypted file saved as '+s_chain+filename+'. Remove file? (y n q): ')
		if ask_remove == 'y':
			subprocess.Popen(['rm '+s_chain+filename],shell=True)	#remove file
		quit()			
		
if __name__ == '__main__':
	main()