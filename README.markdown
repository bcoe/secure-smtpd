Secure SMTPD
============

Secure-SMTPD extends on Petri Lehtinen's SMTPD library adding support for AUTH and SSL.

Usage
-----

```python
from secure_smtpd import SMTPServer, FakeCredentialValidator
SMTPServer(
    self,
    ('0.0.0.0', 465),
    None,
    require_authentication=True,
    ssl=True,
    certfile='examples/server.crt',
    keyfile='examples/server.key',
    credential_validator=FakeCredentialValidator(),
)
asyncore.loop()
```
