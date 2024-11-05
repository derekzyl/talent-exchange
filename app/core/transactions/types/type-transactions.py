from dataclasses import dataclass


@dataclass
class Transaction:
    id: int
    business_id: int
    branch_id: int
    type: str # sell purchase, return, expense, transfer, adjustment, journal, payment, receiptpurchase','sell', 'expense', 'stock_adjustment', 'sell_transfer', 'purchase_transfer', 
            # 'opening_stock', 'sell_return', 'opening_balanc
    status: str
    payment_status: str
    contact_id: int
    invoice_no: str
    ref_no: str
    transaction_date: str
    total_before_tax: float
    tax_id: int
    tax_amount: float
    discount_type: str
    discount_amount: float
    shipping_details: str
    shipping_charges: float
    additional_notes: str
    staff_note: str
    final_total: float
    created_by: int
    created_at: str  # Consider using a proper datetime type if available in your Python environment
    updated_at: str  # Consider using a proper datetime type if available in your Python environment
    document:str
    expense_id: int
    expense_type: str
    shipping_address: str
    delivered_to: str
    expense_for: str
    expense_by:str
