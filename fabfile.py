from fabric.api import *
from fabric.contrib.console import confirm, prompt
from ilogue.fexpect import expect, expecting
from fabric.context_managers import env
from StringIO import StringIO
from os import linesep

prompts = []
prompts += expect("Enter new UNIX password:", "tkdgml00")
prompts += expect("Retype new UNIX password:", "tkdgml00")

#prompts += expect("id: merong: no such user"

env.hosts = ["192.168.0.106"]
env.passwords = {"root@192.168.0.106:22":"tkdgml00"}
#env.abort_on_prompts=True

#@roles("web")
#@hosts('localhost')
def test():
    with expecting(prompts):
        msg = run("useradd merong", shell=True)
        msg = run("passwd merong", shell=True)

        msg = run("env", shell=True)

        print "------------------------>" + msg

        if "JAVA_HOME" not in msg:
            run("echo 'export JAVA_HOME=/usr/lib/jvm/java-8-oracle' >> ~/.profile")

        if "HADOOP_HOME" not in msg:
            run("echo 'export HADOOP_HOME=/root/download/hadoop-2.6.3' >> ~/.profile")


#@hosts('localhost')
def ping():
    file_name = "sample.txt"

    local("echo '%s:' >> %s" % (env.host, file_name))

    testCase(file_name, "ping 8.8.8.8")
    testCase(file_name, "ping 1.1.1.1")
    testCase(file_name, "ping 1.1.1.1")
    testCase(file_name, "ping 1.1.1.1")
    testCase(file_name, "ping 1.1.1.1")
    testCase(file_name, "ping 1.1.1.1")
    testCase(file_name, "ping 1.1.1.1")


def testCase(file_name, command):
    with warn_only():
        local("echo '    - %s' >> %s" % (command, file_name))

        io = StringIO()

        start = run("pidof %s" % command)

        try:
            msg = run(command, stdout=io, stderr=io, shell=True, timeout=10)
        except Exception as e:
            end = run("pidof %s" % command)

            tokens = start.split(" ")
            filtered = filter(lambda x: x not in tokens, end.split(" "))

            print "------------ start: " + start
            print "------------ end: " + end

            if len(filtered) == 1:
                run("kill -9 %s" % filtered[0])


        message = io.getvalue()

        local("echo '%s' >> %s" % (convert(message), file_name))

        io.close()



def convert(message):
    message = message.replace("'", "")
    message = message.replace('"', "")

    converted = ""

    for line in message.split(linesep):
        temp = line.split(":", 1)

        if len(temp) >= 2:
            converted = converted + "        " + temp[1].strip() + linesep
        else:
            pass

    return converted





