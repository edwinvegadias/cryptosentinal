import time
from .analyzer import RedditSentimentAnalyzer
from rich.console import Console
from rich.panel import Panel

console = Console()

# Simple memory of previous mentions
previous_state = {}

def detect_anomalies(current_data):
    global previous_state
    alerts = []

    for coin, data in current_data.items():
        mentions = data["mentions"]
        sentiment = data["sentiment"]
        sentiment_score = sentiment / mentions if mentions > 0 else 0

        prev_mentions = previous_state.get(coin, {}).get("mentions", 1)

        if mentions > prev_mentions * 3 and abs(sentiment_score) > 0.3:
            alerts.append((coin, mentions, sentiment_score))

        previous_state[coin] = data

    return alerts


def run_monitor():
    analyzer = RedditSentimentAnalyzer(
        client_id="your_id_here",
        client_secret="your_secret_here",
        user_agent="CryptoSentinal/0.1"
    )

    while True:
        console.print("[cyan]Fetching latest posts from Reddit...[/cyan]")
        posts = analyzer.fetch_posts(limit=200)
        data = analyzer.analyze_sentiment(posts)

        anomalies = detect_anomalies(data)

        for coin, mentions, sentiment_score in anomalies:
            msg = f"""
🚨 Anomaly Detected!
Coin: ${coin}
Mentions ↑ {mentions}
Sentiment Score: {sentiment_score:.2f}
Potential {"PUMP" if sentiment_score > 0 else "DUMP"} in progress!
"""
            console.print(Panel(msg, title="Alert", style="bold red"))

        console.print("[green]Sleeping for 3 minutes...[/green]")
        time.sleep(180)
