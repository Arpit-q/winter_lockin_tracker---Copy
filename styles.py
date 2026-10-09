"""
Solo Leveling Anime Heads-Up Display (HUD) Theme CSS & Audio Effects Module
Authentic Anime Adaptation Aesthetic:
- Core Signature Colors: Electric Blue & Deep Purple auras on Pitch Black & Charcoal Gray.
- Typography: Michroma (futuristic geometric sans-serif for system windows/HUD) & 
  Plus Jakarta Sans (clean, modern rounded sans-serif for maximum readability across translucent UI).
"""

SOLO_LEVELING_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Michroma&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Chakra+Petch:ital,wght@0,400;0,600;0,700;1,700&family=JetBrains+Mono:wght@400;600;700&display=swap');

/* =========================================================================
   SOLO LEVELING SYSTEM PALETTE & ROOT VARIABLES
   ========================================================================= */
:root {
    /* Signature Power & Aura Tones */
    --sl-electric-blue: #00d2ff;
    --sl-electric-blue-bright: #38e1ff;
    --sl-electric-cyan: #38bdf8;
    --sl-deep-purple: #7c3aed;
    --sl-royal-purple: #6d28d9;
    --sl-shadow-purple: #4c1d95;
    --sl-monarch-violet: #a855f7;
    
    /* Dark High-Contrast Charcoal & Black Palette */
    --sl-dark-void: #030508;
    --sl-charcoal-dark: #080b11;
    --sl-charcoal-mid: #0e131d;
    --sl-charcoal-light: #161c29;
    --sl-text-primary: #f1f5f9;
    --sl-text-secondary: #94a3b8;
    --sl-text-muted: #64748b;
    
    /* Holographic Translucent HUD Glass */
    --sl-panel-bg: rgba(10, 14, 23, 0.88);
    --sl-panel-bg-translucent: rgba(7, 10, 17, 0.78);
    --sl-border-blue: rgba(0, 210, 255, 0.38);
    --sl-border-purple: rgba(124, 58, 237, 0.42);
    --sl-border-subtle: rgba(255, 255, 255, 0.08);
    
    /* Aura Glow Effects */
    --sl-glow-blue: 0 0 22px rgba(0, 210, 255, 0.35);
    --sl-glow-purple: 0 0 26px rgba(124, 58, 237, 0.38);
    --sl-glow-dual: 0 0 24px rgba(0, 210, 255, 0.25), 0 0 40px rgba(124, 58, 237, 0.2);
    --sl-glow-inset: inset 0 0 16px rgba(0, 210, 255, 0.09), inset 0 0 24px rgba(124, 58, 237, 0.08);

    /* Legacy Aliases for seamless component compatibility */
    --hunter-cyan: var(--sl-electric-blue);
    --hunter-blue: #0284c7;
    --hunter-purple: var(--sl-deep-purple);
    --hunter-violet: var(--sl-monarch-violet);
    --hunter-dark: var(--sl-charcoal-dark);
    --hunter-card-bg: var(--sl-panel-bg);
    --hunter-border: var(--sl-border-blue);
    --hunter-glow: var(--sl-glow-blue);
}

/* =========================================================================
   GLOBAL APPLICATION CANVAS & TYPOGRAPHY
   ========================================================================= */
