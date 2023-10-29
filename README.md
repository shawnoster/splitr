# splitr

A Splitwise CLI for use in batch adding of expenses.

This is also an experiement in using Chat GPT to generate code, documentation, and open-source suggestions.

## Setup

```shell
# create and activate virtual environment
py -m venv .venv
.\.venv\Scripts\activate

# update pip
.\.venv\Scripts\python.exe -m pip install --upgrade pip

# install requirments
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

### API Keys and Environment Variables

Development API keys and values are expected in environment variables.

- `SPLITWISE_CLIENT_ID` - Splitwise Client Key
- `SPLITWISE_CLIENT_SECRET` - Splitwise Client Secret

#### Using 1Password

The 1Password CLI can be used to load the API keys into the environment in a "just in time" manner. For the variables to be present when running via an IDE the IDE itself needs to be launched using the `op` CLI. For more information on how to setup this workflow read the [1Password's offical documention](https://developer.1password.com/docs/cli/secrets-environment-variables/).

The following commands load the IDE (VSCode in this example) via 1Password's CLI (`op`), which fetches the secrets defined in the `app.env` file for use as environment variables. Alternativly the environment variables can be exported into the environment using your preferred method.

##### From Visual Studio Code

Fetches secretes from 1Password into a Visual Studio Code instance. Replace `code .` with your preferred IDE.

```powershell
op run --env-file=.\splitr\app.env -- code .
```

##### From the command line

Feetches secrets from 1Password then invokes Python to run the `wonka` CLI as a module.

```powershell
op run --env-file=.\splitr\app.env -- py -m splitr
```