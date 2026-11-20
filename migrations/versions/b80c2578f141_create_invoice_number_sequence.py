"""create invoice number sequence

Revision ID: b80c2578f141
Revises: 75d9796aab5c
Create Date: 2026-11-11 09:24:17.887798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b80c2578f141'
down_revision: Union[str, Sequence[str], None] = '75d9796aab5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        "CREATE SEQUENCE invoice_number_seq START WITH 1 INCREMENT BY 1"
    )


def downgrade():
    op.execute("DROP SEQUENCE invoice_number_seq")
