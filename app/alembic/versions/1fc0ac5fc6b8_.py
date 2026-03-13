"""empty message

Revision ID: 1fc0ac5fc6b8
Revises: a62d71ffb020
Create Date: 2026-03-13 12:01:40.226928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fc0ac5fc6b8'
down_revision: Union[str, Sequence[str], None] = 'a62d71ffb020'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
