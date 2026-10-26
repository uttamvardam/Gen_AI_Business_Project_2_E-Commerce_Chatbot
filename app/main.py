import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Sync secrets from Streamlit Cloud to os.environ if available
try:
    if hasattr(st, "secrets"):
        for sec_key, sec_val in st.secrets.items():
            if isinstance(sec_val, str) and sec_key not in os.environ:
                os.environ[sec_key] = sec_val
except Exception:
    pass

import base64
import re
from pathlib import Path
import streamlit.components.v1 as components
from faq import ingest_faq_data, faq_chain
from sql import sql_chain
from router import router

def render_html(html_str: str):
    """
    Renders custom HTML cleanly without Markdown interpreting indented lines as code blocks.
    Removes HTML comments and collapses whitespace so that CommonMark does not wrap lines in <pre><code>.
    """
    clean = re.sub(r'<!--.*?-->', '', html_str, flags=re.DOTALL)
    lines = [line.strip() for line in clean.splitlines() if line.strip()]
    st.markdown(" ".join(lines), unsafe_allow_html=True)


# ---------------------------------------------------------
# 1. Pipeline & RAG Initialization (Existing Logic Preserved)
# ---------------------------------------------------------
faqs_path = Path(__file__).parent / "resources/faq_data.csv"
ingest_faq_data(faqs_path)

def ask(query):
    route = router(query).name
    if route == 'faq':
        return faq_chain(query)
    elif route == 'sql':
        return sql_chain(query)
    else:
        return f"Route {route} not implemented yet"

# ---------------------------------------------------------
# 2. Page Configuration & Asset Loading
# ---------------------------------------------------------
st.set_page_config(
    page_title="CartIQ - AI-Powered Shopping Assistant",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ASSETS_DIR = Path(__file__).parent / "assets"
user_avatar_path = ASSETS_DIR / "user_avatar.png"
bot_avatar_path = ASSETS_DIR / "bot_avatar.png"
cart_hero_path = ASSETS_DIR / "cart_hero_transparent.png"
sneaker_blue_path = ASSETS_DIR / "sneaker_blue.png"
sneaker_black_path = ASSETS_DIR / "sneaker_black.png"

def get_base64_img(img_path):
    if img_path.exists():
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

cart_hero_b64 = get_base64_img(cart_hero_path)
sneaker_blue_b64 = get_base64_img(sneaker_blue_path)
sneaker_black_b64 = get_base64_img(sneaker_black_path)

# ---------------------------------------------------------
# 3. Custom Design System & CSS (CartIQ Reference Match)
# ---------------------------------------------------------
CARTIQ_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body {{
    background-color: #050816 !important;
    color: #F8FAFC !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    overflow-x: hidden !important;
}}

/* Custom sleek scrollbar */
::-webkit-scrollbar {{
    width: 6px;
    height: 6px;
}}
::-webkit-scrollbar-track {{
    background: #050816;
}}
::-webkit-scrollbar-thumb {{
    background: rgba(99, 102, 241, 0.35);
    border-radius: 9999px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: rgba(99, 102, 241, 0.65);
}}

/* Hide default Streamlit chrome */
#MainMenu {{ visibility: hidden !important; }}
header[data-testid="stHeader"] {{ display: none !important; }}
[data-testid="stToolbar"] {{ display: none !important; }}
footer {{ display: none !important; }}
[data-testid="stDecoration"] {{ display: none !important; }}
[data-testid="stStatusWidget"] {{ display: none !important; }}

/* Futuristic ambient background with dotted matrix */
[data-testid="stAppViewContainer"] {{
    background-color: #050816 !important;
    background-image: 
        radial-gradient(rgba(59, 130, 246, 0.12) 1.2px, transparent 1.2px),
        radial-gradient(circle at 18% 52%, rgba(37, 99, 235, 0.28) 0%, transparent 48%),
        radial-gradient(circle at 82% 40%, rgba(109, 93, 251, 0.22) 0%, transparent 46%),
        radial-gradient(ellipse 70% 25% at 50% 85%, rgba(20, 30, 75, 0.55) 0%, transparent 70%) !important;
    background-size: 24px 24px, 100% 100%, 100% 100%, 100% 100% !important;
    background-attachment: fixed !important;
}}

[data-testid="stAppViewContainer"] > .main {{
    background: transparent !important;
}}

.main .block-container {{
    max-width: 1520px !important;
    padding-top: 10px !important;
    padding-bottom: 120px !important;
    padding-left: 24px !important;
    padding-right: 24px !important;
    margin: 0 auto !important;
}}

/* =========================================================
   TOP NAVIGATION BAR
   ========================================================= */
.cartiq-navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    padding: 12px 0 18px 0;
    margin-bottom: 8px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    position: relative;
    z-index: 20;
}}

