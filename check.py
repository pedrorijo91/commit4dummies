#!/usr/bin/python

import os
import subprocess
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_keywords():
	return {'.java': ['exp', 'print', 'TODO'], '.txt': ['testing', 'xpto']}

def get_commit_hash():
	FNULL = open(os.devnull, 'w')
	head = subprocess.call(['git', 'rev-parse', '--verify', 'HEAD'], stdout=FNULL, stderr=subprocess.STDOUT)

	if head == 0:
		return 'HEAD'
	else:
		return '4b825dc642cb6eb9a060e54bf8d69288fbee4904'

def get_files():
	commit = get_commit_hash()
	return subprocess.check_output(['git', 'diff-index', '--cached', commit, '--name-status'])

def analyse_line(line):
	arr = line.split()
	status = arr[0]
	filename = arr[1]

	return status, filename

def execute_grep(keyword, filename):
	grepResult = subprocess.Popen(['grep', '-n', keyword, filename], stdout=subprocess.PIPE) 
	output = grepResult.stdout.read()
	code = grepResult.poll()

	return output, code

def output_finding(keyword, filename, output):
	print bcolors.WARNING + "found results for '" + keyword + "' in: " + filename + ".\nMatches: " + bcolors.ENDC
	print bcolors.FAIL + output + bcolors.ENDC

def output_no_finding(keyword, filename):
	print bcolors.OKGREEN + "no results for: '" + keyword + "' in: " + filename + bcolors.ENDC

def positive_ans(ans):
	return ans == 'y'

def negative_ans(ans):
	return ans == 'n'

def prompt_exit():
	sys.stdin = open('/dev/tty')
	ans = raw_input(bcolors.OKBLUE + "abort? (y/n)\n" + bcolors.ENDC)
	if positive_ans(ans):
		return True
	if negative_ans(ans):
		return False

	print "Invalid answear '" + ans + "'. Please answear 'y' or 'n'."
	prompt_exit()


keywords = get_keywords()

files = get_files()
for line in files.splitlines():
	status, filename = analyse_line(line)

	if status <> 'D':
		for extension in keywords:
			if filename.endswith(extension):
				for keyword in keywords[extension]:
					
					output, code = execute_grep(keyword, filename)

					if code == 0: # res == 0 => find
						output_finding(keyword, filename, output)
						if prompt_exit():
							print "Aborting commit..."
							sys.exit(1)
					else: # res != 0 => not find
						output_no_finding(keyword, filename)
print "Successfully ending hook"
sys.exit(0)