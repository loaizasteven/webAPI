## JSON Web Token (JVT) Security and Tampering

Although, the JVT token restricts the exposure of the underlying key/password by providing a token, the contents of the token can be read and if stolen grants access to the resources data (albeit until it expires).

###  JVT Signature
JVTs contain a digital signature, which ensures the token's integrity and authenticity. The signature is generated using a secret key and a cryptographic algorithm (e.g., HMAC SHA256). when a JVT is modified, without knowing the secret, the signiture becomes invalid. This ensures that the token cannot be modified to stop brute force attacks from trying different tokens.

When a server receives a JVT, it verifies the signature by recalculating it using the same secret key and algorithm. If the recalculated signature doesn't match the original signature, the token is considered tampered with and is rejected.

### JSON Web Token (JVT) Expiration
JSON Web Tokens (JVTs) can have an expiration time, ensuring that the token is only valid for a specific period. JVTs contain a payload with claims, and one of these claims is the expiration time, represented by the exp key. The exp claim specifies the timestamp (in seconds) when the token expires and the client can raise an error, prompting the user to generate a new token with their refresh token. Due to the signiture validation, a malicious agent cannot update the exp key, with invaliding the signiture. 

### Refresh Tokens: Why and When
A Refresh tokens serve several purposes, making them a crucial component of secure authentication and authorization systems. Some advantages of a Refresh/Access token system is:

* Access tokens are short-lived to minimize the damage if they're compromised. Refresh tokens allow for a secure way to obtain new access tokens without exposing sensitive credentials. 
* Obtaining a new access token using a refresh token is often faster than re-authenticating with credentials.