.navbar-brand {{
    display: flex;
    align-items: center;
    gap: 14px;
}}

.navbar-logo-icon {{
    display: flex;
    align-items: center;
    justify-content: center;
    filter: drop-shadow(0 0 14px rgba(56, 189, 248, 0.7));
}}

.navbar-brand-details {{
    display: flex;
    flex-direction: column;
}}

.navbar-brand-title {{
    font-size: 26px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.4px;
    line-height: 1.1;
}}

.navbar-brand-sub {{
    font-size: 12px;
    font-weight: 500;
    color: #8F9BB3;
    letter-spacing: 0.2px;
    margin-top: 2px;
}}

/* Center Navigation Pills */
.navbar-nav-tabs {{
    display: flex;
    align-items: center;
    gap: 8px;
}}

.nav-tab-pill {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 18px;
    border-radius: 9999px;
    font-size: 13.5px;
    font-weight: 500;
    color: #94A3B8;
    background: transparent;
    border: 1px solid transparent;
    cursor: default;
    transition: all 0.2s ease;
}}

.nav-tab-pill.active {{
    background: rgba(18, 26, 60, 0.9);
    border: 1px solid rgba(59, 130, 246, 0.6);
    color: #FFFFFF;
    box-shadow: 0 0 16px rgba(59, 130, 246, 0.25);
}}

.nav-tab-pill svg {{
    width: 15px;
    height: 15px;
    opacity: 0.85;
}}

/* Right Controls */
.navbar-right {{
    display: flex;
    align-items: center;
    gap: 16px;
}}

.nav-icon-btn {{
    color: #94A3B8;
    background: transparent;
    border: none;
    cursor: default;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 6px;
    border-radius: 8px;
    transition: all 0.2s ease;
}}

.nav-deploy-btn {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.18);
    color: #F1F5F9;
    padding: 6px 18px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    cursor: default;
    backdrop-filter: blur(8px);
}}

/* =========================================================
   TWO-COLUMN MAIN CONTAINER LAYOUT
   ========================================================= */
.cartiq-main-grid {{
    display: grid;
    grid-template-columns: 1.15fr 0.85fr;
    gap: 36px;
    align-items: center;
    margin-top: 6px;
}}

.cartiq-single-col {{
    max-width: 1040px;
    margin: 20px auto 0 auto;
    width: 100%;
}}

.cartiq-single-col .hero-visual-wrapper {{
    justify-content: center;
    gap: 36px;
}}

@media (max-width: 1200px) {{
    .cartiq-main-grid {{
        grid-template-columns: 1fr;
    }}
}}

/* LEFT COLUMN HERO & FEATURES */
.cartiq-left-col {{
    display: flex;
    flex-direction: column;
    gap: 22px;
}}

.hero-visual-wrapper {{
    display: flex;
    align-items: center;
    gap: 24px;
}}

.cart-hero-img-container {{
    width: 290px;
    min-width: 280px;
    filter: drop-shadow(0 0 35px rgba(37, 99, 235, 0.45));
    animation: floatCart 6s ease-in-out infinite alternate;
}}

@keyframes floatCart {{
    0% {{ transform: translateY(0px); }}
    100% {{ transform: translateY(-6px); }}
}}

