# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Add logging with the Python standard logging module. [#21](https://github.com/farmOS/farmOS.py/issues/21)

## [0.1.4] -- 2019-12-02
### Added
- Only save the client_id and client_secret to a profile if provided.
- Add a path attribute to farm.info() to allow requesting other endpoints.

### Fixed
- Include X-CSRF token in all requests. Fixes [#22](https://github.com/farmOS/farmOS.py/issues/22)

## [0.1.3] - 2019-10-03
### Fixed
- Remove hostname parameter when creating ClientConfig.

## [0.1.2] - 2019-10-03
### Added
- Inject a profile_id into the token before saving.
- Allow a ClientConfig object to be passed to the client.

### Fixed
- PEP8 Code Fixes [#20](https://github.com/farmOS/farmOS.py/issues/20)

## [0.1.1] - 2019-09-25
### Added
- Allow hostnames without a scheme, try to build a valid URL.

### Fixed
- Convert token values to string when saving to farm.config.
- Initialize self.profile_name to DEFAULT so default values are loaded from farm.config.
- Initialize self.config_file to None.
- Make default config values strings.

## [0.1.0] - 2019-09-24
### **This release brings early support for farmOS OAuth! [#18](https://github.com/farmOS/farmOS.py/issues/18)**
- Structure the library to support multiple types of authentication
- Use configparser and config files to configure the client
- Add support the OAuth Authorization Flow
- Add support the OAuth Password Credentials Flow
- Auto-refresh Authentication Tokens by default
- Allow external methods to save tokens
- Save Authentication to a Profile in config file

### Added
- Update the format of response objects [#15](https://github.com/farmOS/farmOS.py/issues/15)

## [0.0.2] - 2019-04-30
### Added
- Ability to get requests in pages (default to all pages)
- Tests for paging of logs
- This CHANGELOG.md file

### Fixed
- Return values for `.send()` methods making `PUT` requests

## [0.0.1] - 2019-04-02
### Added
- `farm.authenticate()` method for authenticating with farmOS
- `farm.info()` method for getting information about a farmOS instance
- `farm.log.get()`, `farm.log.send()`, `farm.log.delete()`
- `farm.asset.get()`, `farm.asset.send()`, `farm.asset.delete()`
- `farm.area.get()`, `farm.area.send()`, `farm.area.delete()`
- `farm.term.get()`, `farm.term.send()`, `farm.term.delete()`
- Framework for testing with `pytest`
- Exception for `NotAuthenticatedError`
- Simple examples in README
