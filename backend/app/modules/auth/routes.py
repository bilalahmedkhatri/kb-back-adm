from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.common.email import generate_reset_password_email, send_email
from app.core import security
from app.core.config import settings
from app.modules.auth.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.modules.auth.models import Message, NewPassword, Token
from app.modules.auth.service import (
    generate_password_reset_token,
    verify_password_reset_token,
)
from app.modules.users.schemas import UserPublic, UserUpdate
from app.modules.users.service import authenticate, get_user_by_email, update_user

router = APIRouter(tags=["login"])


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


from app.modules.auth.models import Message, NewPassword, Token, GoogleLoginInput


@router.post("/auth/google", response_model=Token)
def login_google(
    *,
    session: SessionDep,
    google_in: GoogleLoginInput,
) -> Token:
    """
    Google OAuth 2.0 One-Tap / SSO Login Endpoint
    """
    import uuid
    from app.modules.users.models import User, UserRole
    from app.modules.users.service import create_user
    from app.modules.users.schemas import UserCreate

    email = google_in.email or f"google_{uuid.uuid4().hex[:6]}@example.com"
    
    user = get_user_by_email(session=session, email=email)
    if not user:
        user_create = UserCreate(
            email=email,
            password=uuid.uuid4().hex,
            full_name=google_in.full_name or email.split("@")[0],
        )
        user = create_user(session=session, user_create=user_create)
        cred = google_in.credential or google_in.token or "google_token"
        user.avatar_url = google_in.avatar_url
        user.google_sub = cred[:250]
        session.add(user)
        session.commit()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}")
def recover_password(email: str, session: SessionDep) -> Message:
    """
    Password Recovery
    """
    user = get_user_by_email(session=session, email=email)

    if user:
        password_reset_token = generate_password_reset_token(email=email)
        email_data = generate_reset_password_email(
            email_to=user.email, email=email, token=password_reset_token
        )
        send_email(
            email_to=user.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return Message(
        message="If that email is registered, we sent a password recovery link"
    )


@router.post("/reset-password/")
def reset_password(session: SessionDep, body: NewPassword) -> Message:
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    user_in_update = UserUpdate(password=body.new_password)
    update_user(
        session=session,
        db_user=user,
        user_in=user_in_update,
    )
    return Message(message="Password updated successfully")


@router.post(
    "/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_class=HTMLResponse,
)
def recover_password_html_content(email: str, session: SessionDep) -> Any:
    """
    HTML Content for Password Recovery
    """
    user = get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )

    return HTMLResponse(
        content=email_data.html_content, headers={"subject:": email_data.subject}
    )
