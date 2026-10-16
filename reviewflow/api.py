"""HTTP API boundary for the reference approval workflow."""
from pathlib import Path
from typing import Annotated, Callable, Literal

from fastapi import Depends, FastAPI, Header, HTTPException, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator

from .auth import Actor, resolve_demo_actor
from .service import DomainError, ReviewService


class CreateRequest(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=5, max_length=4000)

    @field_validator("title", "description")
    @classmethod
    def no_blank_values(cls, value: str, info) -> str:
        value = value.strip()
        lower, upper = (3, 120) if info.field_name == "title" else (5, 4000)
        if not lower <= len(value) <= upper:
            raise ValueError(f"After trimming, length must be between {lower} and {upper}")
        return value


class DecisionRequest(BaseModel):
    decision: Literal["approve", "reject"]
    note: str = Field(default="", max_length=500)


def create_app(
    db_path: str | Path,
    *,
    demo_mode: bool = False,
    identity_resolver: Callable[[str | None], Actor] | None = None,
) -> FastAPI:
    if demo_mode and identity_resolver is not None:
        raise ValueError("Supply either demo_mode or an identity resolver, not both")
    if not demo_mode and identity_resolver is None:
        raise RuntimeError(
            "No identity provider is configured. This training app intentionally fails closed. "
            "For local training use python -m reviewflow with REVIEWFLOW_DEMO_MODE=1."
        )
    resolver = resolve_demo_actor if demo_mode else identity_resolver
    assert resolver is not None
    service = ReviewService(db_path)
    app = FastAPI(title="ReviewFlow reference", version="1.0.0")

    def identity(authorization: Annotated[str | None, Header()] = None) -> Actor:
        return resolver(authorization)

    @app.exception_handler(DomainError)
    async def domain_exception_handler(_request, exc: DomainError):
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.get("/health")
    def health() -> dict:
        if not service.health():
            raise HTTPException(status_code=503, detail="Storage unavailable")
        return {"status": "ok"}

    @app.post("/api/requests", status_code=201)
    def create_request(body: CreateRequest, response: Response, actor: Annotated[Actor, Depends(identity)]) -> dict:
        item = service.create(actor, body.title, body.description)
        response.headers["Location"] = f"/api/requests/{item['id']}"
        return item

    @app.get("/api/requests")
    def list_requests(actor: Annotated[Actor, Depends(identity)], status: Literal["pending", "approved", "rejected"] | None = None) -> list[dict]:
        return service.list(actor, status)

    @app.get("/api/requests/{identifier}")
    def get_request(identifier: str, actor: Annotated[Actor, Depends(identity)]) -> dict:
        return service.get(actor, identifier)

    @app.post("/api/requests/{identifier}/decision")
    def decide(identifier: str, body: DecisionRequest, actor: Annotated[Actor, Depends(identity)]) -> dict:
        return service.decide(actor, identifier, body.decision, body.note)

    @app.get("/api/requests/{identifier}/audit")
    def audit(identifier: str, actor: Annotated[Actor, Depends(identity)]) -> list[dict]:
        return service.audit(actor, identifier)

    if demo_mode:
        @app.get("/", include_in_schema=False)
        def index():
            return FileResponse(Path(__file__).parent / "static" / "index.html")

    return app
