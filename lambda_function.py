from reports import build_leaderboard, get_distance_change
from datetime import datetime, timedelta, date, time
from misc import create_hash
from db import upload_leaderboard


midnight = datetime.combine(date.today(), time.min)
START_DATE = 1685570400


def lambda_handler(event, context):
    leaderboard_summaries = []

    days = (datetime.now().date() - datetime.fromtimestamp(START_DATE).date()).days + 1

    for i in range(1, days):
        offset = (86400 * i) - 1
        end_date = START_DATE + offset

        summary = build_leaderboard(START_DATE, end_date)

        if i != 1:
            previous_summary = leaderboard_summaries[i - 2]
            get_distance_change(summary, previous_summary)
        else:
            get_distance_change(summary)

        for activity in summary:
            hash_value = create_hash(
                activity[0], activity[1], activity[2], activity[3], activity[5]
            )
            activity.append(hash_value)

        leaderboard_summaries.append(summary)

    upload_leaderboard(leaderboard_summaries)


if __name__ == "__main__":
    lambda_handler(None, None)
