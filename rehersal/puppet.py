import subprocess


EXIT_NO_CHANGE = 0
EXIT_CHANGES = 2
EXIT_FAILURE = 4
EXIT_CHANGES_FAILURES = 6


class Puppet(object):

    def __init__(self, module_path, manifest_path, scm, nice='-19'):
        self._module_path = module_path
        self._manifest_path = manifest_path
        self._scm = scm
        self._nice = nice
        self._output = None
        self._returncode = EXIT_NO_CHANGE

    def __str__(self):
        return "Puppet Handler {0}".format(self.__dict__)

    @property
    def return_code(self):
        return self._returncode

    @property
    def output(self):
        return self._output

    def run(self, branch):
        # bring down puppet code and set branch
        self._scm.clone()
        self._scm.checkout(branch)

        # set module paths localized to clone_dir
        module_path = '{0}/{1}'.format(self._scm.clone_dir, self._module_path)
        manifest_path = '{0}/{1}'.format(
            self._scm.clone_dir, self._manifest_path)

        command = [
            'nice',
            '-n',
            self._nice,
            '/usr/bin/puppet',
            '--test',
            '--noop',
            '--detailed-exitcodes',
            '--modulepath={0}'.format(module_path),
            manifest_path
        ]
        try:
            output = subprocess.check_output(
                command,
                stderr=subprocess.STDOUT,
                shell=True)
        except subprocess.CalledProcessError as e:
            output = e['output']
            returncode = e['returncode']
        finally:
            self._scm.cleanup()

