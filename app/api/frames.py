from typing import List

from app.api.auth import retrieve_active_user
from app.database.schemas.inbox import Inbox
from fastapi import APIRouter, UploadFile, HTTPException, Depends, status

from app.database.schemas.user import User
from app.database.services import inbox
from app.storage.services import file

router = APIRouter()


@router.post("/frames/", response_model=List[Inbox])
async def post(files: List[UploadFile], user: User = Depends(retrieve_active_user)):
    if not 1 <= len(files) <= 15:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The number of transferred files can be from 1 up to 15."
        )

    for element in files:
        if element.content_type != 'image/jpeg':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The images are in jpeg format."
            )

    query = await inbox.post(file.save_files(files))
    return query


@router.get("/frames/{id}", response_model=Inbox)
async def get(id: int, user: User = Depends(retrieve_active_user)):
    query = await inbox.get(id=id)

    if query is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Frames not found"
        )

    return query


@router.delete("/frames/{id}", response_model=Inbox)
async def delete(id: int, user: User = Depends(retrieve_active_user)):
    model = await get(id)

    if file.delete_file(model):
        await inbox.delete(id=id)
    else:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cloud Object Storage not responding"
        )

    return model
