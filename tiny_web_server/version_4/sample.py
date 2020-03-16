import os
import sys

def execute(temp):
    cw, pr  = os.pipe()
    stdin = sys.stdin.fileno()
    stdout = sys.stdout.fileno()
    pid =os.fork()
    if pid:
        # parent process
        os.close(cw)
        os.dup2(pr,stdin)
        print("pr:" +  str(stdin))
        # sys.stdin.flush()
        st = os.read(pr,1024)
        # os.close(pr)
        print(st)
        return st
    else:
        # child process
        os.close(pr)
        os.dup2(cw,stdout)
        exec(open("./tws-bin/test.py").read())

execute("/tws-bin/test.py")
# stdin = sys.stdin.fileno()
# stdout = sys.stdout.fileno()
# exec(open("./tws-bin/test.py").read())
# temp = os.read(stdout,1024)
# os.close(stdout)
# print(temp)
