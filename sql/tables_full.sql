CREATE TABLE IF NOT EXISTS users (
  user_id bigint PRIMARY KEY,
  username text UNIQUE,
  password text,
  steam_id text,
  account_id text
);

CREATE TABLE IF NOT EXISTS heroes_matchups (
  PRIMARY KEY(hero, hero_id),
  hero bigint,
  hero_id bigint,
  games_played text,
  wins text
);

CREATE TABLE IF NOT EXISTS heroes_durations (
  PRIMARY KEY(hero_id, duration_bin),
  hero_id bigint,
  duration_bin bigint,
  games_played text,
  wins text
);

CREATE TABLE IF NOT EXISTS hero_stats (
  id bigint PRIMARY KEY,
  name text,
  localized_name text,
  img text,
  icon text,
  pro_win text,
  pro_pick text,
  hero_id text,
  pro_ban text
);

CREATE TABLE IF NOT EXISTS rankings (
  PRIMARY KEY(hero_id, account_id),
  hero_id bigint,
  account_id text,
  score text
);






CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS tsm_system_rows;

CREATE TABLE IF NOT EXISTS matches (
  match_id bigint PRIMARY KEY,
  match_seq_num bigint,
  radiant_win boolean,
  start_time integer,
  duration integer,
  tower_status_radiant integer,
  tower_status_dire integer,
  barracks_status_radiant integer,
  barracks_status_dire integer,
  cluster integer,
  first_blood_time integer,
  lobby_type integer,
  human_players integer,
  leagueid integer,
  positive_votes integer,
  negative_votes integer,
  game_mode integer,
  engine integer,
  radiant_score integer,
  dire_score integer,
  picks_bans text,
  radiant_team_id integer,
  dire_team_id integer,
  radiant_team_name text,
  dire_team_name text,
  radiant_team_complete smallint,
  dire_team_complete smallint,
  radiant_captain bigint,
  dire_captain bigint,
  chat text,
  objectives text,
  radiant_gold_adv text,
  radiant_xp_adv text,
  teamfights text,
  draft_timings text,
  version integer,
  cosmetics text
);
CREATE INDEX IF NOT EXISTS matches_leagueid_idx on matches(leagueid) WHERE leagueid > 0;

CREATE TABLE IF NOT EXISTS player_matches (
  PRIMARY KEY(match_id, player_slot),
  match_id bigint REFERENCES matches(match_id) ON DELETE CASCADE,
  account_id bigint,
  player_slot integer,
  hero_id integer,
  item_0 integer,
  item_1 integer,
  item_2 integer,
  item_3 integer,
  item_4 integer,
  item_5 integer,
  backpack_0 integer,
  backpack_1 integer,
  backpack_2 integer,
  kills integer,
  deaths integer,
  assists integer,
  leaver_status integer,
  gold integer,
  last_hits integer,
  denies integer,
  gold_per_min integer,
  xp_per_min integer,
  gold_spent integer,
  hero_damage integer,
  tower_damage bigint,
  hero_healing bigint,
  level integer,
  --ability_upgrades text,
  additional_units text,
  --parsed fields below
  stuns real,
  max_hero_hit text,
  times text,
  gold_t text,
  lh_t text,
  dn_t text,
  xp_t text,
  obs_log text,
  sen_log text,
  obs_left_log text,
  sen_left_log text,
  purchase_log text,
  kills_log text,
  buyback_log text,
  runes_log text,
  lane_pos text,
  obs text,
  sen text,
  actions text,
  pings text,
  purchase text,
  gold_reasons text,
  xp_reasons text,
  killed text,
  item_uses text,
  ability_uses text,
  ability_targets text,
  damage_targets text,
  hero_hits text,
  damage text,
  damage_taken text,
  damage_inflictor text,
  runes text,
  killed_by text,
  kill_streaks text,
  multi_kills text,
  life_state text,
  damage_inflictor_received text,
  obs_placed int,
  sen_placed int,
  creeps_stacked int,
  camps_stacked int,
  rune_pickups int,
  ability_upgrades_arr text,
  party_id int,
  permanent_buffs text,
  lane int,
  lane_role int,
  is_roaming boolean,
  firstblood_claimed int,
  teamfight_participation real,
  towers_killed int,
  roshans_killed int,
  observers_placed int,
  party_size int
);
CREATE INDEX IF NOT EXISTS player_matches_account_id_idx on player_matches(account_id) WHERE account_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS player_matches_hero_id_idx on player_matches(hero_id);

