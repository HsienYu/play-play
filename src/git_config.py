import os
import sys

#------------------------------------------------------------
if __name__ == '__main__':

    #Get Repo dir and name
    repo_dir = os.getcwd()
    repo = repo_dir.split('/')[-1]

    #Init Git
    cmd0 = 'git init'

    #Local Git Settings
    cmd1 = 'git config --local user.name "Gijs Joost Brouwer"'
    cmd2 = 'git config --local user.email gbrouwer5151@gmail.com'

    #Set Remote
    cmd9 = 'git remote add origin https://github.com/gbrouwer/' + repo + '.git'
    cmd3 = 'git remote set-url origin https://github.com/gbrouwer/' + repo + '.git'

    #Add/Commit and Push everthing
    cmd4 = 'git add .'
    cmd5 = 'git commit -m "updated repo"'
    cmd6 = 'git push origin master'

    #Print and execute
    print(cmd0)
    os.system(cmd0)
    print(cmd1)
    os.system(cmd1)
    print(cmd2)
    os.system(cmd2)
    print(cmd9)
    os.system(cmd9)
    print(cmd3)
    os.system(cmd3)
    print(cmd4)
    os.system(cmd4)
    print(cmd5)
    os.system(cmd5)
    print(cmd6)
    os.system(cmd6)
