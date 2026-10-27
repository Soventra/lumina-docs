# Event Hooks for SSO Login

<EnterpriseFeature feature="SSO">SSO is free for up to 5 users. Beyond that, an enterprise license is required.</EnterpriseFeature>

## Overview

Lumina provides two different SSO hooks depending on your authentication setup:

| Hook Type | When to Use | What It Does |
|-----------|-------------|--------------|
| **Custom UI SSO Sign-in Handler** | You have an OAuth proxy (oauth2-proxy, Gatekeeper, Vouch, etc.) in front of Lumina | Parses user info from request headers and signs user into UI |
| **Custom SSO Handler** | You use direct SSO providers (Google, Microsoft, SAML) and want custom post-auth logic | Runs custom code after standard OAuth flow to set user permissions/teams |

**Quick Decision Guide:**
- ✅ **Use Custom UI SSO Sign-in Handler** if user authentication happens outside Lumina (via headers)
- ✅ **Use Custom SSO Handler** if you want Lumina to handle OAuth flow + run custom logic afterward

---

## Option 1: Custom UI SSO Sign-in Handler

Use this when you have an **OAuth proxy in front of Lumina** that has already authenticated the user and passes user information via request headers.

### How it works
- User lands on Admin UI  
- **Your custom SSO sign-in handler is called to parse request headers and return user info**
- Lumina has retrieved user information from your custom handler
- User signed in to UI

### Usage

#### 1. Create a custom UI SSO handler file

This handler parses request headers and returns user information as an OpenID object:

```python
from fastapi import Request
from fastapi_sso.sso.base import OpenID
from lumina.integrations.custom_sso_handler import CustomSSOLoginHandler


class MyCustomSSOLoginHandler(CustomSSOLoginHandler):
    """
    Custom handler for parsing OAuth proxy headers
    
    Use this when you have an OAuth proxy (like oauth2-proxy, Vouch, etc.) 
    in front of Lumina that adds user info to request headers
    """
    async def handle_custom_ui_sso_sign_in(
        self,
        request: Request,
    ) -> OpenID:
        # Parse headers from your OAuth proxy
        request_headers = dict(request.headers)
        
        # Extract user info from headers (adjust header names for your proxy)
        user_id = request_headers.get("x-forwarded-user") or request_headers.get("x-user")
        user_email = request_headers.get("x-forwarded-email") or request_headers.get("x-email")
        user_name = request_headers.get("x-forwarded-preferred-username") or request_headers.get("x-preferred-username")
        
        # Return OpenID object with user information
        return OpenID(
            id=user_id or "unknown",
            email=user_email or "unknown@example.com", 
            first_name=user_name or "Unknown",
            last_name="User",
            display_name=user_name or "Unknown User",
            picture=None,
            provider="oauth-proxy",
        )

# Create an instance to be used by Lumina
custom_ui_sso_sign_in_handler = MyCustomSSOLoginHandler()
```

#### 2. Configure in config.yaml

```yaml
model_list: 
  - model_name: "openai-model"
    lumina_params: 
      model: "{{openai_small}}"

general_settings:
  custom_ui_sso_sign_in_handler: custom_sso_handler.custom_ui_sso_sign_in_handler

lumina_settings:
  drop_params: True
  set_verbose: True
```

#### 3. Start the proxy
```shell
$ lumina --config /path/to/config.yaml 
```

#### 4. Navigate to the Admin UI

When a user attempts navigating to the Lumina Admin UI, the request will be routed to your custom UI SSO sign-in handler. 

---

## Option 2: Custom SSO Handler (Post-Authentication)

Use this if you want to run your own code **after** a user signs on to the Lumina UI using standard SSO providers (Google, Microsoft, etc.)

### How it works
- User lands on Admin UI
- Lumina redirects user to your SSO provider (Google, Microsoft, etc.)
- Your SSO provider redirects user back to Lumina  
- Lumina has retrieved user information from your IDP
- **Your custom SSO handler is called and returns an object of type SSOUserDefinedValues**
- User signed in to UI

### Usage

#### 1. Create a custom SSO handler file

Make sure the response type follows the `SSOUserDefinedValues` pydantic object. This is used for logging the user into the Admin UI:

```python
from fastapi_sso.sso.base import OpenID

from lumina.proxy._types import LuminaUserRoles, SSOUserDefinedValues
from lumina.proxy import proxy_server

# These imports are available if you need to create users or manage team membership:
# from lumina.proxy.management_endpoints.internal_user_endpoints import new_user
# from lumina.proxy.management_endpoints.team_endpoints import add_new_member


async def custom_sso_handler(userIDPInfo: OpenID) -> SSOUserDefinedValues:
    try:
        print("inside custom sso handler")  # noqa
        print(f"userIDPInfo: {userIDPInfo}")  # noqa

        if userIDPInfo.id is None:
            raise ValueError(
                f"No ID found for user. userIDPInfo.id is None {userIDPInfo}"
            )
        
        #################################################
        # Access extra fields from SSO provider (requires GENERIC_USER_EXTRA_ATTRIBUTES env var)
        # Example: Set GENERIC_USER_EXTRA_ATTRIBUTES="department,employee_id,groups"
        extra_fields = getattr(userIDPInfo, 'extra_fields', None) or {}
        user_department = extra_fields.get("department")
        employee_id = extra_fields.get("employee_id")
        user_groups = extra_fields.get("groups", [])
        
        print(f"User department: {user_department}")  # noqa
        print(f"Employee ID: {employee_id}")  # noqa
        print(f"User groups: {user_groups}")  # noqa
        #################################################

        #################################################
        # Run your custom code / logic here
        # check if user exists in lumina proxy DB
        if proxy_server.prisma_client is not None:
            _user_info = await proxy_server.prisma_client.get_data(user_id=userIDPInfo.id)
            print("_user_info from lumina DB ", _user_info)  # noqa
        #################################################

        return SSOUserDefinedValues(
            models=[],                                      # models user has access to
            user_id=userIDPInfo.id,                         # user id to use in the Lumina DB
            user_email=userIDPInfo.email,                   # user email to use in the Lumina DB
            user_role=LuminaUserRoles.INTERNAL_USER.value, # role to use for the user 
            max_budget=0.01,                                # Max budget for this UI login Session
            budget_duration="1d",                           # Duration of the budget for this UI login Session, 1d, 2d, 30d ...
        )
    except Exception as e:
        raise Exception("Failed custom auth")
```

#### 2. Configure in config.yaml

Pass the filepath to the config.yaml. 

e.g. if they're both in the same dir - `./config.yaml` and `./custom_sso.py`, this is what it looks like:

```yaml 
model_list: 
  - model_name: "openai-model"
    lumina_params: 
      model: "{{openai_small}}"

general_settings:
  custom_sso: custom_sso.custom_sso_handler

lumina_settings:
  drop_params: True
  set_verbose: True
```

#### 3. Start the proxy
```shell
$ lumina --config /path/to/config.yaml 
```
