from dataclasses import dataclass


@dataclass
class Contact:
    id: int
    business_id: int
    type: str
    supplier_business_name: str
    name: str
    tax_number: str
    city: str
    state: str
    country: str
    landmark: str
    mobile: str
    landline: str
    alternate_number: str
    pay_term_number: int
    pay_term_type: str
    credit_limit:float
    created_by: int
    is_default: bool
    created_at: str  # Consider using a proper datetime type if available in your Python environment
    updated_at: str  # Consider using a proper datetime type if available in your Python environment
