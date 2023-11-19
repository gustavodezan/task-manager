from fastapi import HTTPException, status

def already_exists(entity: str = "Entity"):
    return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"{entity} already exists")

def not_found(entity: str = "Entity"):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{entity} not found")

def internal_error(entity: str = "Entity"):
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error")

def not_enough_permissions():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")

def invalid_format():
    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid format")