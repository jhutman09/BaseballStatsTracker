"""rename team to roster, team_roster to roster_entry

Revision ID: 57aef2887346
Revises: 36936b7b91ff
Create Date: 2026-09-16 15:56:36.541674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57aef2887346'
down_revision: Union[str, None] = '36936b7b91ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('rosters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('season_id', sa.Integer(), nullable=False),
    sa.Column('club_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['club_id'], ['clubs.id'], ),
    sa.ForeignKeyConstraint(['season_id'], ['seasons.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('season_id', 'club_id', name='uq_roster_season_club'),
    sa.UniqueConstraint('season_id', 'name', name='uq_roster_season_name')
    )
    op.create_table('roster_entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.Column('roster_id', sa.Integer(), nullable=False),
    sa.Column('jersey_number', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], ),
    sa.ForeignKeyConstraint(['roster_id'], ['rosters.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('player_id', 'roster_id', name='uq_roster_entry_player_roster')
    )

    # Drop everything that references 'teams' before dropping 'teams' itself.
    op.drop_table('team_rosters')

    op.add_column('batting_lines', sa.Column('roster_id', sa.Integer(), nullable=False))
    op.drop_constraint('batting_lines_team_id_fkey', 'batting_lines', type_='foreignkey')
    op.drop_column('batting_lines', 'team_id')
    op.create_foreign_key(None, 'batting_lines', 'rosters', ['roster_id'], ['id'])

    op.add_column('games', sa.Column('home_roster_id', sa.Integer(), nullable=False))
    op.add_column('games', sa.Column('away_roster_id', sa.Integer(), nullable=False))
    op.drop_constraint('games_home_team_id_fkey', 'games', type_='foreignkey')
    op.drop_constraint('games_away_team_id_fkey', 'games', type_='foreignkey')
    op.drop_column('games', 'away_team_id')
    op.drop_column('games', 'home_team_id')
    op.create_foreign_key(None, 'games', 'rosters', ['away_roster_id'], ['id'])
    op.create_foreign_key(None, 'games', 'rosters', ['home_roster_id'], ['id'])

    op.add_column('pitching_appearances', sa.Column('roster_id', sa.Integer(), nullable=False))
    op.drop_constraint('pitching_appearances_team_id_fkey', 'pitching_appearances', type_='foreignkey')
    op.drop_column('pitching_appearances', 'team_id')
    op.create_foreign_key(None, 'pitching_appearances', 'rosters', ['roster_id'], ['id'])

    op.drop_table('teams')


def downgrade() -> None:
    op.create_table('teams',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('season_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('club_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['club_id'], ['clubs.id'], name='teams_club_id_fkey'),
    sa.ForeignKeyConstraint(['season_id'], ['seasons.id'], name='teams_season_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='teams_pkey'),
    sa.UniqueConstraint('season_id', 'club_id', name='uq_team_season_club'),
    sa.UniqueConstraint('season_id', 'name', name='uq_team_season_name')
    )

    op.add_column('pitching_appearances', sa.Column('team_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'pitching_appearances', type_='foreignkey')
    op.drop_column('pitching_appearances', 'roster_id')
    op.create_foreign_key('pitching_appearances_team_id_fkey', 'pitching_appearances', 'teams', ['team_id'], ['id'])

    op.add_column('games', sa.Column('home_team_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('games', sa.Column('away_team_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'games', type_='foreignkey')
    op.drop_constraint(None, 'games', type_='foreignkey')
    op.drop_column('games', 'away_roster_id')
    op.drop_column('games', 'home_roster_id')
    op.create_foreign_key('games_away_team_id_fkey', 'games', 'teams', ['away_team_id'], ['id'])
    op.create_foreign_key('games_home_team_id_fkey', 'games', 'teams', ['home_team_id'], ['id'])

    op.add_column('batting_lines', sa.Column('team_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'batting_lines', type_='foreignkey')
    op.drop_column('batting_lines', 'roster_id')
    op.create_foreign_key('batting_lines_team_id_fkey', 'batting_lines', 'teams', ['team_id'], ['id'])

    op.create_table('team_rosters',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('player_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('team_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('jersey_number', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], name='team_rosters_player_id_fkey'),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], name='team_rosters_team_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='team_rosters_pkey'),
    sa.UniqueConstraint('player_id', 'team_id', name='uq_roster_player_team')
    )

    op.drop_table('roster_entries')
    op.drop_table('rosters')
