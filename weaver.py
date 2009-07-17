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
    config.user = getattr(settings, 'USER')
    config.repo = getattr(settings, 'REPO')
    config.repo_type = getattr(settings, 'REPO_TYPE')
    
    config.url = getattr(settings, 'URL')
    config.url = dict(
        staging='^%s$' % '\.'.join(config.url[0].split('.')),
        internal='^%s$' % '\.'.join(config.url[1].split('.')),
        production='^%s$' % '\.'.join(config.url[2].split('.')),
    )
    config.port = getattr(settings, 'PORT')
    config.port = dict(
        staging=config.port[0],
        internal=config.port[1],
        production=config.port[2]
    )
    config.admin = getattr(settings, 'ADMIN')
    config.admin = dict(
        staging=config.admin[0],
        internal=config.admin[1],
        production=config.admin[2]
    )
    config.django_process = getattr(settings, 'DJANGO_PROCESS')
    config.django_process = dict(
        staging=config.django_process[0],
        internal=config.django_process[1],
        production=config.django_process[2]
    )

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