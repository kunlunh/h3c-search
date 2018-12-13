# -*- coding:utf-8 -*-
import paramiko
import collections


def swsearch(hostname,mac,tag) :
	tag = tag
	result_dic = {}
	if tag == 'v7' :
		hostname = hostname
		username = 'netadmin'
		password = 'Net!@#'
		paramiko.util.log_to_file('syslogin.log')     #发送paramiko日志到syslogin.log文件
		searchcmd = 'dis mac-address | include ' + mac
	
		ssh = paramiko.SSHClient()          #创建一个SSH客户端client对象
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=hostname,username=username,password=password,allow_agent=False,look_for_keys=False)    #连接汇聚交换机

		stdin,stdout,stderr = ssh.exec_command(searchcmd)      #调用远程执行命令方法exec_command()
		result1 = stdout.readlines()
		ssh.close()
	
	
		if len(result1) <= 8 :
			result_dic[1] = 'Not Found'

		else :
			i = 0
			j = 1
		for line in result1 :
			line = line.strip('\n')
			if i < 8 :
				i = i + 1
			else :
				tecmd = '\ndis lldp nei int G1/0/' + line[49:51] + ' verbose | include "Management address                :"\n'   #组成命令查看接入交换机IP地址的命令
				ssh = paramiko.SSHClient()
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				ssh.connect(hostname=hostname,username=username,password=password,allow_agent=False,look_for_keys=False)   #连接汇聚交换机
				stdin,stdout,stderr = ssh.exec_command(tecmd)
				out1 = stdout.read()
				loc = out1.find(': ')  #在结果中定位交换机IP位置
				ip = out1[loc+2:loc+20].strip('\n')   #得到接入交换机IP
				ssh.close()
				ssh = paramiko.SSHClient()
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				ssh.connect(hostname=ip,username=username,password=password,allow_agent=False,look_for_keys=False)  #连接接入交换机
				seccmd = 'dis mac-address | include ' + line[0:14]
				stdin,stdout,stderr = ssh.exec_command(seccmd)
				out2 = stdout.read()
				loc2 = out2.find('Eth')  #定位接入交换机结果所在行
				ssh.close()
				result2 = out2[loc2-8:loc2+15] #粗略定位接入交换机端口
				all_result = 'MAC: ' + line[0:14] + '\n' + 'Access Switch IP: ' + ip + '\n' + 'Port: ' + result2 + '\n' + 'VLAN: ' + line[17:21] + '\n' + 'BAGG: ' + line[49:51] + '\n'
				result_dic[j] = all_result 
				j = j + 1
				
	elif tag == 'v5' :
		hostname = hostname
		username = 'netadmin'
		password = 'Net!@#'
		paramiko.util.log_to_file('syslogin.log')     #发送paramiko日志到syslogin.log文件
		searchcmd = 'dis mac-address | include ' + mac
		ssh = paramiko.SSHClient()          #创建一个SSH客户端client对象
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=hostname,username=username,password=password,allow_agent=False,look_for_keys=False)    #连接汇聚交换机

		stdin,stdout,stderr = ssh.exec_command(searchcmd)      #调用远程执行命令方法exec_command()
		result1 = stdout.readlines()

		ssh.close()
		length = len(result1)
		del result1[length-1]
		if length <= 9 :
			result_dic[1] = 'Not Found'

		else :
			i = 0
			j = 1
			for line in result1 :
				line = line.strip('\n')
				if i < 8  :
					i = i + 1
				else :
					tecmd = 'dis lldp nei int G1/0/' + line[57:59] + ' | include Management address                :'   #组成命令查看接入交换机IP地址的命令
					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					ssh.connect(hostname=hostname,username=username,password=password,allow_agent=False,look_for_keys=False)   #连接汇聚交换机
					stdin,stdout,stderr = ssh.exec_command(tecmd)
					out1 = stdout.read()
					loc = out1.find(': ')  #在结果中定位交换机IP位置
					ip = out1[loc+2:loc+17].strip('\n')   #得到接入交换机IP
			
					ssh.close()
					ssh = paramiko.SSHClient()
					ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					ssh.connect(hostname=ip,username=username,password=password,allow_agent=False,look_for_keys=False)  #连接接入交换机
					seccmd = 'dis mac-address | include ' + line[0:14]
					stdin,stdout,stderr = ssh.exec_command(seccmd)
					out2 = stdout.read()
					loc2 = out2.find('Eth')  #定位接入交换机结果所在行
					ssh.close()
					result2 = out2[loc2-8:loc2+15] #粗略定位接入交换机端口
					all_result = 'MAC: ' + line[0:14] + '\n' + 'Access Switch IP: ' + ip + '\n' + 'Port: ' + result2 + '\n' + 'VLAN: ' + line[15:19] + '\n' + 'BAGG: ' + line[57:59] + '\n'
					result_dic[j] = all_result 
					j = j + 1
	
	return result_dic

					
