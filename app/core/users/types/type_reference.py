from dataclasses import dataclass


@dataclass
class ReferenceCounts:
    id: int
    ref_type: str
    ref_count: int
    business_id: int
    created_at: str
    updated_at: str
