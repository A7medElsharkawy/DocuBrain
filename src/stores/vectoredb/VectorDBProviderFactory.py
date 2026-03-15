from provider import QdrantDB
from VectorDBEnum import VectorDBEnum
from controllers import BaseController
class VectorDBProviderFactory():
    def __init__(self, config):

        self.config = config
        self.controller = BaseController()

    def create(self, provider:str):
        db_path = self.controller.get_db_path(db_name=self.config.VECTORE_DB_PATH)
        if provider == VectorDBEnum.QDRANT.value:
            return QdrantDB(db_path=db_path,
                            distance_method=self.config.VECTORE_DB_DISTANCE)

        return None


        