import os
import sys
def execute_script():
    pr, cw = os.pipe()
    stdin  = sys.stdin.fileno() # usually 0
    stdout = sys.stdout.fileno() # usually 1
    pid = os.fork()

    if pid:
        os.close(cw)
        os.dup2(pr, stdin)
        st =""
        for line in sys.stdin:
            st+= line
        return st
    else:
        os.close(pr)
        os.dup2(cw, stdout)
        # sys.stdout.flush()
        env = os.environ.copy()
        cmd = "./tws-bin/ls"
        args = [cmd]
        os.execve(args[0],args,env)
        
print(execute_script())

