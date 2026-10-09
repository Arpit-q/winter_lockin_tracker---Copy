"""
Winter Lock-In Command Center — Solo Leveling Hunter System
A dark fantasy gamified tracker for the Winter Arc (Oct 1 → Dec 31, 2026).
"""
from datetime import date, datetime, timedelta
from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from solo_leveling import (
    calculate_hunter_profile,
    evaluate_daily_quests,
    evaluate_achievements,
    get_row_xp_breakdown,
    calculate_row_xp,
    XP_VALUES,
    DEFAULT_DAILY_QUESTS
)
from charts import (
    create_radar_stat_chart,
    create_effort_pie_chart,
    create_academic_pie_chart,
    create_daily_quest_donut,
    create_today_xp_pie,
    create_skill_depth_pie,
    create_task_type_donut,
    create_winter_arc_pace_gauge,
    create_xp_cumulative_chart,
    create_weekly_output_comparison
)
from styles import SOLO_LEVELING_CSS, SYSTEM_SOUNDS_JS
import seed_topics
import ai_assistant

DB_PATH = Path(__file__).parent / "data" / "winter_lockin.db"
START = date(2026, 10, 1)
END = date(2026, 12, 31)

DEFAULT_CONFIG = {
    "hunter_name": "Arpit",
    "hunter_title": "Shadow Monarch in Training",
    "academic_operating_pct": 86.0,
    "sgpa_target": 10.0,
    "agentic_target_phase": 9,
    "x0_phase0_topic_target": 100,
    "sound_effects": 1,
    "groq_api_key": "",
    "groq_model": "qwen/qwen3.8-27b",
}

