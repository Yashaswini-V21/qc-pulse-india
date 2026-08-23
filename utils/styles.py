"""
Premium CSS Design System — "Vibrant Dark Intelligence" aesthetic
Inspired by: Vercel × Linear × Cyberpunk Neon SaaS × Notion AI
"""


def load_custom_css() -> str:
    """Returns the complete premium CSS stylesheet as a string."""
    return """
<style>
/* ═══════════════════════════════════════════════════════════
   SECTION 1 — GLOBAL FOUNDATION
   ═══════════════════════════════════════════════════════════ */

/* Import premium fonts (via cdnfonts — CSP-safe for Streamlit Cloud) */
@import url('https://fonts.cdnfonts.com/css/outfit');
@import url('https://fonts.cdnfonts.com/css/jetbrains-mono-2');
@import url('https://fonts.cdnfonts.com/css/dm-sans');
@import url('https://fonts.cdnfonts.com/css/space-mono');

*:not(.material-symbols-rounded):not(.material-icons) { font-family: 'Outfit', sans-serif !important; }
.material-symbols-rounded { font-family: 'Material Symbols Rounded' !important; }

/* Animated neon mesh gradient background - MORE VIBRANT & COLORFUL */
.stApp {
  background: #03060c !important;
  background-image:
    radial-gradient(ellipse 90% 60% at 10% 25%,
      rgba(139,92,246,0.18) 0%, transparent 65%),
    radial-gradient(ellipse 70% 50% at 90% 70%,
      rgba(59,130,246,0.16) 0%, transparent 60%),
    radial-gradient(ellipse 50% 60% at 50% 100%,
      rgba(6,182,212,0.15) 0%, transparent 65%),
    radial-gradient(circle 400px at 40% 50%,
      rgba(244,63,94,0.06) 0%, transparent 70%) !important;
  background-attachment: fixed !important;
}

/* Animated grid texture overlay for premium depth */
.stApp::before {
  content: '';
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-image:
    linear-gradient(rgba(139,92,246,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(139,92,246,0.04) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
  z-index: 0;
  opacity: 0.8;
}

/* Base text color and smoothing */
html, body, [class*="css"] {
  color: #F8FAFC;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Smooth custom neon scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #050810; }
::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #8B5CF6, #06B6D4);
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #A78BFA, #22D3EE);
}


/* ═══════════════════════════════════════════════════════════
   SECTION 2 — PREMIUM SIDEBAR
   ═══════════════════════════════════════════════════════════ */

[data-testid="stSidebar"] {
  background: linear-gradient(180deg,
    #050811 0%,
    #020408 100%) !important;
  border-right: 1px solid rgba(139,92,246,0.2) !important;
  box-shadow: 8px 0 30px rgba(0, 0, 0, 0.6);
}

/* Sidebar navigation items - Premium cyber buttons */
[data-testid="stSidebar"] .stRadio label {
  display: flex;
  align-items: center;
  padding: 12px 18px;
  border-radius: 12px;
  font-size: 13.5px !important;
  font-weight: 600 !important;
  color: #94A3B8 !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  margin: 4px 0;
  border: 1px solid transparent;
  background: rgba(13,17,23,0.3);
}

[data-testid="stSidebar"] .stRadio label:hover {
  background: linear-gradient(90deg, rgba(139,92,246,0.15), rgba(6,182,212,0.1));
  color: #FFFFFF !important;
  border-color: rgba(139,92,246,0.3) !important;
  transform: translateX(4px);
  box-shadow: 0 4px 15px rgba(139,92,246,0.1);
}

/* Selected option indicators */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-checked="true"] {
  background: linear-gradient(90deg,
    rgba(139,92,246,0.25) 0%,
    rgba(6,182,212,0.15) 100%) !important;
  color: #A78BFA !important;
  border-color: rgba(139,92,246,0.45) !important;
  font-weight: 700 !important;
  box-shadow: 0 4px 20px rgba(139,92,246,0.2), inset 0 0 10px rgba(139,92,246,0.15);
}


/* ═══════════════════════════════════════════════════════════
   SECTION 3 — METRIC CARDS
   ═══════════════════════════════════════════════════════════ */

[data-testid="metric-container"] {
  background: linear-gradient(135deg,
    rgba(13,20,35,0.85) 0%,
    rgba(7,10,22,0.9) 100%) !important;
  border: 1px solid rgba(139,92,246,0.22) !important;
  border-radius: 20px !important;
  padding: 24px 28px !important;
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  animation: cardEntrance 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  box-shadow: 0 15px 35px rgba(0,0,0,0.5);
}

/* Vibrant glowing top border with dual color accents */
[data-testid="metric-container"]::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg,
    #8B5CF6, #3B82F6, #06B6D4, #F43F5E);
  opacity: 0.85;
}

/* Beautiful micro-shimmer effect on hover */
[data-testid="metric-container"]:hover {
  border-color: rgba(6,182,212,0.45) !important;
  transform: translateY(-5px);
  box-shadow:
    0 25px 50px rgba(0,0,0,0.6),
    0 0 35px rgba(139,92,246,0.2);
}

[data-testid="metric-container"] label {
  font-size: 11.5px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.15em !important;
  color: #94A3B8 !important;
}

[data-testid="stMetricValue"] {
  font-size: 34px !important;
  font-weight: 900 !important;
  letter-spacing: -0.04em !important;
  background: linear-gradient(135deg, #FFFFFF, #E9D5FF, #93C5FD) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  margin-top: 8px !important;
}

[data-testid="stMetricDelta"] {
  font-size: 12px !important;
  font-weight: 600 !important;
  padding: 2px 8px;
  border-radius: 99px;
  display: inline-block;
  margin-top: 4px !important;
}

/* Staggered delays */
[data-testid="metric-container"]:nth-child(1) { animation-delay: 0s; }
[data-testid="metric-container"]:nth-child(2) { animation-delay: 0.08s; }
[data-testid="metric-container"]:nth-child(3) { animation-delay: 0.16s; }
[data-testid="metric-container"]:nth-child(4) { animation-delay: 0.24s; }


/* ═══════════════════════════════════════════════════════════
   SECTION 4 — GLASS CARDS
   ═══════════════════════════════════════════════════════════ */

.glass-card {
  background: linear-gradient(135deg,
    rgba(15,23,42,0.8) 0%,
    rgba(8,12,24,0.65) 100%);
  border: 1px solid rgba(139,92,246,0.18);
  border-radius: 24px;
  padding: 30px 34px;
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  position: relative;
  overflow: hidden;
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 20px 45px rgba(0,0,0,0.5);
}

.glass-card::after {
  content: '';
  position: absolute;
  top: -50%; right: -50%;
  width: 100%; height: 100%;
  background: radial-gradient(
    circle, rgba(6,182,212,0.06), transparent 75%);
  pointer-events: none;
}

.glass-card:hover {
  border-color: rgba(139,92,246,0.35);
  box-shadow:
    0 30px 60px rgba(0,0,0,0.6),
    0 0 30px rgba(139,92,246,0.12);
  transform: translateY(-2px);
}


/* ═══════════════════════════════════════════════════════════
   SECTION 5 — INSIGHT CARDS
   ═══════════════════════════════════════════════════════════ */

.insight-card {
  background: linear-gradient(135deg,
    rgba(13,20,35,0.9), rgba(6,8,16,0.85));
  border: 1px solid rgba(139,92,246,0.18);
  border-radius: 18px;
  padding: 22px 26px;
  margin-bottom: 16px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  box-shadow: 0 10px 25px rgba(0,0,0,0.4);
}

.insight-card::before {
  content: '';
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, #8B5CF6, #06B6D4, #F43F5E);
  border-radius: 4px 0 0 4px;
}

.insight-card:hover {
  border-color: rgba(6,182,212,0.4);
  transform: translateX(6px) translateY(-2px);
  box-shadow:
    -6px 12px 30px rgba(139,92,246,0.15),
    0 10px 25px rgba(0,0,0,0.5);
}

.insight-card h4 {
  font-size: 13.5px !important;
  font-weight: 800 !important;
  color: #C4B5FD !important;
  margin-bottom: 10px !important;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.insight-card p {
  font-size: 14px;
  color: #E2E8F0;
  line-height: 1.8;
  margin: 0;
}

.insight-card .num {
  font-size: 26px !important;
  font-weight: 900 !important;
  background: linear-gradient(135deg, #FFFFFF, #C4B5FD, #06B6D4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: block;
  margin-bottom: 6px;
}

.insight-card:nth-child(1) { animation-delay: 0.08s; }
.insight-card:nth-child(2) { animation-delay: 0.16s; }
.insight-card:nth-child(3) { animation-delay: 0.24s; }


/* ═══════════════════════════════════════════════════════════
   SECTION 6 — SECTION LABELS AND HEADERS
   ═══════════════════════════════════════════════════════════ */

.section-label {
  font-size: 11.5px;
  font-weight: 800;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #64748B;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-label::before {
  content: '';
  display: inline-block;
  width: 20px;
  height: 3px;
  background: linear-gradient(90deg, #8B5CF6, #06B6D4);
  border-radius: 2px;
}

h1 {
  font-size: 42px !important;
  font-weight: 900 !important;
  letter-spacing: -0.04em !important;
  background: linear-gradient(135deg,
    #FFFFFF 0%, #C4B5FD 35%, #60A5FA 70%, #06B6D4 100%) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  line-height: 1.15 !important;
  margin-bottom: 8px !important;
  text-shadow: 0 10px 40px rgba(139,92,246,0.15);
}

h2, h3 {
  color: #FFFFFF !important;
  font-weight: 800 !important;
  letter-spacing: -0.02em !important;
}

.page-subtitle {
  font-size: 14.5px;
  color: #64748B;
  font-weight: 500;
  margin-bottom: 36px;
  letter-spacing: 0.01em;
}


/* ═══════════════════════════════════════════════════════════
   SECTION 7 — PLATFORM BADGES
   ═══════════════════════════════════════════════════════════ */

.platform-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: 99px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.05em;
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
  transition: all 0.3s ease;
}

.platform-badge:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.4);
}

.badge-blinkit {
  background: rgba(239,68,68,0.15);
  border: 1px solid rgba(239,68,68,0.4);
  color: #FCA5A5;
}

.badge-zepto {
  background: rgba(16,185,129,0.15);
  border: 1px solid rgba(16,185,129,0.4);
  color: #6EE7B7;
}

.badge-bigbasket {
  background: rgba(139,92,246,0.15);
  border: 1px solid rgba(139,92,246,0.4);
  color: #C4B5FD;
}

/* Stat badge for page headers */
.stat-badge {
  display: inline-block;
  background: rgba(6,182,212,0.15);
  border: 1px solid rgba(6,182,212,0.35);
  color: #22D3EE;
  font-size: 11px;
  font-weight: 800;
  padding: 4px 12px;
  border-radius: 99px;
  letter-spacing: 0.12em;
  margin-bottom: 10px;
  box-shadow: 0 0 15px rgba(6,182,212,0.15);
}


/* ═══════════════════════════════════════════════════════════
   SECTION 8 — BUTTONS
   ═══════════════════════════════════════════════════════════ */

.stButton > button {
  background: linear-gradient(135deg, #8B5CF6, #3B82F6, #06B6D4) !important;
  color: white !important;
  border: none !important;
  border-radius: 14px !important;
  font-size: 13.5px !important;
  font-weight: 700 !important;
  padding: 12px 32px !important;
  letter-spacing: 0.05em !important;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
  position: relative !important;
  overflow: hidden !important;
  box-shadow: 0 10px 25px rgba(139,92,246,0.35) !important;
}

.stButton > button:hover {
  transform: translateY(-3px) !important;
  box-shadow:
    0 15px 35px rgba(139,92,246,0.5),
    0 0 25px rgba(6,182,212,0.3) !important;
}

.stButton > button:active {
  transform: translateY(-1px) !important;
}


/* ═══════════════════════════════════════════════════════════
   SECTION 9 — SELECTBOXES AND INPUTS
   ═══════════════════════════════════════════════════════════ */

.stSelectbox > div > div {
  background: rgba(10,15,30,0.85) !important;
  border: 1px solid rgba(139,92,246,0.25) !important;
  border-radius: 12px !important;
  color: #FFFFFF !important;
  padding: 2px 4px !important;
  backdrop-filter: blur(10px);
}

.stSelectbox > div > div:hover {
  border-color: rgba(6,182,212,0.45) !important;
  box-shadow: 0 0 15px rgba(6,182,212,0.15);
}

.stSlider > div > div > div {
  background: rgba(139,92,246,0.25) !important;
}

.stSlider > div > div > div > div {
  background: linear-gradient(135deg, #8B5CF6, #06B6D4) !important;
  box-shadow: 0 0 15px rgba(139,92,246,0.4);
}

.stNumberInput > div > div > input {
  background: rgba(10,15,30,0.85) !important;
  border: 1px solid rgba(139,92,246,0.25) !important;
  border-radius: 12px !important;
  color: #FFFFFF !important;
}

.stNumberInput > div > div > input:hover {
  border-color: rgba(6,182,212,0.45) !important;
}


/* ═══════════════════════════════════════════════════════════
   SECTION 10 — TABS
   ═══════════════════════════════════════════════════════════ */

.stTabs [data-baseweb="tab-list"] {
  background: rgba(10,15,30,0.5) !important;
  border-radius: 16px !important;
  padding: 6px !important;
  border: 1px solid rgba(139,92,246,0.18) !important;
  gap: 8px !important;
  box-shadow: 0 12px 35px rgba(0,0,0,0.45);
}

.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 12px !important;
  color: #94A3B8 !important;
  font-weight: 600 !important;
  font-size: 13.5px !important;
  padding: 12px 28px !important;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
  border: 1px solid transparent !important;
  margin: 2px 0 !important;
}

.stTabs [data-baseweb="tab"]:hover {
  color: #FFFFFF !important;
  background: rgba(139,92,246,0.08) !important;
  border-color: rgba(139,92,246,0.18) !important;
}

.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg,
    rgba(139,92,246,0.25), rgba(6,182,212,0.18)) !important;
  color: #FFFFFF !important;
  border-color: rgba(6,182,212,0.45) !important;
  font-weight: 700 !important;
  box-shadow:
    0 4px 20px rgba(139,92,246,0.15),
    inset 0 0 10px rgba(139,92,246,0.12) !important;
}

/* Hide annoying Streamlit default tab borders */
.stTabs [data-baseweb="tab-border"] {
  background-color: transparent !important;
}

.stTabs [data-baseweb="tab-highlight-bar"] {
  background: linear-gradient(90deg, #8B5CF6, #06B6D4) !important;
  height: 3px !important;
  border-radius: 3px !important;
}


/* ═══════════════════════════════════════════════════════════
   SECTION 11 — DATAFRAMES
   ═══════════════════════════════════════════════════════════ */

[data-testid="stDataFrame"] {
  background: rgba(10,15,30,0.85) !important;
  border-radius: 20px !important;
  border: 1px solid rgba(139,92,246,0.18) !important;
  overflow: hidden !important;
  box-shadow: 0 20px 45px rgba(0,0,0,0.5);
}


/* ═══════════════════════════════════════════════════════════
   SECTION 12 — DIVIDERS
   ═══════════════════════════════════════════════════════════ */

hr {
  border: none !important;
  height: 1px !important;
  background: linear-gradient(90deg,
    transparent,
    rgba(139,92,246,0.25),
    rgba(6,182,212,0.25),
    transparent) !important;
  margin: 36px 0 !important;
}


/* ═══════════════════════════════════════════════════════════
   SECTION 13 — ANIMATIONS
   ═══════════════════════════════════════════════════════════ */

@keyframes cardEntrance {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 15px rgba(16,185,129,0.3);
  }
  50% {
    box-shadow: 0 0 30px rgba(16,185,129,0.65);
  }
}


/* ═══════════════════════════════════════════════════════════
   SECTION 14 — STATUS INDICATORS
   ═══════════════════════════════════════════════════════════ */

.status-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 8px;
}

.status-live {
  background: #10B981;
  box-shadow: 0 0 10px rgba(16,185,129,0.7);
  animation: pulse-glow 2s infinite;
}

.status-warning {
  background: #F59E0B;
  box-shadow: 0 0 10px rgba(245,158,11,0.7);
}

/* Live indicator badge */
.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  background: rgba(16,185,129,0.15);
  border: 1px solid rgba(16,185,129,0.4);
  border-radius: 99px;
  font-size: 10px;
  font-weight: 700;
  color: #6EE7B7;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  box-shadow: 0 0 15px rgba(16,185,129,0.1);
}


/* ═══════════════════════════════════════════════════════════
   SECTION 15 — SPECIAL COMPONENTS
   ═══════════════════════════════════════════════════════════ */

/* KPI change indicators */
.kpi-change-up {
  color: #10B981;
  font-size: 11.5px;
  font-weight: 700;
}

.kpi-change-down {
  color: #EF4444;
  font-size: 11.5px;
  font-weight: 700;
}

/* Score badge for scorecard */
.score-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  border-radius: 14px;
  font-size: 18px;
  font-weight: 900;
  background: linear-gradient(135deg,
    rgba(139,92,246,0.2), rgba(6,182,212,0.15));
  border: 1px solid rgba(139,92,246,0.3);
  color: #C4B5FD;
  box-shadow: inset 0 0 15px rgba(139,92,246,0.15);
}

/* Winner highlight in comparison */
.winner-cell {
  background: rgba(139,92,246,0.18);
  border-radius: 8px;
  padding: 3px 10px;
  color: #C4B5FD;
  font-weight: 800;
}


/* ═══════════════════════════════════════════════════════════
   SECTION 16 — HERO BANNER
   ═══════════════════════════════════════════════════════════ */

.hero-banner {
  background: linear-gradient(135deg,
    rgba(15,23,42,0.85) 0%,
    rgba(8,12,24,0.7) 100%);
  border: 1px solid rgba(139,92,246,0.22);
  border-radius: 24px;
  padding: 36px;
  margin-bottom: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 36px;
  flex-wrap: wrap;
  backdrop-filter: blur(25px);
  position: relative;
  overflow: hidden;
  animation: fadeIn 0.8s ease;
  box-shadow: 0 25px 55px rgba(0,0,0,0.55);
}

.hero-banner::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg,
    transparent, #8B5CF6, #06B6D4, transparent);
  opacity: 0.8;
}

.hero-left {
  flex: 1 1 450px;
}

.hero-stats {
  display: flex;
  gap: 18px;
  flex-wrap: wrap;
  flex: 1 1 400px;
  justify-content: flex-end;
}

.hero-stat-card {
  background: rgba(5,8,16,0.85);
  border: 1px solid rgba(139,92,246,0.22);
  border-radius: 20px;
  padding: 20px 24px;
  min-width: 140px;
  text-align: center;
  flex: 1 1 140px;
  transition: all 0.35s cubic-bezier(0.16,1,0.3,1);
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0,0,0,0.4);
}

.hero-stat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1.5px;
  background: linear-gradient(90deg,
    transparent, rgba(6,182,212,0.6), transparent);
}

.hero-stat-card:hover {
  transform: translateY(-4px);
  border-color: rgba(6,182,212,0.45);
  box-shadow:
    0 15px 35px rgba(0,0,0,0.5),
    0 0 20px rgba(139,92,246,0.12);
}

.hero-stat-value {
  font-size: 32px;
  font-weight: 900;
  background: linear-gradient(135deg, #FFFFFF, #C4B5FD, #60A5FA);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.02em;
}

.hero-stat-label {
  font-size: 10px;
  color: #64748B;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-weight: 700;
  margin-top: 6px;
}

@keyframes statScale {
  0% { transform: scale(0.92); opacity: 0; filter: blur(4px); }
  100% { transform: scale(1); opacity: 1; filter: blur(0); }
}

.animate-stat {
  animation: statScale 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}


/* ═══════════════════════════════════════════════════════════
   SECTION 17 — HIDE STREAMLIT BRANDING
   ═══════════════════════════════════════════════════════════ */

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.stDeployButton { display: none; }

</style>
"""
