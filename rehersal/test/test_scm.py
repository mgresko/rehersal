import sys, os
mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, mypath + '/../../')
print sys.path

from pytest import fixture, raises

from rehersal.scm import Git

@fixture
def setup_git_repo(request):
    repo = Git()

    def setup_repo_teardown():
        repo.cleanup()
        assert not os.path.exists(repo.clone_dir)
    request.addfinalizer(setup_repo_teardown)

    return repo

def test_tempdir_git(setup_git_repo):
    assert '' != setup_git_repo.clone_dir
