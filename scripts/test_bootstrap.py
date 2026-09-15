import contextlib
import io
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import bootstrap


class BootstrapTests(unittest.TestCase):
    def test_apply_and_rerun_preserve_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            profile = Path(tmp) / 'profiles' / 'test' / 'bootstrap.json'
            config = bootstrap.configuration('mint-hp', '/home/example/projects/test')
            with patch('bootstrap.subprocess.run') as run:
                bootstrap.apply_profile(profile, config)
                original = profile.read_bytes()
                bootstrap.apply_profile(profile, config)
                self.assertEqual(profile.read_bytes(), original)
                self.assertEqual(run.call_count, 2)

    def test_ssh_failure_does_not_write_success_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            profile = Path(tmp) / 'profiles' / 'test' / 'bootstrap.json'
            config = bootstrap.configuration('mint-hp', '/home/example/projects/test')
            with patch('bootstrap.subprocess.run', side_effect=subprocess.CalledProcessError(255, ['ssh'])):
                with self.assertRaises(subprocess.CalledProcessError):
                    bootstrap.apply_profile(profile, config)
            self.assertFalse(profile.exists())

    def test_conflicting_profile_blocks_remote_action(self):
        with tempfile.TemporaryDirectory() as tmp:
            profile = Path(tmp) / 'bootstrap.json'
            profile.write_text('{"existing": true}')
            with patch('bootstrap.subprocess.run') as run:
                with self.assertRaises(ValueError):
                    bootstrap.apply_profile(profile, bootstrap.configuration('mint-hp', '/home/example/projects/test'))
            run.assert_not_called()
            self.assertEqual(profile.read_text(), '{"existing": true}')

    def test_profile_symlink_parent_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / 'outside').mkdir()
            (root / 'link').symlink_to(root / 'outside', target_is_directory=True)
            with patch('bootstrap.subprocess.run') as run:
                with self.assertRaises(ValueError):
                    bootstrap.apply_profile(root / 'link' / 'bootstrap.json',
                                            bootstrap.configuration('mint-hp', '/home/example/projects/test'))
            run.assert_not_called()

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
        mkdir = bootstrap.remote_command(path).split(' && mkdir -p -- ', 1)[1].split(' && ', 1)[0]
        tokens = ['mkdir', '-p', '--'] + shlex.split(mkdir)
        self.assertEqual(tokens, ['mkdir', '-p', '--', path + '/checkout', path + '/artifacts'])

    def test_preview_never_connects_or_writes(self):
        with patch('sys.argv', ['bootstrap.py']), patch('builtins.input', side_effect=['test-preview', '', '/home/example/projects/test']), \
             patch('bootstrap.subprocess.run') as run, patch('pathlib.Path.mkdir') as mkdir, \
             patch('pathlib.Path.open') as write, contextlib.redirect_stdout(io.StringIO()) as output:
            bootstrap.main()
        run.assert_not_called()
        mkdir.assert_not_called()
        write.assert_not_called()
        self.assertIn('Preview complete', output.getvalue())

    def test_cancel_apply_has_no_side_effects(self):
        with patch('sys.argv', ['bootstrap.py', '--apply']), \
             patch('builtins.input', side_effect=['test-cancel', '', '/home/example/projects/test', 'no']), \
             patch('bootstrap.subprocess.run') as run, patch('pathlib.Path.mkdir') as mkdir, \
             contextlib.redirect_stdout(io.StringIO()):
            bootstrap.main()
        run.assert_not_called()
        mkdir.assert_not_called()


if __name__ == '__main__':
    unittest.main()
