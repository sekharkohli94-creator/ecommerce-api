"""add cart tables

Revision ID: 8f2550516c8e
Revises: 4ece64fe3f16
Create Date: 2026-08-26 09:01:52.524716

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "8f2550516c8e"
down_revision: Union[str, Sequence[str], None] = "4ece64fe3f16"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Cart tables are already created in the initial migration."""
    pass


def downgrade() -> None:
    """Nothing to downgrade."""
    pass