.cart-hero-img-container img {{
    width: 100%;
    height: auto;
    display: block;
}}

.hero-text-block {{
    flex: 1;
}}

.hero-pill {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 5px 18px;
    background: rgba(18, 23, 48, 0.85);
    border: 1px solid rgba(109, 93, 251, 0.45);
    border-radius: 9999px;
    color: #C4B5FD;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.3px;
    box-shadow: 0 0 16px rgba(109, 93, 251, 0.2);
    margin-bottom: 12px;
}}

.hero-pill-sparkle {{
    color: #38BDF8;
    font-size: 13px;
}}

.hero-main-title {{
    font-size: 46px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -1.2px;
    line-height: 1.12;
    margin: 0 0 12px 0;
}}

.gradient-ai-chatbot {{
    background: linear-gradient(135deg, #3B82F6 10%, #A855F7 90%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
    filter: drop-shadow(0 0 25px rgba(99, 102, 241, 0.5));
}}

.hero-sub-desc {{
    font-size: 15px;
    color: #94A3B8;
    font-weight: 400;
    line-height: 1.5;
    margin: 0;
}}

/* 4 Feature Cards Row */
.features-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
}}

.feature-card {{
    background: rgba(13, 19, 44, 0.7);
    border: 1px solid rgba(59, 130, 246, 0.22);
    border-radius: 18px;
    padding: 16px 12px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    backdrop-filter: blur(12px);
    transition: all 0.2s ease;
}}

.feature-card:hover {{
    border-color: rgba(99, 102, 241, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}}

.feature-icon-circle {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: rgba(20, 28, 64, 0.9);
    border: 1.5px solid rgba(56, 189, 248, 0.45);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #38BDF8;
    margin-bottom: 10px;
    box-shadow: 0 0 14px rgba(56, 189, 248, 0.3);
}}

.feature-title {{
    font-size: 13.5px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 4px;
}}

.feature-desc {{
    font-size: 11.5px;
    color: #8F9BB3;
    line-height: 1.4;
}}

/* 4 Quick Query Chips Row */
.query-chips-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
}}

.query-chip {{
    background: rgba(12, 18, 42, 0.8);
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 9999px;
    padding: 9px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 500;
    color: #E2E8F0;
    cursor: pointer;
    backdrop-filter: blur(10px);
    transition: all 0.2s ease;
    text-decoration: none;
}}

.query-chip:hover {{
    border-color: rgba(139, 92, 246, 0.7);
    background: rgba(25, 34, 75, 0.9);
    color: #FFFFFF;
    transform: translateY(-1px);
    box-shadow: 0 0 16px rgba(99, 102, 241, 0.3);
}}

.chip-left {{
    display: flex;
    align-items: center;
    gap: 6px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}

.chip-arrow {{
    color: #94A3B8;
    font-size: 14px;
    margin-left: 4px;
}}

/* =========================================================
   RIGHT COLUMN: CHAT WIDGET WINDOW
   ========================================================= */
.cartiq-chat-card {{
    background: rgba(10, 15, 38, 0.82);
    border: 1px solid rgba(59, 130, 246, 0.35);
    border-radius: 26px;
    padding: 22px;
    box-shadow: 0 0 35px rgba(37, 99, 235, 0.2), 0 12px 40px rgba(0, 0, 0, 0.55);
    backdrop-filter: blur(20px);
    display: flex;
    flex-direction: column;
    gap: 16px;
    min-height: 480px;
    max-height: 530px;
    overflow-y: auto;
    position: relative;
}}

/* Empty state when no messages yet */
.chat-empty-state {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    min-height: 420px;
    text-align: center;
    padding: 24px;
}}

.chat-empty-icon {{
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #38BDF8;
    margin-bottom: 16px;
    box-shadow: 0 0 24px rgba(56, 189, 248, 0.22);
}}

.chat-empty-title {{
    font-size: 18px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 8px;
    letter-spacing: -0.3px;
}}

.chat-empty-subtitle {{
    font-size: 13px;
    color: #8F9BB3;
    max-width: 320px;
    line-height: 1.55;
    margin: 0;
}}

