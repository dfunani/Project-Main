"""Created Tables

Revision ID: 253e5639e327
Revises: 
Create Date: 2022-09-21 21:00:56.375388

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '253e5639e327'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('dev_profile', postgresql.ENUM('Python', 'C', 'Full-Stack', 'Unity', 'Android', name='myUsers2'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Processes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('batch_location', sa.String(length=255), nullable=False),
    sa.Column('project_location', sa.String(length=255), nullable=False),
    sa.Column('next_runtime', sa.DateTime(), nullable=False),
    sa.Column('last_runtime', sa.DateTime(), nullable=False),
    sa.Column('exec_duration', sa.Time(), nullable=True),
    sa.Column('outcome', sa.String(length=50), nullable=True),
    sa.Column('log_location', sa.String(length=255), nullable=True),
    sa.Column('exec_by', sa.Integer(), nullable=True),
    sa.Column('triggers', postgresql.ENUM('Hourly', 'Daily', 'Weekly', 'Monthly', 'Quarter', 'Bi-Annually', 'Yearly', 'Email', name='triggerENUM'), nullable=False),
    sa.Column('args', sa.JSON(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=True),
    sa.Column('createdby', sa.Integer(), nullable=True),
    sa.Column('createdate', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['createdby'], ['User.id'], ),
    sa.ForeignKeyConstraint(['exec_by'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Email',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('process_id', sa.Integer(), nullable=True),
    sa.Column('subject', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['process_id'], ['Processes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Email')
    op.drop_table('Processes')
    op.drop_table('User')
    # ### end Alembic commands ###