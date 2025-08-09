import csv
from pathlib import Path

SCHEDULE_PATH = Path(__file__).with_name('wl_schedule.csv')

STAR_FIELDS = ['star1_pct', 'star2_pct', 'star3_pct', 'star4_pct', 'star5_pct']


def load_schedule(path: Path = SCHEDULE_PATH):
    """Load world level schedule with star distributions."""
    with path.open(newline='') as f:
        reader = csv.DictReader(f)
        schedule = []
        for row in reader:
            total = sum(float(row[field]) for field in STAR_FIELDS)
            row['star0_pct'] = max(0.0, 100 - total)
            schedule.append(row)
        return schedule


def main():
    for row in load_schedule():
        parts = [f"WL{row['wl']}",
                 f"0★ {float(row['star0_pct']):.0f}%",
                 f"1★ {row['star1_pct']}%",
                 f"2★ {row['star2_pct']}%",
                 f"3★ {row['star3_pct']}%",
                 f"4★ {row['star4_pct']}%",
                 f"5★ {row['star5_pct']}%"]
        print(', '.join(parts))


if __name__ == '__main__':
    main()
