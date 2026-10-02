"""Install project-scoped review instructions without overwriting existing files.

Python 3.10+, standard library only. No downloads, AI calls or configuration edits.
"""
from pathlib import Path
import argparse
import shutil

ROOT = Path(__file__).resolve().parents[1]
NAME = 'spring-boot-reviewer-lite'
SOURCE = ROOT / 'skills' / NAME
PORTABLE = ROOT / 'portable' / f'{NAME}.md'
# Use the documented shared directory to avoid redundant copies across these clients.
CLIENT_PATHS = {
    'codex': '.agents/skills',
    'kiro': '.kiro/skills',
    'claude': '.claude/skills',
    'cursor': '.agents/skills',
    'copilot': '.agents/skills',
    'gemini': '.agents/skills',
    'portable': 'ai-review',
}


def contents(path):
    if path.is_symlink():
        raise ValueError(f'Refusing symbolic link: {path}')
    if path.is_file():
        return {'': path.read_bytes()}
    if not path.is_dir():
        raise ValueError(f'Expected a file or directory: {path}')
    files = {}
    for item in path.rglob('*'):
        if item.is_symlink():
            raise ValueError(f'Refusing symbolic link: {item}')
        if item.is_file():
            files[item.relative_to(path).as_posix()] = item.read_bytes()
    return files


def plan_install(project, clients):
    project = Path(project).expanduser().resolve(strict=True)
    if not project.is_dir():
        raise ValueError('Project path must be an existing directory')
    requested = list(CLIENT_PATHS) if 'all' in clients else clients
    plans = {}
    for client in requested:
        source = PORTABLE if client == 'portable' else SOURCE
        relative = Path(CLIENT_PATHS[client]) / (f'{NAME}.md' if client == 'portable' else NAME)
        destination = project / relative
        # Reject linked installation roots instead of writing outside the project.
        node = project
        for part in relative.parts:
            node = node / part
            if node.is_symlink():
                raise ValueError(f'Refusing symbolic link: {node}')
            if node != destination and node.exists() and not node.is_dir():
                raise ValueError(f'Parent is not a directory: {node}')
        expected = contents(source)
        identical = False
        if destination.exists():
            identical = source.is_dir() == destination.is_dir() and contents(destination) == expected
            if not identical:
                raise ValueError(f'Existing installation differs: {destination}. '
                                 'Back it up and remove only that installation before updating.')
        plans[destination] = (source, identical)
    return plans


def install(project, clients, dry_run=False):
    plans = plan_install(project, clients)  # Detect every conflict before copying anything.
    results = []
    for destination, (source, identical) in plans.items():
        if identical:
            action = 'Already current'
        elif dry_run:
            action = 'Would install'
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                # Exclusive creation also refuses a file created after preflight.
                with destination.open('xb') as output:
                    output.write(source.read_bytes())
            action = 'Installed'
        results.append((action, destination))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--client', nargs='+', required=True, choices=[*CLIENT_PATHS, 'all'])
    parser.add_argument('--project', required=True, help='Existing application or demo directory')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        results = install(args.project, args.client, args.dry_run)
    except (OSError, ValueError) as error:
        parser.exit(1, f'Installation stopped: {error}\n')
    for action, path in results:
        print(f'{action}: {path}')
    print('Open the project in your assistant and use the prompt in docs/COMPATIBILITY.md.')


if __name__ == '__main__':
    main()
