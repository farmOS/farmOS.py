from configparser import ConfigParser, ExtendedInterpolation

class ClientConfig(ConfigParser):
    def __init__(self):
        super(ClientConfig, self).__init__(interpolation=ExtendedInterpolation())

        self.add_section("Client")
        self.set("Client", "auto_authenticate", 'True')
        self.set("Client", "development", 'False')

        self.add_section("Authentication")
        self.set("Authentication", "hostname", "")

        self.add_section("OAuth")
        self.set("OAuth", "oauth_authorization_url", "${Authentication:hostname}/oauth2/authorize")
        self.set("OAuth", "oauth_redirect_url", "${Authentication:hostname}/api/authorized")
        self.set("OAuth", "oauth_token_url", "${Authentication:hostname}/oauth2/token")
        self.set("OAuth", "oauthlib_insecure_transport", 'False')

    def write(self, path="farmos_default_config.cfg"):
        with open(path, "w") as config_file:
            super(ClientConfig, self).write(config_file)
