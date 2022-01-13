# Mortgage Payments Tracker API

```bash
# For Local Dev work:
# Use pyenv + virtualwrapper to create an env

pyenv activate <name-of-env>
pip install -e <path_to_package>
```

1) When a user goes to the `/login` endpoint, they submit login details via basic Auth.
Connexion does the handling automatically. A db connection is made to retrieve users and the username/password is matched against the database
if a match is found, then the user is given a session token that lasts 6 hours

On every API call, `get_session` is called to ensure they are authenticated.
