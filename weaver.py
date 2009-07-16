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
    load_settings()
    scripts()
    conf()

def load_settings():
    working_dir = os.getcwd()
    sys.path += [working_dir]
    import settings
    
    config.project = getattr(settings, 'PROJECT_HOME')
    config.code = getattr(settings, 'CODE_HOME')
    
    config.url = getattr(settings, 'SITE_URL')
    config.url = dict(
        staging='^%s$' % '\.'.join(config.url[0].split('.')),
        internal='^%s$' % '\.'.join(config.url[1].split('.')),
        production='^%s$' % '\.'.join(config.url[2].split('.')),
    )
    config.port = getattr(settings, 'APACHE_PORT')
    config.port = dict(
        staging=config.port[0],
        internal=config.port[1],
        production=config.port[2]
    )

def scripts():
    os.mkdir('scripts')
    
    template = env.get_template('scripts/setup_directories.sh.tmpl')
    content = template.render(PROJECT=config.project)
    file(os.path.join('scripts', 'setup_directories.sh'), 'w').write(content)
    
    template = env.get_template('scripts/setup_syslinks.sh.tmpl')
    content = template.render(PROJECT=config.project, CODE=config.code)
    file(os.path.join('scripts', 'setup_syslinks.sh'), 'w').write(content)

def conf():
    os.mkdir('conf')
    os.mkdir(os.path.join('conf', 'staging'))
    os.mkdir(os.path.join('conf', 'internal'))
    os.mkdir(os.path.join('conf', 'production'))
    
    template = env.get_template('conf/lighttpd.tmpl')
    staging_content = template.render(project=config.project, 
                                      url=config.url['staging'], 
                                      port=config.port['staging'])
    production_content = template.render(project=config.project,
                                         url=config.url['production'],
                                         port=config.port['production'])
    internal_content = template.render(project=config.project,
                                       url=config.url['internal'],
                                       port=config.port['internal'])
    filename = '99-%s.conf' % config.project
    file(os.path.join('conf', 'staging', filename), 'w').write(staging_content)
    file(os.path.join('conf', 'production', filename), 'w').write(production_content)
    file(os.path.join('conf', 'internal', filename), 'w').write(internal_content)
    
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