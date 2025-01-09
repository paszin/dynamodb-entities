
import boto3

from datastore import Datastore

if __name__ == "__main__":

    import random
    import datetime

    import boto3

    import tablespecs
    datastore_tablename = "pascal-highscore"

    session = boto3.Session(profile_name='local', region_name="localhost")
    client = session.client('dynamodb', endpoint_url="http://localhost:8000")

    spec = tablespecs.DATASTORE_DESCRIPTION
    spec["TableName"] = datastore_tablename
    try:
        client.delete_table(TableName=datastore_tablename)
    except:
        pass
    client.create_table(**spec)

    # ddb = boto3.resource('dynamodb',
    #                      endpoint_url='http://localhost:8000',
    #                      aws_access_key_id="", # insert here
    #                      aws_secret_access_key="", # insert here
    #                      region_name="localhost")
    # table = ddb.Table('pascal-highscore')

    datastore = Datastore(table_name=datastore_tablename, session=session, endpoint_url='http://localhost:8000')

    usernames = [
        "ShadowFox",
        "LunaWhisp",
        "StarFlare",
        "FrostWing",
        "MysticOrb",
        "BlazeDrift",
        "EchoWolf",
        "DuskTide",
        "NovaSpark",
        "FlameVine"
    ]

    for user in usernames:
        for i in range(20):
            datastore.add_play(user, datetime.datetime(2024, 12, 1, 12, 0, 0) +
                               datetime.timedelta(hours=10*i+random.randrange(10)), random.randrange(0, 1000))

    # Get global highscore
    highscore = datastore.get_highscore(convert=True)
    print("Highscore")
    for pos, item in enumerate(highscore, start=1):
        print(pos, item.points, item.username)

    # get last 10 plays of player "ShadowFox"
    print("\nRecent Plays of ShadowFox")
    recent_plays = datastore.get_recent_plays("ShadowFox", convert=True)
    for item in recent_plays:
        print(item.date, item.points)

    print("\nPersonal Highscore of ShadowFox")
    user_highscore = datastore.get_user_highscore("ShadowFox", convert=True)
    for pos, item in enumerate(user_highscore, start=1):
        print(pos, item.points, item.date)

    print("\nUser Stats of ShadowFox")
    user_stats = datastore.get_user_stats("ShadowFox", convert=True)
    print(user_stats, "plays:", user_stats[0].playCount)