/* User Bubble in Chat Card */
.chat-user-row {{
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 10px;
}}

.chat-user-bubble {{
    background: rgba(22, 34, 78, 0.9);
    border: 1px solid rgba(99, 102, 241, 0.45);
    border-radius: 18px 18px 4px 18px;
    padding: 11px 18px;
    font-size: 14px;
    color: #FFFFFF;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    white-space: pre-wrap;
    word-break: break-word;
}}

.chat-user-avatar {{
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg, #2563EB, #3B82F6);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 12px rgba(37, 99, 235, 0.5);
    flex-shrink: 0;
}}

/* Product Cards Carousel in Chat Card */
.chat-products-row {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin: 4px 0;
}}

.product-mini-card {{
    background: rgba(16, 24, 54, 0.85);
    border: 1px solid rgba(59, 130, 246, 0.25);
    border-radius: 14px;
    padding: 10px;
    position: relative;
    display: flex;
    flex-direction: column;
    transition: all 0.2s ease;
}}

.product-mini-card:hover {{
    border-color: rgba(99, 102, 241, 0.6);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
}}

.product-heart-icon {{
    position: absolute;
    top: 8px;
    right: 8px;
    color: rgba(255, 255, 255, 0.6);
    font-size: 13px;
}}

.product-img-box {{
    width: 100%;
    height: 75px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 6px;
}}

.product-img-box img {{
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.5));
}}

.product-price {{
    font-size: 14px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 2px;
}}

.product-rating {{
    font-size: 10.5px;
    color: #FBBF24;
    display: flex;
    align-items: center;
    gap: 3px;
}}

.rating-count {{
    color: #94A3B8;
}}

/* Bot Bubble in Chat Card */
.chat-bot-row {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
}}

.chat-bot-avatar {{
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg, #3B82F6, #6366F1);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.5);
    flex-shrink: 0;
}}

.chat-bot-bubble {{
    background: rgba(14, 20, 48, 0.9);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 4px 18px 18px 18px;
    padding: 13px 18px;
    font-size: 14px;
    line-height: 1.55;
    color: #E2E8F0;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.3);
    flex: 1;
    white-space: pre-wrap;
    word-break: break-word;
}}

/* Action buttons under responses */
.msg-actions {{
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 10px;
    margin-top: 8px;
    padding-top: 4px;
}}

.msg-action-btn {{
    background: transparent;
    border: none;
    color: #64748B;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 4px;
    border-radius: 4px;
    transition: all 0.2s ease;
}}

.msg-action-btn:hover {{
    color: #38BDF8;
    background: rgba(56, 189, 248, 0.1);
}}

/* =========================================================
   BOTTOM FLOATING INPUT BAR
   ========================================================= */
[data-testid="stBottom"] {{
    background: transparent !important;
    border: none !important;
    padding-bottom: 22px !important;
    z-index: 50 !important;
}}

[data-testid="stBottom"] > div {{
    background: transparent !important;
    max-width: 1050px !important;
    margin: 0 auto !important;
    padding: 0 16px !important;
}}

[data-testid="stChatInput"] {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}}

[data-testid="stChatInput"] > div {{
    background: rgba(11, 16, 38, 0.95) !important;
    border: 1.5px solid rgba(99, 102, 241, 0.5) !important;
    border-radius: 9999px !important;
    box-shadow: 0 0 30px rgba(59, 130, 246, 0.2), 0 10px 30px rgba(0, 0, 0, 0.6) !important;
    backdrop-filter: blur(20px) !important;
    padding: 6px 12px 6px 16px !important;
    display: flex !important;
    align-items: center !important;
    transition: all 0.25s ease !important;
}}

[data-testid="stChatInput"] > div:focus-within {{
    border-color: rgba(139, 92, 246, 0.85) !important;
    box-shadow: 0 0 35px rgba(99, 102, 241, 0.35), 0 12px 35px rgba(0, 0, 0, 0.7) !important;
}}

