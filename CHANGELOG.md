# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- Specify correct Content-Type header for 1.x servers.

## [1.0.0-beta.2] -- 2021-07-20
### Changed
- The `token_updater` defaults to an empty lambda function to suppress the `requests_oauthlib.TokenUpdated` exception.
- Set default values in preparation for farmOS 2.x. The `version` defaults to 2 and scope defaults to `farm_manager`.

## [1.0.0-beta.1] -- 2021-03-19

- First beta release.

## [1.0.0-alpha.2] -- 2021-01-29
### Changed
- Create a resource.get_id method instead of supplying an ID as the filters param. [#42](https://github.com/farmOS/farmOS.py/issues/42)
- Rename the `filters` parameter to `params`. [#42](https://github.com/farmOS/farmOS.py/issues/42)

### Added
- Support for subrequests. [#43](https://github.com/farmOS/farmOS.py/issues/43)

## [1.0.0-alpha.1] -- 2021-01-20
### Added
- Use the common OAuth Token path `/oauth/token` available in farmOS ^1.6
- Initial support for farmOS 2.x servers [#39](https://github.com/farmOS/farmOS.py/issues/39)
- Add iterator support to the 2.x client methods [#2](https://github.com/farmOS/farmOS.py/issues/2)

## [0.2.0] -- 2020-08-05
### Removed
- Removed support for the Drupal Session Auth has been removed from the client.
- Removed `farm.authenticate()` method (use `farm.authorize()` instead).
- Removed dependency on ConfigParser used to save default OAuth config and profiles.
- Removed support for OAuth Authorization flow. This can be completed externally of the farmOS.py library.

### Added
- Add `farm.authorize()` method for consistency with OAuth and farmOS.js API.
- Re-export `HTTPError` and OAuth exceptions for convenience.
- Additional OAuth tests.
- [Black](https://black.readthedocs.io/en/stable/) code formatting.

### Fixed
- Don't make requests to `/farm.json` and `/restws/session/token` [#37](https://github.com/farmOS/farmOS.py/issues/37)
- Write tests for OAuth Integration [#33](https://github.com/farmOS/farmOS.py/issues/33)

## [0.1.6] -- 2020-04-24

### Added
- Support for OAuth Clients on the farmOS Server!
- Default to `user_access` OAuth Scope
- Set default `oauth_client_id` to `farm`
- Updated documentation.

### Fixed
- Unset the 'expires_at' key to avoid Requests Exception

## [0.1.6b3] -- 2020-02-10
### Added
- Add an optional `token` parameter to the client API for supplying OAuth tokens.

## [0.1.6b2] -- 2020-02-04
### Fixed
- Fix spelling of default `oauth_scope` config key
- Use mapping protocol access instead of the Legacy get/set API for ConfigParser. Fixes bug for loading tokens from config.

## [0.1.6b1] -- 2020-02-03
### Added
- Support for custom OAuth Clients [#32](https://github.com/farmOS/farmOS.py/pull/32)

### Fixed
- Complex passwords are not correctly read from config file. [#29](https://github.com/farmOS/farmOS.py/issues/29)

## [0.1.5] -- 2019-12-19
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
