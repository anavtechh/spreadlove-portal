import json
import shutil
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from post_generator import PostGenerator

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "posts_store.json"
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)
(STATIC_DIR / "banners").mkdir(exist_ok=True)
(STATIC_DIR / "uploads").mkdir(exist_ok=True)

generator = PostGenerator()
app = FastAPI(title="Spread Love Foundation - LinkedIn Automation Portal")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

def get_store():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"pending": [], "approved": []}

def save_store(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.get("/api/today-event")
def api_today_event():
    return generator.check_today_event()

@app.get("/api/all-events")
def api_all_events():
    return generator.special_days

@app.post("/api/generate-event-post")
def api_generate_event(payload: dict):
    event_title = payload.get("title")
    target_event = None
    for ev in generator.special_days:
        if ev["title"] == event_title:
            target_event = ev
            break
    if not target_event:
        target_event = {"title": event_title, "theme": payload.get("theme", ""), "category": "General"}
    
    post = generator.generate_special_day_post(target_event)
    banner_url = generator.generate_banner(post["title"])
    post["banner_url"] = banner_url
    return post

@app.post("/api/convert-instagram")
def api_convert_instagram(payload: dict):
    caption = payload.get("caption", "")
    post = generator.convert_instagram_to_linkedin(caption)
    banner_url = generator.generate_banner(post["title"])
    post["banner_url"] = banner_url
    return post

@app.post("/api/generate-from-idea")
def api_generate_from_idea(payload: dict):
    idea = payload.get("idea", "")
    post = generator.generate_from_idea(idea)
    banner_url = generator.generate_banner(post["title"])
    post["banner_url"] = banner_url
    return post

@app.post("/api/generate-banner")
def api_generate_banner(payload: dict):
    title = payload.get("title", "Spread Love Foundation")
    subtitle = payload.get("subtitle", "Commit • Contribute • Conserve")
    banner_url = generator.generate_banner(title, subtitle)
    return {"banner_url": banner_url}

@app.post("/api/upload-image")
async def api_upload_image(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix or ".jpg"
    filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
    dest = STATIC_DIR / "uploads" / filename
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"image_url": f"/static/uploads/{filename}"}

@app.post("/api/approve-post")
def api_approve_post(payload: dict):
    store = get_store()
    post_item = {
        "id": len(store["approved"]) + 1,
        "title": payload.get("title", "Approved Post"),
        "content": payload.get("content", ""),
        "image_url": payload.get("image_url", ""),
        "approved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "APPROVED"
    }
    store["approved"].insert(0, post_item)
    save_store(store)
    return {"status": "success", "post": post_item}

@app.get("/api/history")
def api_history():
    store = get_store()
    return store.get("approved", [])

@app.get("/", response_class=HTMLResponse)
def index():
    html_content = """<!DOCTYPE html>
<html lang="ta">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spread Love Foundation | LinkedIn Automation Hub</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #0a66c2;
            --primary-hover: #004182;
            --green: #057642;
            --green-dark: #1b5e20;
            --green-light: #e8f5e9;
            --bg: #f3f6f8;
            --card: #ffffff;
            --text-dark: #191919;
            --text-muted: #666666;
            --border: #e0e0e0;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
        body { background: var(--bg); color: var(--text-dark); min-height: 100vh; padding-bottom: 60px; }
        
        /* Navbar */
        header {
            background: #ffffff;
            border-bottom: 1px solid var(--border);
            padding: 14px 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .brand-badge {
            background: linear-gradient(135deg, #2e7d32, #1b5e20);
            color: white;
            font-size: 20px;
            font-weight: 700;
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 10px rgba(46,125,50,0.2);
        }
        .brand-text h1 { font-size: 18px; font-weight: 800; color: #1b5e20; letter-spacing: -0.3px; }
        .brand-text p { font-size: 12px; color: var(--text-muted); font-weight: 500; }

        .links-bar {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .pill-btn {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 7px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s;
        }
        .pill-ig { background: #fdf2f4; color: #d62976; border: 1px solid #f8bbd0; }
        .pill-ig:hover { background: #f8bbd0; }
        .pill-li { background: #e8f4f9; color: var(--primary); border: 1px solid #b3d7ff; }
        .pill-li:hover { background: #d0e7ff; }

        /* Main Container */
        .container {
            max-width: 1240px;
            margin: 24px auto;
            padding: 0 20px;
            display: grid;
            grid-template-columns: 1.05fr 1fr;
            gap: 24px;
        }
        @media(max-width: 960px) {
            .container { grid-template-columns: 1fr; }
        }

        /* Tabs */
        .tab-nav {
            display: flex;
            gap: 6px;
            background: #e9ecef;
            padding: 6px;
            border-radius: 12px;
            margin-bottom: 16px;
        }
        .tab-btn {
            flex: 1;
            padding: 10px 14px;
            border-radius: 8px;
            border: none;
            background: transparent;
            font-size: 13px;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        .tab-btn.active {
            background: #ffffff;
            color: var(--green-dark);
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
            font-weight: 700;
        }

        /* Card styles */
        .card {
            background: var(--card);
            border-radius: 14px;
            padding: 22px;
            border: 1px solid var(--border);
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            margin-bottom: 20px;
        }
        .card h2 {
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Idea Quick Chips */
        .chips-row {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 12px;
        }
        .chip {
            background: #f1f8e9;
            color: #2e7d32;
            border: 1px solid #c8e6c9;
            padding: 5px 10px;
            border-radius: 16px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s;
        }
        .chip:hover {
            background: #c8e6c9;
        }

        /* Upload Dropzone */
        .upload-box {
            border: 2px dashed #b0bec5;
            border-radius: 10px;
            padding: 14px;
            text-align: center;
            background: #fafafa;
            margin-bottom: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .upload-box:hover {
            border-color: var(--green);
            background: #f1f8e9;
        }
        .upload-box p { font-size: 12px; color: var(--text-muted); margin-top: 4px; }

        /* Form Controls */
        textarea, select, input {
            width: 100%;
            padding: 12px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 14px;
            outline: none;
            transition: border 0.2s;
            margin-bottom: 12px;
        }
        textarea:focus, select:focus { border-color: var(--green); }
        textarea { resize: vertical; min-height: 110px; }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 10px 18px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
        }
        .btn-primary { background: var(--primary); color: white; }
        .btn-primary:hover { background: var(--primary-hover); }
        .btn-success { background: var(--green); color: white; }
        .btn-success:hover { background: #046337; }
        .btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text-dark); }
        .btn-outline:hover { background: #f0f0f0; }

        /* Banner banner */
        .event-banner {
            background: linear-gradient(135deg, #e8f5e9, #c8e6c9);
            border: 1px solid #a5d6a7;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }
        .event-info h3 { font-size: 15px; color: #1b5e20; font-weight: 700; }
        .event-info p { font-size: 13px; color: #2e7d32; margin-top: 4px; }

        /* LinkedIn Mockup Card */
        .linkedin-preview {
            background: #ffffff;
            border: 1px solid #dcdcdc;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        }
        .li-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }
        .li-avatar {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: #1b5e20;
            color: white;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        }
        .li-meta h4 { font-size: 14px; font-weight: 700; color: #191919; }
        .li-meta p { font-size: 12px; color: var(--text-muted); }
        .li-body {
            font-size: 13.5px;
            line-height: 1.6;
            color: #262626;
            white-space: pre-wrap;
            background: #fafafa;
            border: 1px solid #eeeeee;
            padding: 14px;
            border-radius: 8px;
            max-height: 280px;
            overflow-y: auto;
            margin-bottom: 12px;
        }

        /* Image Attachment in Preview */
        .media-preview-container {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
            background: #121212;
            position: relative;
            margin-bottom: 14px;
        }
        .media-preview-img {
            width: 100%;
            max-height: 280px;
            object-fit: cover;
            display: block;
        }
        .media-actions {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #ffffff;
            padding: 8px 12px;
            border-top: 1px solid #e0e0e0;
        }

        .action-row {
            margin-top: 14px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .toast {
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #263238;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 14px;
            display: none;
            z-index: 1000;
            box-shadow: 0 6px 16px rgba(0,0,0,0.25);
        }
        
        .tag-pill {
            display: inline-block;
            background: #e8f5e9;
            color: #2e7d32;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
        }
    </style>
</head>
<body>

    <header>
        <div class="brand">
            <div class="brand-badge">🌱</div>
            <div class="brand-text">
                <h1>Spread Love Foundation</h1>
                <p>Social Media Impact Engine • Idea & Instagram ➔ LinkedIn Hub</p>
            </div>
        </div>
        <div class="links-bar">
            <a href="https://www.instagram.com/spreadlove2030" target="_blank" class="pill-btn pill-ig">
                📸 @spreadlove2030
            </a>
            <a href="https://www.linkedin.com/in/spread-love-foundation-394085418" target="_blank" class="pill-btn pill-li">
                💼 LinkedIn Profile
            </a>
        </div>
    </header>

    <div class="container">
        <!-- Left Column: Tabs & Inputs -->
        <div>
            <!-- Navigation Tabs -->
            <div class="tab-nav">
                <button class="tab-btn active" id="btnTab1" onclick="switchTab(1)">
                    💡 என் யோசனை (Custom Idea)
                </button>
                <button class="tab-btn" id="btnTab2" onclick="switchTab(2)">
                    📸 Instagram கன்வெர்ட்டர்
                </button>
                <button class="tab-btn" id="btnTab3" onclick="switchTab(3)">
                    🌍 இயற்கை தினங்கள் (Events)
                </button>
            </div>

            <!-- Tab 1: Custom Mind Idea -->
            <div id="tab1Content" class="card">
                <h2>💡 உங்கள் மனதில் தோன்றும் எண்ணங்கள் (Thoughts to Post)</h2>
                <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 10px;">
                    உங்கள் மனதில் தோன்றும் எளிய வரிகளை உள்ளிடுங்கள் (தமிழ் அல்லது ஆங்கிலத்தில்). AI அதை முழுமையான LinkedIn பதிவாக மாற்றும்:
                </p>
                
                <div class="chips-row">
                    <span class="chip" onclick="setIdea('Spread Love Foundation ஏன் ரொம்ப இம்பார்ட்டன்ட் அப்படின்னா நேச்சருக்கு')">
                        🌱 SLF ஏன் இயற்கைக்கு முக்கியம்?
                    </span>
                    <span class="chip" onclick="setIdea('விதைப்பந்து தயாரிப்பதன் பயன்கள் மற்றும் இளைஞர்களின் பங்களிப்பு')">
                        🌰 விதைப்பந்து இயக்கம்
                    </span>
                    <span class="chip" onclick="setIdea('ஏரிகளை தூர்வாருவது மற்றும் நிலத்தடி நீர்மட்டத்தை உயர்த்துவது')">
                        💧 ஏரி சீரமைப்பு
                    </span>
                    <span class="chip" onclick="setIdea('கார்ப்பரேட் நிறுவனங்களின் CSR மூலம் மரம் நடும் திட்டம்')">
                        🤝 CSR மரம் நடுதல்
                    </span>
                </div>

                <textarea id="ideaInput" placeholder="உதாரணமாக:
Spread Love Foundation ஏன் ரொம்ப இம்பார்ட்டன்ட் அப்படின்னா நேச்சருக்கு, நாம களத்துல இறங்கி மரக்கன்றுகள் நடுறோம், ஏரிகளை மீட்டெடுக்கிறோம்..."></textarea>

                <!-- Optional Image Upload -->
                <label style="font-size: 12px; font-weight: 600; color: var(--text-muted); display: block; margin-bottom: 4px;">
                    புகைப்படம் இணைக்க (விருப்பப்பட்டால்):
                </label>
                <div class="upload-box" onclick="document.getElementById('imgUploadInput').click()">
                    <span style="font-size: 20px;">📷</span>
                    <p id="uploadText">புகைப்படத்தை தேர்ந்தெடுக்க இங்கே கிளிக் செய்யவும் (JPG, PNG)</p>
                    <input type="file" id="imgUploadInput" accept="image/*" style="display: none;" onchange="handleImageUpload(event)">
                </div>

                <div style="display: flex; gap: 10px;">
                    <button class="btn btn-success" style="flex: 1;" onclick="generateFromIdea()">
                        ✨ Generate Post & AI Banner
                    </button>
                </div>
            </div>

            <!-- Tab 2: Instagram Caption Converter -->
            <div id="tab2Content" class="card" style="display: none;">
                <h2>📸 Convert Instagram Post ➔ LinkedIn Post</h2>
                <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 12px;">
                    இன்ஸ்டாகிராமில் பதிவிட்ட கேப்ஷன், விதைப்பந்து, மரம் நடுதல் அல்லது ஏரி சீரமைப்பு நிகழ்வு விவரங்களை உள்ளிடவும்:
                </p>
                <textarea id="igCaption" placeholder="உதாரணமாக:
Today our Spread Love Foundation volunteers planted 500 saplings in Coimbatore with Hirotec team! Native species like Neem and Peepal planted for biodiversity restoration..."></textarea>
                
                <div style="display: flex; gap: 10px;">
                    <button class="btn btn-primary" onclick="convertInstagramPost()">
                        ⚡ Convert to Professional LinkedIn Post
                    </button>
                    <button class="btn btn-outline" onclick="loadSampleCaption()">
                        📝 Load Sample
                    </button>
                </div>
            </div>

            <!-- Tab 3: Nature & Health Special Days -->
            <div id="tab3Content" class="card" style="display: none;">
                <h2>🌍 Nature & Health Days Generator</h2>
                <div id="eventBanner" class="event-banner">
                    <div class="event-info">
                        <span class="tag-pill" id="eventBadge">TODAY'S EVENT</span>
                        <h3 id="eventTitle">Loading events...</h3>
                        <p id="eventTheme"></p>
                    </div>
                    <button class="btn btn-success" id="genEventBtn" onclick="generateCurrentEventPost()">
                        ✨ Generate Post
                    </button>
                </div>

                <label style="font-size: 12px; font-weight: 600; color: var(--text-muted); display: block; margin-bottom: 6px;">
                    அல்லது ஏதேனும் ஒரு சிறப்பு தினத்தைத் தேர்ந்தெடுக்கவும்:
                </label>
                <select id="eventSelector" onchange="onSelectCustomEvent()">
                    <option value="">-- சுற்றுச்சூழல் / சுகாதார தினத்தைத் தேர்ந்தெடுக்கவும் --</option>
                </select>
            </div>
        </div>

        <!-- Right Column: LinkedIn Live Preview & Media -->
        <div>
            <div class="card">
                <h2>👀 LinkedIn Post Preview (Review & Approve)</h2>
                
                <div class="linkedin-preview">
                    <div class="li-header">
                        <div class="li-avatar">SL</div>
                        <div class="li-meta">
                            <h4>Spread Love Foundation</h4>
                            <p>Driving Climate Action Through CSR | Commit • Contribute • Conserve</p>
                            <p style="font-size: 11px; color: #888;">Just now • 🌐 Public</p>
                        </div>
                    </div>
                    
                    <div id="previewBody" class="li-body">தயாரான LinkedIn போஸ்ட் இங்கே தோன்றும்.

இடது பக்கத்தில் உங்கள் எண்ணங்களை உள்ளிட்டு "Generate Post & AI Banner" கிளிக் செய்யுங்கள்!</div>

                    <!-- Image / Banner Container -->
                    <div id="mediaBox" class="media-preview-container" style="display: none;">
                        <img id="attachedImg" class="media-preview-img" src="" alt="Post Visual">
                        <div class="media-actions">
                            <span style="font-size: 12px; color: #2e7d32; font-weight: 600;" id="mediaLabel">🌿 AI Generated Banner</span>
                            <div style="display: flex; gap: 8px;">
                                <a id="downloadImgBtn" href="#" download="spread_love_post.png" class="btn btn-outline" style="padding: 4px 10px; font-size: 11px;">
                                    📥 Download Image
                                </a>
                                <button class="btn btn-outline" style="padding: 4px 10px; font-size: 11px;" onclick="regenerateBanner()">
                                    🔄 New Banner
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="action-row">
                        <button class="btn btn-success" onclick="approveAndShare()">
                            🚀 Approve & Post on LinkedIn
                        </button>
                        <button class="btn btn-primary" onclick="copyToClipboard()">
                            📋 Copy Text
                        </button>
                        <button class="btn btn-outline" onclick="editPost()">
                            ✏️ Edit Draft
                        </button>
                    </div>
                </div>
            </div>

            <!-- Approved History -->
            <div class="card">
                <h2>📜 Approved Posts History</h2>
                <div id="historyList" style="max-height: 180px; overflow-y: auto; font-size: 13px; color: var(--text-muted);">
                    இன்னும் போஸ்ட்கள் அனுமதிக்கப்படவில்லை.
                </div>
            </div>
        </div>
    </div>

    <div id="toast" class="toast"></div>

    <script>
        let currentPost = null;
        let todayEvent = null;
        let activeImageUrl = null;

        function showToast(msg) {
            const t = document.getElementById("toast");
            t.innerText = msg;
            t.style.display = "block";
            setTimeout(() => { t.style.display = "none"; }, 3200);
        }

        function switchTab(num) {
            [1, 2, 3].forEach(n => {
                document.getElementById('tab' + n + 'Content').style.display = (n === num) ? 'block' : 'none';
                document.getElementById('btnTab' + n).classList.toggle('active', n === num);
            });
        }

        function setIdea(text) {
            document.getElementById("ideaInput").value = text;
        }

        function setMediaPreview(url, label) {
            activeImageUrl = url;
            const box = document.getElementById("mediaBox");
            const img = document.getElementById("attachedImg");
            const lbl = document.getElementById("mediaLabel");
            const dl = document.getElementById("downloadImgBtn");

            if (url) {
                img.src = url;
                lbl.innerText = label || "Attached Visual";
                dl.href = url;
                box.style.display = "block";
            } else {
                box.style.display = "none";
            }
        }

        async function handleImageUpload(e) {
            const file = e.target.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append("file", file);

            document.getElementById("uploadText").innerText = "Uploading " + file.name + "...";

            try {
                const res = await fetch("/api/upload-image", {
                    method: "POST",
                    body: formData
                });
                const data = await res.json();
                setMediaPreview(data.image_url, "📸 Uploaded Reference Photo: " + file.name);
                document.getElementById("uploadText").innerText = "Attached: " + file.name;
                showToast("Uploaded photo attached!");
            } catch (err) {
                alert("Upload failed: " + err);
            }
        }

        async function generateFromIdea() {
            const idea = document.getElementById("ideaInput").value.trim();
            if (!idea) {
                alert("தயவுசெய்து உங்கள் எண்ணங்களை உள்ளிடவும்!");
                return;
            }

            showToast("Crafting LinkedIn Post & Generating Banner...");

            const res = await fetch("/api/generate-from-idea", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ idea })
            });
            const data = await res.json();
            currentPost = data;
            document.getElementById("previewBody").innerText = data.content;

            // If user hasn't uploaded a custom photo, use generated AI banner
            if (!activeImageUrl || activeImageUrl.includes("/banners/")) {
                setMediaPreview(data.banner_url, "🌿 AI Generated Branded Banner");
            }
            showToast("Post & AI Banner Ready!");
        }

        async function regenerateBanner() {
            if (!currentPost) return;
            showToast("Generating new banner...");
            const res = await fetch("/api/generate-banner", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    title: currentPost.title,
                    subtitle: "Commit • Contribute • Conserve"
                })
            });
            const data = await res.json();
            setMediaPreview(data.banner_url, "🌿 AI Generated Branded Banner");
            showToast("New banner generated!");
        }

        async function convertInstagramPost() {
            const caption = document.getElementById("igCaption").value.trim();
            if (!caption) {
                alert("தயவுசெய்து Instagram கேப்ஷனை உள்ளிடவும்!");
                return;
            }
            const res = await fetch("/api/convert-instagram", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ caption })
            });
            const data = await res.json();
            currentPost = data;
            document.getElementById("previewBody").innerText = data.content;
            if (!activeImageUrl || activeImageUrl.includes("/banners/")) {
                setMediaPreview(data.banner_url, "🌿 AI Generated Banner");
            }
            showToast("Converted to LinkedIn format!");
        }

        function loadSampleCaption() {
            document.getElementById("igCaption").value = 
`Massive Afforestation Drive with our dedicated volunteers! 
Planted 1,200 native saplings in Kurinji Thottam with local youth brigade and corporate CSR support. 
Focusing on biodiversity restoration, bird habitats and ground water recharge. 
Commit. Contribute. Conserve. #SpreadLove #Afforestation #PlantTrees #GreenCover #TamilNadu`;
        }

        async function generateCurrentEventPost() {
            if (!todayEvent) return;
            const res = await fetch("/api/generate-event-post", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(todayEvent)
            });
            const data = await res.json();
            currentPost = data;
            document.getElementById("previewBody").innerText = data.content;
            setMediaPreview(data.banner_url, "🌿 Event Awareness Banner");
            showToast("Special Day LinkedIn Post Generated!");
        }

        async function onSelectCustomEvent() {
            const val = document.getElementById("eventSelector").value;
            if (!val) return;
            const res = await fetch("/api/generate-event-post", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: val })
            });
            const data = await res.json();
            currentPost = data;
            document.getElementById("previewBody").innerText = data.content;
            setMediaPreview(data.banner_url, "🌿 Event Awareness Banner");
            showToast("Generated post for " + val);
        }

        async function approveAndShare() {
            const content = document.getElementById("previewBody").innerText;
            if (!content || content.includes("தயாரான LinkedIn போஸ்ட் இங்கே")) {
                alert("முதலில் ஒரு போஸ்ட்டை உருவாக்கவும்!");
                return;
            }

            await fetch("/api/approve-post", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    title: currentPost ? currentPost.title : "LinkedIn Post",
                    content: content,
                    image_url: activeImageUrl
                })
            });

            await navigator.clipboard.writeText(content);
            showToast("Approved! Copied text & opening LinkedIn...");

            setTimeout(() => {
                window.open("https://www.linkedin.com/feed/?shareActive=true", "_blank");
            }, 800);

            loadHistory();
        }

        async function copyToClipboard() {
            const content = document.getElementById("previewBody").innerText;
            await navigator.clipboard.writeText(content);
            showToast("Copied to clipboard!");
        }

        function editPost() {
            const current = document.getElementById("previewBody").innerText;
            const updated = prompt("போஸ்ட் உள்ளடக்கத்தைத் திருத்தவும்:", current);
            if (updated !== null) {
                document.getElementById("previewBody").innerText = updated;
                showToast("Updated draft!");
            }
        }

        async function loadHistory() {
            const res = await fetch("/api/history");
            const data = await res.json();
            const list = document.getElementById("historyList");
            if (!data || data.length === 0) {
                list.innerHTML = "<p>இன்னும் போஸ்ட்கள் அனுமதிக்கப்படவில்லை.</p>";
                return;
            }
            list.innerHTML = data.map(item => `
                <div style="padding: 8px 0; border-bottom: 1px solid #eee;">
                    <strong>${item.title}</strong>
                    <div style="font-size: 11px; color: #888;">${item.approved_at} • APPROVED</div>
                </div>
            `).join("");
        }

        async function init() {
            try {
                const res = await fetch("/api/today-event");
                const data = await res.json();
                const badge = document.getElementById("eventBadge");
                const title = document.getElementById("eventTitle");
                const theme = document.getElementById("eventTheme");

                if (data.is_today && data.event) {
                    todayEvent = data.event;
                    badge.innerText = "TODAY'S SPECIAL EVENT";
                    badge.style.background = "#e8f5e9";
                    badge.style.color = "#1b5e20";
                    title.innerText = data.event.title;
                    theme.innerText = data.event.theme;
                } else if (data.upcoming) {
                    todayEvent = data.upcoming;
                    badge.innerText = "UPCOMING OBSERVANCE (" + data.upcoming.date + ")";
                    badge.style.background = "#e3f2fd";
                    badge.style.color = "#0d47a1";
                    title.innerText = data.upcoming.title;
                    theme.innerText = data.upcoming.theme;
                }

                const allRes = await fetch("/api/all-events");
                const allEvents = await allRes.json();
                const sel = document.getElementById("eventSelector");
                allEvents.forEach(e => {
                    const opt = document.createElement("option");
                    opt.value = e.title;
                    opt.innerText = `[${e.date}] ${e.title} (${e.category})`;
                    sel.appendChild(opt);
                });

                loadHistory();
            } catch (err) {
                console.error(err);
            }
        }

        window.onload = init;
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)