def db():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    con = db()
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS daily_log(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dt TEXT NOT NULL,
        m3_attempted INTEGER DEFAULT 0,
        m3_solved INTEGER DEFAULT 0,
        m3_correct INTEGER DEFAULT 0,
        m3_chapter TEXT DEFAULT '',
        m3_topic TEXT DEFAULT '',
        coos_numericals INTEGER DEFAULT 0,
        coos_correct INTEGER DEFAULT 0,
        coos_theory_learned INTEGER DEFAULT 0,
        coos_theory_revised INTEGER DEFAULT 0,
        coos_practicals INTEGER DEFAULT 0,
        python_tasks INTEGER DEFAULT 0,
        python_loc_written INTEGER DEFAULT 0,
        python_loc_read INTEGER DEFAULT 0,
        python_topics_learned INTEGER DEFAULT 0,
        python_topics_applied INTEGER DEFAULT 0,
        dsa_theory INTEGER DEFAULT 0,
        dsa_problems INTEGER DEFAULT 0,
        dsa_leetcode INTEGER DEFAULT 0,
        dsa_java_impl INTEGER DEFAULT 0,
        dsa_revision INTEGER DEFAULT 0,
        uhv_learned INTEGER DEFAULT 0,
        uhv_revised INTEGER DEFAULT 0,
        agency_prospects INTEGER DEFAULT 0,
        agency_contacted INTEGER DEFAULT 0,
        agency_outreach INTEGER DEFAULT 0,
        agency_followups INTEGER DEFAULT 0,
        agency_replies INTEGER DEFAULT 0,
        agency_conversations INTEGER DEFAULT 0,
        agency_calls INTEGER DEFAULT 0,
        agency_proposals INTEGER DEFAULT 0,
        agency_deals INTEGER DEFAULT 0,
        agency_new_mrr REAL DEFAULT 0,
        agency_current_mrr REAL DEFAULT 0,
        linkedin_posts INTEGER DEFAULT 0,
        instagram_posts INTEGER DEFAULT 0,
        other_content INTEGER DEFAULT 0,
        agentic_topics_learned INTEGER DEFAULT 0,
        agentic_topics_revised INTEGER DEFAULT 0,
        agentic_topics_deepened INTEGER DEFAULT 0,
        agentic_requirements_solved INTEGER DEFAULT 0,
        agentic_projects INTEGER DEFAULT 0,
        agentic_features INTEGER DEFAULT 0,
        agentic_deployments INTEGER DEFAULT 0,
        agentic_bugs_fixed INTEGER DEFAULT 0,
        agentic_capabilities INTEGER DEFAULT 0,
        x0_topics_learned INTEGER DEFAULT 0,
        x0_topics_revised INTEGER DEFAULT 0,
        x0_topics_deepened INTEGER DEFAULT 0,
        x0_experiments INTEGER DEFAULT 0,
        x0_hypotheses INTEGER DEFAULT 0,
        x0_questions_resolved INTEGER DEFAULT 0,
        x0_sources INTEGER DEFAULT 0,
        x0_milestones INTEGER DEFAULT 0,
        dads_investigated INTEGER DEFAULT 0,
        dads_implementing INTEGER DEFAULT 0,
        dads_improved INTEGER DEFAULT 0,
        dads_independent INTEGER DEFAULT 0,
        dads_tech_impl INTEGER DEFAULT 0,
        dads_tech_knowledge REAL DEFAULT 0,
        dads_ops_knowledge REAL DEFAULT 0,
        deep_work_hours REAL DEFAULT 0,
        notes TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS m3_topic_log(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dt TEXT NOT NULL,
        chapter TEXT NOT NULL,
        topic TEXT NOT NULL,
        attempted INTEGER DEFAULT 0,
        solved INTEGER DEFAULT 0,
        correct INTEGER DEFAULT 0,
        revision INTEGER DEFAULT 0,
        notes TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS agentic_topics(
        topic_id TEXT PRIMARY KEY,
        topic TEXT NOT NULL,
        phase INTEGER NOT NULL,
        category TEXT DEFAULT '',
        importance TEXT DEFAULT 'Medium',
        target_depth INTEGER DEFAULT 3,
        current_depth INTEGER DEFAULT 0,
        status TEXT DEFAULT 'Not started',
        learned_date TEXT DEFAULT '',
        revised_date TEXT DEFAULT '',
        evidence TEXT DEFAULT '',
        notes TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS x0_topics(
        topic_id TEXT PRIMARY KEY,
        topic TEXT NOT NULL,
        phase TEXT DEFAULT '0',
        category TEXT DEFAULT '',
        importance TEXT DEFAULT 'Medium',
        target_depth INTEGER DEFAULT 3,
        current_depth INTEGER DEFAULT 0,
        status TEXT DEFAULT 'Not started',
        covered_date TEXT DEFAULT '',
        revised_date TEXT DEFAULT '',
        evidence TEXT DEFAULT '',
        notes TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS projects(
        project_id TEXT PRIMARY KEY,
        project_name TEXT NOT NULL,
        domain TEXT DEFAULT '',
        start_date TEXT DEFAULT '',
        completion_date TEXT DEFAULT '',
        status TEXT DEFAULT 'Planned',
        project_type TEXT DEFAULT '',
        real_client INTEGER DEFAULT 0,
        production INTEGER DEFAULT 0,
        topics_used TEXT DEFAULT '',
        topics_learned TEXT DEFAULT '',
        topics_revised TEXT DEFAULT '',
        technologies TEXT DEFAULT '',
        evidence TEXT DEFAULT '',
        outcome TEXT DEFAULT '',
        notes TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS dads_operations(
        operation_id TEXT PRIMARY KEY,
        operation_name TEXT NOT NULL,
        current_process TEXT DEFAULT '',
        problem TEXT DEFAULT '',
        technology TEXT DEFAULT '',
        tech_implemented TEXT DEFAULT '',
        status TEXT DEFAULT 'Identified',
        observed INTEGER DEFAULT 0,
        assisted INTEGER DEFAULT 0,
        executed INTEGER DEFAULT 0,
        independently_controlled INTEGER DEFAULT 0,
        workload_reduction TEXT DEFAULT '',
        technical_knowledge TEXT DEFAULT '',
        operational_knowledge TEXT DEFAULT '',
        evidence TEXT DEFAULT '',
        dt TEXT DEFAULT '',
        notes TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS daily_goals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dt TEXT NOT NULL,
        task_name TEXT NOT NULL,
        target_val REAL DEFAULT 1,
        actual_val REAL DEFAULT 0,
        unit TEXT DEFAULT '',
        category TEXT DEFAULT 'Custom',
        xp_reward INTEGER DEFAULT 50,
        completed INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS config(
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    """)
    for k, v in DEFAULT_CONFIG.items():
        cur.execute("INSERT OR IGNORE INTO config(key,value) VALUES(?,?)", (k, str(v)))
    con.commit()
    con.close()

def get_config():
    con = db()
    df = pd.read_sql_query("SELECT key,value FROM config", con)
    con.close()
    out = DEFAULT_CONFIG.copy()
    for _, r in df.iterrows():
        try:
            val = r["value"]
            if "." in val:
                out[r["key"]] = float(val)
            else:
                out[r["key"]] = int(val)
        except Exception:
            out[r["key"]] = r["value"]
    return out

def update_config_key(key, val):
    con = db()
    con.execute("INSERT OR REPLACE INTO config(key, value) VALUES(?,?)", (key, str(val)))
    con.commit()
    con.close()

def save_daily(values):
    con = db()
    cols = ", ".join(values.keys())
    qs = ", ".join(["?"] * len(values))
    con.execute(f"INSERT INTO daily_log({cols}) VALUES({qs})", tuple(values.values()))
    con.commit()
    con.close()

def read(table, query=None):
    con = db()
    try:
        if query:
            df = pd.read_sql_query(query, con)
        else:
            df = pd.read_sql_query(f"SELECT * FROM {table}", con)
    except Exception:
        df = pd.DataFrame()
    finally:
        con.close()
    return df

def save_custom_goal(dt, task_name, target_val, unit, category, xp_reward):
    con = db()
    con.execute("""
        INSERT INTO daily_goals(dt, task_name, target_val, actual_val, unit, category, xp_reward, completed)
        VALUES(?,?,?,?,?,?,?,0)
    """, (str(dt), task_name, target_val, 0, unit, category, xp_reward))
    con.commit()
    con.close()

def toggle_custom_goal(goal_id, completed):
    con = db()
    con.execute("UPDATE daily_goals SET completed = ? WHERE id = ?", (1 if completed else 0, goal_id))
    con.commit()
    con.close()

# Initialize DB and Config
init_db()
cfg = get_config()

# Page Setup & Theme Injection
st.set_page_config(
    page_title=f"{cfg.get('hunter_name', 'Player')} — Winter Arc Solo Leveling System",
    page_icon="🗡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(SOLO_LEVELING_CSS, unsafe_allow_html=True)
st.markdown(SYSTEM_SOUNDS_JS, unsafe_allow_html=True)

# Load Primary Datasets
daily_df = read("daily_log")
agentic_df = read("agentic_topics")
x0_df = read("x0_topics")
dads_df = read("dads_operations")
projects_df = read("projects")
custom_goals_df = read("daily_goals")

# Calculate Hunter System Stats
hunter = calculate_hunter_profile(daily_df, agentic_df, x0_df, dads_df)
achievements_data = evaluate_achievements(daily_df, agentic_df, x0_df, dads_df)
today_quests = evaluate_daily_quests(hunter["today_row"])

# Auto-seed curriculum if empty so user has immediate rich data structure
if len(agentic_df) == 0 or len(x0_df) == 0:
    seed_topics.seed_topics_master()
    agentic_df = read("agentic_topics")
    x0_df = read("x0_topics")

# =========================================================================
# TOP HOLOGRAPHIC HUNTER STATUS WINDOW (SOLO LEVELING HUD)
# =========================================================================
hud_col1, hud_col2 = st.columns([3, 1])

with hud_col1:
    st.markdown(f"""
    <div class="hunter-hud-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <span class="hunter-badge-tag">[ SYSTEM STATUS: AWAKENED ]</span>
                <h1 class="system-title">{cfg.get('hunter_name', 'ARPIT').upper()}</h1>
                <div class="hunter-name-title">
                    <span style="color: {hunter['rank_color']}; font-weight:700;">{hunter['rank_badge']} {hunter['rank']}</span> · 
                    <span style="color: #cbd5e1;">Title: {cfg.get('hunter_title', 'Shadow Monarch in Training')}</span>
                </div>
            </div>
            <div class="rank-display">
                <div class="rank-text-huge" style="color: {hunter['rank_color']}; text-shadow: {hunter['rank_glow']};">
                    LV. {hunter['level']}
                </div>
                <div class="rank-tier-sub">{hunter['tier']}</div>
            </div>
        </div>
        <div style="margin-top: 14px;">
            <div style="display: flex; justify-content: space-between; font-size: 0.78rem; font-family: 'Michroma', sans-serif; letter-spacing: 1px;">
                <span style="color: #00d2ff;">EXP PROGRESSION</span>
                <span style="color: #cbd5e1;">{hunter['total_xp']:,} / {hunter['next_level_xp']:,} EXP ({hunter['progress_pct']}%)</span>
            </div>
            <div class="exp-bar-container">
                <div class="exp-bar-fill" style="width: {hunter['progress_pct']}%;"></div>
                <div class="exp-bar-text">{hunter['xp_needed']:,} EXP TO LEVEL {hunter['level'] + 1}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with hud_col2:
    st.markdown(f"""
    <div class="hunter-hud-card" style="padding: 18px 20px;">
        <span class="hunter-badge-tag">[ WINTER ARC SPRINTS ]</span>
        <div style="font-family: 'Michroma', sans-serif; font-size: 1.4rem; font-weight: 700; color: #00d2ff; letter-spacing: 1px; text-shadow: 0 0 14px rgba(0, 210, 255, 0.4);">
            DAY {hunter['day_num']} <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 400;">/ {hunter['total_days']}</span>
        </div>
        <div style="font-size: 0.85rem; color: #94a3b8; margin-top: 4px; font-family: 'Plus Jakarta Sans', sans-serif;">
            Lock-In: Oct 1 → Dec 31
        </div>
        <div style="margin-top: 12px; display: flex; align-items: center; justify-content: space-between; border-top: 1px solid rgba(0, 210, 255, 0.2); padding-top: 10px;">
            <div>
                <div style="font-family: 'Michroma', sans-serif; font-size: 0.65rem; color: #7dd3fc; letter-spacing: 1px; text-transform: uppercase;">Lock-In Streak</div>
                <div style="font-family: 'Michroma', monospace; font-size: 1.05rem; font-weight: 700; color: #fbbf24;">🔥 {hunter['streak']} DAYS</div>
            </div>
            <div style="text-align: right;">
                <div style="font-family: 'Michroma', sans-serif; font-size: 0.65rem; color: #7dd3fc; letter-spacing: 1px; text-transform: uppercase;">Today's EXP</div>
                <div style="font-family: 'Michroma', monospace; font-size: 1.05rem; font-weight: 700; color: #34d399;">+{hunter['today_xp']:,} XP</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# System Notification / Quest Cleared Banner
if today_quests["all_completed"]:
    st.markdown("""
    <div class="system-notification" style="border-left-color: #10b981; background: linear-gradient(90deg, rgba(16, 185, 129, 0.15) 0%, rgba(13, 20, 36, 0.8) 100%);">
        <span class="system-notification-tag" style="color: #34d399;">[ SYSTEM: ALL DAILY QUESTS CLEARED ]</span>
        <span class="system-notification-msg">Outstanding execution! Daily quota fulfilled. +250 Bonus EXP granted to your Hunter Profile!</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="system-notification">
        <span class="system-notification-tag">[ SYSTEM ACTIVE ]</span>
        <span class="system-notification-msg">Daily Quest Progress: <b>{today_quests['completed_count']} of {today_quests['total_count']} objectives cleared ({today_quests['completion_pct']}%)</b>. Eliminate remaining targets before midnight.</span>
    </div>
    """, unsafe_allow_html=True)

# =========================================================================
# NAVIGATION SYSTEM
# =========================================================================
nav = st.sidebar.radio(f"{cfg.get('hunter_name', 'Arpit').upper()} NAVIGATION", [
    "🗡️ Hunter Status & Growth",
    "📜 Daily Quests & Lock-In Log",
    "📊 Visual Growth & Pie Charts Deck",
    "🏆 Hunter Achievements & Trophies",
    "📐 Academics (Semester 3)",
    "🤖 Agentic AI Mastery",
    "🌌 ML Project X-0",
    "🛠️ Projects & Proof",
    "💬 AI Hunter Assistant",
    "⚙️ Hunter Config & Reset"
])

# Quick Sound / Status Trigger in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Hunter Level:** `LV. {hunter['level']} ({hunter['rank']})`")
st.sidebar.markdown(f"**Total Grind Output:** `{hunter['total_xp']:,} EXP`")
st.sidebar.markdown(f"**Achievements:** `{achievements_data['unlocked_count']} / {achievements_data['total_count']} Unlocked`")

# =========================================================================
# 1. HUNTER STATUS & GROWTH (CENTRAL HUD)
# =========================================================================
if nav == "🗡️ Hunter Status & Growth":
    st.subheader("Hunter Core Attributes & Status Polygon")
    
    col_rad, col_don = st.columns([1, 1])
    with col_rad:
        fig_radar = create_radar_stat_chart(hunter["stats"])
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Attribute Pills
        stats = hunter["stats"]
        p1, p2, p3, p4, p5 = st.columns(5)
        p1.metric("INT", stats["INT"], "Academics")
        p2.metric("STR", stats["STR"], "Execution")
        p3.metric("PER", stats["PER"], "Research")
        p4.metric("AGI", stats["AGI"], "Agentic")
        p5.metric("VIT", stats["VIT"], "Stamina")

    with col_don:
        fig_effort = create_effort_pie_chart(daily_df)
        st.plotly_chart(fig_effort, use_container_width=True)

    st.markdown("---")
    st.subheader("Winter Arc Lock-In Progression Pace")

    col_gauge, col_growth = st.columns([1, 2])
    with col_gauge:
        fig_gauge = create_winter_arc_pace_gauge(hunter["days_elapsed"], hunter["total_days"], hunter["total_xp"])
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.caption(f"Target: 50,000 EXP across 92 Winter Arc days. Current pace: **{hunter['total_xp'] // max(1, hunter['days_elapsed'])} EXP/day**.")

    with col_growth:
        fig_cum = create_xp_cumulative_chart(daily_df, calculate_row_xp)
        st.plotly_chart(fig_cum, use_container_width=True)

    # Core Output Metrics
    st.subheader("Cumulative Winter Arc Outputs")
    m1, m2, m3 = st.columns(3)
    total_math = int(daily_df["m3_solved"].sum()) if len(daily_df) else 0
    total_loc = int(daily_df["python_loc_written"].sum()) if len(daily_df) else 0
    deep_hours = float(daily_df["deep_work_hours"].sum()) if len(daily_df) else 0.0

    m1.metric("Math Questions Solved", f"{total_math:,}", "Target: 500+")
    m2.metric("Python LOC Written", f"{total_loc:,}", "Target: 10,000+")
    m3.metric("Deep Work Hours", f"{deep_hours:.1f} hrs", "Stamina")

# =========================================================================
# 2. DAILY QUESTS & LOCK-IN LOG (INTERACTIVE DAILY ENTRY + QUESTS)
# =========================================================================
elif nav == "📜 Daily Quests & Lock-In Log":
    st.subheader("Solo Leveling Daily Quest: Preparation to Become a Monarch")
    st.caption("Fulfill all daily training quotas to avoid penalty mode and earn maximum EXP.")

    # Daily Quests Status Overview
    q_col1, q_col2 = st.columns([1, 2])
    with q_col1:
        fig_qdonut = create_daily_quest_donut(today_quests["completed_count"], today_quests["total_count"])
        st.plotly_chart(fig_qdonut, use_container_width=True)
    
    with q_col2:
        st.markdown(f"### Objectives Status ({today_quests['completed_count']} / {today_quests['total_count']} Cleared)")
        for q in today_quests["quests"]:
            done_class = "quest-item-done" if q["completed"] else ""
            status_icon = "✅ CLEARED" if q["completed"] else f"{q['actual']:.0f} / {q['target']:.0f} {q['unit']}"
            status_color = "#34d399" if q["completed"] else "#38bdf8"
            
            st.markdown(f"""
            <div class="quest-item-card {done_class}">
                <div>
                    <span style="font-size: 1.15rem; margin-right: 8px;">{q['icon']}</span>
                    <strong style="color: #e2e8f0;">{q['title']}</strong>
                    <span style="font-size: 0.75rem; color: #94a3b8; margin-left: 8px;">[{q['domain']}]</span>
                </div>
                <div>
                    <span style="font-family: 'Michroma', monospace; font-weight: 700; color: {status_color}; font-size: 0.8rem; letter-spacing: 1px;">
                        {status_icon}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Custom Goals Section
    st.markdown("---")
    st.subheader("Personal Daily Custom Goals")
    c_goal_col1, c_goal_col2 = st.columns([2, 1])
    
    with c_goal_col1:
        today_str = str(date.today())
        goals_for_today = custom_goals_df[custom_goals_df["dt"] == today_str] if len(custom_goals_df) else pd.DataFrame()
        
        if len(goals_for_today) > 0:
            for _, g in goals_for_today.iterrows():
                checked = st.checkbox(
                    f"{g['task_name']} — Target: {g['target_val']} {g['unit']} (+{g['xp_reward']} XP)",
                    value=bool(g["completed"]),
                    key=f"goal_{g['id']}"
                )
                if checked != bool(g["completed"]):
                    toggle_custom_goal(g["id"], checked)
                    st.rerun()
        else:
            st.info("No custom goals created for today yet. Use the quick adder on the right!")

    with c_goal_col2:
        with st.expander("➕ Add Custom Daily Goal", expanded=False):
            with st.form("add_goal"):
                g_name = st.text_input("Goal / Task Name", placeholder="e.g. Read 1 ArXiv Paper")
                g_target = st.number_input("Target Value", min_value=1.0, value=1.0, step=1.0)
                g_unit = st.text_input("Unit", value="times")
                g_cat = st.selectbox("Category", ["Academics", "Coding", "Research", "Health & Gym", "Other"])
                g_xp = st.number_input("XP Reward", min_value=10, max_value=500, value=50, step=10)
                submitted_goal = st.form_submit_button("Add Goal")
                if submitted_goal and g_name:
                    save_custom_goal(date.today(), g_name, g_target, g_unit, g_cat, g_xp)
                    st.success("Custom goal added!")
                    st.rerun()

    # Daily Fast-Entry Form
    st.markdown("---")
    st.subheader("Daily Output Logging Terminal")
    st.caption("Record your battle accomplishments. The system will calculate EXP and rank increases instantly.")

    with st.form("daily_entry_form"):
        entry_date = st.date_input("Log Date", value=date.today())
        
        # Tabs inside form for organized entry
        tab_acad, tab_mastery, tab_stamina = st.tabs([
            "📐 Academics", "🤖 Agentic AI & X-0", "⏳ Stamina & Deep Work"
        ])
        
        with tab_acad:
            st.markdown("#### Mathematics III")
            ac1, ac2, ac3, ac4 = st.columns(4)
            m3_att = ac1.number_input("M3 Attempted", 0, 500, 0)
            m3_sol = ac2.number_input("M3 Solved", 0, 500, 0)
            m3_cor = ac3.number_input("M3 Correct", 0, 500, 0)
            m3_chap = ac4.text_input("M3 Chapter", placeholder="e.g. Vector Calculus")
            m3_top = st.text_input("M3 Specific Topic", placeholder="e.g. Stokes' Theorem")
            
            st.markdown("#### COOS (Computer Organization & OS)")
            co1, co2, co3, co4, co5 = st.columns(5)
            co_num = co1.number_input("Numericals", 0, 200, 0)
            co_cor = co2.number_input("Correct", 0, 200, 0)
            co_tl = co3.number_input("Theory Learned", 0, 50, 0)
            co_tr = co4.number_input("Theory Revised", 0, 50, 0)
            co_prac = co5.number_input("Practicals", 0, 20, 0)
            
            st.markdown("#### Python & DSA")
            py1, py2, py3, py4, py5 = st.columns(5)
            py_task = py1.number_input("Python Tasks", 0, 50, 0)
            py_loc_w = py2.number_input("LOC Written", 0, 50000, 0, step=50)
            py_loc_r = py3.number_input("LOC Read", 0, 50000, 0, step=50)
            dsa_prob = py4.number_input("DSA Problems", 0, 100, 0)
            dsa_leet = py5.number_input("LeetCode Solved", 0, 100, 0)
            
            ds1, ds2, uh1, uh2 = st.columns(4)
            dsa_java = ds1.number_input("Java Implements", 0, 50, 0)
            dsa_rev = ds2.number_input("DSA Revisions", 0, 50, 0)
            uhv_l = uh1.number_input("UHV Learned", 0, 50, 0)
            uhv_r = uh2.number_input("UHV Revised", 0, 50, 0)

        with tab_mastery:
            st.markdown("#### Agentic AI Mastery")
            at1, at2, at3, at4, at5 = st.columns(5)
            at_l = at1.number_input("Agentic Topics Learned", 0, 50, 0)
            at_r = at2.number_input("Topics Revised", 0, 50, 0)
            at_d = at3.number_input("Topics Deepened", 0, 50, 0)
            at_req = at4.number_input("Requirements Solved", 0, 50, 0)
            at_prj = at5.number_input("Projects Completed", 0, 20, 0)
            
            st.markdown("#### ML Project X-0")
            x1, x2, x3, x4, x5 = st.columns(5)
            x_l = x1.number_input("X-0 Topics Learned", 0, 50, 0)
            x_r = x2.number_input("X-0 Revised", 0, 50, 0)
            x_d = x3.number_input("X-0 Deepened", 0, 50, 0)
            x_exp = x4.number_input("Experiments Run", 0, 50, 0)
            x_hyp = x5.number_input("Hypotheses Resolved", 0, 50, 0)

        with tab_stamina:
            st.markdown("#### Stamina & Deep Work")
            st1, st2 = st.columns([1, 3])
            deep_hrs = st1.number_input("Deep Work Hours", 0.0, 24.0, 0.0, step=0.5)
            notes = st2.text_input("Daily Reflection / Battlefield Notes", placeholder="What made today legendary?")

        save_btn = st.form_submit_button("⚔️ Log Daily Record & Awaken Stats", type="primary")
        if save_btn:
            row_dict = {
                "dt": str(entry_date),
                "m3_attempted": m3_att, "m3_solved": m3_sol, "m3_correct": m3_cor, "m3_chapter": m3_chap, "m3_topic": m3_top,
                "coos_numericals": co_num, "coos_correct": co_cor, "coos_theory_learned": co_tl, "coos_theory_revised": co_tr, "coos_practicals": co_prac,
                "python_tasks": py_task, "python_loc_written": py_loc_w, "python_loc_read": py_loc_r, "python_topics_learned": 0, "python_topics_applied": 0,
                "dsa_theory": 0, "dsa_problems": dsa_prob, "dsa_leetcode": dsa_leet, "dsa_java_impl": dsa_java, "dsa_revision": dsa_rev,
                "uhv_learned": uhv_l, "uhv_revised": uhv_r,
                "agency_prospects": 0, "agency_contacted": 0, "agency_outreach": 0, "agency_followups": 0,
                "agency_replies": 0, "agency_conversations": 0, "agency_calls": 0, "agency_proposals": 0,
                "agency_deals": 0, "agency_new_mrr": 0.0, "agency_current_mrr": 0.0,
                "linkedin_posts": 0, "instagram_posts": 0, "other_content": 0,
                "agentic_topics_learned": at_l, "agentic_topics_revised": at_r, "agentic_topics_deepened": at_d,
                "agentic_requirements_solved": at_req, "agentic_projects": at_prj, "agentic_features": 0, "agentic_deployments": 0,
                "agentic_bugs_fixed": 0, "agentic_capabilities": 0,
                "x0_topics_learned": x_l, "x0_topics_revised": x_r, "x0_topics_deepened": x_d,
                "x0_experiments": x_exp, "x0_hypotheses": x_hyp, "x0_questions_resolved": 0, "x0_sources": 0, "x0_milestones": 0,
                "dads_investigated": 0, "dads_implementing": 0, "dads_improved": 0, "dads_independent": 0,
                "dads_tech_impl": 0, "dads_tech_knowledge": 0.0, "dads_ops_knowledge": 0.0,
                "deep_work_hours": deep_hrs, "notes": notes
            }
            save_daily(row_dict)
            xp_gained = calculate_row_xp(row_dict)
            st.balloons()
            st.success(f"⚔️ Battle record logged for {entry_date}! +{xp_gained:,} EXP added to your Hunter Core!")
            st.rerun()

# =========================================================================
# 3. VISUAL GROWTH & PIE CHARTS DECK (DIRECT USER FOCUS)
# =========================================================================
elif nav == "📊 Visual Growth & Pie Charts Deck":
    st.subheader("Visual Growth & Multidimensional Pie Chart Analytics")
    st.markdown("Gain crystalline visibility into your energy expenditure, problem distributions, and skill masteries.")

    # Row 1 of Pie Charts
    p_row1_c1, p_row1_c2 = st.columns(2)
    with p_row1_c1:
        st.plotly_chart(create_effort_pie_chart(daily_df), use_container_width=True)
    with p_row1_c2:
        st.plotly_chart(create_academic_pie_chart(daily_df), use_container_width=True)

    # Row 2 of Pie Charts
    p_row2_c1, p_row2_c2 = st.columns(2)
    with p_row2_c1:
        st.plotly_chart(create_task_type_donut(daily_df), use_container_width=True)
    with p_row2_c2:
        st.plotly_chart(create_skill_depth_pie(agentic_df, x0_df), use_container_width=True)

    # Row 3 of Pie Charts
    p_row3_c1, p_row3_c2 = st.columns(2)
    with p_row3_c1:
        today_breakdown = get_row_xp_breakdown(hunter["today_row"])
        st.plotly_chart(create_today_xp_pie(today_breakdown), use_container_width=True)
    with p_row3_c2:
        st.plotly_chart(create_daily_quest_donut(today_quests["completed_count"], today_quests["total_count"]), use_container_width=True)

    st.markdown("---")
    st.subheader("Weekly Output Comparison Across Domains")
    st.plotly_chart(create_weekly_output_comparison(daily_df), use_container_width=True)

# =========================================================================
# 4. HUNTER ACHIEVEMENTS & TROPHIES
# =========================================================================
elif nav == "🏆 Hunter Achievements & Trophies":
    st.subheader(f"Hunter Awakening Badges ({achievements_data['unlocked_count']} / {achievements_data['total_count']} Unlocked — {achievements_data['pct_unlocked']}%)")
    st.caption("Unlock permanent titles, reputation, and EXP bonuses by reaching pivotal milestones.")

    # Progress summary bar
    st.progress(achievements_data["pct_unlocked"] / 100.0)
    
    # 3-column badge gallery
    cols = st.columns(3)
    for idx, ach in enumerate(achievements_data["achievements"]):
        col = cols[idx % 3]
        status_class = "unlocked" if ach["unlocked"] else "locked"
        status_tag = "✅ UNLOCKED" if ach["unlocked"] else f"{ach['progress_pct']}% LOCKED"
        rarity_class = f"rarity-{ach['rarity'].lower()}"
        
        with col:
            st.markdown(f"""
            <div class="achievement-card {status_class}" style="margin-bottom: 16px;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span class="rarity-pill {rarity_class}">{ach['rarity']}</span>
                        <span style="font-family: 'Michroma', monospace; font-size: 0.7rem; color: #34d399; font-weight:700; letter-spacing: 1px;">
                            +{ach['xp_reward']} EXP
                        </span>
                    </div>
                    <div style="font-size: 1.3rem; margin-bottom: 4px; font-family: 'Plus Jakarta Sans', sans-serif;">{ach['icon']} <b>{ach['title']}</b></div>
                    <div style="font-size: 0.82rem; color: #94a3b8; line-height: 1.3; font-family: 'Plus Jakarta Sans', sans-serif;">{ach['desc']}</div>
                </div>
                <div style="margin-top: 14px; border-top: 1px solid rgba(0, 210, 255, 0.15); padding-top: 8px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.72rem; font-family: 'Michroma', monospace; color: {'#34d399' if ach['unlocked'] else '#64748b'}; letter-spacing: 0.5px;">
                        <span>{status_tag}</span>
                        <span>[{ach['category']}]</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# =========================================================================
# 5. ACADEMICS TRACK
# =========================================================================
elif nav == "📐 Academics (Semester 3)":
    st.subheader("Semester 3 Academic Mastery")
    
    if len(daily_df):
        a1, a2, a3, a4, a5 = st.columns(5)
        a1.metric("M3 Questions Solved", int(daily_df["m3_solved"].sum()))
        a2.metric("COOS Numericals", int(daily_df["coos_numericals"].sum()))
        a3.metric("Python Tasks", int(daily_df["python_tasks"].sum()))
        a4.metric("Python LOC", f"{int(daily_df['python_loc_written'].sum()):,}")
        a5.metric("DSA Problems", int(daily_df["dsa_problems"].sum() + daily_df["dsa_leetcode"].sum()))

        c_pie, c_trend = st.columns([1, 1])
        with c_pie:
            st.plotly_chart(create_academic_pie_chart(daily_df), use_container_width=True)
        with c_trend:
            df_acad = daily_df.copy()
            df_acad["Date"] = pd.to_datetime(df_acad["dt"])
            df_acad["Week"] = df_acad["Date"].dt.to_period("W").astype(str)
            week_acad = df_acad.groupby("Week").agg(
                M3=("m3_solved", "sum"),
                COOS=("coos_numericals", "sum"),
                Python=("python_tasks", "sum"),
                DSA=("dsa_problems", "sum")
            ).reset_index()
            fig_bar = px.bar(week_acad, x="Week", y=["M3", "COOS", "Python", "DSA"], barmode="group", title="Academic Outputs by Week")
            fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#cbd5e1"))
            st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("M3 Chapter Ledger")
        m3_ledger = read("m3_topic_log")
        if len(m3_ledger):
            agg = m3_ledger.groupby("chapter").agg(
                Attempted=("attempted", "sum"),
                Solved=("solved", "sum"),
                Correct=("correct", "sum")
            ).reset_index()
            agg["Accuracy (%)"] = (agg["Correct"] / agg["Solved"].replace(0, pd.NA) * 100).round(1)
            st.dataframe(agg, use_container_width=True)
        else:
            st.info("Log individual M3 sessions to generate granular chapter analytics.")
    else:
        st.info("No daily logs recorded yet. Use the Daily Quests & Entry tab to start.")

# =========================================================================
# 6. AGENTIC AI TRACK
# =========================================================================
elif nav == "🤖 Agentic AI Mastery":
    st.subheader(f"Agentic AI Mastery (December Target: Phase ≤ {cfg['agentic_target_phase']})")
    
    if len(agentic_df):
        cur_phase = int(agentic_df.loc[agentic_df.current_depth > 0, "phase"].max()) if (agentic_df.current_depth > 0).any() else 0
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Highest Phase", f"Phase {cur_phase}")
        c2.metric("Target Phase", f"≤ Phase {cfg['agentic_target_phase']}")
        c3.metric("Topics Touched", int((agentic_df.current_depth > 0).sum()))
        c4.metric("Deep Mastery (≥4)", int((agentic_df.current_depth >= 4).sum()))

        c_phase, c_depth = st.columns(2)
        with c_phase:
            phase_agg = agentic_df.groupby("phase").agg(
                Total=("topic_id", "count"),
                Learned=("current_depth", lambda s: int((s > 0).sum()))
            ).reset_index()
            fig_p = px.bar(phase_agg, x="phase", y=["Total", "Learned"], barmode="group", title="Agentic Curriculum by Phase")
            fig_p.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#cbd5e1"))
            st.plotly_chart(fig_p, use_container_width=True)
        with c_depth:
            d_counts = agentic_df["current_depth"].value_counts().sort_index().reindex(range(6), fill_value=0).reset_index()
            d_counts.columns = ["Depth", "Count"]
            fig_d = px.pie(d_counts, names="Depth", values="Count", hole=0.55, title="Agentic Topic Depth Breakdown (0-5)")
            fig_d.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#cbd5e1"))
            st.plotly_chart(fig_d, use_container_width=True)

        st.subheader("Curriculum Topic Master")
        st.dataframe(agentic_df.sort_values(["phase", "topic_id"]), use_container_width=True)
    else:
        st.info("Curriculum is being populated. Seed topics in config.")

# =========================================================================
# 8. ML PROJECT X-0 TRACK
# =========================================================================
elif nav == "🌌 ML Project X-0":
    st.subheader(f"ML Project X-0 — Phase 0 ({cfg['x0_phase0_topic_target']} Deep Topics)")
    
    if len(x0_df):
        covered = int((x0_df.current_depth > 0).sum())
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Topics Covered", f"{covered} / {cfg['x0_phase0_topic_target']}")
        c2.metric("Depth ≥3", int((x0_df.current_depth >= 3).sum()))
        c3.metric("Depth ≥4", int((x0_df.current_depth >= 4).sum()))
        c4.metric("Remaining", max(0, cfg["x0_phase0_topic_target"] - covered))

        c_x0_pie, c_x0_hist = st.columns(2)
        with c_x0_pie:
            st.plotly_chart(create_skill_depth_pie(pd.DataFrame(), x0_df), use_container_width=True)
        with c_x0_hist:
            x0_counts = x0_df["current_depth"].value_counts().sort_index().reindex(range(6), fill_value=0).reset_index()
            x0_counts.columns = ["Depth", "Topics"]
            fig_xd = px.bar(x0_counts, x="Depth", y="Topics", title="X-0 Depth Distribution (0-5)")
            fig_xd.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#cbd5e1"))
            st.plotly_chart(fig_xd, use_container_width=True)

        st.subheader("X-0 Topic Ledger")
        st.dataframe(x0_df.sort_values(["category", "topic_id"]), use_container_width=True)
    else:
        st.info("No X-0 topics loaded yet.")

# =========================================================================
# 8. PROJECTS & PROOF
# =========================================================================
elif nav == "🛠️ Projects & Proof":
    st.subheader("Project Portfolio & Deployment Proof")
    
    if len(projects_df):
        st.dataframe(projects_df, use_container_width=True)
    else:
        st.info("No projects registered yet.")

    with st.expander("Register New Project"):
        with st.form("new_prj"):
            pid = st.text_input("Project ID", placeholder="PRJ-01")
            pname = st.text_input("Project Name", placeholder="Autonomous Agent Orchestrator")
            pdomain = st.selectbox("Domain", ["Agentic AI", "ML Project X-0", "Academics", "Engineering", "Other"])
            ptech = st.text_input("Technologies", placeholder="Python, FastAPI, Streamlit, LangGraph")
            pout = st.text_area("Outcome / Measurable Impact")
            p_sub = st.form_submit_button("Save Project")
            if p_sub and pid and pname:
                con = db()
                con.execute("""
                    INSERT OR REPLACE INTO projects(project_id, project_name, domain, technologies, outcome, status)
                    VALUES(?,?,?,?,?, 'Active')
                """, (pid, pname, pdomain, ptech, pout))
                con.commit()
                con.close()
                st.success("Project registered!")
                st.rerun()

# =========================================================================
# 9. AI HUNTER ASSISTANT (GROQ POWERED)
# =========================================================================
elif nav == "💬 AI Hunter Assistant":
    st.subheader("🔮 AI System Assistant & Shadow Companion")
    st.markdown("""
    <div class="system-notification" style="border-left-color: #8b5cf6; background: linear-gradient(90deg, rgba(139, 92, 246, 0.15) 0%, rgba(13, 20, 36, 0.8) 100%);">
        <span class="system-notification-tag" style="color: #a78bfa;">[ NEURAL LINK ACTIVE: GROQ ENGINE ]</span>
        <span class="system-notification-msg">Direct line to your Solo Leveling System Companion. Ask any question on <b>Mathematics III</b>, <b>COOS</b>, <b>Python & DSA</b>, <b>Agentic AI</b>, or <b>Project X-0</b>.</span>
    </div>
    """, unsafe_allow_html=True)

    api_key = cfg.get("groq_api_key", "")

    with st.expander("⚙️ Companion Tuning & Model Configuration", expanded=False):
        c1, c2, c3 = st.columns([1.5, 1.5, 1])
        with c1:
            persona_style = st.selectbox(
                "Companion Persona",
                ["System Monarch Companion", "Academic & Code Tutor", "General AI Assistant"],
                index=0,
                help="Defines the tone and contextual focus of the AI companion."
            )
        with c2:
            avail_models = ai_assistant.get_available_models(api_key)
            default_m = cfg.get("groq_model", "qwen/qwen3.8-27b")
            m_idx = avail_models.index(default_m) if default_m in avail_models else 0
            selected_model = st.selectbox("Groq Model", avail_models, index=m_idx)
        with c3:
            temperature = st.slider("Creativity / Temp", 0.0, 1.0, 0.7, step=0.05)

    # Quick Tactical Prompt Chips
    st.markdown("<div style='font-family: Michroma, sans-serif; font-size: 0.72rem; color: #7dd3fc; letter-spacing: 1px; margin-bottom: 8px;'>TACTICAL PROMPT PRESETS:</div>", unsafe_allow_html=True)
    chip_cols = st.columns(4)
    quick_prompt = None
    if chip_cols[0].button("📐 Solve M3 Cauchy-Euler", use_container_width=True):
        quick_prompt = "Explain step-by-step how to solve a Cauchy-Euler differential equation with variable coefficients, showing the transformation x = e^z with a concrete exam-style example."
    if chip_cols[1].button("🤖 LangGraph Agent Routing", use_container_width=True):
        quick_prompt = "Explain how to construct a conditional edge router in LangGraph with stateful agent workflows, showing clean Python code."
    if chip_cols[2].button("🌌 Attention Math & Shapes", use_container_width=True):
        quick_prompt = "Derive the exact Scaled Dot-Product Attention mathematical equation and tensor shapes for batch B, sequence length S, and head dimension D for ML Project X-0."
    if chip_cols[3].button("⚔️ Lock-In Status Report", use_container_width=True):
        quick_prompt = "Review my current Hunter Level and Winter Arc progression. Give me a motivating System evaluation and a structured 4-hour deep work study plan for today."

    # Initialize Chat History in session state
    if "chat_messages" not in st.session_state or not st.session_state["chat_messages"]:
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": (
                    f"[ SYSTEM INITIALIZED ]\n\nGreetings, {cfg.get('hunter_name', 'Arpit')}. I am your dedicated AI Companion for the Winter Arc Lock-In.\n\n"
                    f"I have active awareness of your Hunter Rank, stats, and study curriculums (Mathematics III, COOS, Python, DSA, Agentic AI, and ML Project X-0).\n\n"
                    f"What challenge shall we conquer today?"
                )
            }
        ]

    # Render Chat Messages
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state["chat_messages"]:
            avatar = "🗡️" if msg["role"] == "user" else "⚡"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    # Clear Chat button
    col_btn1, col_btn2 = st.columns([6, 1])
    with col_btn2:
        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state["chat_messages"] = [
                {
                    "role": "assistant",
                    "content": f"[ SYSTEM RESET ]\n\nMemory cache cleared. Standing by for new orders, {cfg.get('hunter_name', 'Arpit')}."
                }
            ]
            st.rerun()

    # Input Handling
    user_input = st.chat_input(f"Ask your AI System Companion (M3, Agentic AI, X-0, Python, DSA)...")
    final_input = quick_prompt or user_input

    if final_input:
        st.session_state["chat_messages"].append({"role": "user", "content": final_input})
        with st.chat_message("user", avatar="🗡️"):
            st.markdown(final_input)

        sys_prompt = ai_assistant.build_system_prompt(hunter, cfg, style=persona_style)
        api_messages = [{"role": "system", "content": sys_prompt}]
        for m in st.session_state["chat_messages"]:
            api_messages.append({"role": m["role"], "content": m["content"]})

        with st.chat_message("assistant", avatar="⚡"):
            try:
                response_generator = ai_assistant.stream_groq_chat(
                    api_key=api_key,
                    messages=api_messages,
                    model=selected_model,
                    temperature=temperature
                )
                full_response = st.write_stream(response_generator)
            except Exception as ex:
                try:
                    full_response = ai_assistant.send_groq_chat(
                        api_key=api_key,
                        messages=api_messages,
                        model=selected_model,
                        temperature=temperature
                    )
                    st.markdown(full_response)
                except Exception as inner_ex:
                    full_response = f"⚠️ **[ SYSTEM ERROR ]**: Unable to communicate with AI engine. {str(inner_ex)}"
                    st.error(full_response)

        st.session_state["chat_messages"].append({"role": "assistant", "content": full_response})

# =========================================================================
# 10. HUNTER CONFIG & SYSTEM RESET
# =========================================================================
elif nav == "⚙️ Hunter Config & Reset":
    st.subheader("Hunter System Configuration & Core Targets")
    st.write("Customize your Hunter title, targets, API keys, and seed sample battle data.")

    with st.form("config_form"):
        h_name = st.text_input("Hunter Name", value=str(cfg.get("hunter_name", "Arpit")))
        h_title = st.text_input("Hunter Title", value=str(cfg.get("hunter_title", "Shadow Monarch in Training")))
        sgpa = st.number_input("SGPA Target", min_value=0.0, max_value=10.0, value=float(cfg.get("sgpa_target", 10.0)), step=0.1)
        ag_phase = st.number_input("Agentic AI Target Phase", min_value=1, max_value=12, value=int(cfg.get("agentic_target_phase", 9)))
        x0_target = st.number_input("X-0 Topic Target", min_value=10, max_value=200, value=int(cfg.get("x0_phase0_topic_target", 100)))
        value=str(cfg.get("groq_api_key", "")), type="password")
        models_list = ai_assistant.get_available_models(groq_k)
        m_idx = models_list.index(curr_m) if curr_m in models_list else 0
        groq_m = st.selectbox("Default Groq Model", models_list, index=m_idx)
        
        save_cfg = st.form_submit_button("Save System Configuration", type="primary")
        if save_cfg:
            update_config_key("hunter_name", h_name)
            update_config_key("hunter_title", h_title)
            update_config_key("sgpa_target", sgpa)
            update_config_key("agentic_target_phase", ag_phase)
            update_config_key("x0_phase0_topic_target", x0_target)
            update_config_key("groq_api_key", groq_k)
            update_config_key("groq_model", groq_m)
            st.success("System parameters calibrated successfully.")
            st.rerun()

    st.markdown("---")
    st.subheader("Battlefield Data Generator & Reset")
    st.write("Demonstrate the complete Solo Leveling system with realistic 7-day Lock-In sample data.")

    col_seed, col_clear = st.columns(2)
    with col_seed:
        if st.button("🌟 Awaken with Realistic 7-Day Lock-In Sample Data", type="primary"):
            a_cnt, x_cnt = seed_topics.seed_topics_master()
            d_cnt = seed_topics.seed_sample_daily_logs()
            st.balloons()
            st.success(f"System awakened! Loaded {d_cnt} consecutive days of lock-in progress, {a_cnt} Agentic topics, and {x_cnt} X-0 topics!")
            st.rerun()

    with col_clear:
        if st.button("⚠️ Reset / Clear All Daily Logs to 0"):
            con = db()
            con.execute("DELETE FROM daily_log")
            con.execute("DELETE FROM m3_topic_log")
            con.commit()
            con.close()
            st.warning("Daily logs wiped. Ready for fresh manual daily entry.")
            st.rerun()
