import yaml

from niuApi.arg import get_args
from niuApi.exceptions import NIUConfigError

class NIUConfig():

    def __init__(self, config_file=None) -> None:
        """Initialize NIUConfig Class

        Args:
            config_file (str, optional): Set specific config file. Defaults to None.
        """

        args = get_args()
        if config_file is None:    
            self.config_file = args.config_file
        else:
            self.config_file = config_file

    def read(self):
        """Read the config file

        Raises:
            NIUConfigError: On YAMLError

        Returns:
            dict: YAMLFile as dict
        """

        with open(self.config_file, 'r') as read_file:
            try:
                return yaml.safe_load(read_file)
            except yaml.YAMLError as exc:
                raise NIUConfigError(f'Failed to read {self.config_file}: {exc}')

    def __getitem__(self, key):
        """Return specific item from read function

        Args:
            key (str): Which key should be returned

        Returns:
            dict|str|list: value of key
        """

        read = self.read()

        return read[key]
