from ..extensions import oauth

google = oauth.register(
    name="google",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    access_token_url="https://accounts.google.com/o/oauth2/token",
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    client_kwargs={"scope": "openid profile email"},
)

microsoft = oauth.register(
    name="microsoft",
    authorize_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
    access_token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
    api_base_url="https://graph.microsoft.com/v1.0/",
    client_kwargs={"scope": "User.Read"},
)

github = oauth.register(
    name="github",
    authorize_url="https://github.com/login/oauth/authorize",
    access_token_url="https://github.com/login/oauth/access_token",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)
