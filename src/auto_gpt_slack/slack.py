import asyncio
from typing import Optional

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# slack_token = os.environ["SLACK_BOT_TOKEN"]
# client = WebClient(token=slack_token)


class SlackUtils():
    def __init__(self, slack_token: str, slack_channel: str):
        self.client = WebClient(token=slack_token)
        self.slack_channel = slack_channel
        self.user_id = self.client.auth_test()["user_id"]
        self.latest_ts = self.client.conversations_history(
            channel=self.slack_channel,
            limit=1
        )["messages"][0]["ts"]

        print("SlackBot initialized with user_id: " + self.user_id)
        print("SlackBot initialized with latest_ts: " + self.latest_ts)

    def send_slack_message(self, message: str, channel: Optional[str] = None):
        """
        Send a message to configured Slack channel.

        Args:
            message (str): The message to be sent to slack.

        Returns:
            str: Message
        """
        slack_channel = channel if channel is not None else self.slack_channel

        if slack_channel is None:
            return "Failed to send a slack message. Reason: no default slack channel configured"

        try:
            self.client.chat_postMessage(
                channel=self.slack_channel,
                text=message
            )
            return "Sent message to Slack"
        except SlackApiError as e:
            return "Failed to send message, error: " + e.response["error"]

    # wait for latest message from slack channel mentioning the bot user id 
    async def wait_for_message(self):
        """
        Wait for a message to be sent to configured Slack channel mentioning the bot user id.

        Returns:
            str: Message
        """
        while True:
            try:
                print("Polling for new messages...")
                response = self.client.conversations_history(
                    channel=self.slack_channel,
                    oldest=self.latest_ts,
                    limit=1
                )

                if len(response["messages"]) > 0:
                    message = response["messages"][0]
                    self.latest_ts = message["ts"]
            
                    if message.text is not None and "<@" + self.user_id + ">" in message.text:
                        return message.text.replace("<@" + self.user_id + ">", "").strip()
            except SlackApiError as e:
                print("Failed to get message, error: " + e.response["error"])
            
            await asyncio.sleep(1)