.stApp {
    /* Atmospheric dungeon aura gradient: deep shadow purple at crown melting into pitch black and charcoal */
    background: radial-gradient(circle at 50% -12%, #1a1033 0%, #0c1220 35%, #05070c 80%, #030407 100%) !important;
    color: var(--sl-text-primary) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* System Titles & Sci-Fi Headers */
h1, h2, h3 {
    font-family: 'Michroma', 'Chakra Petch', sans-serif !important;
    letter-spacing: 1.5px !important;
    color: #ffffff !important;
}

h2 {
    font-size: 1.35rem !important;
    border-left: 4px solid var(--sl-electric-blue) !important;
    padding-left: 12px !important;
    margin-top: 24px !important;
    margin-bottom: 16px !important;
    text-shadow: 0 0 12px rgba(0, 210, 255, 0.35);
}

h3 {
    font-size: 1.1rem !important;
    color: #e2e8f0 !important;
}

/* Custom Scrollbar for HUD aesthetics */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #06080d;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--sl-electric-blue) 0%, var(--sl-deep-purple) 100%);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #38e1ff;
    box-shadow: 0 0 10px rgba(0, 210, 255, 0.8);
}

/* =========================================================================
   SIDEBAR (THE SYSTEM MENU)
   ========================================================================= */
[data-testid="stSidebar"] {
    background: rgba(6, 9, 15, 0.96) !important;
    border-right: 1px solid rgba(0, 210, 255, 0.22) !important;
    box-shadow: 6px 0 28px rgba(0, 0, 0, 0.8), 2px 0 12px rgba(124, 58, 237, 0.12) !important;
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    font-family: 'Michroma', sans-serif !important;
    font-size: 0.95rem !important;
    letter-spacing: 1.5px !important;
    color: var(--sl-electric-blue) !important;
}

[data-testid="stSidebar"] .stRadio label {
    color: #cbd5e1 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.92rem !important;
    padding: 7px 12px !important;
    border-radius: 8px !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: 1px solid transparent !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
    color: #ffffff !important;
    background: linear-gradient(90deg, rgba(0, 210, 255, 0.12) 0%, rgba(124, 58, 237, 0.08) 100%) !important;
    border-color: rgba(0, 210, 255, 0.3) !important;
    transform: translateX(3px) !important;
}

/* =========================================================================
   ANIME SYSTEM HEADS-UP DISPLAY (HUD) WINDOW CARDS
   ========================================================================= */
.hunter-hud-card {
    background: linear-gradient(135deg, rgba(12, 17, 28, 0.92) 0%, rgba(7, 10, 18, 0.96) 100%);
    border: 1px solid var(--sl-border-blue);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7), var(--sl-glow-dual), var(--sl-glow-inset);
    border-radius: 12px;
    padding: 22px 26px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

/* Anime Glowing Top Accent Strip (Electric Blue to Deep Purple Aura) */
.hunter-hud-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent 0%, var(--sl-electric-blue) 35%, var(--sl-deep-purple) 75%, transparent 100%);
    box-shadow: 0 0 12px var(--sl-electric-blue);
}

/* Tech Bracket Cutout Accents on Corners */
.hunter-hud-card::after {
    content: "";
    position: absolute;
    bottom: 0;
    right: 0;
    width: 24px;
    height: 24px;
    border-right: 2px solid var(--sl-deep-purple);
    border-bottom: 2px solid var(--sl-deep-purple);
    border-bottom-right-radius: 12px;
    pointer-events: none;
}

.hunter-badge-tag {
    font-family: 'Michroma', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    padding: 4px 10px;
    border-radius: 4px;
    background: linear-gradient(90deg, rgba(0, 210, 255, 0.15) 0%, rgba(124, 58, 237, 0.12) 100%);
    border: 1px solid rgba(0, 210, 255, 0.45);
    color: var(--sl-electric-blue-bright);
    display: inline-block;
    margin-bottom: 8px;
    text-transform: uppercase;
    box-shadow: 0 0 12px rgba(0, 210, 255, 0.2);
}

.system-title {
    font-family: 'Michroma', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.85rem !important;
    letter-spacing: 2px !important;
    background: linear-gradient(90deg, #ffffff 0%, #38e1ff 45%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 !important;
    padding-bottom: 4px;
    text-shadow: 0 0 20px rgba(0, 210, 255, 0.3);
}

.hunter-name-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: #94a3b8;
    margin-top: 3px;
    letter-spacing: 0.5px;
}

.rank-display {
    text-align: right;
}

.rank-text-huge {
    font-family: 'Michroma', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: 2px;
    line-height: 1;
    margin: 0;
}

.rank-tier-sub {
    font-family: 'Chakra Petch', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #cbd5e1;
    margin-top: 4px;
}

/* =========================================================================
   SOLO LEVELING EXP BAR (ELECTRIC BLUE & SHADOW PURPLE)
   ========================================================================= */
.exp-bar-container {
    background: rgba(8, 11, 18, 0.9);
    border: 1px solid rgba(0, 210, 255, 0.25);
    box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.8);
    border-radius: 8px;
    height: 20px;
    width: 100%;
    position: relative;
    overflow: hidden;
    margin-top: 10px;
}

.exp-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #0284c7 0%, var(--sl-electric-blue) 45%, var(--sl-deep-purple) 85%, var(--sl-monarch-violet) 100%);
    box-shadow: 0 0 16px rgba(0, 210, 255, 0.7), 0 0 24px rgba(124, 58, 237, 0.5);
    border-radius: 7px;
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.exp-bar-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-family: 'Michroma', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #ffffff;
    text-shadow: 0 0 6px rgba(0, 0, 0, 0.95), 0 0 10px rgba(0, 210, 255, 0.6);
}

/* =========================================================================
   ANIME SYSTEM NOTIFICATION / MESSAGE POPUPS
   ========================================================================= */
