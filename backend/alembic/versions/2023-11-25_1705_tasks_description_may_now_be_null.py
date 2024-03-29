"""tasks description may now be null

Revision ID: 2512a86734f4
Revises: 685dd7e2bc70
Create Date: 2023-11-25 17:05:44.778868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2512a86734f4'
down_revision: Union[str, None] = '685dd7e2bc70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('tasks', 'parent_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'parent_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('tasks', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
