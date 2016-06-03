from subprocess import check_call
import time
import docker
import pytest


@pytest.fixture(scope='module')
def cli(request):
    return docker.Client()


@pytest.fixture(scope='module')
def container(cli):
    return cli.containers(
        filters={"label": "com.docker.compose.service=memcached"})[0]


def setup_module(module):
    check_call(['docker-compose', 'up', '-d'])
    time.sleep(30)


def teardown_module(module):
    check_call(['docker-compose', 'down'])


def test_memcached_check_proc(cli, container):
    res = cli.exec_create(container['Id'], "pgrep memcached")
    cli.exec_start(res)
    assert cli.exec_inspect(res)['ExitCode'] == 0

def test_memecached_port():
    cmd = ['nc', '-z', '-v', '-w5', '127.0.0.1', '11219']
    check_call(cmd)
