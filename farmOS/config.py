from configparser import ConfigParser, BasicInterpolation

class ClientConfig(ConfigParser):
    def __init__(self):
        defaults = {
            'auto_authenticate': 'True',
            'development': 'False',
            'oauthlib_insecure_transport': 'False',
            'oauth_authorization_url': '%(hostname)s/oauth2/authorize',
            'oauth_redirect_url': '%(hostname)s/api/authorized',
            'oauth_token_url': '%(hostname)s/oauth2/token',
        }

        super(ClientConfig, self).__init__(defaults=defaults, interpolation=BasicInterpolation())

    def write(self, path="farmos_default_config.cfg"):
        with open(path, "w") as config_file:
            super(ClientConfig, self).write(config_file)
