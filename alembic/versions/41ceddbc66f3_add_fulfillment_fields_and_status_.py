"""add_fulfillment_fields_and_status_constraints

Revision ID: 41ceddbc66f3
Revises: 73dc54a4bbd8
Create Date: 2026-04-06 12:52:46.355002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41ceddbc66f3'
down_revision: Union[str, Sequence[str], None] = '73dc54a4bbd8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add status CheckConstraint to Order
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'chk_order_status',
            "status IN ('draft', 'submitted', 'processing', 'partially_dispatched', 'dispatched', 'delivered', 'cancelled', 'rejected')"
        )

    # Add fulfilled_quantity and constraints to OrderItem
    with op.batch_alter_table('order_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fulfilled_quantity', sa.Integer(), nullable=False, server_default='0'))
        batch_op.create_check_constraint('chk_order_item_fulfilled_quantity', 'fulfilled_quantity >= 0')
        batch_op.create_check_constraint('chk_order_item_fulfillment_limit', 'fulfilled_quantity <= quantity')

    # Add status CheckConstraint to DispatchBatch
    with op.batch_alter_table('dispatch_batch', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'chk_batch_status',
            "status IN ('draft', 'consolidated', 'confirmed', 'shipped', 'cancelled')"
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('dispatch_batch', schema=None) as batch_op:
        batch_op.drop_constraint('chk_batch_status', type_='check')

    with op.batch_alter_table('order_item', schema=None) as batch_op:
        batch_op.drop_constraint('chk_order_item_fulfillment_limit', type_='check')
        batch_op.drop_constraint('chk_order_item_fulfilled_quantity', type_='check')
        batch_op.drop_column('fulfilled_quantity')

    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.drop_constraint('chk_order_status', type_='check')
