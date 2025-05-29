import subprocess
import os
import sys
import re

root_dir = 'Repo1'
branch_name1 = 'main'
branch_name2 = 'main'
#release = '2025.1'
try:
	root_dir, branch_name1, branch_name2 = sys.argv[1:]
except:
        print("Missing Files Path Argument At Run Time")
if not os.path.exists(root_dir):
        subprocess.call('git clone --recurse-submodules https://github.com/Bapuji-patta/Repo1.git',shell=True)
os.chdir(root_dir)
subprocess.call('git pull', shell=True)
#subprocess.call('git checkout '+branch_name1, shell=True)

#subprocess.call('git pull',shell=True)
os.chdir('library')
pull_output = subprocess.check_output('git pull origin '+branch_name2, shell=True)
os.chdir('..')
diff_output  = subprocess.check_output('git diff', shell=True)
output_gitdiff = re.findall('Subproject commit \w+\d+',diff_output.decode())

final_output = '..'.join(re.findall('\w+\d+' ,''.join(output_gitdiff)))
print(f'git log --pretty=%s {final_output}', 'final_outputfinal_output')
print("Current Directory:", os.getcwd())

os.chdir('library')
print("Current Directory:", os.getcwd())


if final_output:
	
	pretty_output = ''.join(subprocess.check_output("git log --pretty='%s'"+ final_output, shell=True).decode())
	os.chdir('../..')
	subprocess.run('git add -A .', shell=True)
	pretty_output = "Updated Commit ID"+'\n'+'\n'+ pretty_output
	cmd = 'git commit -m "%s"' % pretty_output
	pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(out, error) = pipe.communicate()
	subprocess.call('git push origin '+branch_name1,shell=True)
	
	subprocess.call('git clean -xdf', shell=True)

