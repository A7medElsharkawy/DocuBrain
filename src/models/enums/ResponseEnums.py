from enum import Enum

class ResponseStatus(Enum):
    FILE_TYPE_NOT_ALLOWED = "File type not allowed"
    FILE_SIZE_EXCEEDS = "File size exceeds maximum allowed size"
    FILE_VALID = "File is valid"
    UPLOAD_SUCCESS = "File uploaded successfully"