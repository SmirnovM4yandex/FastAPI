from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas.auth import Token
from src.domain.auth.authenticate_user import AuthenticateUserUseCase
from src.domain.auth.create_access_token import CreateAccessTokenUseCase
from src.api.depends import (
    authenticate_user_use_case,
    create_access_token_use_case,
)
from src.core.exceptions.exceptions import NotFoundException, WrongPasswordException

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_use_case: Annotated[
        AuthenticateUserUseCase,
        Depends(authenticate_user_use_case)
    ],
    token_use_case: Annotated[
        CreateAccessTokenUseCase,
        Depends(create_access_token_use_case)
    ],
):
    try:
        user = await auth_use_case.execute(
            login=form_data.username,
            password=form_data.password
        )

        token = await token_use_case.execute(login=user.username)

        return Token(access_token=token, token_type="bearer")

    except NotFoundException as ex:
        ex.log()
        raise HTTPException(404, ex.message)

    except WrongPasswordException as ex:
        ex.log()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ex.message,
            headers={"WWW-Authenticate": "Bearer"},
        )