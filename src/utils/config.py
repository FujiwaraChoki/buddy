import os
import toml

def get_root_path():
    pth = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    if pth.endswith('src'):
        return os.path.dirname(pth)
    
    return pth

def load_config():
    config_path = os.path.join(get_root_path(), 'config.toml')
    with open(config_path, 'r') as f:
        return toml.load(f)
    
