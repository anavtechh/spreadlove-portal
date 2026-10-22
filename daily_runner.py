import sys
import io
from pathlib import Path
from datetime import datetime

# Ensure utf-8 output on Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from post_generator import PostGenerator

def main():
    print("=" * 60)
    print("🌱 Spread Love Foundation - LinkedIn Automation Engine")
    print("=" * 60)
    
    gen = PostGenerator()
    check = gen.check_today_event()
    
    if check["is_today"]:
        ev = check["event"]
        print(f"\n[!] TODAY IS A SPECIAL OBSERVANCE: {ev['title']}")
        print(f"Theme: {ev['theme']}")
        post = gen.generate_special_day_post(ev)
    else:
        up = check["upcoming"]
        print(f"\nToday is normal calendar day. Next Upcoming Day: {up['title']} ({up['date']})")
        choice = input("\nGenerate post for this upcoming day? (y/n) or paste Instagram caption (c): ").strip().lower()
        if choice == 'c':
            caption = input("\nPaste Instagram post text/caption: ").strip()
            post = gen.convert_instagram_to_linkedin(caption)
        else:
            post = gen.generate_special_day_post(up)

    print("\n" + "=" * 60)
    print("PREVIEW - DRAFT LINKEDIN POST:")
    print("=" * 60)
    print(post["content"])
    print("=" * 60)
    
    approve = input("\nDo you APPROVE this post to be published on LinkedIn? (yes/no): ").strip().lower()
    if approve in ["yes", "y"]:
        print("\n✅ APPROVED! Post copied to clipboard or ready for LinkedIn publishing.")
        print("🔗 Open LinkedIn to share: https://www.linkedin.com/feed/?shareActive=true")
    else:
        print("\n❌ Post rejected/held for editing.")

if __name__ == "__main__":
    main()
