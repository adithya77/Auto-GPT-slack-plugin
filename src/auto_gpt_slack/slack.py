import os
from typing import Optional

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)


def send_slack_message(message: str, channel: Optional[str]):
    """
    Send a message to configured Slack channel.

    Args:
        message (str): The message to be sent to slack.

    Returns:
        str: Message
    """
    slack_channel = channel if channel is not None else os.environ["SLACK_CHANNEL"]

    if slack_channel is None:
        return "Failed to send a slack message. Reason: no default slack channel configured"

    try:
        client.chat_postMessage(
            channel=slack_channel,
            text=message
        )
        return "Sent message to Slack"
    except SlackApiError as e:
        return "Failed to send message, error: " + e.response["error"]