[data-testid="stChatInputTextArea"] {{
    background-color: transparent !important;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='%2394A3B8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48'%3E%3C/path%3E%3C/svg%3E") !important;
    background-repeat: no-repeat !important;
    background-position: 8px center !important;
    background-size: 20px 20px !important;
    padding-left: 42px !important;
    padding-top: 10px !important;
    padding-bottom: 10px !important;
    color: #FFFFFF !important;
    font-size: 15px !important;
    font-family: inherit !important;
    line-height: 1.5 !important;
    caret-color: #38BDF8 !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}}

[data-testid="stChatInputTextArea"]::placeholder {{
    color: #94A3B8 !important;
    font-size: 15px !important;
    font-weight: 400 !important;
}}

[data-testid="stChatInputSubmitButton"] {{
    background: linear-gradient(135deg, #3B82F6 0%, #6366F1 100%) !important;
    border-radius: 50% !important;
    width: 40px !important;
    height: 40px !important;
    min-width: 40px !important;
    min-height: 40px !important;
    border: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 0 18px rgba(59, 130, 246, 0.5) !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    padding: 0 !important;
    margin-left: 8px !important;
}}

[data-testid="stChatInputSubmitButton"]:hover {{
    transform: scale(1.06) !important;
    box-shadow: 0 0 24px rgba(99, 102, 241, 0.75) !important;
}}

[data-testid="stChatInputSubmitButton"] svg {{
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
    width: 18px !important;
    height: 18px !important;
}}
</style>
"""

st.markdown(CARTIQ_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. Top Navigation Bar Component
# ---------------------------------------------------------
NAVBAR_HTML = """
<header class="cartiq-navbar">
    <div class="navbar-brand">
        <div class="navbar-logo-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 34 34" width="46" height="46" fill="none">
              <defs>
                <linearGradient id="cartGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#38BDF8"/>
                  <stop offset="100%" stop-color="#6366F1"/>
                </linearGradient>
                <filter id="cartGlow" x="-20%" y="-20%" width="140%" height="140%">
                  <feGaussianBlur stdDeviation="1.5" result="blur" />
                  <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
              </defs>
              <g filter="url(#cartGlow)">
                <path d="M4 6h4l3.4 13.5a1.5 1.5 0 0 0 1.45 1.1h12.5a1.5 1.5 0 0 0 1.45-1.1L29 9.5H8.8" stroke="url(#cartGrad)" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="14" cy="26" r="2.2" fill="url(#cartGrad)"/>
                <circle cx="24.5" cy="26" r="2.2" fill="url(#cartGrad)"/>
                <path d="M28 3l.8 2.2L31 6l-2.2.8L28 9l-.8-2.2L25 6l2.2-.8z" fill="#38BDF8"/>
              </g>
            </svg>
        </div>
        <div class="navbar-brand-details">
            <span class="navbar-brand-title">CartIQ</span>
            <span class="navbar-brand-sub">AI-Powered Shopping Assistant</span>
        </div>
    </div>
    
    <div class="navbar-nav-tabs">
        <div class="nav-tab-pill active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                <polyline points="9 22 9 12 15 12 15 22"></polyline>
            </svg>
            <span>Home</span>
        </div>
        <div class="nav-tab-pill">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            </svg>
            <span>Products</span>
        </div>
        <div class="nav-tab-pill">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
            </svg>
            <span>Orders</span>
        </div>
        <div class="nav-tab-pill">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="23 4 23 10 17 10"></polyline>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
            </svg>
            <span>Returns</span>
        </div>
        <div class="nav-tab-pill">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            <span>Help</span>
        </div>
    </div>
    
    <div class="navbar-right">
        <button class="nav-icon-btn" title="Toggle theme">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="1" x2="12" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="23"></line>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                <line x1="1" y1="12" x2="3" y2="12"></line>
                <line x1="21" y1="12" x2="23" y2="12"></line>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </svg>
        </button>
        <button class="nav-deploy-btn" type="button">
            <span>Deploy</span>
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                <polyline points="15 3 21 3 21 9"></polyline>
                <line x1="10" y1="14" x2="21" y2="3"></line>
            </svg>
        </button>
        <button class="nav-icon-btn" title="More options">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <circle cx="12" cy="5" r="2.2" />
                <circle cx="12" cy="12" r="2.2" />
                <circle cx="12" cy="19" r="2.2" />
            </svg>
        </button>
    </div>
</header>
"""

render_html(NAVBAR_HTML)

# ---------------------------------------------------------
# 5. Helper for Action Buttons
# ---------------------------------------------------------
ACTION_BUTTONS_HTML = """
<div class="msg-actions">
    <button class="msg-action-btn" title="Copy response" onclick="var card=this.closest('.chat-bot-bubble'); var content=card?card.innerText:''; if(navigator.clipboard && content){navigator.clipboard.writeText(content); var btn=this; btn.style.color='#38BDF8'; setTimeout(function(){btn.style.color='';}, 1600);}">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
    </button>
    <button class="msg-action-btn" title="Helpful" onclick="this.style.color='#38BDF8'; this.style.transform='scale(1.15)';">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path>
        </svg>
    </button>
    <button class="msg-action-btn" title="Not helpful" onclick="this.style.color='#F43F5E'; this.style.transform='scale(1.15)';">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h3a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-3"></path>
        </svg>
    </button>
</div>
"""

# ---------------------------------------------------------
# 6. Conversation State (Preserves Exact RAG Logic)
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# JS helper to trigger question clicks into Streamlit chat input
TRIGGER_QUERY_SCRIPT = """
<script>
window.parent.triggerChatQuery = function(queryText) {
    var chatInput = window.parent.document.querySelector('[data-testid="stChatInputTextArea"]') || document.querySelector('[data-testid="stChatInputTextArea"]');
    if (chatInput) {
        chatInput.value = queryText;
        chatInput.dispatchEvent(new Event('input', { bubbles: true }));
        setTimeout(function() {
            var sendBtn = window.parent.document.querySelector('[data-testid="stChatInputSubmitButton"]') || document.querySelector('[data-testid="stChatInputSubmitButton"]');
            if (sendBtn) sendBtn.click();
        }, 120);
    }
};
</script>
"""
components.html(TRIGGER_QUERY_SCRIPT, height=0, width=0)

# Build Left Column Hero & Features HTML
cart_img_html = f'<img src="data:image/png;base64,{cart_hero_b64}" alt="3D Cart" />' if cart_hero_b64 else ''

LEFT_COL_HTML = f"""
<div class="cartiq-left-col">
    <!-- Hero with 3D Cart and Title -->
    <div class="hero-visual-wrapper">
        <div class="cart-hero-img-container">
            {cart_img_html}
        </div>
        <div class="hero-text-block">
            <div class="hero-pill">
                <span class="hero-pill-sparkle">✦</span>
                <span>Ask. Shop. Compare, Decide.</span>
            </div>
            <h1 class="hero-main-title">E-Commerce <span class="gradient-ai-chatbot">AI Chatbot</span></h1>
            <p class="hero-sub-desc">Find products, compare prices, track orders, handle returns and get instant shopping support — all in one place.</p>
        </div>
    </div>

    <!-- 4 Feature Cards Row -->
    <div class="features-row">
        <div class="feature-card">
            <div class="feature-icon-circle">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
            </div>
            <div class="feature-title">Find Products</div>
            <div class="feature-desc">Get perfect recommendations</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon-circle">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="20" x2="18" y2="10"></line>
                    <line x1="12" y1="20" x2="12" y2="4"></line>
                    <line x1="6" y1="20" x2="6" y2="14"></line>
                </svg>
            </div>
            <div class="feature-title">Compare & Decide</div>
            <div class="feature-desc">Compare prices, features and reviews</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon-circle">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="21 8 21 21 3 21 3 8"></polyline>
                    <rect x="1" y="3" width="22" height="5"></rect>
                    <line x1="10" y1="12" x2="14" y2="12"></line>
                </svg>
            </div>
            <div class="feature-title">Track Orders</div>
            <div class="feature-desc">Real-time order updates</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon-circle">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="23 4 23 10 17 10"></polyline>
                    <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
                </svg>
            </div>
            <div class="feature-title">Returns & Support</div>
            <div class="feature-desc">Easy returns and instant help</div>
        </div>
    </div>

    <!-- 4 Quick Query Chips Row -->
    <div class="query-chips-row">
        <div class="query-chip" onclick="(window.triggerChatQuery || window.parent.triggerChatQuery)('best smartphones under 25000')">
            <div class="chip-left">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                <span>best smartphones under 25000</span>
            </div>
            <span class="chip-arrow">›</span>
        </div>
        <div class="query-chip" onclick="(window.triggerChatQuery || window.parent.triggerChatQuery)('current offers and discounts')">
            <div class="chip-left">
                <span style="color:#C4B5FD; font-weight:700;">%</span>
                <span>current offers and discounts</span>
            </div>
            <span class="chip-arrow">›</span>
        </div>
        <div class="query-chip" onclick="(window.triggerChatQuery || window.parent.triggerChatQuery)('track my order #OD12345')">
            <div class="chip-left">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#818CF8" stroke-width="2"><polyline points="21 8 21 21 3 21 3 8"></polyline><rect x="1" y="3" width="22" height="5"></rect></svg>
                <span>track my order #OD12345</span>
            </div>
            <span class="chip-arrow">›</span>
        </div>
        <div class="query-chip" onclick="(window.triggerChatQuery || window.parent.triggerChatQuery)('how to return a product')">
            <div class="chip-left">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2"><polyline points="23 4 23 10 17 10"></polyline><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path></svg>
                <span>how to return a product</span>
            </div>
            <span class="chip-arrow">›</span>
        </div>
    </div>
</div>
"""

# Render Dashboard Layout:
# When no messages yet -> Only render the clean, centered hero layout (NO chat card shown at all)
if len(st.session_state.messages) == 0:
    GRID_HTML = f"""
    <div class="cartiq-single-col">
        {LEFT_COL_HTML}
    </div>
    """
    render_html(GRID_HTML)
else:
    # Render actual conversation history dynamically
    chat_rows = []
    for msg in st.session_state.messages:
        content_escaped = msg['content'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
        if msg['role'] == 'user':
            chat_rows.append(f"""
            <div class="chat-user-row">
                <div class="chat-user-bubble">{content_escaped}</div>
                <div class="chat-user-avatar">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="#FFFFFF"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
                </div>
            </div>
            """)
        else:
            chat_rows.append(f"""
            <div class="chat-bot-row">
                <div class="chat-bot-avatar">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="#FFFFFF"><rect x="4" y="6" width="16" height="12" rx="3"/><circle cx="9" cy="11" r="1.5" fill="#3B82F6"/><circle cx="15" cy="11" r="1.5" fill="#3B82F6"/><line x1="9" y1="14" x2="15" y2="14" stroke="#3B82F6" stroke-width="1.5"/><line x1="12" y1="3" x2="12" y2="6" stroke="#FFFFFF" stroke-width="2"/></svg>
                </div>
                <div class="chat-bot-bubble">
                    {content_escaped}
                    {ACTION_BUTTONS_HTML}
                </div>
            </div>
            """)
    CHAT_WINDOW_CONTENT = "".join(chat_rows)

    RIGHT_COL_HTML = f"""
    <div class="cartiq-chat-card">
        {CHAT_WINDOW_CONTENT}
    </div>
    """

    # Render Two-Column Dashboard Layout
    GRID_HTML = f"""
    <div class="cartiq-main-grid">
        {LEFT_COL_HTML}
        {RIGHT_COL_HTML}
    </div>
    """
    render_html(GRID_HTML)

# ---------------------------------------------------------
# 7. Bottom Floating Chat Input & Query Execution
# ---------------------------------------------------------
query = st.chat_input("Ask anything about products, orders, returns...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    
    # Exact RAG & SQL pipeline reasoning
    response = ask(query)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
