import os
from runloop_api_client import Runloop

runloop_client = Runloop(
    bearer_token="ak_30iNCfvH5eJfuGefB1krx",
    base_url="https://api.runloop.pro"
)
# create the devbox and wait for it to be ready
devbox = runloop_client.devboxes.create_and_await_running(create_args={
    "name": "test-devbox"
})
print(devbox.id)
