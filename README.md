## SSO - OAuth2

Single Sign On using oAuth2 & JWT
The project constist of 3 apps:

## Authorization Server

This application has a users database and and a login form to validate them. It implements oAuth2 server service auth:

Ask for permissions

```
http://127.0.0.1:8000/users/auth/
?response_type=code
&client_id=1
&redirect_uri=http://127.0.0.1:8000/app1/auth_landing_page
&state=asdf1234
&scope=all
```

Get code and redirect the browser to redirect_uri

```
http://127.0.0.1:8000/users/authorize/
?response_type=code
&client_id=1
&redirect_uri=http://127.0.0.1:8000/app1/auth_landing_page
&state=asdf1234
&scope=all

```

## Application 1 and Application 2 

Independent applications that uses the Authorization Server to validate its users.

Redirect URI:

```
http://127.0.0.1:8000/app1/auth_landing_page
?code=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
&state=yyyyyy

```