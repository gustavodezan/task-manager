from fastapi import HTTPException, status

def already_exists(entity: str = "Entity"):
    return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"{entity} already exists")

def not_found(entity: str = "Entity"):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{entity} not found")
    