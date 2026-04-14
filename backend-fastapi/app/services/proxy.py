import httpx
from fastapi import Request, Response

BACKEND_URL = "https://httpbin.org" #dummy backend

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
}

def filter_headers(headers):
    return {
        key: value
        for key, value in headers.items()
        if key.lower() not in HOP_BY_HOP_HEADERS and key.lower() != "host"
    }

async def forward_request(request: Request):
    async with httpx.AsyncClient(timeout=5.0) as client:
        url = f"{BACKEND_URL}{request.url.path}"
        if request.url.query:
            url += f"?{request.url.query}"
        
        # Filter incoming headers
        headers = filter_headers(request.headers)
        
        #Forward request
        backend_response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=await request.body()
        )

        # Filter outgoing headers too
        response_headers = filter_headers(backend_response.headers)

        return Response(
            content=backend_response.content,
            status_code=backend_response.status_code,
            headers=response_headers
        )