from config import DEFAULT_PAYLOAD


# Prepare the payload for an API request
def prepare_payload(messages, payload=None):
    # If a custom payload is provided, copy it; otherwise, use the default payload
    payload = payload.copy() if payload else DEFAULT_PAYLOAD.copy()

    # Add messages to the payload
    payload["messages"] = messages

    # Return the final payload
    return payload
