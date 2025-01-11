import os
import logging
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import main as lm

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s : %(message)s"
)
logger = logging.getLogger(__name__)

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


def handle_mention(logger, event, say):
    """メンション時"""
    logger.info(f"Start handle_mention")
    logger.info(f"{event}")

    # 履歴保持用のセッションID(thread_ts or ts)を設定
    session_id = event["thread_ts"] if "thread_ts" in event else event["ts"]
    config = {
        "session_id": session_id,
    }

    message = get_raw_message(event["text"])
    try:
        # API呼び出し
        content = lm.chat_with_history().invoke(
            {"user_input": message}, config={"configurable": config}
        )
        logger.info(f"Response:{content['output']}")
        say(content['output'], thread_ts=event["ts"])
    except Exception as e:
        logger.error(f"{e}")
        say(f"ERROR: {e}", thread_ts=event["ts"])


def just_ack(ack):
    """3秒以内にackを返す"""
    ack()


def get_raw_message(message):
    """メンション部削除"""
    raw_message = re.sub(r"<@" + os.environ.get("SLACK_BOT_ID") + ">", "", message)
    raw_message = re.sub(r"\s+", " ", raw_message).strip()
    return raw_message


# Event Actions
app.event("app_mention")(ack=just_ack, lazy=[handle_mention])

if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
