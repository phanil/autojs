#!/usr/bin/python

import sys
import os
import shutil

# current working directory
cwd = ""

# repos
repos= [	\
	#comment follows because of GFW
	#{ "url":"https://chromium.googlesource.com/chromium/tools/depot_tools.git", "tag":"", "name":"" },	\
	#{ "url":"https://chromium.googlesource.com/external/gyp.git", "tag":"", "name":"" },	\
	
	{ "url":"https://github.com/libuv/libuv.git", "tag":"v1.7.5", "name":"libuv" },	\
	{ "url":"https://github.com/v8/v8.git", "tag":"4.8.33", "name":"v8" },	\
]


def add_ignore(dst):
	tmp = os.path.join(dst, ".gitignore")
	file = open(tmp, 'a')
	file.write("\r\n.git_\r\n")
	file.close()
	return

def clone_repo(url, tag, name):
	print "git clone: %s @ %s to %s ..."%(url, tag, name)
	if len(tag) == 0:
		os.system("git clone --depth=1 %s %s"%(url, name))
	else:
		os.system("git clone --depth=1 --branch %s %s %s"%(tag, url, name))
	dst = os.path.join(cwd, name)
	tmp_old = os.path.join(dst, ".git")
	tmp_new = os.path.join(dst, ".git_")
	if os.path.exists(tmp_old):
		# rename .git folder, avoid of been detected as subproject
		os.rename(tmp_old, tmp_new)
		add_ignore(dst)
	return

def pull_repo(name):
	repo = os.path.join(cwd, name)
	os.chdir(repo)
	print "git pull: %s @ %s ..."%(name, os.getcwd())
	os.system("git pull")
	os.chdir(cwd)
	return
	
def fetch_repo(url, tag, name):
	if len(url) == 0:
		return
	print "fetch repo(%s) from %s"%(name, url)
	dst = os.path.join(cwd, name)
	if os.path.exists(dst):
		return
	return clone_repo(url, tag, name)
	
if __name__ == "__main__":
	# insure the current working directory
	tmp_path = sys.path[0]
	if os.path.isdir(tmp_path):
		cwd = tmp_path
	elif os.path.isfile(tmp_path):
		cwd = os.path.dirname(tmp_path)
	os.chdir(cwd)
	print "Current Working Directory: %s"%(os.getcwd())
	
	# delete all repos
	try:
		for repo in repos:
			dst = os.path.join(cwd, repo["name"])
			if os.path.exists(dst):
				os.system("git rm -r -f %s"%(dst))
			if os.path.exists(dst):
				#shutil.rmtree(dst)
				os.removedirs(dst)
	except Exception as e:
		print "Error: Delete Repo @ %s"%(e)
		sys.exit()
	
	# fetch repos
	try:
		for repo in repos:
			fetch_repo(repo["url"], repo["tag"], repo["name"])
	except Exception as e:
		print "fetch repo error: %s"%(e)
		sys.exit()
	
	raw_input("Press Enter to Exit ...")
	
	
