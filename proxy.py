from litellm.proxy.proxy_server import ProxyMiddleware
from fastapi import Request, HTTPException

ALLOWED_DOMAINS = [
    "app.stickball.biz",
    "musketeers.dev"
]

class DomainFilterMiddleware(ProxyMiddleware):
    async def pre_request(self, request: Request):
        origin = request.headers.get("origin")
        referer = request.headers.get("referer")

        domain = None
        if origin:
            domain = origin.replace("https://", "").replace("http://", "").split("/")[0]
        elif referer:
            domain = referer.replace("https://", "").replace("http://", "").split("/")[0]

        if domain not in ALLOWED_DOMAINS:
            raise HTTPException(status_code=403, detail="Forbidden: Domain not allowed")

        return request
