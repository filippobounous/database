from fastapi import Request, HTTPException, status


def is_authenticated(request: Request) -> bool:
    return bool(request.session.get("user"))


def require_auth(request: Request):
    if not is_authenticated(request):
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/"})
