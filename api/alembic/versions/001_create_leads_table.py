"""create leads table

Revision ID: 001_create_leads
Revises: 
Create Date: 2026-10-10 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_create_leads'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'leads',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('email', sa.String(length=254), nullable=False),
        sa.Column('service_slug', sa.String(length=120), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=20), server_default='new', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("status IN ('new', 'contacted', 'closed')", name='check_lead_status')
    )
    op.create_index('ix_leads_created_at', 'leads', [sa.text('created_at DESC')])


def downgrade() -> None:
    op.drop_index('ix_leads_created_at', table_name='leads')
    op.drop_table('leads')
