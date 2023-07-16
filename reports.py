from db import database
from typing import Final, Dict, List

ACTIVITY_NAMES_MAP: Final[Dict[str, str]] = {
    "mountain bike ride": "ride",
    "weight training": "workout",
}


def build_leaderboard(start_date: int, end_date: int) -> List[list]:
    leaderboard = []

    for activity in database:
        if int(activity["timestamp"]) < start_date:
            continue

        if int(activity["timestamp"]) > end_date:
            continue

        if not (activity_dst := activity.get("distance")):
            continue

        activity_dst = int(float(activity_dst))
        activity_id = [activity["id"]]

        athlete_id = activity["athlete_id"]
        athlete_name = activity["athlete_name"]
        activity_type = ACTIVITY_NAMES_MAP.get(activity["type"], activity["type"])

        for summary in leaderboard:
            if summary[0] == athlete_id and summary[1] == activity_type:
                summary[3] += activity_dst
                summary[4].extend(activity_id)

                break

        else:
            leaderboard.append(
                [
                    athlete_id,
                    activity_type,
                    athlete_name,
                    activity_dst,
                    activity_id,
                    end_date,
                ]
            )

    leaderboard.sort(key=lambda x: (x[1], x[3]), reverse=True)
    return leaderboard


def calculate_dst_delta(activity: list, previous_summary: List[list]) -> int:
    for prev_activity in previous_summary:
        if prev_activity[0] == activity[0] and prev_activity[1] == activity[1]:
            return activity[3] - prev_activity[3]
    return activity[3]


def get_distance_change(
    current_summary: List[list], previous_summary: List[list] = None
) -> List[list]:
    for activity in current_summary:
        if previous_summary:
            dst_delta = calculate_dst_delta(activity, previous_summary)
            activity.append(dst_delta)
        else:
            activity.append(activity[3])

    return current_summary
