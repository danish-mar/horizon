import redis
import json


def notify_user(user_id, message):
    r = redis.StrictRedis(host="shinobi", port=6379, db=0)

    channel = f"user:{user_id}"
    r.publish(channel, message)
    print("Sent message to NPI app")


def publish_notification(account_number, title, message):
    r = redis.StrictRedis(host="shinobi", port=6379, db=0)

    notification = {
        'title': title,
        'message': message
    }

    json_message = json.dump(notification, indent=4)

    channel = f"user:{account_number}"

    r.publish(channel, json_message)
