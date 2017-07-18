from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm


env.hosts = ['root@128.199.215.91']


# LOCAL TASKS #
def mmm():
    local('python src/manage.py makemigrations && python src/manage.py migrate')


def push():
    with settings(warn_only=True):
        local('git add -p && git commit')
    local('git push')


def prepare():
    # todo: add pull
    push()


# SERVER TASKS #

code_dir = '/var/www/tutors'


def touch():
    run('touch /etc/uwsgi/vassals/tutors.ini')


def migrate():
    with cd(code_dir):
        run('python src/manage.py migrate')


def pull():
    with cd(code_dir):
        run('git pull')
    touch()


def deploy():
    with cd(code_dir):
        run('git pull')
        # run('pip install -r requirements.txt')
        # migrate()
        # run('bower install --allow-root')
        run('python src/manage.py collectstatic --noinput')
    touch()


def createsuperuser():
    with cd(code_dir):
        run('python src/manage.py createsuperuser')


def cmd_setupperm():
    with cd(code_dir):
        run('python src/manage.py setupperm')
