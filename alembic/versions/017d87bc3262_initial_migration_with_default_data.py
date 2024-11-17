"""Initial migration with default data

Revision ID: 017d87bc3262
Revises: 
Create Date: 2024-11-16 16:55:52.607849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '017d87bc3262'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    tags_table = op.create_table(
        'tags',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False)
    )

    op.bulk_insert(tags_table, [
        {'name': 'warframe'},
        {'name': 'primary'},
        {'name': 'secondary'},
        {'name': 'melee'},
        {'name': 'necramech'},
        {'name': 'any'}
    ])

    types_table = op.create_table(
        'types',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False)
    )

    op.bulk_insert(types_table, [
        {'name': 'component'},
        {'name': 'arcane_enhancement'},
        {'name': 'mod'},
        {'name': 'any'}
    ])

    op.create_table(
        'items',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name_en', sa.String, nullable=False, unique=True),
        sa.Column('name_es', sa.String, nullable=False),
        sa.Column('url_name', sa.String, nullable=False),
        sa.Column('icon', sa.String, nullable=False),
        sa.Column('tag_id', sa.Integer, sa.ForeignKey('tags.id'), nullable=True),
        sa.Column('type_id', sa.Integer, sa.ForeignKey('types.id'), nullable=True)
    )

    op.create_table(
        'forty_eight_hours',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('volume', sa.Integer, nullable=False),
        sa.Column('avg_price', sa.Numeric, nullable=False),
        sa.Column('rank', sa.Integer, nullable=False),
        sa.Column('item_id', sa.Integer, sa.ForeignKey('items.id', ondelete='CASCADE'), nullable=True)
    )

    op.create_table(
        'ninety_days',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('volume', sa.Integer, nullable=False),
        sa.Column('avg_price', sa.Numeric, nullable=False),
        sa.Column('rank', sa.Integer, nullable=False),
        sa.Column('item_id', sa.Integer, sa.ForeignKey('items.id', ondelete='CASCADE'), nullable=True)
    )


def downgrade():
    op.drop_table('ninety_days')
    op.drop_table('forty_eight_hours')
    op.drop_table('items')
    op.drop_table('types')
    op.drop_table('tags')
