from configparser import ConfigParser, ExtendedInterpolation

class ClientConfig(ConfigParser):
    def __init__(self):
        super(ClientConfig, self).__init__(interpolation=ExtendedInterpolation())

        self.add_section("client")
        self.set("client", "auto_authenticate", 'True')
        self.set("client", "development", 'False')

        self.add_section("authentication")
        self.set("authentication", "hostname", "http://localhost")

        self.add_section("oauth")
        self.set("oauth", "oauth_authorization_url", "${authentication:hostname}/oauth2/authorize")
        self.set("oauth", "oauth_redirect_url", "${authentication:hostname}/api/authorized")
        self.set("oauth", "oauth_token_url", "${authentication:hostname}/oauth2/token")
        self.set("oauth", "oauthlib_insecure_transport", 'False')

    def write(self, path="farmos_default_config.cfg"):
        with open(path, "w") as config_file:
            super(ClientConfig, self).write(config_file)
