"""Create models

Revision ID: 0cad6b1092fe
Revises: 
Create Date: 2025-04-23 02:17:48.456175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0cad6b1092fe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('tg_group_id', sa.BigInteger(), nullable=False),
    sa.Column('status', sa.Enum('PREPARATION', 'REGISTRATION', 'ACTIVE', 'FINISHED', 'CANCELED', name='game_status'), server_default='PREPARATION', nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('winners', sa.Integer(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_game_tg_group_id'), 'game', ['tg_group_id'], unique=False)
    op.create_table('session',
    sa.Column('session_key', sa.UUID(), nullable=False),
    sa.Column('session_data', sa.String(), nullable=False),
    sa.Column('expire_date', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('session_key')
    )
    op.create_index('idx_session_key_expire_date', 'session', ['session_key', 'expire_date'], unique=False)
    op.create_table('theme',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), server_default='false', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game_player',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('game_id', sa.BigInteger(), nullable=False),
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('track', sa.Enum('RED', 'YELLOW', 'GREEN', name='track_color'), nullable=False),
    sa.Column('correct_answers', sa.Integer(), server_default='0', nullable=False),
    sa.Column('incorrect_answers', sa.Integer(), server_default='0', nullable=False),
    sa.Column('in_game', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('place', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_game_player_game_id'), 'game_player', ['game_id'], unique=False)
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('theme_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('SINGLE', 'MULTI', name='question_type'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['theme_id'], ['theme.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_question_theme_id'), 'question', ['theme_id'], unique=False)
    op.create_index(op.f('ix_question_user_id'), 'question', ['user_id'], unique=False)
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_answer_question_id'), 'answer', ['question_id'], unique=False)
    op.create_table('game_round',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('game_id', sa.BigInteger(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.BigInteger(), nullable=False),
    sa.Column('answer', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['player_id'], ['game_player.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_game_round_game_id'), 'game_round', ['game_id'], unique=False)
    op.create_index(op.f('ix_game_round_player_id'), 'game_round', ['player_id'], unique=False)
    op.create_index(op.f('ix_game_round_question_id'), 'game_round', ['question_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_game_round_question_id'), table_name='game_round')
    op.drop_index(op.f('ix_game_round_player_id'), table_name='game_round')
    op.drop_index(op.f('ix_game_round_game_id'), table_name='game_round')
    op.drop_table('game_round')
    op.drop_index(op.f('ix_answer_question_id'), table_name='answer')
    op.drop_table('answer')
    op.drop_index(op.f('ix_question_user_id'), table_name='question')
    op.drop_index(op.f('ix_question_theme_id'), table_name='question')
    op.drop_table('question')
    op.drop_index(op.f('ix_game_player_game_id'), table_name='game_player')
    op.drop_table('game_player')
    op.drop_table('user')
    op.drop_table('theme')
    op.drop_index('idx_session_key_expire_date', table_name='session')
    op.drop_table('session')
    op.drop_index(op.f('ix_game_tg_group_id'), table_name='game')
    op.drop_table('game')
    # ### end Alembic commands ###