CREATE TABLE IF NOT EXISTS players (
  account_id bigint PRIMARY KEY,
  steamid text,
  avatar text,
  avatarmedium text,
  avatarfull text,
  profileurl text,
  personaname text,
  last_login timestamp with time zone,
  full_history_time timestamp with time zone,
  cheese integer DEFAULT 0,
  fh_unavailable boolean,
  loccountrycode text,
  last_match_time timestamp with time zone
  /*
    "communityvisibilitystate" : 3,
    "lastlogoff" : 1426020853,
    "loccityid" : 44807,
    "locstatecode" : "16",
    "personastate" : 0,
    "personastateflags" : 0,
    "primaryclanid" : "103582791433775490",
    "profilestate" : 1,
    "realname" : "Alper",
    "timecreated" : 1332289262,
  */
);
CREATE INDEX IF NOT EXISTS players_cheese_idx on players(cheese) WHERE cheese IS NOT NULL AND cheese > 0;
CREATE INDEX IF NOT EXISTS players_personaname_idx on players USING GIN(personaname gin_trgm_ops);

CREATE TABLE IF NOT EXISTS player_ratings (
  PRIMARY KEY(account_id, time),
  account_id bigint,
  match_id bigint,
  solo_competitive_rank integer,
  competitive_rank integer,
  time timestamp with time zone
);

CREATE TABLE IF NOT EXISTS subscriptions (
  PRIMARY KEY(customer_id),
  account_id bigint REFERENCES players(account_id) ON DELETE CASCADE,
  customer_id text,
  amount int,
  active_until date
);
CREATE INDEX IF NOT EXISTS subscriptions_account_id_idx on subscriptions(account_id);
CREATE INDEX IF NOT EXISTS subscriptions_customer_id_idx on subscriptions(customer_id);

CREATE TABLE IF NOT EXISTS api_keys (
  PRIMARY KEY(account_id),
  account_id bigint UNIQUE,
  api_key uuid UNIQUE,
  customer_id text
);
CREATE INDEX IF NOT EXISTS api_keys_account_id_idx on api_keys(account_id);

CREATE TABLE IF NOT EXISTS api_key_usage (
  PRIMARY KEY(account_id, api_key, timestamp),
  account_id bigint REFERENCES api_keys(account_id),
  customer_id text,
  api_key uuid,
  usage_count bigint,
  ip text,
  timestamp timestamp default current_timestamp
);
CREATE INDEX IF NOT EXISTS api_keys_usage_account_id_idx on api_key_usage(account_id);
CREATE INDEX IF NOT EXISTS api_keys_usage_timestamp_idx on api_key_usage(timestamp);

CREATE TABLE IF NOT EXISTS user_usage (
  account_id bigint,
  ip text,
  usage_count bigint,
  timestamp timestamp default current_timestamp
);
CREATE INDEX IF NOT EXISTS user_usage_account_id_idx on user_usage(account_id);
CREATE INDEX IF NOT EXISTS user_usage_timestamp_idx on user_usage(timestamp);
CREATE UNIQUE INDEX IF NOT EXISTS user_usage_unique_idx on user_usage(account_id, ip, timestamp);

CREATE TABLE IF NOT EXISTS notable_players (
  account_id bigint PRIMARY KEY,
  name text,
  country_code text,
  fantasy_role int,
  team_id int,
  team_name text,
  team_tag text,
  is_locked boolean,
  is_pro boolean,
  locked_until integer
);

