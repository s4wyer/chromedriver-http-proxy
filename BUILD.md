# Build (Docker)

Also works with Podman.

```sh
docker build -t 'chromedriver-http-proxy' .
docker run --rm -p "32323:32323" chromedriver-http-proxy
```

