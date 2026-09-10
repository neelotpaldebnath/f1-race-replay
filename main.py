from argparse import ArgumentParser
from src.f1_data import get_race_telemetry, load_race_session, enable_cache, get_circuit_rotation
from src.arcade_replay import run_arcade_replay


def parse_args():
    parser = ArgumentParser(
        description="F1 Race Replay - telemetry-driven race visualization"
    )

    parser.add_argument(
        "--year",
        type=int,
        default=2025,
        help="F1 season year"
    )

    parser.add_argument(
        "--round",
        type=int,
        default=12,
        help="F1 championship round"
    )

    parser.add_argument(
        "--session",
        choices=["R", "S"],
        default="R",
        help="Session type: R for Race, S for Sprint"
    )

    parser.add_argument(
        "--speed",
        type=float,
        choices=[0.5, 1.0, 2.0, 4.0],
        default=1.0,
        help="Initial replay playback speed"
    )

    return parser.parse_args()
  
  
def main(year=None, round_number=None, playback_speed=1, session_type='R'):
  session = load_race_session(year, round_number, session_type)
  print(f"Loaded session: {session.event['EventName']} - {session.event['RoundNumber']}")

  # Enable cache for fastf1
  enable_cache()

  # Get the drivers who participated in the race

  race_telemetry = get_race_telemetry(session, session_type=session_type)

  # Get example lap for track layout

  example_lap = session.laps.pick_fastest().get_telemetry()

  drivers = session.drivers

  # Get circuit rotation

  circuit_rotation = get_circuit_rotation(session)

  # Run the arcade replay

  try:
    run_arcade_replay(
      frames=race_telemetry['frames'],
      track_statuses=race_telemetry['track_statuses'],
      example_lap=example_lap,
      drivers=drivers,
      playback_speed=playback_speed,
      driver_colors=race_telemetry['driver_colors'],
      title=f"{session.event['EventName']} - {'Sprint' if session_type == 'S' else 'Race'}",
      total_laps=race_telemetry['total_laps'],
      circuit_rotation=circuit_rotation,
    )
  except Exception as e:
    print(f"Error running arcade replay: {e}")
    import traceback
    traceback.print_exc()

if __name__ == "__main__":
    args = parse_args()

    main(
        year=args.year,
        round_number=args.round,
        playback_speed=args.speed,
        session_type=args.session
    )