CREATE TABLE IF NOT EXISTS match_logs (
  match_id bigint REFERENCES matches(match_id) ON DELETE CASCADE,
  time int,
  type text,
  team smallint,
  unit text,
  key text,
  value int,
  slot smallint,
  player_slot smallint,
  player1 int,
  player2 int,
  attackerhero boolean,
  targethero boolean,
  attackerillusion boolean,
  targetillusion boolean,
  inflictor text,
  gold_reason smallint,
  xp_reason smallint,
  attackername text,
  targetname text,
  sourcename text,
  targetsourcename text,
  valuename text,
  gold int,
  lh int,
  xp int,
  x smallint,
  y smallint,
  z smallint,
  entityleft boolean,
  ehandle int,
  stuns real,
  hero_id smallint,
  life_state smallint,
  level smallint,
  kills smallint,
  deaths smallint,
  assists smallint,
  denies smallint,
  attackername_slot smallint,
  targetname_slot smallint,
  sourcename_slot smallint,
  targetsourcename_slot smallint,
  player1_slot smallint,
  obs_placed int,
  sen_placed int,
  creeps_stacked int,
  camps_stacked int,
  rune_pickups int
);
CREATE INDEX IF NOT EXISTS match_logs_match_id_idx ON match_logs(match_id);
CREATE INDEX IF NOT EXISTS match_logs_match_id_player_slot_idx ON match_logs(match_id, player_slot) WHERE player_slot IS NOT NULL;
CREATE INDEX IF NOT EXISTS match_logs_match_id_player1_slot_idx ON match_logs(match_id, player1_slot) WHERE player1_slot IS NOT NULL;
CREATE INDEX IF NOT EXISTS match_logs_match_id_attackername_slot_idx ON match_logs(match_id, attackername_slot) WHERE attackername_slot IS NOT NULL;
CREATE INDEX IF NOT EXISTS match_logs_match_id_targetname_slot_idx ON match_logs(match_id, targetname_slot) WHERE targetname_slot IS NOT NULL;
CREATE INDEX IF NOT EXISTS match_logs_match_id_sourcename_slot_idx ON match_logs(match_id, sourcename_slot) WHERE sourcename_slot IS NOT NULL;
CREATE INDEX IF NOT EXISTS match_logs_match_id_targetsourcename_slot_idx ON match_logs(match_id, targetsourcename_slot) WHERE targetsourcename_slot IS NOT NULL;
CREATE INDEX IF NOT EXISTS match_logs_match_id_valuename_idx ON match_logs(match_id, valuename) WHERE valuename IS NOT NULL;
CREATE INDEX IF NOT EXISTS match_logs_match_id_type_idx ON match_logs(match_id, type);
CREATE INDEX IF NOT EXISTS match_logs_valuename_idx ON match_logs(valuename) WHERE valuename IS NOT NULL;
CREATE INDEX IF NOT EXISTS match_logs_type_idx ON match_logs(type);

CREATE TABLE IF NOT EXISTS picks_bans(
  match_id bigint REFERENCES matches(match_id) ON DELETE CASCADE,
  is_pick boolean,
  hero_id int,
  team smallint,
  ord smallint,
  PRIMARY KEY (match_id, ord)
);

CREATE TABLE IF NOT EXISTS leagues(
  leagueid bigint PRIMARY KEY,
  ticket text,
  banner text,
  tier text,
  name text
);

CREATE TABLE IF NOT EXISTS teams(
  team_id bigint PRIMARY KEY,
  name text,
  tag text,
  logo_url text
);

CREATE TABLE IF NOT EXISTS heroes(
  id int PRIMARY KEY,
  name text,
  localized_name text,
  primary_attr text,
  attack_type text,
  roles text,
  img text
);

CREATE TABLE IF NOT EXISTS match_patch(
  match_id bigint REFERENCES matches(match_id) ON DELETE CASCADE PRIMARY KEY,
  patch text
);

CREATE TABLE IF NOT EXISTS team_match(
  team_id bigint,
  match_id bigint REFERENCES matches(match_id) ON DELETE CASCADE,
  radiant boolean,
  PRIMARY KEY(team_id, match_id)
);

CREATE TABLE IF NOT EXISTS match_gcdata(
  match_id bigint PRIMARY KEY,
  cluster int,
  replay_salt int,
  series_id int,
  series_type int
);

CREATE TABLE IF NOT EXISTS items(
  id int PRIMARY KEY,
  name text,
  cost int,
  secret_shop smallint,
  side_shop smallint,
  recipe smallint,
  localized_name text
);

CREATE TABLE IF NOT EXISTS cosmetics(
  item_id int PRIMARY KEY,
  name text,
  prefab text,
  creation_date timestamp with time zone,
  image_inventory text,
  image_path text,
  item_description text,
  item_name text,
  item_rarity text,
  item_type_name text,
  used_by_heroes text
);

