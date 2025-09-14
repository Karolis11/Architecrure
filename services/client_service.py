from fastapi import HTTPException
from typing import List
from models.client import Client, ClientIn
from repositories.client_repository import ClientRepository

class ClientService:
    def __init__(self, repo: ClientRepository):
        self.repo = repo

    def list_clients(self) -> List[Client]:
        return self.repo.list()

    def get_client(self, client_id: int) -> Client:
        c = self.repo.get(client_id)
        if not c:
            raise HTTPException(404, "Client not found")
        return c

    def create_client(self, data: ClientIn) -> Client:
        return self.repo.add(data)

    def update_client(self, client_id: int, data: ClientIn) -> Client:
        try:
            return self.repo.update(client_id, data)
        except KeyError:
            raise HTTPException(404, "Client not found")

    def delete_client(self, client_id: int) -> None:
        self.repo.delete(client_id)
