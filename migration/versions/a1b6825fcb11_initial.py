"""'initial'

Revision ID: a1b6825fcb11
Revises: 14b6bfbbd1ec
Create Date: 2024-07-14 16:00:34.860699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b6825fcb11'
down_revision: Union[str, None] = '14b6bfbbd1ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
