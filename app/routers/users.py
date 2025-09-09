from fastapi import APIRouter, Query, Response
from app.schemas import UserCreate, UserUpdate, UserInDB
from app import crud

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserInDB, status_code=201)
async def create_user(user: UserCreate):
    return await crud.create_user(user)


@router.get("/", response_model=list[UserInDB])
async def list_users(
    q: str = Query(None),
    min_age: int = Query(None),
    max_age: int = Query(None),
    is_active: bool = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    return await crud.list_users(q, min_age, max_age, is_active, page, limit)


@router.get("/{user_id}", response_model=UserInDB)
async def get_user(user_id: str):
    return await crud.get_user(user_id)


@router.put("/{user_id}", response_model=UserInDB)
async def update_user(user_id: str, data: UserUpdate):
    return await crud.update_user(user_id, data)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str):
    await crud.delete_user(user_id)
    return Response(status_code=204)
