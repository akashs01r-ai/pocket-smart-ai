import json
import urllib.request


URL = (
    "http://127.0.0.1:8000"
    "/api/health"
)


with urllib.request.urlopen(
    URL,
    timeout=5,
) as response:

    data = json.loads(
        response.read()
    )

    print(
        json.dumps(
            data,
            indent=2,
        )
    )