CREATE TABLE IF NOT EXISTS public_matches (
  match_id bigint PRIMARY KEY,
  match_seq_num bigint,
  radiant_win boolean,
  start_time integer,
  duration integer,
  avg_mmr integer,
  num_mmr integer,
  lobby_type integer,
  game_mode integer,
  avg_rank_tier double precision,
  num_rank_tier integer,
  cluster integer
);
CREATE INDEX IF NOT EXISTS public_matches_start_time_idx on public_matches(start_time);
CREATE INDEX IF NOT EXISTS public_matches_avg_mmr_idx on public_matches(avg_mmr);
CREATE INDEX IF NOT EXISTS public_matches_avg_rank_tier_idx on public_matches(avg_rank_tier) WHERE avg_rank_tier IS NOT NULL;

CREATE TABLE IF NOT EXISTS public_player_matches (
  PRIMARY KEY(match_id, player_slot),
  match_id bigint REFERENCES public_matches(match_id) ON DELETE CASCADE,
  player_slot integer,
  hero_id integer
);
CREATE INDEX IF NOT EXISTS public_player_matches_hero_id_idx on public_player_matches(hero_id);
CREATE INDEX IF NOT EXISTS public_player_matches_match_id_idx on public_player_matches(match_id);

CREATE TABLE IF NOT EXISTS team_rating (
  PRIMARY KEY(team_id),
  team_id bigint,
  rating real,
  wins int,
  losses int,
  last_match_time bigint
);
CREATE INDEX IF NOT EXISTS team_rating_rating_idx ON team_rating(rating);

CREATE TABLE IF NOT EXISTS hero_ranking (
  PRIMARY KEY (account_id, hero_id),
  account_id bigint,
  hero_id int,
  score double precision
);
CREATE INDEX IF NOT EXISTS hero_ranking_hero_id_score_idx ON hero_ranking(hero_id, score);

CREATE TABLE IF NOT EXISTS queue (
  PRIMARY KEY (id),
  id bigserial,
  type text,
  timestamp timestamp with time zone,
  attempts int,
  data text,
  next_attempt_time timestamp with time zone,
  priority int
);
CREATE INDEX IF NOT EXISTS queue_priority_id_idx on queue(priority, id);

CREATE TABLE IF NOT EXISTS mmr_estimates (
  PRIMARY KEY (account_id),
  account_id bigint,
  estimate int
);

CREATE TABLE IF NOT EXISTS solo_competitive_rank (
  PRIMARY KEY (account_id),
  account_id bigint,
  rating int
);

CREATE TABLE IF NOT EXISTS competitive_rank (
  PRIMARY KEY (account_id),
  account_id bigint,
  rating int
);

CREATE TABLE IF NOT EXISTS rank_tier (
  PRIMARY KEY (account_id),
  account_id bigint,
  rating int
);

CREATE TABLE IF NOT EXISTS leaderboard_rank (
  PRIMARY KEY (account_id),
  account_id bigint,
  rating int
);

CREATE TABLE IF NOT EXISTS scenarios (
  hero_id smallint,
  item text,
  time integer,
  lane_role smallint,
  games bigint DEFAULT 1,
  wins bigint,
  epoch_week integer,
  UNIQUE (hero_id, item, time, epoch_week),
  UNIQUE (hero_id, lane_role, time, epoch_week)
); 

CREATE TABLE IF NOT EXISTS team_scenarios (
  scenario text,
  is_radiant boolean,
  region smallint,
  games bigint DEFAULT 1,
  wins bigint,
  epoch_week integer,
  UNIQUE (scenario, is_radiant, region, epoch_week)
);  

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'readonly') THEN
        GRANT SELECT ON matches TO readonly;
        GRANT SELECT ON player_matches TO readonly;
        GRANT SELECT ON heroes TO readonly;
        GRANT SELECT ON leagues TO readonly;
        GRANT SELECT ON items TO readonly;
        GRANT SELECT ON teams TO readonly;
        GRANT SELECT ON team_match TO readonly;
        GRANT SELECT ON match_patch TO readonly;
        GRANT SELECT ON picks_bans TO readonly;
        GRANT SELECT ON match_logs TO readonly;
        GRANT SELECT ON notable_players TO readonly;
        GRANT SELECT ON public_matches TO readonly;
        GRANT SELECT ON public_player_matches TO readonly;
        GRANT SELECT ON players TO readonly;
    END IF;
END
$$;
