"""
module_config.py

Configuration loader for TalkMate AI.
"""
import configparser
import os
from dotenv import load_dotenv

def load_config():
    """Load configuration from config.ini and environment variables."""
    load_dotenv()  # Load .env file
    
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    
    # Convert to dictionary format
    config_dict = {}
    for section in config.sections():
        config_dict[section] = {}
        for key, value in config.items(section):
            # Convert string values to appropriate types
            if value.lower() in ['true', 'false']:
                config_dict[section][key] = value.lower() == 'true'
            elif value.isdigit():
                config_dict[section][key] = int(value)
            elif value.replace('.', '', 1).isdigit():
                config_dict[section][key] = float(value)
            else:
                config_dict[section][key] = value
    
    # Override API key from environment if available
    if 'LLM' in config_dict:
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            config_dict['LLM']['api_key'] = api_key
        elif 'api_key' not in config_dict['LLM']:
            config_dict['LLM']['api_key'] = ''
    
    return config_dict

def get_config_value(config, section, key, default=None):
    """Get a configuration value with a default fallback."""
    try:
        return config[section][key]
    except KeyError:
        return default
