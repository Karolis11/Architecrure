from typing import List
from fastapi import APIRouter, Depends, Response
from models.client import Client, ClientIn
from services.client_service import ClientService
from core.container import get_client_service

router = APIRouter(prefix="/clients", tags=["clients"])

@router.get("", response_model=List[Client])
def list_clients(service: ClientService = Depends(get_client_service)):
    return service.list_clients()


@router.get("/{client_id}", response_model=Client)
def get_client(client_id: int, service: ClientService = Depends(get_client_service)):
    return service.get_client(client_id)


@router.post("", response_model=Client, status_code=201)
def create_client(dto: ClientIn, service: ClientService = Depends(get_client_service)):
    return service.create_client(dto)


@router.put("/{client_id}", response_model=Client)
def update_client(client_id: int, dto: ClientIn, service: ClientService = Depends(get_client_service)):
    return service.update_client(client_id, dto)


@router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, service: ClientService = Depends(get_client_service)):
    service.delete_client(client_id)
    return Response(status_code=204)
