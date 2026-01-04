"""add_oauth_state_table

Revision ID: 15216b40982d
Revises: 75c9c20a8ece
Create Date: 2026-01-04 17:10:37.628076

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15216b40982d'
down_revision: Union[str, None] = '75c9c20a8ece'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create oauth_states table
    op.create_table(
        'oauth_states',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('state', sa.String(length=64), nullable=False),
        sa.Column('provider', sa.String(length=20), nullable=False),
        sa.Column('used', sa.Boolean(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_oauth_states_id'), 'oauth_states', ['id'], unique=False)
    op.create_index(op.f('ix_oauth_states_state'), 'oauth_states', ['state'], unique=True)


def downgrade() -> None:
    # Drop oauth_states table
    op.drop_index(op.f('ix_oauth_states_state'), table_name='oauth_states')
    op.drop_index(op.f('ix_oauth_states_id'), table_name='oauth_states')
    op.drop_table('oauth_states')
