#!/usr/bin/python
import sys
import os
import shutil
from jinja2 import Environment, FileSystemLoader

WEAVER_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(os.path.join(WEAVER_DIR, 'templates')))

class WeaverConfig(object):
    '''This is just a container class to hold procesing data'''
    pass

config = WeaverConfig()

def init(args):
    target_dir = args[0]
    try:
        os.mkdir(target_dir)
    except OSError:
        print 'Cannot start project. A project with that name (%s) appears to already exist.' % target_dir
        sys.exit(1)
    else:
        shutil.copy(
            os.path.join(WEAVER_DIR, 'templates', 'settings.py.tmpl'), 
            os.path.join(target_dir, 'settings.py')
        )

def build(args):
    scripts(working_dir)
    conf(working_dir)

def load_settings(working_dir):
    working_dir = os.getcwd()
    sys.path += [working_dir]
    import settings
    
    config.project = getattr(settings, 'PROJECT_HOME')
    config.code = getattr(settings, 'CODE_HOME')

def scripts(working_dir):
    os.mkdir('scripts')
    
    template = env.get_template('scripts/setup_directories.sh.tmpl')
    content = template.render(PROJECT=config.project)
    file(os.path.join(working_dir, 'scripts', 'setup_directories.sh'), 'w').write(content)
    
    template = env.get_template('scripts/setup_syslinks.sh.tmpl')
    content = template.render(PROJECT=config.project, CODE=config.code)
    file(os.path.join(working_dir, 'scripts', 'setup_syslinks.sh'), 'w').write(content)

commands = {
    'init':init,
    'build':build
}

if __name__ == '__main__':
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    try:
        commands[cmd](args)
    except KeyError:
        print '%s is not a weaver command.' % cmd