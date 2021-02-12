"""Contains the TOML controller."""
from typing import Dict

from ..use_cases.abstract import UseCase
from ..use_cases.clean import CleanRequestModel
from . import FACADE_CONFIGS
from .interfaces import TOMLFacade
from .minio_gateway import MinIOLocation
from .pymysql_gateway import PyMySQLLocation


class TOMLController:
    """Controls the execution of use-cases using TOML formatted configuration information."""

    def __init__(self, facade: TOMLFacade, use_cases: Dict[str, UseCase]) -> None:
        """Initialize Controller."""
        self.facade = facade
        self.use_cases = use_cases

    def clean(self) -> None:
        """Execute the clean use-case."""
        config = self.facade.get_configuration()
        for cleaning_run in config["cleaning_runs"]:
            db_server_config = config["database_servers"][cleaning_run["database_server"]]
            storage_server_kind, storage_server_name = cleaning_run["storage_server"].split(".")
            storage_server_config = config["storage_servers"][storage_server_kind][storage_server_name]
            db_config = FACADE_CONFIGS["database"](**db_server_config)
            external_config = FACADE_CONFIGS[storage_server_kind](**storage_server_config)
            db_location = PyMySQLLocation(cleaning_run["schema"], cleaning_run["store"])
            external_location = MinIOLocation(cleaning_run["schema"], cleaning_run["bucket"], cleaning_run["location"])
            self.use_cases["clean"](CleanRequestModel(db_config, external_config, db_location, external_location))

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"{self.__class__.__name__}(use_cases={self.use_cases})"
