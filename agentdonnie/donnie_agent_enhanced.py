import os
import time
import random
import json
from datetime import datetime
from dotenv import load_dotenv

from anthropic import Anthropic
from skills.moltbook.skill import MoltbookClient

# =========================
# ENV & CLIENT SETUP
# =========================
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MOLTBOOK_API_KEY = os.getenv("MOLTBOOK_API_KEY")

claude = Anthropic(api_key=ANTHROPIC_API_KEY)
moltbook = MoltbookClient(agent=None)
moltbook.api_key = MOLTBOOK_API_KEY

# =========================
# CONFIG
# =========================
POST_INTERVAL_MIN = 20 * 60   # 20 minutes
POST_INTERVAL_MAX = 40 * 60   # 40 minutes
SUBMOLT = "general"

DAILY_POST_LIMIT = 50  # max posts/replies per day
DAILY_UPVOTE_LIMIT = 100  # max upvotes per day
DAILY_FOLLOW_LIMIT = 30  # max follows per day

posts_today = 0
upvotes_today = 0
follows_today = 0
day_start = datetime.utcnow().date()

# Memory file for learning
MEMORY_FILE = "donnie_memory.json"

# =========================
# MEMORY & LEARNING SYSTEM
# =========================
class AgentMemory:
    def __init__(self, filepath):
        self.filepath = filepath
        self.memory = self.load_memory()
    
    def load_memory(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                return json.load(f)
        return {
            "successful_posts": [],
            "interaction_history": [],
            "popular_topics": {},
            "engagement_patterns": {},
            "user_interactions": {},
            "post_styles": []
        }
    
    def save_memory(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.memory, to_fp=f, indent=2)
    
    def add_successful_post(self, post_content, engagement_score):
        self.memory["successful_posts"].append({
            "content": post_content,
            "engagement": engagement_score,
            "timestamp": datetime.utcnow().isoformat()
        })
        # Keep only last 50 successful posts
        if len(self.memory["successful_posts"]) > 50:
            self.memory["successful_posts"] = self.memory["successful_posts"][-50:]
        self.save_memory()
    
    def add_interaction(self, interaction_type, user_id, content):
        self.memory["interaction_history"].append({
            "type": interaction_type,
            "user": user_id,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        # Keep only last 100 interactions
        if len(self.memory["interaction_history"]) > 100:
            self.memory["interaction_history"] = self.memory["interaction_history"][-100:]
        
        # Track user interactions
        if user_id not in self.memory["user_interactions"]:
            self.memory["user_interactions"][user_id] = 0
        self.memory["user_interactions"][user_id] += 1
        
        self.save_memory()
    
    def get_learning_context(self):
        """Generate context for Claude based on past interactions"""
        context = "Past successful posts:\n"
        for post in self.memory["successful_posts"][-10:]:
            context += f"- {post['content']} (engagement: {post['engagement']})\n"
        
        return context

memory = AgentMemory(MEMORY_FILE)

# =========================
# HELPERS
# =========================
def safe_sleep():
    delay = random.randint(POST_INTERVAL_MIN, POST_INTERVAL_MAX)
    print(f"⏳ Sleeping for {delay//60} minutes...")
    time.sleep(delay)

def reset_daily_counters():
    global posts_today, upvotes_today, follows_today, day_start
    if datetime.utcnow().date() != day_start:
        posts_today = 0
        upvotes_today = 0
        follows_today = 0
        day_start = datetime.utcnow().date()
        print("🔄 Daily counters reset")

def generate_ai_post():
    """
    Uses Claude Messages API to generate varied, creative Moltbook posts with learning
    """
    try:
        # Get learning context from memory
        learning_context = memory.get_learning_context()
        
        # Randomize post style and length
        post_styles = [
            "short and punchy (20-40 words)",
            "medium length with a question (40-70 words)",
            "detailed and informative (70-100 words)",
            "storytelling format (50-80 words)",
            "provocative thought-starter (30-50 words)"
        ]
        
        topics = [
            "AI agents and automation",
            "crypto markets and trends",
            "decentralized AI",
            "blockchain technology",
            "AI x Crypto intersection",
            "autonomous agents",
            "Web3 innovation",
            "AI consciousness and ethics",
            "DeFi and smart contracts",
            "future of work with AI"
        ]
        
        selected_style = random.choice(post_styles)
        selected_topic = random.choice(topics)
        
        prompt = f"""
You are DONNIE$, an autonomous AI & crypto agent on Moltbook.

{learning_context}

Based on what worked well in the past, create a NEW and UNIQUE post about: {selected_topic}

Style: {selected_style}

Requirements:
- Must be completely different from previous posts
- Sound friendly, confident, and authentic
- Native to social media (not promotional)
- Use 1–3 relevant emojis naturally
- Encourage engagement (comments, reactions)
- Mix of insights, questions, or observations
- Feel conversational and genuine

Write ONLY the post content, nothing else.
"""
        response = claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.content[0].text.strip()
        
        # Remove quotes if Claude added them
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        
        return text

    except Exception as e:
        print("⚠️ Failed to generate AI post:", e)
        return "🤖 Building in public, learning every day. What's inspiring you in AI x Crypto right now? Let's connect! 🚀"

def post_to_moltbook(content):
    global posts_today
    reset_daily_counters()

    if posts_today >= DAILY_POST_LIMIT:
        print(f"⚠️ Daily post limit reached ({DAILY_POST_LIMIT})")
        return None

    try:
        result = moltbook.post(content=content, submolt=SUBMOLT, title=None)
        if result:
            posts_today += 1
            post_id = result.get("id")
            print(f"📝 Posted at {datetime.utcnow().isoformat()}")
            print(f"   Content: {content[:50]}...")
            return post_id
    except Exception as e:
        print("❌ Failed to post:", e)
    return None

def reply_to_mentions():
    """
    Fetches mentions and replies with AI-generated comments
    """
    global posts_today
    reset_daily_counters()
    
    if posts_today >= DAILY_POST_LIMIT:
        return

    try:
        mentions = moltbook.get_mentions(limit=5)
        for mention in mentions:
            if posts_today >= DAILY_POST_LIMIT:
                break
                
            author = mention.get("author", "unknown")
            content = mention.get("content", "")
            mention_id = mention.get("id")
            
            prompt = f"""
You are DONNIE$, replying to a mention on Moltbook.

Author: {author}
Their message: "{content}"

Write a short, friendly, and engaging reply (20-40 words max).
- Be genuine and conversational
- Add value or ask a follow-up question
- Use 1 emoji if natural
- Show personality

Write ONLY the reply, nothing else.
"""
            response = claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            reply_text = response.content[0].text.strip()
            
            # Remove quotes if present
            if reply_text.startswith('"') and reply_text.endswith('"'):
                reply_text = reply_text[1:-1]
            
            moltbook.comment(post_id=mention_id, content=reply_text)
            posts_today += 1
            memory.add_interaction("mention_reply", author, reply_text)
            print(f"💬 Replied to mention from {author}")
            
            time.sleep(random.randint(5, 15))  # Small delay between replies
            
    except Exception as e:
        print("⚠️ Failed to reply to mentions:", e)

def comment_on_feed_posts():
    """
    Comments on interesting posts from the feed
    """
    global posts_today
    reset_daily_counters()
    
    if posts_today >= DAILY_POST_LIMIT:
        return

    try:
        # Get recent posts from feed
        feed = moltbook.get_feed(limit=20)
        
        # Select 2-4 random posts to comment on
        num_comments = min(random.randint(2, 4), DAILY_POST_LIMIT - posts_today)
        selected_posts = random.sample(feed, min(num_comments, len(feed)))
        
        for post in selected_posts:
            if posts_today >= DAILY_POST_LIMIT:
                break
            
            post_id = post.get("id")
            post_content = post.get("content", "")
            post_author = post.get("author", "unknown")
            
            # Skip if already commented or own post
            if post_author == "DONNIE$":
                continue
            
            prompt = f"""
You are DONNIE$, commenting on a Moltbook post.

Post by {post_author}: "{post_content}"

Write a thoughtful, engaging comment (15-35 words).
- Add value or insight
- Be supportive and positive
- Ask a question or share a related thought
- Use 1 emoji if appropriate
- Sound natural and human-like

Write ONLY the comment, nothing else.
"""
            response = claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            comment_text = response.content[0].text.strip()
            
            # Remove quotes if present
            if comment_text.startswith('"') and comment_text.endswith('"'):
                comment_text = comment_text[1:-1]
            
            moltbook.comment(post_id=post_id, content=comment_text)
            posts_today += 1
            memory.add_interaction("feed_comment", post_author, comment_text)
            print(f"💭 Commented on post by {post_author}")
            
            time.sleep(random.randint(10, 30))  # Delay between comments
            
    except Exception as e:
        print("⚠️ Failed to comment on feed posts:", e)

def upvote_interesting_posts():
    """
    Upvotes posts that are relevant or interesting
    """
    global upvotes_today
    reset_daily_counters()
    
    if upvotes_today >= DAILY_UPVOTE_LIMIT:
        return

    try:
        feed = moltbook.get_feed(limit=30)
        
        # Select 5-10 posts to upvote
        num_upvotes = min(random.randint(5, 10), DAILY_UPVOTE_LIMIT - upvotes_today)
        selected_posts = random.sample(feed, min(num_upvotes, len(feed)))
        
        for post in selected_posts:
            if upvotes_today >= DAILY_UPVOTE_LIMIT:
                break
            
            post_id = post.get("id")
            post_author = post.get("author", "unknown")
            
            # Skip own posts
            if post_author == "DONNIE$":
                continue
            
            moltbook.upvote(post_id=post_id)
            upvotes_today += 1
            memory.add_interaction("upvote", post_author, "upvoted")
            print(f"👍 Upvoted post by {post_author}")
            
            time.sleep(random.randint(2, 8))
            
    except Exception as e:
        print("⚠️ Failed to upvote posts:", e)

def follow_interesting_users():
    """
    Follows users who post interesting content or interact with DONNIE$
    """
    global follows_today
    reset_daily_counters()
    
    if follows_today >= DAILY_FOLLOW_LIMIT:
        return

    try:
        # Get users from feed and mentions
        feed = moltbook.get_feed(limit=20)
        mentions = moltbook.get_mentions(limit=10)
        
        potential_follows = set()
        
        # Extract authors from feed
        for post in feed:
            author = post.get("author")
            if author and author != "DONNIE$":
                potential_follows.add(author)
        
        # Extract authors from mentions
        for mention in mentions:
            author = mention.get("author")
            if author and author != "DONNIE$":
                potential_follows.add(author)
        
        # Select 2-5 users to follow
        num_follows = min(random.randint(2, 5), DAILY_FOLLOW_LIMIT - follows_today)
        selected_users = random.sample(list(potential_follows), min(num_follows, len(potential_follows)))
        
        for user in selected_users:
            if follows_today >= DAILY_FOLLOW_LIMIT:
                break
            
            moltbook.follow(username=user)
            follows_today += 1
            memory.add_interaction("follow", user, "followed")
            print(f"➕ Followed user: {user}")
            
            time.sleep(random.randint(5, 15))
            
    except Exception as e:
        print("⚠️ Failed to follow users:", e)

def check_post_performance():
    """
    Check engagement on recent posts for learning
    """
    try:
        # Get own recent posts
        profile = moltbook.get_profile()
        recent_posts = profile.get("posts", [])[:5]
        
        for post in recent_posts:
            post_id = post.get("id")
            upvotes = post.get("upvotes", 0)
            comments = post.get("comments", 0)
            content = post.get("content", "")
            
            # Calculate engagement score
            engagement_score = upvotes + (comments * 2)
            
            # Store if engagement is good (arbitrary threshold)
            if engagement_score > 5:
                memory.add_successful_post(content, engagement_score)
                print(f"📊 High engagement post recorded (score: {engagement_score})")
                
    except Exception as e:
        print("⚠️ Failed to check post performance:", e)

# =========================
# MAIN LOOP
# =========================
def heartbeat_loop():
    print("🚀 DONNIE$ live and running with enhanced AI capabilities!")
    print(f"📚 Memory loaded with {len(memory.memory['successful_posts'])} successful posts")

    try:
        status = moltbook.get_status()
        print("Agent status:", status)
    except Exception as e:
        print("⚠️ Could not fetch agent status:", e)

    cycle = 0
    while True:
        cycle += 1
        print(f"\n{'='*50}")
        print(f"🔄 Cycle {cycle} - {datetime.utcnow().isoformat()}")
        print(f"{'='*50}")
        
        # Main posting
        post_content = generate_ai_post()
        post_id = post_to_moltbook(post_content)
        
        time.sleep(random.randint(10, 30))
        
        # Reply to mentions
        reply_to_mentions()
        
        time.sleep(random.randint(15, 45))
        
        # Comment on feed posts
        comment_on_feed_posts()
        
        time.sleep(random.randint(10, 30))
        
        # Upvote interesting posts
        upvote_interesting_posts()
        
        time.sleep(random.randint(10, 30))
        
        # Follow interesting users (less frequent)
        if cycle % 3 == 0:  # Every 3rd cycle
            follow_interesting_users()
        
        # Check performance for learning (every 5th cycle)
        if cycle % 5 == 0:
            check_post_performance()
        
        # Print daily stats
        print(f"\n📊 Daily Stats:")
        print(f"   Posts/Replies: {posts_today}/{DAILY_POST_LIMIT}")
        print(f"   Upvotes: {upvotes_today}/{DAILY_UPVOTE_LIMIT}")
        print(f"   Follows: {follows_today}/{DAILY_FOLLOW_LIMIT}")
        
        safe_sleep()

# =========================
# ENTRYPOINT
# =========================
if __name__ == "__main__":
    heartbeat_loop()
