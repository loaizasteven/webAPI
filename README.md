# webAPI
Example of use for FastAPI 

# Run Example
```python
fastapi dev localDevAPI/main.py
```
# Installation
## Mac Installation

Add command-line JSON processer `jq`: https://jqlang.github.io/jq/
```bash
brew install jq
```
Be sure to check if your machine has an Apple silicon or Intel chip
[Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)

## FastAPI in Containers - Docker
View `README.Docker.md` file.

# Authentication and Tokens
FASTAPI provides a tutorial on this token, [OAuth2 with Password (and hashing), Bearer with JWT tokens](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
## OAuth 2.0
OAuth 2.0 is an authentication framework that allows a client (e.g. the [web appication](localDevAPI/main.py)) to access resources on a resource server (e.g an API) on behalf of a resource owner/user. It provides a secure way for the client to acccess the resources without sharing/exposing the credentials. For instance, it can be used to authenticate a user and authroize access to a model service without directly requiring knowledge or pass-through of the API key.

## JSON Web Token (JVT)
"JWT is an open standard that defines a compact and self-contrained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed. JWTs can be signed using a secret (with the HMAC algorithm)" 
\- [JWT Website](https://jwt.io/introduction)

### JSON Web Token (JVT) Example
Here's an example of a JVT:
```
#Header
JSON Object
{
  "alg": "HS256",
  "typ": "JWT"
}
#Payload
JSON Object
{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true,
  "exp": 1690455564
}
# Signature
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret_key
)
```
The Encoded JVT will be

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwidXNlcl9pZCI6IjEyMzQ1Njc4OTAiLCJleHAiOjE2OTA0NTU1NjR9.WxL5E3xPzF8p6F0jLZ7XQ
```
Breakdown
- Header: Specifies the algorithm (HS256) and token type (JWT).
- Payload: Contains claims (key-value pairs) about the user, such as subject (sub), name, admin status, and expiration time (exp).
- Signature: Generated using the header, payload, and a secret key.
Encoded JVT: The header, payload, and signature are base64Url encoded and concatenated with dots (.) to form the final token.

Note: All of the information contained within the JWT can easily be decoded and exposed to user. Be sure not to send sentitive information within the token. Learn more at [security/README.md](/security/README.md).