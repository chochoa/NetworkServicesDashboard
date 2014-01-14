import subprocess
pipe = subprocess.Popen(["./jonMaPerlPIScript.pl"], stdout=subprocess.PIPE)
result = pipe.stdout.read()
print result