.system-notification {
    background: linear-gradient(90deg, rgba(0, 210, 255, 0.12) 0%, rgba(124, 58, 237, 0.14) 60%, rgba(8, 12, 20, 0.85) 100%);
    border-left: 4px solid var(--sl-electric-blue);
    border-top: 1px solid rgba(0, 210, 255, 0.3);
    border-right: 1px solid rgba(124, 58, 237, 0.3);
    border-bottom: 1px solid rgba(0, 210, 255, 0.2);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6), 0 0 20px rgba(0, 210, 255, 0.15);
    border-radius: 8px;
    padding: 14px 20px;
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    gap: 14px;
    backdrop-filter: blur(12px);
}

.system-notification-tag {
    font-family: 'Michroma', monospace;
    font-weight: 700;
    font-size: 0.72rem;
    color: var(--sl-electric-blue-bright);
    letter-spacing: 1.5px;
    text-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
    white-space: nowrap;
}

.system-notification-msg {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.92rem;
    color: #e2e8f0;
    line-height: 1.45;
}

/* =========================================================================
   DAILY QUEST CARDS & CHECKLISTS
   ========================================================================= */
.quest-item-card {
    background: rgba(11, 15, 24, 0.82);
    border: 1px solid rgba(0, 210, 255, 0.18);
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 12px;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    backdrop-filter: blur(8px);
}

.quest-item-card:hover {
    border-color: var(--sl-electric-blue);
    background: rgba(14, 20, 32, 0.95);
    box-shadow: 0 0 20px rgba(0, 210, 255, 0.22), inset 0 0 10px rgba(124, 58, 237, 0.12);
    transform: translateY(-2px);
}

.quest-item-done {
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.14) 0%, rgba(10, 16, 26, 0.85) 100%) !important;
    border-color: rgba(16, 185, 129, 0.45) !important;
    box-shadow: 0 0 16px rgba(16, 185, 129, 0.15) !important;
}

/* =========================================================================
   STREAMLIT NATIVE METRIC CARDS (HUD DATA CELLS)
   ========================================================================= */
div[data-testid="stMetric"] {
    background: rgba(10, 14, 23, 0.9) !important;
    border: 1px solid rgba(0, 210, 255, 0.25) !important;
    border-top: 2px solid var(--sl-electric-blue) !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6), inset 0 0 12px rgba(124, 58, 237, 0.08) !important;
    transition: all 0.25s ease !important;
    backdrop-filter: blur(12px) !important;
}

div[data-testid="stMetric"]:hover {
    border-color: var(--sl-electric-blue) !important;
    border-top: 2px solid #38e1ff !important;
    box-shadow: 0 0 24px rgba(0, 210, 255, 0.3), inset 0 0 18px rgba(124, 58, 237, 0.16) !important;
    transform: translateY(-2px) !important;
}

div[data-testid="stMetricLabel"] {
    color: #7dd3fc !important;
    font-size: 0.75rem !important;
    font-family: 'Michroma', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}

div[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-family: 'Michroma', monospace !important;
    font-weight: 700 !important;
    font-size: 1.45rem !important;
    text-shadow: 0 0 14px rgba(0, 210, 255, 0.45) !important;
}

div[data-testid="stMetricDelta"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
}

/* =========================================================================
   ACHIEVEMENT BADGES & TROPHY TILES
   ========================================================================= */
.achievement-card {
    background: rgba(10, 14, 23, 0.88);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 16px;
    height: 100%;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    backdrop-filter: blur(10px);
}

.achievement-card.unlocked {
    border-color: var(--sl-border-blue);
    background: linear-gradient(145deg, rgba(14, 20, 34, 0.92) 0%, rgba(20, 14, 38, 0.95) 100%);
    box-shadow: 0 0 25px rgba(0, 210, 255, 0.2), inset 0 0 16px rgba(124, 58, 237, 0.15);
}

.achievement-card.locked {
    opacity: 0.52;
    filter: grayscale(50%);
}

