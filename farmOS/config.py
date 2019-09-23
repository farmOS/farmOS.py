from configparser import ConfigParser, NoSectionError

class ClientConfig(ConfigParser):
    def __init__(self):
        super(ClientConfig, self).__init__()

        self.add_section("client")
        self.set("client", "auto_authenticate", 'True')
        self.set("client", "development", 'False')

        self.add_section("oauth")
        self.set("oauth", "oauth_authorization_url", "/oauth2/authorize")
        self.set("oauth", "oauth_redirect_url", "/api/authorized")
        self.set("oauth", "oauth_token_url", "/oauth2/token")
        self.set("oauth", "oauthlib_insecure_transport", '0')

    def write(self, path="farmos_default_config.cfg"):
        with open(path, "w") as config_file:
            super(ClientConfig, self).write(config_file)
