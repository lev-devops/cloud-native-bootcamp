import contextlib
import io
import shlex
import unittest
from unittest.mock import patch

import bootstrap


class BootstrapTests(unittest.TestCase):
    def test_configuration_keeps_builds_remote(self):
        result = bootstrap.configuration('lev@mint-hp', '/home/lev/projects/bootcamp')
        self.assertEqual(result['image_build_location'], 'remote')

    def test_rejects_unsafe_hosts_and_paths(self):
        for target in ('-oProxyCommand=bad', 'host; touch x', 'host\ncommand'):
            with self.assertRaises(ValueError):
                bootstrap.host(target)
        for path in ('relative', '/home/lev/../etc', '/', '/tmp'):
            with self.assertRaises(ValueError):
                bootstrap.remote_path(path)

    def test_remote_paths_are_shell_quoted(self):
        path = '/home/lev/a space/$(touch injected)'
        tokens = shlex.split(bootstrap.remote_command(path))
        self.assertEqual(tokens, ['mkdir', '-p', '--', path + '/checkout', path + '/artifacts'])

    def test_preview_never_connects_or_writes(self):
        with patch('sys.argv', ['bootstrap.py']), patch('builtins.input', side_effect=['test-preview', '', '']), \
             patch('bootstrap.subprocess.run') as run, patch('pathlib.Path.mkdir') as mkdir, \
             patch('pathlib.Path.open') as write, contextlib.redirect_stdout(io.StringIO()) as output:
            bootstrap.main()
        run.assert_not_called()
        mkdir.assert_not_called()
        write.assert_not_called()
        self.assertIn('Preview complete', output.getvalue())

    def test_cancel_apply_has_no_side_effects(self):
        with patch('sys.argv', ['bootstrap.py', '--apply']), \
             patch('builtins.input', side_effect=['test-cancel', '', '', 'no']), \
             patch('bootstrap.subprocess.run') as run, patch('pathlib.Path.mkdir') as mkdir, \
             contextlib.redirect_stdout(io.StringIO()):
            bootstrap.main()
        run.assert_not_called()
        mkdir.assert_not_called()


if __name__ == '__main__':
    unittest.main()
