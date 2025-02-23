import os
import logging
import re
import time
from typing import Dict, Any, List
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
from markdown_to_mrkdwn import SlackMarkdownConverter
import main as lm

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s [%(filename)s:%(lineno)d] : %(message)s"
)
logger = logging.getLogger(__name__)

# Markdownコンバーターの初期化
markdown_converter = SlackMarkdownConverter()

def validate_environment():
    """環境変数の検証"""
    required_vars = ["SLACK_BOT_TOKEN", "SLACK_APP_TOKEN", "SLACK_BOT_ID"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# 環境変数の検証
validate_environment()

# Slackアプリの初期化
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

def get_thread_history(channel: str, thread_ts: str) -> List[Dict[str, Any]]:
    """Slackスレッドの会話履歴を取得"""
    try:
        # スレッドの返信を取得
        result = app.client.conversations_replies(
            channel=channel,
            ts=thread_ts
        )
        
        if not result["ok"]:
            logger.error(f"Failed to fetch thread history: {result.get('error', 'Unknown error')}")
            return []

        messages = result.get("messages", [])
        # ボットのIDを取得
        bot_id = os.environ.get("SLACK_BOT_ID")
        
        # メッセージを整形（ボットとユーザーの会話のみ抽出）
        conversation_history = []
        for msg in messages:
            # ボットへのメンション（ユーザーからの質問）
            if "user" in msg and f"<@{bot_id}>" in msg.get("text", ""):
                conversation_history.append({
                    "role": "user",
                    "content": get_raw_message(msg["text"])
                })
            # ボットからの返信
            elif msg.get("bot_id") and "text" in msg:
                conversation_history.append({
                    "role": "assistant",
                    "content": msg["text"]
                })
        
        return conversation_history
    
    except SlackApiError as e:
        logger.error(f"Slack API error: {str(e)}", exc_info=True)
        return []
    
    except Exception as e:
        logger.error(f"Error fetching thread history: {str(e)}", exc_info=True)
        return []

def convert_to_mrkdwn(text: str) -> str:
    """MarkdownをSlackのmrkdwn形式に変換"""
    try:
        return markdown_converter.convert(text)
    except Exception as e:
        logger.error(f"Error converting markdown to mrkdwn: {str(e)}", exc_info=True)
        return text

def handle_mention(logger, event, say):
    """メンション時のハンドラー"""
    start_time = time.time()
    logger.info(f"Received mention event: {event.get('type')} in channel: {event.get('channel')}")

    try:
        # スレッドIDの取得
        thread_ts = event.get("thread_ts", event.get("ts"))
        if not thread_ts:
            raise ValueError("Failed to get thread ID from event")

        # チャンネルIDの取得
        channel = event.get("channel")
        if not channel:
            raise ValueError("Failed to get channel ID from event")

        # スレッドの会話履歴を取得
        conversation_history = get_thread_history(channel, thread_ts)
        
        config = {
            "session_id": thread_ts,
            "channel": channel,
            "user": event.get("user"),
            "conversation_history": conversation_history
        }

        message = get_raw_message(event["text"])
        if not message.strip():
            say("メッセージが空です。質問や指示を入力してください。", thread_ts=event["ts"])
            return

        # API呼び出し（タイムアウト制御付き）
        timeout = float(os.environ.get("API_TIMEOUT", "60"))
        start_process = time.time()
        content = lm.chat_with_history().invoke(
            {"user_input": message},
            config={"configurable": config}
        )
        process_time = time.time() - start_process

        # レスポンスをmrkdwn形式に変換
        mrkdwn_response = convert_to_mrkdwn(content['output'])
        
        # レスポンス送信
        logger.info(
            f"Response generated in {process_time:.2f}s - Length: {len(mrkdwn_response)}"
        )
        say(text=mrkdwn_response, thread_ts=event["ts"])

    except Exception as e:
        logger.error(f"Error in handle_mention: {str(e)}", exc_info=True)
        error_message = "申し訳ありません。エラーが発生しました。"
        if os.environ.get("DEBUG", "false").lower() == "true":
            error_message += f"\nError: {str(e)}"
        say(error_message, thread_ts=event["ts"])

    finally:
        total_time = time.time() - start_time
        logger.info(f"Total processing time: {total_time:.2f}s")

def just_ack(ack):
    """3秒以内にackを返す"""
    ack()

def get_raw_message(message: str) -> str:
    """メンション部分を削除してメッセージを取得"""
    if not message:
        return ""
    
    bot_id = os.environ.get("SLACK_BOT_ID")
    if not bot_id:
        logger.warning("SLACK_BOT_ID is not set")
        return message.strip()

    raw_message = re.sub(f"<@{bot_id}>", "", message)
    return re.sub(r"\s+", " ", raw_message).strip()

# Slackイベントの設定
app.event("app_mention")(
    ack=just_ack,
    lazy=[handle_mention]
)

if __name__ == "__main__":
    try:
        handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
        logger.info("Starting Slack bot in socket mode...")
        handler.start()
    except Exception as e:
        logger.critical(f"Failed to start Slack bot: {e}", exc_info=True)
        raise
