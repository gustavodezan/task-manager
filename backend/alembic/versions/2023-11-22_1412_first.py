"""first

Revision ID: f1753a41ea53
Revises: 
Create Date: 2023-11-22 14:12:32.708981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision: str = 'f1753a41ea53'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_id'), 'comments', ['id'], unique=False)
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(), nullable=False),
    sa.Column('color', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tags_id'), 'tags', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(), nullable=False),
    sa.Column('email', sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('profile_pic', sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('access_level', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('workspaces',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workspaces_id'), 'workspaces', ['id'], unique=False)
    op.create_table('subtasks',
    sa.Column('child_id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['child_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('child_id', 'parent_id')
    )
    op.create_table('teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(), nullable=False),
    sa.Column('slug', sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.Column('workspace_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teams_id'), 'teams', ['id'], unique=False)
    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(), nullable=False),
    sa.Column('color', sa.String(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(), nullable=False),
    sa.Column('description', sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(), nullable=False),
    sa.Column('start_at', sa.DateTime(), nullable=True),
    sa.Column('due_on', sa.DateTime(), nullable=True),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.Column('color', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
    op.drop_index(op.f('ix_projects_id'), table_name='projects')
    op.drop_table('projects')
    op.drop_index(op.f('ix_teams_id'), table_name='teams')
    op.drop_table('teams')
    op.drop_table('subtasks')
    op.drop_index(op.f('ix_workspaces_id'), table_name='workspaces')
    op.drop_table('workspaces')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_tags_id'), table_name='tags')
    op.drop_table('tags')
    op.drop_index(op.f('ix_comments_id'), table_name='comments')
    op.drop_table('comments')
    # ### end Alembic commands ###
