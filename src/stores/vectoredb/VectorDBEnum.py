from enum import Enum

class VectorDBEnum(Enum):
    QDRANT = "QDRANT"

class DistnaceMethodEnums(Enum):
    COSINE = "cosine"
    DOT  = "dot"