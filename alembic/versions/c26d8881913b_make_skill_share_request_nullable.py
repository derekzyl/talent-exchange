"""make skill share request nullable

Revision ID: c26d8881913b
Revises: a53c6405c318
Create Date: 2025-02-02 12:32:51.930005

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c26d8881913b'
down_revision: Union[str, None] = 'a53c6405c318'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # First drop the foreign key constraints
    op.drop_constraint(
        'REVIEWS_skill_share_id_fkey',
        'REVIEWS',
        type_='foreignkey'
    )
    
    op.drop_constraint(
        'ONGOING_SKILL_SHARES_skill_share_id_fkey',
        'ONGOING_SKILL_SHARES',
        type_='foreignkey'
    )
    
    op.drop_constraint(
        'SKILL_TOKEN_TRANSACTIONS_skill_share_request_id_fkey',
        'SKILL_TOKEN_TRANSACTIONS',
        type_='foreignkey'
    )

    # Now make skill_share_request_id nullable in SKILL_TOKEN_TRANSACTIONS
    op.alter_column('SKILL_TOKEN_TRANSACTIONS',
                    'skill_share_request_id',
                    existing_type=sa.VARCHAR(),
                    nullable=True)

    # Re-create the foreign key constraints with ON DELETE SET NULL
    op.create_foreign_key(
        'SKILL_TOKEN_TRANSACTIONS_skill_share_request_id_fkey',
        'SKILL_TOKEN_TRANSACTIONS',
        'SKILL_SHARE_REQUESTS',
        ['skill_share_request_id'],
        ['id'],
        ondelete='SET NULL'
    )

    op.create_foreign_key(
        'REVIEWS_skill_share_id_fkey',
        'REVIEWS',
        'SKILL_SHARE_REQUESTS',
        ['skill_share_id'],
        ['id'],
        ondelete='CASCADE'
    )

    op.create_foreign_key(
        'ONGOING_SKILL_SHARES_skill_share_id_fkey',
        'ONGOING_SKILL_SHARES',
        'SKILL_SHARE_REQUESTS',
        ['skill_share_id'],
        ['id'],
        ondelete='CASCADE'
    )

def downgrade():
    # First drop the foreign key constraints
    op.drop_constraint(
        'SKILL_TOKEN_TRANSACTIONS_skill_share_request_id_fkey',
        'SKILL_TOKEN_TRANSACTIONS',
        type_='foreignkey'
    )
    
    op.drop_constraint(
        'REVIEWS_skill_share_id_fkey',
        'REVIEWS',
        type_='foreignkey'
    )
    
    op.drop_constraint(
        'ONGOING_SKILL_SHARES_skill_share_id_fkey',
        'ONGOING_SKILL_SHARES',
        type_='foreignkey'
    )

    # Make skill_share_request_id not nullable again
    op.alter_column('SKILL_TOKEN_TRANSACTIONS',
                    'skill_share_request_id',
                    existing_type=sa.VARCHAR(),
                    nullable=False)

    # Re-create the original foreign key constraints
    op.create_foreign_key(
        'SKILL_TOKEN_TRANSACTIONS_skill_share_request_id_fkey',
        'SKILL_TOKEN_TRANSACTIONS',
        'SKILL_SHARE_REQUESTS',
        ['skill_share_request_id'],
        ['id']
    )

    op.create_foreign_key(
        'REVIEWS_skill_share_id_fkey',
        'REVIEWS',
        'SKILL_SHARE_REQUESTS',
        ['skill_share_id'],
        ['id']
    )

    op.create_foreign_key(
        'ONGOING_SKILL_SHARES_skill_share_id_fkey',
        'ONGOING_SKILL_SHARES',
        'SKILL_SHARE_REQUESTS',
        ['skill_share_id'],
        ['id']
    )
