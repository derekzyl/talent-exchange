
# services/service_token.py
from typing import Optional
from app.config.database.db import AsyncSession
from app.core.skill_share.model.skill_share_model import SkillShareRequestModel
from app.core.skill_share.model.skill_share_token import TokenSkillModel, TokenSkillTransactionModel

# from app.core.skill_share.services.services_skill_share import SkillShareService
from app.utils import convert_sqlalchemy_dict
from app.utils.crud.service_crud import CrudService
from app.utils.crud.types_crud import ResponseMessage, response_message
from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.sql.expression import desc 
class TokenSkillService(CrudService):
    def __init__(self, db: AsyncSession):
        super().__init__(model=TokenSkillModel, db=db) # type: ignore
    async def get_or_create_user_token(self, user_id: str) -> ResponseMessage:
        token = await self.get_one({"user_id": user_id})
        
        if not token.get('data'):
            token = await self.create({
                "user_id": user_id,
                "balance": 20.0
            })
        
        return token

    async def process_skill_share_token(
        self,
        requester_id: str,
        skill_share_request_id: str,
        token_amount: float = 5.0
    ) -> ResponseMessage:
        # Get or create requester's token account
        requester_token = await self.get_or_create_user_token(requester_id)
        if not requester_token.get('data'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not process token transaction"
            )

        # Check if requester has enough tokens
        converted_data = convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(requester_token['data'])
        if not converted_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not process token transaction"
            )
        
        current_balance = float(converted_data.get('balance', 0))
        if current_balance < token_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient token balance. Required: {token_amount}, Current balance: {current_balance}"
            )

        # Create transaction record
        transaction = await self.db.merge(TokenSkillTransactionModel(
            token_id=converted_data.get('id'),
            skill_share_request_id=skill_share_request_id,
            amount=token_amount,
            transaction_type='DEBIT'
        ))
        
        # Update token balance
        new_balance = current_balance - token_amount
        await self.update(
            filter={"id": converted_data.get('id')},
            data={"balance": new_balance}
        )
        
        await self.db.commit()
        return response_message(
            data={"new_balance": new_balance},
            message="Token transaction processed successfully",
            success_status=True
        )

    async def refund_tokens(
        self,
        requester_id: str,
        skill_share_request_id: str,
        token_amount: float = 5.0
    ) -> ResponseMessage:
        requester_token = await self.get_or_create_user_token(requester_id)
        if not requester_token.get('data'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not process token refund"
            )

        converted_data = convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(requester_token['data'])
        if not converted_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not process token refund"
            )

        # Create refund transaction record
        transaction = await self.db.merge(TokenSkillTransactionModel(
            token_id=converted_data.get('id'),
            skill_share_request_id=skill_share_request_id,
            amount=token_amount,
            transaction_type='CREDIT'
        ))
        
        # Update token balance
        current_balance = float(converted_data.get('balance', 0))
        new_balance = current_balance + token_amount
        await self.update(
            filter={"id": converted_data.get('id')},
            data={"balance": new_balance}
        )
        
        await self.db.commit()
        return response_message(
            data={"new_balance": new_balance},
            message="Token refund processed successfully",
            success_status=True
        )

    async def check_request_ownership(self, skill_share_request_id: str, user_id: str) -> bool:
        # Query the skill share request directly without importing SkillShareService
        query = select(SkillShareRequestModel).where(
            and_(
                SkillShareRequestModel.id == skill_share_request_id,
                SkillShareRequestModel.requester_id == user_id
            )
        )
        result = await self.db.execute(query)
        request = result.scalar_one_or_none()
        return request is not None

    async def purchase_tokens(
        self,
        user_id: str,
        amount: float,
        payment_method: str,
        currency: str = 'USD'
    ) -> ResponseMessage:
        # Get or create user's token account
        user_token = await self.get_or_create_user_token(user_id)
        if not user_token.get('data'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not process token purchase"
            )

        converted_data = convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(user_token['data'])
        if not converted_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not process token purchase"
            )

        # Create purchase transaction record
        transaction = await self.db.merge(TokenSkillTransactionModel(
            token_id=converted_data.get('id'),
            amount=amount,
            transaction_type='PURCHASE',
            payment_method=payment_method,
            currency=currency
        ))

        # Update token balance
        current_balance = float(converted_data.get('balance', 0))
        new_balance = current_balance + amount
        await self.update(
            filter={"id": converted_data.get('id')},
            data={"balance": new_balance}
        )

        await self.db.commit()
        return response_message(
            data={
                "new_balance": new_balance,
                "transaction_id": transaction.id,
                "amount_purchased": amount
            },
            message="Tokens purchased successfully",
            success_status=True
        )

    async def transfer_tokens(
        self,
        sender_id: str,
        recipient_id: str,
        amount: float,
        message: Optional[str] = None
    ) -> ResponseMessage:
        # Check sender's balance
        sender_token = await self.get_or_create_user_token(sender_id)
        if not sender_token.get('data'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not process token transfer"
            )

        sender_data = convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(sender_token['data'])
        if not sender_data or float(sender_data.get('balance', 0)) < amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient token balance for transfer"
            )

        # Get or create recipient's token account
        recipient_token = await self.get_or_create_user_token(recipient_id)
        if not recipient_token.get('data'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Recipient account not found"
            )

        recipient_data = convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(recipient_token['data'])
        if not recipient_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not process token transfer"
            )

        # Create transfer transactions
        sender_transaction = await self.db.merge(TokenSkillTransactionModel(
            token_id=sender_data.get('id'),
            amount=amount,
            transaction_type='TRANSFER_SENT',
            message=message,
            related_user_id=recipient_id
        ))

        recipient_transaction = await self.db.merge(TokenSkillTransactionModel(
            token_id=recipient_data.get('id'),
            amount=amount,
            transaction_type='TRANSFER_RECEIVED',
            message=message,
            related_user_id=sender_id
        ))

        # Update balances
        sender_balance = float(sender_data.get('balance', 0)) - amount
        recipient_balance = float(recipient_data.get('balance', 0)) + amount

        await self.update(
            filter={"id": sender_data.get('id')},
            data={"balance": sender_balance}
        )
        await self.update(
            filter={"id": recipient_data.get('id')},
            data={"balance": recipient_balance}
        )

        await self.db.commit()
        return response_message(
            data={
                "sender_balance": sender_balance,
                "recipient_balance": recipient_balance,
                "amount_transferred": amount
            },
            message="Token transfer completed successfully",
            success_status=True
        )

    async def get_user_transactions(
        self,
        user_id: str,
        limit: int = 10,
        offset: int = 0
    ) -> ResponseMessage:
        # Get user's token account
        token = await self.get_or_create_user_token(user_id)
        if not token.get('data'):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User token account not found"
            )

        token_data = convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(token['data'])
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not fetch transactions"
            )

        # Query transactions
        query = (
            select(TokenSkillTransactionModel)
            .where(TokenSkillTransactionModel.token_id == token_data.get('id'))
            .order_by(desc(TokenSkillTransactionModel.created_at))
            .offset(offset)
            .limit(limit)
        )

        result = await self.db.execute(query)
        transactions = result.scalars().all()
        
        # Convert transactions to dict
        transaction_list = [
            convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(trans)
            for trans in transactions
        ]

        return response_message(
            data={
                "transactions": transaction_list,
                "total": len(transaction_list),
                "current_balance": token_data['balance']
            },
            message="Transactions retrieved successfully",
            success_status=True
        )

    # async def process_refund(
    #     self,
    #     user_id: str,
    #     skill_share_id: str
    # ) -> ResponseMessage:
    #     # This is a manual refund endpoint, separate from the automatic refund in update_share_request_status
    #     # First verify the skill share request exists and belongs to the user
    #     share_service = SkillShareService(self.db)
    #     share_request = await share_service.get_one({"id": skill_share_id})
        
    #     if not share_request.get('data'):
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail="Skill share request not found"
    #         )

    #     share_data = convert_sqlalchemy_dict.sqlalchemy_obj_to_dict(share_request['data'])
    #     if not share_data or share_data.get('requester_id') != user_id:
    #         raise HTTPException(
    #             status_code=status.HTTP_403_FORBIDDEN,
    #             detail="Not authorized to refund this request"
    #         )

    #     # Process the refund
    #     return await self.refund_tokens(
    #         requester_id=user_id,
    #         skill_share_request_id=skill_share_id
    #     )
