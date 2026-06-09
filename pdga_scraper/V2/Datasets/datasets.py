from dataclasses import dataclass, field

@dataclass
class DataSets:
    events: dict = field(default_factory=dict)
    event_divisions: dict = field(default_factory=dict)
    courses: dict = field(default_factory=dict)
    course_layouts: dict = field(default_factory=dict)
    layout_holes: dict = field(default_factory=dict)
    tournament_rounds: dict = field(default_factory=dict)
    player_rounds: dict = field(default_factory=dict)
    player_scores: dict = field(default_factory=dict)
    tournament_player: dict = field(default_factory=dict)
    all_players: dict = field(default_factory=dict)
    player_round_stats: dict = field(default_factory=dict)
    player_hole_stats: dict = field(default_factory=dict)