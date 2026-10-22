import json
import re
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

import json
import re
import os
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent
FONTS_DIR = Path(os.environ.get("WINDIR", "C:\\Windows")) / "Fonts"

class PostGenerator:
    def __init__(self):
        self.special_days_file = BASE_DIR / "special_days.json"
        self.special_days = self._load_special_days()
        self.static_dir = BASE_DIR / "static"
        self.static_dir.mkdir(exist_ok=True)
        (self.static_dir / "banners").mkdir(exist_ok=True)
        (self.static_dir / "uploads").mkdir(exist_ok=True)
        
    def _load_special_days(self):
        if self.special_days_file.exists():
            with open(self.special_days_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def check_today_event(self, date_str=None):
        """
        Check if today (or given MM-DD) matches any special day.
        Returns matching day info or closest upcoming event.
        """
        if not date_str:
            date_str = datetime.now().strftime("%m-%d")
        
        for item in self.special_days:
            if item["date"] == date_str:
                return {"is_today": True, "event": item}
                
        today_tuple = tuple(map(int, date_str.split("-")))
        upcoming = []
        for item in self.special_days:
            m, d = map(int, item["date"].split("-"))
            if (m, d) >= today_tuple:
                upcoming.append(((m, d), item))
                
        if upcoming:
            upcoming.sort(key=lambda x: x[0])
            return {"is_today": False, "upcoming": upcoming[0][1]}
        elif self.special_days:
            return {"is_today": False, "upcoming": self.special_days[0]}
        return {"is_today": False, "upcoming": None}

    def generate_special_day_post(self, event):
        title = event.get("title", "Special Awareness Day")
        theme = event.get("theme", "")
        category = event.get("category", "Environment")
        
        if "Health" in title or "Health" in category:
            post = f"""🌱 World Health Day: Clean Air, Green Spaces & Human Wellbeing

When we talk about public health, we often look at hospitals, medicines, and healthcare facilities. But the true foundation of human health begins with the air we breathe, the water we drink, and the environment we inhabit.

At Spread Love Foundation, our mission connects environmental restoration directly with human vitality:

🔹 Urban Green Lungs: Every native tree planted absorbs harmful particulate matter, reduces urban heat islands, and pumps fresh oxygen into our communities.
🔹 Waterbody Rejuvenation: Clean, restored lakes prevent vector-borne diseases and recharge vital groundwater tables for surrounding villages.
🔹 Community Wellness: Access to green cover and biodiversity parks dramatically enhances mental well-being and reduces respiratory illnesses.

Healthy ecosystems build healthy communities. One cannot exist without the other.

As we commemorate {title}, we reaffirm our pledge: Commit • Contribute • Conserve.

🤝 To our corporate CSR partners and passionate volunteers: Thank you for investing in preventative public health through tangible ecological action!

#SpreadLoveFoundation #WorldHealthDay #OneHealth #ClimateAction #PublicHealth #GreenCover #Afforestation #CSRIndia #Sustainability #ESG"""

        elif "Wetland" in title or "Water" in title:
            post = f"""💧 {title} | Preserving Every Drop Through Community Action

Water is not just a resource; it is the lifeblood of our ecosystems and communities. As groundwater levels drop and climate unpredictability increases, reviving our traditional waterbodies has never been more urgent.

At Spread Love Foundation, water security is at the heart of our conservation model:

🌊 Lake & Pond Desilting: Removing deep silt and invasive weeds to expand natural storage capacity.
🌿 Bund Strengthening & Miyawaki Afforestation: Planting native root systems along waterbanks to stop soil erosion and filter runoff water naturally.
💧 Recharging Deep Aquifers: Transforming dried-up village catchment zones into perennial water sanctuaries for local farmers and wildlife.

Every restored waterbody is a living insurance policy against future droughts.

Together with our visionary CSR partners and local volunteer networks, we are bringing forgotten lakes back to life.

👉 Join hands with us to adopt and revive a local waterbody!

#SpreadLoveFoundation #{title.replace(' ', '')} #WaterConservation #LakeRestoration #SaveWater #CSRInitiative #TamilNadu #SustainableFuture #SDG6"""

        elif "Forest" in title or "Tree" in title or "Van Mahotsav" in title or "Earth" in title:
            post = f"""🌳 {title} | Transforming Barren Lands Into Thriving Green Sanctuaries

Trees are Earth’s most effective carbon capture technology. But afforestation isn’t just about putting saplings into the soil—it’s about nurturing polyculture ecosystems that can sustain themselves for generations.

At Spread Love Foundation, our green restoration drives focus on:

✅ Native & Indigenous Saplings: Planting species suited to local soil chemistry that require minimal water after establishment.
✅ Seed Ball Germination Drives: Involving thousands of students and youth in mass seed ball dispersion across barren hillocks and dry zones.
✅ Dedicated Maintenance & High Survival Rates: Ensuring geo-tagging, regular organic manuring, and sustained care rather than mere photo-ops.

When corporate leaders, student volunteers, and grassroots communities unite under one vision, barren landscapes turn vibrant and green.

On this {title}, let’s move beyond symbolic gestures to measurable, on-ground climate action.

🌱 Commit • Contribute • Conserve

#SpreadLoveFoundation #{title.replace(' ', '')} #Afforestation #TreePlantation #ClimateAction #GreenCover #Biodiversity #CSRIndia #YouthForEarth #SDG13 #SDG15"""

        else:
            post = f"""🌍 Observing {title} with Ground-Level Impact

Theme Focus: {theme}

Today reminds us of our collective responsibility towards ecological balance. Real climate resilience does not happen inside boardrooms alone—it takes root on the ground, in the soil, and through community solidarity.

At Spread Love Foundation, our four pillars guide every single initiative:
1️⃣ Afforestation & Green Cover Expansion
2️⃣ Wetland & Water Sanctuary Revitalization
3️⃣ Youth Mobilization & Environmental Awareness
4️⃣ Corporate Social Responsibility (CSR) Partnerships for Sustainable Scale

Every single sapling planted, every lake desilted, and every volunteer trained contributes directly to a healthier, greener India.

We thank our volunteers, community stakeholders, and corporate allies for walking this transformative journey with us.

Let us commit to nature today, so future generations can thrive tomorrow.

#SpreadLoveFoundation #{title.replace(' ', '')} #Sustainability #CSR #ClimateAction #EnvironmentalConservation #EcoWarriors #GreenIndia"""

        return {
            "title": f"LinkedIn Post: {title}",
            "event": event,
            "content": post.strip(),
            "created_at": datetime.now().isoformat()
        }

    def convert_instagram_to_linkedin(self, instagram_text, image_description=None):
        clean_text = re.sub(r'#\w+', '', instagram_text).strip()
        lines = [line.strip() for line in clean_text.split('\n') if line.strip()]
        topic_summary = " ".join(lines[:2]) if lines else "Community Environmental Impact Drive"
        
        is_plantation = any(k in instagram_text.lower() for k in ["tree", "plant", "sapling", "maram", "green", "forest", "afforestation"])
        is_seedball = any(k in instagram_text.lower() for k in ["seed", "seedball", "vithai", "ball"])
        is_water = any(k in instagram_text.lower() for k in ["lake", "pond", "water", "cleanup", "kulam", "river"])

        if is_seedball:
            pillar = "Seed Ball Movement & Natural Greening"
            impact_points = [
                "Empowered youth and school volunteers to craft nutrient-rich native seed balls.",
                "Strategic aerial and ground dispersal across dry rural belts to harness upcoming seasonal rains.",
                "High natural germination rates with zero chemical additives, reviving endemic flora."
            ]
        elif is_water:
            pillar = "Wetland & Waterbody Ecological Rejuvenation"
            impact_points = [
                "De-silting and systematic clearing of weeds to revive water percolation channels.",
                "Reinforcing bunds with indigenous vetiver grass and soil-binding flora to halt erosion.",
                "Restoring vital stopovers for local migratory birds and sustaining groundwater for nearby hamlets."
            ]
        elif is_plantation:
            pillar = "Afforestation & Indigenous Green Cover"
            impact_points = [
                "Careful selection of indigenous species (Neem, Peepal, Pongamia, Jamun) suited for native climate.",
                "Adopting scientific spacing and drip/organic mulching for optimal survival rate.",
                "Creating long-term micro-climates that cool surroundings and capture atmospheric carbon."
            ]
        else:
            pillar = "Grassroots Community & Environmental Action"
            impact_points = [
                "Uniting local volunteers and community changemakers for sustained ecological action.",
                "Spreading hands-on awareness to nurture environmental stewardship in young minds.",
                "Aligning grassroots momentum with global UN Sustainable Development Goals (SDGs)."
            ]

        numbers = re.findall(r'\b\d+[\d,]*\+?\b', instagram_text)
        metric_highlight = f"Proud to have achieved a milestone of {numbers[0]} units/participants in this impactful drive!" if numbers else ""

        linkedin_post = f"""🌿 Driving Tangible Climate Impact on the Ground!

{topic_summary}

At Spread Love Foundation, our mission is built on translating intent into verifiable environmental outcomes. Through our latest initiative under {pillar}, our dedicated volunteer brigade and partners stepped onto the field to create lasting change.

Key Highlights & Impact:
• {impact_points[0]}
• {impact_points[1]}
• {impact_points[2]}

{metric_highlight}

Why Corporate & Community Partnerships Matter:
Environmental degradation cannot be fought in silos. When corporate ESG initiatives join forces with passionate on-ground changemakers, the result is scalable, measurable, and enduring sustainability.

A huge salute to every volunteer, team member, and partner organization whose dedication makes this possible. 

🌱 Commit • Contribute • Conserve

Interested in partnering with us for employee volunteering or CSR green projects? Let's connect!

#SpreadLoveFoundation #ClimateAction #Afforestation #CSRIndia #Sustainability #GreenInitiative #CommunityImpact #EcoLeadership #SDGs #ESG"""

        return {
            "title": f"LinkedIn Post from Instagram ({pillar})",
            "original_caption": instagram_text,
            "content": linkedin_post.strip(),
            "created_at": datetime.now().isoformat()
        }

    def generate_from_idea(self, idea_text, image_context=None):
        """
        Takes the user's raw thoughts / mind ideas in Tamil, English, or Tanglish
        and expands it into an executive-level, persuasive LinkedIn post.
        """
        idea_clean = idea_text.strip()
        lower = idea_clean.lower()

        # Check key themes (supports Tamil, English, Tanglish)
        is_why_important = any(k in lower for k in [
            "why", "ஏன்", "முக்கியம்", "முக்கிய", "இம்பார்ட்டன்ட்", "இம்பார்டன்ட்", "important", 
            "importance", "காரணம்", "crucial", "nature", "நேச்சர்", "நேச்சருக்கு", "இயற்கை", "need"
        ])
        is_seedball = any(k in lower for k in ["seed", "விதை", "seedball", "சீட்பால்", "விதைப்பந்து"])
        is_lake = any(k in lower for k in ["lake", "pond", "ஏரி", "குளம்", "water", "நீர்", "தூர்வார", "தூர்வாருவது", "சுத்தம்"])
        is_plantation = any(k in lower for k in ["plant", "tree", "sapling", "மரம்", "மரக்கன்று", "நட்டோம்", "காடு", "afforestation", "forest", "green cover"])
        is_youth_vol = any(k in lower for k in ["youth", "volunteer", "மாணவ", "வாலண்டியர்", "இளைஞர்", "students"])
        is_csr = any(k in lower for k in ["csr", "corporate", "நிறுவன", "partnership", "பங்களிப்பு", "ஹிரோடெக்", "துராவிட்"])

        if is_why_important and ("spread love" in lower or "foundation" in lower or "பவுண்டேஷன்" in lower or "அமைப்பு" in lower or "nature" in lower or "நேச்சர்" in lower or "இயற்கை" in lower):
            headline = "Why is Spread Love Foundation Crucial for Nature & Future Generations?"
            body = f"""🌍 Why Does Spread Love Foundation Exist, and Why is Our Mission Critical for Nature?

Reflecting on our core purpose: "{idea_clean}"

In an era of rising global temperatures, recurring droughts, and rapid urban concrete expansion, the earth doesn't just need awareness campaigns—it needs boots on the ground, hands in the soil, and communities taking active responsibility.

Here is why Spread Love Foundation is playing a pivotal role in environmental rejuvenation:

1️⃣ Grassroots Direct Action Over Empty Talks:
We don't stop with seminars. From planting native saplings on barren lands to reviving degraded water catchment bodies, every initiative produces tangible, verifiable ecological results.

2️⃣ Scientific & Indigenous Approach:
We prioritize native flora—species like Neem, Peepal, Pongamia, and Jamun—ensuring high survival rates, deep groundwater recharge, and self-sustaining micro-forests.

3️⃣ Youth & Volunteer Movement:
We believe true conservation happens when the next generation falls in love with nature. Involving thousands of student volunteers creates lifelong eco-warriors and responsible citizens.

4️⃣ A Trusted Partner for Corporate ESG & CSR:
We bridge the gap between corporate sustainability mandates and ground-level execution, ensuring every CSR rupee creates measurable carbon offsetting and biodiversity restoration.

Nature has supported humanity for centuries. Now, it is our turn to give back.

🌱 Commit • Contribute • Conserve

What role do you think grassroots foundations should play in accelerating India's climate goals? Share your thoughts below!

#SpreadLoveFoundation #ClimateAction #EnvironmentalStewardship #Afforestation #CSRIndia #Sustainability #NatureConservation #EcoWarriors #GreenFuture #SDG13 #SDG15"""

        elif is_seedball:
            headline = "The Power of a Simple Seed Ball: Revolutionizing Green Cover"
            body = f"""🌱 How a Simple Seed Ball Can Regreen Miles of Barren Land

Reflecting on our initiative: "{idea_clean}"

A seed ball looks humble, but inside that blend of clay, organic compost, and native seed lies the blueprint of a future forest.

At Spread Love Foundation, our Seed Ball initiative is one of our most loved and impactful programs:

🔹 Zero Chemical, 100% Native: We source indigenous tree and shrub seeds that thrive in harsh local climates with minimal water.
🔹 Maximum Accessibility: School children, college students, and corporate teams can easily make thousands of seed balls within hours, fostering immediate emotional connection with nature.
🔹 High Germination Success: Encased in protective soil until the first monsoon showers hit, the seeds germinate naturally at the ideal moment.

Small steps, when multiplied by thousands of passionate hands, transform entire barren landscapes.

🌱 Commit • Contribute • Conserve

Have you ever participated in a seed ball making drive? Let us know your experience!

#SpreadLoveFoundation #SeedBalls #Afforestation #YouthAction #GreenMovement #Biodiversity #GrassrootsConservation #CSRIndia #SustainableLiving"""

        elif is_lake:
            headline = "Reviving Our Lakes: The Lifeline of Our Communities"
            body = f"""🌊 Why Rejuvenating Lakes is Critical for Our Collective Survival

Reflecting on our initiative: "{idea_clean}"

Water security is the ultimate foundation of civilized life. Yet, across towns and villages, centuries-old waterbodies are choked with invasive silt, garbage, and encroachment.

At Spread Love Foundation, our lake and pond restoration drives address the root cause:

1️⃣ De-silting & Deep Excavation: Restoring natural percolation depth so monsoon rainwater doesn't run off into waste.
2️⃣ Native Bund Afforestation: Planting vetiver and soil-binding trees along the bunds to prevent erosion and create bird sanctuaries.
3️⃣ Community Ownership: Engaging local villagers so the waterbody remains protected and maintained for decades.

Clean lakes mean recharged borewells, thriving agriculture, and resilience against scorching summers.

🌱 Commit • Contribute • Conserve

Let’s protect our water heritage before it's too late.

#SpreadLoveFoundation #LakeRestoration #WaterConservation #WaterSecurity #TamilNadu #SDG6 #CommunityAction #CSRImpact #SaveWater"""

        elif is_plantation:
            headline = "Afforestation in Action: Breathing Life Back into the Soil"
            body = f"""🌳 Transforming Barren Spaces into Thriving Green Landscapes

Reflecting on our field drive: "{idea_clean}"

Planting a tree is a vote for the future. But afforestation is not just about putting a sapling in the earth—it is about nurturing polyculture ecosystems that can sustain themselves for generations.

At Spread Love Foundation, every plantation drive is guided by three principles:
✅ 100% Indigenous Native Species: Specially chosen to match the soil and climate.
✅ High Survival Strategy: Systematic organic mulching, geo-tagging, and long-term watering.
✅ Community & Volunteer Participation: Connecting local youth directly to environmental stewardship.

Every native tree planted absorbs harmful carbon, enriches the soil, and provides shelter for local pollinators and birds.

🌱 Commit • Contribute • Conserve

🤝 Ready to turn your corporate CSR or weekend volunteer group into an environmental force? Join us!

#SpreadLoveFoundation #Afforestation #TreePlantation #ClimateAction #GreenCover #Biodiversity #CSRIndia #YouthForEarth #SDG13 #SDG15"""

        else:
            headline = "Action-Driven Environmental Leadership | Spread Love Foundation"
            body = f"""🌿 Transforming Thoughts into Tangible Climate Action

Reflecting on our vision: "{idea_clean}"

At Spread Love Foundation, every project begins with a simple thought: How can we leave this planet better than we found it?

Through our core pillars:
• Afforestation & High-Density Native Plantations
• Wetland & Waterbody Rejuvenation
• Youth Mobilization & Environmental Education
• Corporate CSR Alliances for Scalable Impact

We continue to prove that when communities and organizations unite behind a shared ecological vision, lasting change is not just possible—it is inevitable.

🌱 Commit • Contribute • Conserve

🤝 Join us on this mission. Whether as a volunteer, donor, or CSR partner, your contribution matters!

#SpreadLoveFoundation #ClimateAction #Afforestation #Sustainability #GreenIndia #CSR #EcoLeadership #CommunityImpact"""

        return {
            "title": headline,
            "original_idea": idea_clean,
            "content": body.strip(),
            "created_at": datetime.now().isoformat()
        }

        return {
            "title": headline,
            "original_idea": idea_clean,
            "content": body.strip(),
            "created_at": datetime.now().isoformat()
        }

    def generate_banner(self, headline, subtitle="Commit • Contribute • Conserve"):
        """
        Generates a premium 1200x628 LinkedIn banner image using Pillow.
        Saves into static/banners/ and returns the relative file path.
        """
        width, height = 1200, 628
        # Create image with a rich dark forest-green background
        base = Image.new("RGB", (width, height), color=(14, 43, 28))
        draw = ImageDraw.Draw(base)

        # Draw diagonal accent gradient stripes
        for i in range(height):
            # Gradient from #0d3b24 (13, 59, 36) to #1b5e20 (27, 94, 32)
            r = int(13 + (27 - 13) * (i / height))
            g = int(52 + (88 - 52) * (i / height))
            b = int(30 + (48 - 30) * (i / height))
            draw.line([(0, i), (width, i)], fill=(r, g, b))

        # Accent decorative shapes
        draw.ellipse([width - 320, -100, width + 100, 320], fill=(22, 75, 46))
        draw.ellipse([width - 240, -40, width + 40, 240], fill=(29, 94, 58))
        draw.rectangle([60, 40, width - 60, 44], fill=(76, 175, 80))

        # Load fonts
        try:
            title_font = ImageFont.truetype(str(FONTS_DIR / "segoeuib.ttf"), 54)
            brand_font = ImageFont.truetype(str(FONTS_DIR / "segoeuib.ttf"), 30)
            sub_font = ImageFont.truetype(str(FONTS_DIR / "arialbd.ttf"), 32)
            pill_font = ImageFont.truetype(str(FONTS_DIR / "arialbd.ttf"), 22)
        except Exception:
            title_font = ImageFont.load_default()
            brand_font = ImageFont.load_default()
            sub_font = ImageFont.load_default()
            pill_font = ImageFont.load_default()

        # Top Branding
        draw.text((70, 70), "SPREAD LOVE FOUNDATION", font=brand_font, fill=(165, 214, 167))
        draw.text((70, 115), "DRIVING CLIMATE ACTION THROUGH CSR & COMMUNITY", font=pill_font, fill=(200, 230, 201))

        # Main Headline wrapping
        clean_headline = headline.replace("LinkedIn Post: ", "").replace("🌱", "").replace("🌿", "").replace("🌍", "").strip()
        words = clean_headline.split()
        lines = []
        curr = ""
        for w in words:
            test = curr + " " + w if curr else w
            if len(test) < 32:
                curr = test
            else:
                lines.append(curr)
                curr = w
        if curr:
            lines.append(curr)

        y_text = 210
        for line in lines[:3]:
            draw.text((70, y_text), line, font=title_font, fill=(255, 255, 255))
            y_text += 70

        # Accent separator
        draw.line([(70, y_text + 20), (320, y_text + 20)], fill=(76, 175, 80), width=4)

        # Subtitle / Core Motto
        draw.text((70, y_text + 45), subtitle, font=sub_font, fill=(255, 235, 59))

        # Footer Badges
        footer_y = height - 90
        badges = ["🌿 Afforestation", "💧 Water Restoration", "🌱 Seed Balls", "🤝 CSR Partnerships"]
        bx = 70
        for b in badges:
            # Draw pill
            b_w = len(b) * 12 + 24
            draw.rounded_rectangle([bx, footer_y, bx + b_w, footer_y + 40], radius=8, fill=(24, 78, 48), outline=(76, 175, 80))
            draw.text((bx + 12, footer_y + 8), b, font=pill_font, fill=(255, 255, 255))
            bx += b_w + 16

        # Save image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"banner_{timestamp}.png"
        out_file = self.static_dir / "banners" / filename
        base.save(out_file, "PNG")
        
        return f"/static/banners/{filename}"