.rarity-pill {
    font-family: 'Michroma', monospace;
    font-size: 0.6rem;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.rarity-common { background: rgba(148, 163, 184, 0.18); color: #cbd5e1; border: 1px solid #64748b; }
.rarity-rare { background: rgba(0, 210, 255, 0.18); color: #38e1ff; border: 1px solid #0284c7; box-shadow: 0 0 10px rgba(0, 210, 255, 0.3); }
.rarity-epic { background: rgba(124, 58, 237, 0.22); color: #c084fc; border: 1px solid #9333ea; box-shadow: 0 0 12px rgba(124, 58, 237, 0.35); }
.rarity-legendary { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #d97706; box-shadow: 0 0 14px rgba(245, 158, 11, 0.4); }

/* =========================================================================
   SCI-FI COMMAND BUTTONS
   ========================================================================= */
.stButton > button {
    background: linear-gradient(135deg, rgba(0, 210, 255, 0.18) 0%, rgba(124, 58, 237, 0.25) 100%) !important;
    border: 1px solid var(--sl-electric-blue) !important;
    color: #ffffff !important;
    font-family: 'Michroma', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 1.5px !important;
    border-radius: 8px !important;
    padding: 10px 22px !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4), inset 0 0 10px rgba(0, 210, 255, 0.1) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0, 210, 255, 0.42) 0%, rgba(124, 58, 237, 0.55) 100%) !important;
    border-color: #38e1ff !important;
    box-shadow: 0 0 25px rgba(0, 210, 255, 0.55), 0 0 35px rgba(124, 58, 237, 0.4) !important;
    transform: translateY(-2px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* =========================================================================
   HUD TABS
   ========================================================================= */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(9, 13, 22, 0.7) !important;
    border-radius: 10px !important;
    padding: 6px !important;
    border: 1px solid rgba(0, 210, 255, 0.2) !important;
    gap: 8px !important;
}

.stTabs [data-baseweb="tab"] {
    color: #94a3b8 !important;
    font-family: 'Michroma', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    letter-spacing: 1.2px !important;
    border-radius: 6px !important;
    padding: 8px 18px !important;
    border: none !important;
    transition: all 0.2s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #ffffff !important;
    background: rgba(0, 210, 255, 0.08) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0, 210, 255, 0.25) 0%, rgba(124, 58, 237, 0.3) 100%) !important;
    color: #ffffff !important;
    border: 1px solid var(--sl-electric-blue) !important;
    box-shadow: 0 0 18px rgba(0, 210, 255, 0.35) !important;
}

/* =========================================================================
   FORMS, INPUTS, AND DROPDOWNS
   ========================================================================= */
input, textarea, [data-baseweb="select"] {
    background-color: rgba(9, 13, 22, 0.85) !important;
    border: 1px solid rgba(0, 210, 255, 0.25) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

input:focus, textarea:focus {
    border-color: var(--sl-electric-blue) !important;
    box-shadow: 0 0 14px rgba(0, 210, 255, 0.4), inset 0 0 8px rgba(124, 58, 237, 0.2) !important;
}

/* Streamlit Native Progress Bar Glow */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--sl-electric-blue) 0%, #38bdf8 45%, var(--sl-deep-purple) 85%, var(--sl-monarch-violet) 100%) !important;
    box-shadow: 0 0 16px rgba(0, 210, 255, 0.6) !important;
}

/* Dataframe & Tables styling */
[data-testid="stDataFrame"] {
    background: rgba(9, 13, 22, 0.85) !important;
    border: 1px solid rgba(0, 210, 255, 0.2) !important;
    border-radius: 8px !important;
}

/* Streamlit Alert Callouts */
.stAlert {
    background: rgba(9, 13, 22, 0.9) !important;
    border: 1px solid rgba(0, 210, 255, 0.3) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}
</style>
"""

# Client-side Web Audio API synthesizer for Solo Leveling system sounds
SYSTEM_SOUNDS_JS = """
<script>
window.playSoloLevelingSound = function(type) {
    try {
        var AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!AudioContext) return;
        var ctx = new AudioContext();

        if (type === 'level_up') {
            // Fanfare sequence
            var notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
            notes.forEach(function(freq, index) {
                var osc = ctx.createOscillator();
                var gain = ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(freq, ctx.currentTime + (index * 0.1));
                gain.gain.setValueAtTime(0.2, ctx.currentTime + (index * 0.1));
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + (index * 0.1) + 0.35);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(ctx.currentTime + (index * 0.1));
                osc.stop(ctx.currentTime + (index * 0.1) + 0.36);
            });
        } else if (type === 'quest_clear') {
            // High chime
            var osc = ctx.createOscillator();
            var gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(880, ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(1760, ctx.currentTime + 0.2);
            gain.gain.setValueAtTime(0.25, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(ctx.currentTime);
            osc.stop(ctx.currentTime + 0.41);
        } else if (type === 'click') {
            var osc = ctx.createOscillator();
            var gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(1200, ctx.currentTime);
            gain.gain.setValueAtTime(0.1, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(ctx.currentTime);
            osc.stop(ctx.currentTime + 0.09);
        }
    } catch(e) {
        console.log("Audio not allowed or supported:", e);
    }
};
</script>
"""
