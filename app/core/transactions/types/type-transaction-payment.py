from dataclasses import dataclass


@dataclass
class TransactionPayment:
    id: int
    transaction_id: int
    type:str  # Consider using a proper enum type if available in your [return, referrals, purchase, inventory]
    amount: float
    business_id: int
    branch_id: int
    method: str
    card_transaction_number: str
    card_number: str
    card_type: str
    card_holder_name: str
    card_month: str
    card_year: str
    card_security: str
    cheque_number: str
    bank_account_number: str
    account_id:str
    payment_date:str
    note: str
    payment_status:str
    is_returned:bool
    payment_for:str
    created_at: str  # Consider using a proper datetime type if available in your Python environment
    updated_at: str  # Consider using a proper datetime type if available in your Python environment
