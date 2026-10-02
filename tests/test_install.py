"""Exercise filesystem behavior of the installer, not model accuracy."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import install
import build_portable


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / 'project with spaces'
        self.project.mkdir()

    def test_all_clients_preserve_complete_skill_and_share_common_copy(self):
        result = install.install(self.project, ['all'])
        self.assertEqual(len(result), 4)
        for directory in ['.agents/skills', '.kiro/skills', '.claude/skills']:
            self.assertEqual(install.contents(self.project / directory / install.NAME),
                             install.contents(install.SOURCE))
        self.assertEqual((self.project / 'ai-review' / f'{install.NAME}.md').read_bytes(),
                         install.PORTABLE.read_bytes())

    def test_second_install_is_noop(self):
        install.install(self.project, ['codex', 'kiro'])
        before = {p: p.stat().st_mtime_ns for p in self.project.rglob('*') if p.is_file()}
        self.assertTrue(all(action == 'Already current' for action, _ in
                            install.install(self.project, ['codex', 'kiro'])))
        self.assertEqual(before, {p: p.stat().st_mtime_ns for p in before})

    def test_conflict_does_not_overwrite_or_install_other_targets(self):
        install.install(self.project, ['kiro'])
        target = self.project / '.kiro/skills' / install.NAME / 'SKILL.md'
        target.write_text('user customization', encoding='utf-8')
        with self.assertRaises(ValueError):
            install.install(self.project, ['codex', 'kiro'])
        self.assertFalse((self.project / '.agents').exists())
        self.assertEqual(target.read_text(encoding='utf-8'), 'user customization')

    def test_dry_run_creates_nothing(self):
        self.assertEqual(len(install.install(self.project, ['all'], dry_run=True)), 4)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_missing_project_rejected(self):
        with self.assertRaises(FileNotFoundError):
            install.install(self.project / 'missing', ['codex'])

    def test_parent_file_rejected_before_other_target_write(self):
        (self.project / '.kiro').write_text('keep me', encoding='utf-8')
        with self.assertRaises(ValueError):
            install.install(self.project, ['codex', 'kiro'])
        self.assertFalse((self.project / '.agents').exists())

    def test_symlink_install_root_rejected(self):
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        try:
            (self.project / '.kiro').symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest('Symlinks unavailable on this host')
        with self.assertRaises(ValueError):
            install.install(self.project, ['kiro'])
        self.assertEqual(list(outside.iterdir()), [])

    def test_portable_contains_current_references_and_no_relative_skill_links(self):
        rendered = build_portable.render()
        self.assertEqual(install.PORTABLE.read_text(encoding='utf-8'), rendered)
        self.assertNotIn('(references/', rendered)
        for filename, _ in build_portable.REFERENCES:
            self.assertIn((install.SOURCE / 'references' / filename).read_text(encoding='utf-8').strip(), rendered)


if __name__ == '__main__':
    unittest.main()
