from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database.db import get_db
from app.core.skill_share.services.token_share import TokenSkillService
from app.core.users.services.service_user import UserService
from app.core.users.types.type_user import UserT
from app.utils.crud.service_crud import ResponseMessage

token_router = APIRouter()


@token_router.get("/balance", response_model=ResponseMessage)
async def get_token_balance(
    current_user: Annotated[UserT, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Get the token balance for the current user"""
    service = TokenSkillService(db)
    return await service.get_or_create_user_token(current_user["id"])

@token_router.post("/purchase", response_model=ResponseMessage)
async def purchase_tokens(
    purchase_data: Any,
    current_user: Annotated[UserT, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Purchase tokens"""
    service = TokenSkillService(db)
    return await service.purchase_tokens(mc      user_id=current_user["id"],
        amount=purchase_data.amount,
        payment_method=purchase_data.payment_method,
        currency=purchase_data.currency
    )

@token_router.post("/transfer", response_model=ResponseMessage)
async def transfer_tokens(
    transfer_data: Any,
    current_user: Annotated[UserT, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Transfer tokens to another user"""
    service = TokenSkillService(db)
    return await service.transfer_tokens(
        sender_id=current_user["id"],
        recipient_id=transfer_data.recipient_id,
        amount=transfer_data.amount,
        message=transfer_data.message
    )

@token_router.get("/transactions", response_model=ResponseMessage)
async def get_token_transactions(
    current_user: Annotated[UserT, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = 10,
    offset: int = 0
):
    """Get token transaction history"""
    service = TokenSkillService(db)
    return await service.get_user_transactions(
        user_id=current_user["id"],
        limit=limit,
        offset=offset
    )

@token_router.post("/refund/{skill_share_id}", response_model=ResponseMessage)
async def refund_tokens(
    skill_share_id: str,
    current_user: Annotated[UserT, Depends(UserService.get_logged_in_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Refund tokens for a canceled skill share request"""
    service = TokenSkillService(db)
    return await service.process_refund(
        user_id=current_user["id"],
        skill_share_id=skill_share_id
    )
