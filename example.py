import subprocess
import os
import sys
import re

root_dir = 'Repo1'
branch_name1 = 'main'
branch_name2 = 'main'
# --- Configuration ---
repo_url = 'https://github.com/Bapuji-patta/Repo1.git'
sub_dir = 'library'

# --- Input Args ---
try:
    root_dir, branch_name1, branch_name2 = sys.argv[1:]
except ValueError:
    print("Usage: python script.py <root_dir> <branch_name1> <branch_name2>")
    sys.exit(1)

# --- Clone repo if needed ---
if not os.path.exists(root_dir):
    subprocess.check_call(['git', 'clone', '--recurse-submodules', repo_url, root_dir])

os.chdir(root_dir)

# --- Pull latest changes ---
subprocess.check_call(['git', 'pull'])
os.chdir(sub_dir)

# --- Pull from specified branch ---
subprocess.check_call(['git', 'pull', 'origin', branch_name2])
os.chdir('..')

# --- Get diff output ---
diff_output = subprocess.check_output(['git', 'diff']).decode('utf-8')

# --- Parse submodule commit hashes ---
matches = re.findall(r'Subproject commit (\w+)', diff_output)
if len(matches) < 2:
    print("Could not find two commit hashes in submodule diff.")
    sys.exit(1)

# Reverse to get correct order: old..new
commit_range = f"{matches[0]}..{matches[1]}"
print(f'git log --pretty=%s{commit_range}')
#--- Get commit messages ---

os.chdir(sub_dir) 
try:
    commit_messages = subprocess.check_output([
        'git', 'log', '--pretty=%s', commit_range, shell=True,stderr=subprocess.STDOUT,
    ]).decode('utf-8')
except subprocess.CalledProcessError as e:
    print("Git log failed:\n", e.output.decode() if e.output else str(e))
    sys.exit(1)
os.chdir('..')

# --- Commit changes ---
subprocess.check_call(['git', 'add', '-A'])
commit_msg = f"library: Updated Commit ID\n\n{commit_messages.strip()}"
subprocess.check_call(['git', 'commit', '-m', commit_msg])
subprocess.check_call(['git', 'push', 'origin', branch_name1])

# --- Clean repo ---
subprocess.call(['git', 'clean', '-xdf'])
