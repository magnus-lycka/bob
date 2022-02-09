import os
import hmac

# get the webhook secret from the environment
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

# caclulate hmac digest of payload with shared secret token
def calc_signature(payload):
    digest = hmac.new(
        key=WEBHOOK_SECRET.encode("utf-8"), msg=payload, digestmod="sha1"
    ).hexdigest()
    return f"sha1={digest}"