from fabric.api import run
from fabric.context_managers import env
from config import configs
from StringIO import StringIO


for (node, value) in configs.items():
     temp = "%s@%s:%s" % ('root', node, '22')

     env.passwords[temp] = value['password']
     env.hosts.append(node)


def setup():
    """ """
    msg = run("apt-update")
    print msg
