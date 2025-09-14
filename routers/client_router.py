from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from services.client_service import ClientService
from core.container import get_client_service_db as get_client_service
from views.renderer import render
from pydantic import ValidationError
from models.client import ClientIn

router = APIRouter()

@router.get("/clients", response_class=HTMLResponse)
async def list_clients(service: ClientService = Depends(get_client_service)):
    clients = service.list_clients()
    return render("clients/index.html", title="Clients", clients=clients, flash=None)

@router.get("/clients/new", response_class=HTMLResponse)
async def new_client():
    return render(
        "clients/form.html",
        title="New Client",
        heading="Create new client",
        action="/clients",
        method="POST",
        values={},
        errors={},
    )

@router.post("/clients", response_class=HTMLResponse)
async def create_client(
    request: Request,
    service: ClientService = Depends(get_client_service),
):
    form = await request.form()
    data = dict(form)
    try:
        dto = ClientIn(**data)
    except ValidationError as e:
        errors = {err["loc"][0]: err["msg"] for err in e.errors()}
        return render(
            "clients/form.html",
            title="New Client",
            heading="Create new client",
            action="/clients",
            method="POST",
            values=data,
            errors=errors,
        )
    service.create_client(dto)
    return RedirectResponse("/clients", status_code=303)

@router.get("/clients/{client_id}", response_class=HTMLResponse)
async def show_client(client_id: int, service: ClientService = Depends(get_client_service)):
    c = service.get_client(client_id)
    return render("clients/show.html", title=f"Client #{c.id}", c=c, flash=None)

@router.get("/clients/{client_id}/edit", response_class=HTMLResponse)
async def edit_client(client_id: int, service: ClientService = Depends(get_client_service)):
    c = service.get_client(client_id)
    return render(
        "clients/form.html",
        title=f"Edit Client #{c.id}",
        heading=f"Edit client #{c.id}",
        action=f"/clients/{c.id}",
        method="PUT",
        values=c.model_dump(),
        errors={},
    )

@router.post("/clients/{client_id}", response_class=HTMLResponse)
async def update_client(
    client_id: int,
    request: Request,
    service: ClientService = Depends(get_client_service),
):
    form = await request.form()
    data = dict(form)
    if data.get("_method", "").upper() == "PUT":
        data.pop("_method", None)
    try:
        dto = ClientIn(**data)
    except ValidationError as e:
        errors = {err["loc"][0]: err["msg"] for err in e.errors()}
        return render(
            "clients/form.html",
            title=f"Edit Client #{client_id}",
            heading=f"Edit client #{client_id}",
            action=f"/clients/{client_id}",
            method="PUT",
            values=data,
            errors=errors,
        )
    service.update_client(client_id, dto)
    return RedirectResponse(f"/clients/{client_id}", status_code=303)

@router.post("/clients/{client_id}/delete")
async def delete_client(client_id: int, service: ClientService = Depends(get_client_service)):
    service.delete_client(client_id)
    return RedirectResponse("/clients", status_code=303)
