from repositories.client_repository import InMemoryClientRepository, ClientRepository
from services.client_service import ClientService
from typing import Dict

class Container:
    def __init__(self):
        self._singletons: Dict[str, object] = {}

    def client_repository(self) -> ClientRepository:
        if "client_repo" not in self._singletons:
            self._singletons["client_repo"] = InMemoryClientRepository()
        return self._singletons["client_repo"]

    def client_service(self) -> ClientService:
        return ClientService(self.client_repository())

container = Container()

def get_client_service() -> ClientService:
    return container.client_service()
