#!/usr/bin/python
import sys
import os
import shutil
from jinja2 import Environment, FileSystemLoader

from utils import get_setting

WEAVER_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(os.path.join(WEAVER_DIR, 'templates')))

class WeaverConfig(object):
    '''This is just a container class to hold procesing data'''
    pass

config = WeaverConfig()

repo_types = dict(
    'git':'git clone',
    'svn':'svn co',
    'hg':'hg clone'
)

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
    
    config.project = get_setting(settings, 'PROJECT_HOME')
    config.code = get_setting(settings, 'CODE_HOME')
    config.user = get_setting(settings, 'USER')
    config.repo = get_setting(settings, 'REPO')
    config.repo_type = get_setting(settings, 'REPO_TYPE')
    config.url = get_setting(settings, 'URL', lambda x: '\.'.join(x.split('.')))
    config.port = get_setting(settings, 'PORT')
    config.admin = get_setting(settings, 'ADMIN')
    config.django_process = get_setting(settings, 'DJANGO_PROCESS')
    config.repo = get_setting(settings, 'REPO')
    config.repo_cmd = get_settings(settings, 'REPO_TYPE',lambda x: repo_types[x])

def scripts():
    os.mkdir('scripts')
    
    template = env.get_template('scripts/setup_directories.sh.tmpl')
    content = template.render(project=config.project)
    file(os.path.join('scripts', 'setup_directories.sh'), 'w').write(content)
    
    template = env.get_template('scripts/setup_syslinks.sh.tmpl')
    content = template.render(project=config.project, code=config.code)
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
    
    template = env.get_template('conf/apache.tmpl')
    staging_content = template.render(project=config.project,
                                      port=config.port['staging'],
                                      djangoprocess=config.django_process['staging'],
                                      admin=config.admin['staging'],
                                      code=config.code)
    production_content = template.render(project=config.project,
                                         port=config.port['production'],
                                         djangoprocess=config.django_process['production'],
                                         admin=config.admin['production'],
                                         code=config.code)
    internal_content = template.render(project=config.project,
                                       port=config.port['internal'],
                                       djangoprocess=config.django_process['internal'],
                                       admin=config.admin['internal'],
                                       code=config.code)
    filename = '%s' % config.project
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
    
    c = commands.get(cmd, None)
    if c is None:
        print '%s is not a weaver command.' % cmd
    else:
        c(args)
