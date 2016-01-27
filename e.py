#!/usr/bin/env python
# -*- coding: utf-8 -*-
#	Commands are formulated as $ e e filename
#					or $ e d filename
#					to encrypt/decrypt
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
def sub_perm(actions,doc,pw,pw_num,action):
	for i in actions:
		if i[0] == 's':
			doc = sub_doc(doc,i,pw,pw_num,action)
		elif i[0] == 'p':
			doc = perm_doc(doc,i,pw,pw_num,action)
	return doc
def ask_cont(new_file):
	cont = ''
	while cont not in list('ynq'):
		cont = raw_input('old doc will be replaced. continue? (y n q): ')
	if cont in list('nq'): 
		print 'new file saved as: ',new_file
		raise
def open_file(action,file):	
	with open(file,'r') as f:
		if action == 'e':
			return json.dumps({file:f.read()},encoding='latin1')
		else:
			return f.read().decode('utf8')
def main():
	try:
		if len(sys.argv) != 3: raise
		if sys.argv[1] not in list('ed'): raise 	
		if not os.path.exists(sys.argv[2]): raise
		action = sys.argv[1]; file = sys.argv[2]	
		doc = open_file(action,file)
		pw = getpass.getpass('pw: ')
		pw_num = [ord(i) for i in pw]
		s_chain = ''.join([str(int(9*random.random())) for x in range(10)])		
		if action == 'e':
			doc += ''.join([unichr(int(random.random()*100)) for x in range(100-(len(doc)%100))])
			doc = sub_perm(['s1','p1','s2','p2'],doc,pw,pw_num,action)	
			with open(file+'e'+s_chain,'w') as f:	#save temp
				f.write(doc.encode('utf8'))
		elif action == 'd':
			doc = sub_perm(['p2','s2','p1','s1'],doc,pw,pw_num,action)
			for i in range(len(doc)-1,-1,-1):
				if doc[i] == '}':	#eliminate padding after final '}'
					doc = doc[0:i+1]
					break
			file_dict = json.loads(str(doc))
			with open(file+'e'+s_chain,'w') as f:
				f.write(file_dict[file].encode('latin1'))
		ask_cont(file+'e'+s_chain)	
		subprocess.Popen(['cp '+file+'e'+s_chain+' '+file+'; rm '+file+'e'+s_chain],shell=True)		
		if action == 'd':
			subprocess.Popen(['open -a textedit '+file],shell=True)	#change file-opening app here
	except:
		print 'Something went wrong. Exiting...';sys.exit()
		
if __name__ == '__main__':
	main()