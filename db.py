import boto3

# from misc import cache_request

dynamodb = boto3.resource("dynamodb")
activities_table = dynamodb.Table("leaderboard_activities")
summaries_table = dynamodb.Table("leaderboard_summary")


# @cache_request()
def get_activities():
    done = False
    start_key = None
    while not done:
        if start_key:
            response["ExclusiveStartKey"] = start_key
        response = activities_table.scan()
        start_key = response.get("LastEvaluatedKey", None)
        done = start_key is None

    return response.get("Items", [])


database = get_activities()


def upload_leaderboard(summaries):
    fields_definition = [
        "athlete_id",
        "activity_type",
        "athlete_name",
        "distance",
        "activity_ids",
        "timestamp",
        "distance_gain",
        "id",
    ]

    for summary in summaries:
        for activity in summary:
            item = dict(
                zip(
                    fields_definition,
                    [str(fld) if i != 4 else fld for i, fld in enumerate(activity)],
                )
            )

            summaries_table.put_item(Item=item)
