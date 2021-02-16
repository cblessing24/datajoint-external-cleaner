"""Contains the facade of the MinIO interface."""
from typing import List, Optional, Set, TypedDict

from minio import Minio
from minio.deleteobjects import DeleteObject

from ..adapters.interfaces import AbstractMinIOFacade


class MinIOFacadeConfig(TypedDict):  # pylint: disable=inherit-non-class
    """Configuration for the MinIOFacade."""

    endpoint: str
    access_key: str
    secret_key: str
    secure: bool


class MinIOFacade(AbstractMinIOFacade):  # pylint: disable=unsubscriptable-object
    """Facade of the MinIO interface."""

    def __init__(self) -> None:
        """Initialize MinIOFacade."""
        self._client: Optional[Minio] = None  # pylint: disable=unsubscriptable-object

    @property
    def client(self) -> Minio:
        """Return already instantiated MinIO client if possible or instantiate and return a new one."""
        if not self._client:
            raise RuntimeError(f"{self.__class__.__name__} is not configured")
        return self._client

    def configure(self, config: MinIOFacadeConfig) -> None:
        """Configure the facade."""
        self._client = Minio(**config)

    def get_object_paths(self, bucket_name: str, prefix: str) -> List[str]:
        """Get all paths that match the provided prefix of MinIO objects from the bucket."""
        objects = self.client.list_objects(bucket_name, prefix=prefix, recursive=True)
        object_paths = [x.object_name for x in objects]
        return object_paths

    def remove_objects(self, bucket_name: str, object_paths: Set[str]) -> None:
        """Delete the MinIO objects identified by the provided paths from the bucket."""
        delete_object_list = [DeleteObject(x) for x in object_paths]
        errors = self.client.remove_objects(bucket_name, delete_object_list=delete_object_list)
        for error in errors:
            print(error)

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}()"
