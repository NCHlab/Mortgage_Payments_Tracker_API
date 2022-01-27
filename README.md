# Mortgage Payments Tracker API

```bash
# For Local Dev work:
# Use pyenv + virtualwrapper to create an env

pyenv activate <name-of-env>
pip install -e <path_to_package>
```

Welcome to the Mortgage Payments Tracker API. This is the backend system for the REACTJS website and works with the associated [MPT GUI](https://github.com/NCHlab/mortgage_payments_tracker_gui).

> Note: Due to specific considerations, an instance of this server + API can only be used by 1 set of people who know each other. This is due to data on some endpoints being shared for all users (this project has a specific case for me - which is obvious by its name), thus adding in features for gobal public use has not been done.

Demo Access can be found on: [demo.nayamc.com/mortgage/api/v1/](demo.nayamc.com/mortgage/api/v1/)

Documentation regarding endpoints can be found in `openapi/spec.yml`


# Notes

On every API call, `get_session` is called to ensure they are authenticated.

```
When a user goes to the `/login` endpoint, they submit login details via basic Auth.
Connexion does the handling automatically. A db connection is made to retrieve users and the username/password is matched against the database
If a match is found, then the user is given a session token that lasts 6 hours.

After 4 failed login attempts, the account is locked and requires an administrator to remove the lock.
```

