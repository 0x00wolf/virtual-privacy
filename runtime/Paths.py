import os
import json


class Paths:
    """
    RuntimePaths class generates the required directories at runtime and points
    to the location of the user database.
    """

    def __init__(self, user):
        # user database & config files
        self.home_dir = os.path.dirname(os.path.abspath('virtualprivacy.py'))
        self._keys_dir = f"{self.home_dir}/keys"  # Credentials root
        self._local_dir = f"{self.keys_dir}/local"
        self._remote_dir = f"{self.keys_dir}/remote"
        self._data_dir = f"{self.home_dir}/data"
        self._generate_data_dir()
        self._generate_keys_dir()
        self._generate_local_dir()
        self._generate_remote_dir()
        self._user_database = f"{self.data_dir}/{user}_database.db"

    def _generate_keys_dir(self):
        if not os.path.exists(self.keys_dir):
            os.makedirs(self.keys_dir)

    def _generate_local_dir(self):
        if not os.path.exists(self.local_dir):
            os.makedirs(self.local_dir)

    def _generate_remote_dir(self):
        if not os.path.exists(self.remote_dir):
            os.makedirs(self.remote_dir)

    def _generate_data_dir(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    @property
    def data_dir(self):
        return self._data_dir

    @property
    def keys_dir(self):
        return self._keys_dir

    @property
    def remote_dir(self):
        return self._remote_dir

    @property
    def local_dir(self):
        return self._local_dir

    @property
    def user_database(self):
        return self._user_database

