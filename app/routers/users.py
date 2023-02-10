from fastapi import APIRouter


router = APIRouter()


@router.get("/{id}")
def get_user(id: int):
    pass


@router.post("/")
def post_user():
    pass


@router.patch("/{id}")
def patch_user():
    pass


@router.delete("/{id}")
def delete_user():
    pass


