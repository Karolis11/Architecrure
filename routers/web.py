from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from services.client_service import ClientService
from core.container import get_client_service_db as get_client_service
from views.renderer import render

router = APIRouter()

@router.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/clients")

@router.get("/clients", response_class=HTMLResponse)
def clients_page(service: ClientService = Depends(get_client_service)):
    return render("clients/index.html", title="Clients")