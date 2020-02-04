from configparser import ConfigParser, BasicInterpolation


class ClientConfig(ConfigParser):
    def __init__(
            self,
            profile_name=None,
            defaults=None,
            **kwargs):

        config_defaults = {
            'auto_authenticate': 'True',
            'development': 'False',
            'oauthlib_insecure_transport': 'False',
            'oauth_authorization_url': '%(hostname)s/oauth2/authorize',
            'oauth_client_id': 'farmos_api_client',
            'oauth_client_secret': '',
            'oauth_redirect_url': '%(hostname)s/api/authorized',
            'oauth_scope': 'user_access',
            'oauth_token_url': '%(hostname)s/oauth2/token',
        }

        # Merge additional default values if provided.
        if defaults is not None:
            config_defaults = {**config_defaults, **defaults}

        # Initialize the config object.
        super().__init__(defaults=config_defaults, interpolation=BasicInterpolation())

        # Add a section for the profile.
        if profile_name is not None:
            self.add_section(profile_name)
        else:
            profile_name = 'DEFAULT'

        # Load additional kwargs into the config.
        for key, value in kwargs.items():
            if value is not None:
                self.set(profile_name, key, value)


    def write(self, path="farmos_default_config.cfg"):
        with open(path, "w") as config_file:
            super().write(config_file)
