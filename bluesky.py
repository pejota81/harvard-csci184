from atproto import Client, models
import json
import os
import time

KEYWORDS = [
    "mental health",
    "anxiety",
    "depression",
    "therapy",
    "panic attack",
    "stress"
]

client = Client()
client.login(os.environ["BSKY_HANDLE"], os.environ["BSKY_APP_PASSWORD"])

all_posts = []

for kw in KEYWORDS:
    params = models.AppBskyFeedSearchPosts.Params(
        q=kw,
        limit=50
    )

    results = client.app.bsky.feed.search_posts(params)

    for p in results.posts:
        post = p.post
        all_posts.append({
            "keyword": kw,
            "text": post.record.text,
            "likes": post.like_count,
            "replies": post.reply_count,
            "reposts": post.repost_count,
            "quotes": post.quote_count,
            "created_at": post.record.created_at,
            "uri": post.uri,
            "author_did": post.author.did
        })

    time.sleep(1)

with open("bluesky_mental_health_full_metrics.json", "w") as f:
    json.dump(all_posts, f, indent=2)

print(f"Collected {len(all_posts)} posts.")
