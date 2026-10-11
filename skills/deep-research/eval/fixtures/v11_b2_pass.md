# Verify: does the prod config disable TLS 1.0?

Deliverable: verify

Per-claim verdict block:

| Claim | Verdict | Strongest source | What would change it |
|-------|---------|------------------|----------------------|
| TLS 1.0 is disabled in nginx.conf | CONFIRMED | `conf/nginx.conf:42` `ssl_protocols TLSv1.2 TLSv1.3;` | an override in a sites-enabled vhost |
| HSTS is enforced | PARTIAL | header present but max-age=0 | raising max-age in the vhost |
| Legacy cipher suite removed | REFUTED | `ssl_ciphers` still lists `DES-CBC3-SHA` | removing it from the cipher line |
| OCSP stapling on | UNVERIFIABLE | no stapling directive found, cannot reach prod | prod `nginx -T` dump |
