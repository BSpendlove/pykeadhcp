# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Coding Style

- Minimum version of Python to use during development and production releases is 3.10.6
- Always use f-strings as they are far more superior than `%` and `.format()`
- Currently `black` is used with the default configuration, please ensure you use `black` to format your python code. If you are running VSCode then you can set to format on save with the black formatter to save time, however you must provide output of running `black` before your pull request is considered
- Always write tests for new command features that interact with the Kea API or the local cached configuration
- Any functions should follow the Kea API documentation (with the exception of reserved variable names) as closely as possible
- List comprehensions should always be used where possible unless the code is too ugly and unreadable, that is up for you and the reviewer to agree with :-)

## Tests

A basic infrastructure is provided in this project under the `tests/test_infrastructure` folder which creates a basic ISC Kea DHCP server running the 4 main daemons (control-agent, ddns, dhcp4 and dhcp6). Before code is merged into main, you must ensure that you implement the relevant pytest functions in the appropriate test file (eg. `test_kea_dhcp4.py` contains all the relevant tests against the dhcp4 API command).

You must adhere to the following formats for tests:
1. All relevant tests must be placed in their respective file for that daemon (eg. dhcp4 tests must be placed inside `test_kea_dhcp4.py` test file)
2. All functions must following the format of `test_kea_<daemon_name>_<API reference command>` where the `API reference command` follows the same name as the Kea API documentation, replacing special charaters (hypthens) and spaces with an underscore. For example if you are implementing the dhcp4 config-get API command, the function name must be `test_kea_dhcp4_config_get`.

## Docker Test Infrastructure

The docker infrastructure is still being worked on but for now, runs as expected from a fresh clone. The following docker compose files are provided:

- docker-compose.yml
   - Standalone instance of Kea with support for hooks if you fill out the environment variables discussed shortly.
- docker-compose-sql.yml
   - Standalone instance of Kea with a database backend (config + lease + host reservations) used to test mainly cb_config hooks.
- docker-compose-ha-sql.yml
   - Primary and Secondary Kea instances with a database backend (config + lease + host reservations) to test HA functionality.

### HA Testing

The `docker-compose-ha-sql.yml` file contains a separate network (192.0.2.128/25) with IP addresses configured directly under the kea services. The HA hook configuration parameters only takes IP addresses and not hostnames (for obvious reasons, it's always DNS... wouldn't want DHCP HA to depend on DNS resolution now would we?) therefore the hard-coded IP addresses should factor in any additional services configured on the network for testing purposes (hence why kea instances use IPs further in the /25 range).

### Premium Hooks

If you are developing or testing the premium hooks, create a file called `.env` in the tests/test_infrastructure folder with the following variables:

```
KEA_VERSION="<version-here"
KEA_REPO="<private-token>/isc/kea-<version eg. 2-4>-prv"
KEA_PREMIUM="premium"
```

Rebuild the container using `docker-compose up --build` and the hooks should install as required if your token is correct and has correct permissions to download via the private repository.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a 
   build.
2. Update any documentation with details of changes (readme, commands, etc...), this includes new environment 
   variables, exposed ports, useful file locations and container parameters.
3. Use poetry release command `poetry version prerelease` so that the dev CI/CD pipeline is able to upload to the test py-pi repository. You should then run the tests in the next step against this prerelease module that was uploaded to test pypi.
4. Perform tests as required using pytest `pytest -s tests`. If you are only implementing API changes for dhcp4 and the control agent but not dhcp6, you can skip these tests using `pytest -s tests -k "dhcp4"`. Ensure that you provide the output of the tests in the pull request as this will be compared when another developer runs the test to validate the new test work along with the old tests.
5. You may merge the Pull Request in once you have the sign-off of two other developers, or if you 
   do not have permission to do that, you may request the second reviewer to merge it for you.

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

### Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team at [INSERT EMAIL ADDRESS]. All
complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. The project team is
obligated to maintain confidentiality with regard to the reporter of an incident.
Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.

### Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [http://contributor-covenant.org/version/1/4][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/