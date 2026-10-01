#!/usr/bin/env python3
"""Access token de Google para la cuenta de servicio, sin dependencias (firma RS256 con openssl)."""
import json, base64, time, subprocess, urllib.request, urllib.parse, os, tempfile
SA = os.path.expanduser("~/.config/autolab/google-sa.json")
SCOPES = "https://www.googleapis.com/auth/analytics.readonly https://www.googleapis.com/auth/webmasters.readonly"
def b64(b): return base64.urlsafe_b64encode(b).rstrip(b"=")
def token():
    sa = json.load(open(SA)); now = int(time.time())
    hdr = b64(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    claim = b64(json.dumps({"iss": sa["client_email"], "scope": SCOPES, "aud": sa["token_uri"], "iat": now, "exp": now + 3600}).encode())
    msg = hdr + b"." + claim
    with tempfile.NamedTemporaryFile("w", suffix=".pem", delete=False) as f: f.write(sa["private_key"]); pem = f.name
    try: sig = subprocess.run(["openssl", "dgst", "-sha256", "-sign", pem], input=msg, capture_output=True, check=True).stdout
    finally: os.unlink(pem)
    jwt = (msg + b"." + b64(sig)).decode()
    data = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt}).encode()
    return json.load(urllib.request.urlopen(urllib.request.Request(sa["token_uri"], data=data)))["access_token"]
def get(url, tok): return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": "Bearer " + tok})))
def post(url, tok, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))
if __name__ == "__main__": print("token OK" if token() else "fallo")
