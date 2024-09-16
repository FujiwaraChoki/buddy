import os
import sys
import toml
import utils.config as config

def set_project(path: str) -> bool:
    if not os.path.exists(path):
        return False

    # If not absolute path, make it one
    if not os.path.isabs(path):
        path = os.path.abspath(path)

    with open(os.path.join(config.get_root_path(), 'config.toml')) as f:
        data = toml.load(f)

    if not data.get('project'):
        data['project'] = {}

    data['project']['path'] = path

    with open(os.path.join(config.get_root_path(), 'config.toml'), 'w') as f:
        toml.dump(data, f)

    return True

if __name__ == '__main__':
    args = sys.argv[1:]

    if not args:
        print('Please provide a path to set as the current project.')
        sys.exit(1)

    path = args[0]

    if not set_project(path):
        print('Could not set project. Please try again.')
        sys.exit(1)

    print('Project set successfully.')
