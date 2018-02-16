"""
  Each match must have status. When we start new tournament
  the initial status is "NOT_PLANNED". Two teams or admins
  must agree to date, time and place of this match. After it will be
  agreed, the match status will be PLANNED. After this teams can start match.
  If match is started now, the status is LIVE. It can be paused because of
  different issues - bad weather, angry doc on the fotball field and etc.
  If there is no problem, the home (away) team verify result of the match into te system.
  The status is "HOME_VERIFIED" (AWAY_VERIFIED). After this another team verify the result.
  If both results are same, the status is "COMPLETED", in other case the status is "CONFLICT".
  Only manager of ADFS can resolve the conflict.

  By tournament table calculation we use only COMPLETED AND TECHNICAL statuses.
"""

match_statuses = {
    'LIVE': 0,         # Match is going now
    'PLANNED': 1,      # Match is planned and time is taken
    'COMPLETED': 2,    # There is verified result of this match
    'PAUSED': 3,       # Match was in LIVE status, but now it paused. (Because of dog on the stadion)
    'CANCELED': 4,     # Match was in PLANNED status, but canceled by Admins or teams
    'NOT_PLANNED': 5,  # There is no info about this match
    'HOME_VERIFIED': 6 # The home team is grand result of this match
    'AWAY_VERIFIED': 7 # The away team is grand result of this match,
    "CONFLICT": 8,     # If home verified is not equals to away verified
    "TECHNICAL": 9,
}

player_types = {
    'FORWARD': 0,
    'TOWARD': 1,
    'DEFENDER': 2,
}

stadion_types = {
    'HALL': 0,
    'STADION': 1,
    'SCHOOL_FIELD': 2,
    'PARK_FIELD': 3,
    'STREET_FIELD': 4,
}

stadion_cover_types = {
    'GRASS': 0,
    'ASPHALT': 1,
    'GROUND': 2,
    'PARQUET': 3,
    'SYNTETIC': 4,
    'RUBBER': 5,
}