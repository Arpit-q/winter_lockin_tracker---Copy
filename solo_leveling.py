"""
Solo Leveling Gamification & Hunter System Engine
Calculates XP, Hunter Ranks, 6-Dimensional Attributes, Quests, and Achievements.
"""
from datetime import date, datetime, timedelta
import math
import pandas as pd

# XP Multipliers for Output Tasks
XP_VALUES = {
    # Academics
    "m3_solved": 15,
    "coos_numericals": 15,
    "coos_theory_learned": 10,
    "coos_practicals": 20,
    "python_tasks": 25,
    "python_loc_per_100": 20,  # 20 XP per 100 LOC
    "dsa_problems": 30,
    "dsa_leetcode": 45,
    "dsa_java_impl": 35,
    "uhv_learned": 10,
    
    # Mastery & Research
    "agentic_topics_learned": 35,
    "agentic_topics_deepened": 50,
    "agentic_requirements_solved": 75,
    "agentic_projects": 150,
    "agentic_deployments": 100,
    "agentic_bugs_fixed": 30,
    "x0_topics_learned": 35,
    "x0_topics_deepened": 50,
    "x0_experiments": 60,
    "x0_hypotheses": 40,
    
    # Stamina & Deep Work
    "deep_work_hour": 50,
    
    # Quests
    "daily_quest_cleared": 250,
}

# Hunter Rank Thresholds
HUNTER_RANKS = [
    {"rank": "E-Rank", "tier": "Awakened Novice", "min_level": 1, "color": "#94a3b8", "badge": "🔰", "glow": "0 0 16px rgba(148, 163, 184, 0.35)"},
    {"rank": "D-Rank", "tier": "Dungeon Explorer", "min_level": 11, "color": "#38bdf8", "badge": "⚡", "glow": "0 0 20px rgba(56, 189, 248, 0.5)"},
    {"rank": "C-Rank", "tier": "Elite Striker", "min_level": 26, "color": "#00d2ff", "badge": "⚔️", "glow": "0 0 22px rgba(0, 210, 255, 0.55)"},
    {"rank": "B-Rank", "tier": "Guild Vanguard", "min_level": 46, "color": "#818cf8", "badge": "🛡️", "glow": "0 0 24px rgba(129, 140, 248, 0.55)"},
    {"rank": "A-Rank", "tier": "High-Tier Slayer", "min_level": 71, "color": "#a855f7", "badge": "👑", "glow": "0 0 26px rgba(168, 85, 247, 0.6)"},
    {"rank": "S-Rank", "tier": "National Calamity", "min_level": 91, "color": "#c084fc", "badge": "🔥", "glow": "0 0 30px rgba(192, 132, 252, 0.7), 0 0 15px rgba(0, 210, 255, 0.5)"},
    {"rank": "MONARCH", "tier": "Shadow Monarch", "min_level": 100, "color": "#00d2ff", "badge": "🌌", "glow": "0 0 25px rgba(0, 210, 255, 0.8), 0 0 45px rgba(124, 58, 237, 0.85)"},
]

# Core Daily Quest Objectives
DEFAULT_DAILY_QUESTS = [
    {"key": "m3", "title": "Solve 10+ Mathematics III Questions", "domain": "Academics", "target": 10, "unit": "questions", "col": "m3_solved", "icon": "📐"},
    {"key": "dsa", "title": "Solve 5+ DSA / LeetCode Problems", "domain": "Academics", "target": 5, "unit": "problems", "col": "dsa_problems", "icon": "🧠"},
    {"key": "code", "title": "Ship 150+ Lines of Python Code", "domain": "Academics", "target": 150, "unit": "LOC", "col": "python_loc_written", "icon": "💻"},
    {"key": "mastery", "title": "Learn / Deepen 2+ Agentic or X-0 Topics", "domain": "Mastery", "target": 2, "unit": "topics", "col": "topics_combo", "icon": "🤖"},
    {"key": "deep_work", "title": "Lock In 3.0+ Deep Work Hours", "domain": "Stamina", "target": 3.0, "unit": "hours", "col": "deep_work_hours", "icon": "⏳"},
]

# Hunter Achievements
ACHIEVEMENTS_LIST = [
    {
        "id": "awakening",
        "title": "First Awakening",
        "desc": "Log your first day into the Winter Arc system",
        "category": "General",
        "icon": "🌟",
        "rarity": "Common",
        "xp_reward": 100,
        "check": lambda daily, topics_a, topics_x, dads: len(daily) >= 1,
        "progress": lambda daily, topics_a, topics_x, dads: min(len(daily) / 1.0, 1.0)
    },
    {
        "id": "streak_3",
        "title": "Unbroken Focus",
        "desc": "Maintain a 3-day Winter Arc lock-in streak",
        "category": "Discipline",
        "icon": "⚡",
        "rarity": "Common",
        "xp_reward": 150,
        "check": lambda daily, topics_a, topics_x, dads: calculate_streak(daily) >= 3,
        "progress": lambda daily, topics_a, topics_x, dads: min(calculate_streak(daily) / 3.0, 1.0)
    },
    {
        "id": "streak_7",
        "title": "Iron Will",
        "desc": "Maintain a 7-day Winter Arc lock-in streak",
        "category": "Discipline",
        "icon": "🔥",
        "rarity": "Rare",
        "xp_reward": 350,
        "check": lambda daily, topics_a, topics_x, dads: calculate_streak(daily) >= 7,
        "progress": lambda daily, topics_a, topics_x, dads: min(calculate_streak(daily) / 7.0, 1.0)
    },
    {
        "id": "streak_21",
        "title": "Habit Transmutation",
        "desc": "Maintain a 21-day Winter Arc lock-in streak",
        "category": "Discipline",
        "icon": "👑",
        "rarity": "Epic",
        "xp_reward": 1000,
        "check": lambda daily, topics_a, topics_x, dads: calculate_streak(daily) >= 21,
        "progress": lambda daily, topics_a, topics_x, dads: min(calculate_streak(daily) / 21.0, 1.0)
    },
    {
        "id": "math_50",
        "title": "Calculus Initiate",
        "desc": "Solve 50+ total Mathematics III questions",
        "category": "Academics",
        "icon": "📐",
        "rarity": "Common",
        "xp_reward": 200,
        "check": lambda daily, topics_a, topics_x, dads: daily["m3_solved"].sum() >= 50 if len(daily) else False,
        "progress": lambda daily, topics_a, topics_x, dads: min(daily["m3_solved"].sum() / 50.0, 1.0) if len(daily) else 0.0
    },
    {
        "id": "math_200",
        "title": "Math Berserker",
        "desc": "Solve 200+ total Mathematics III questions",
        "category": "Academics",
        "icon": "⚔️",
        "rarity": "Rare",
        "xp_reward": 500,
        "check": lambda daily, topics_a, topics_x, dads: daily["m3_solved"].sum() >= 200 if len(daily) else False,
        "progress": lambda daily, topics_a, topics_x, dads: min(daily["m3_solved"].sum() / 200.0, 1.0) if len(daily) else 0.0
    },
    {
        "id": "dsa_50",
        "title": "Algorithm Striker",
        "desc": "Solve 50+ Data Structures & Algorithms problems",
        "category": "Academics",
        "icon": "🧠",
        "rarity": "Rare",
        "xp_reward": 400,
        "check": lambda daily, topics_a, topics_x, dads: (daily["dsa_problems"].sum() + daily["dsa_leetcode"].sum()) >= 50 if len(daily) else False,
        "progress": lambda daily, topics_a, topics_x, dads: min((daily["dsa_problems"].sum() + daily["dsa_leetcode"].sum()) / 50.0, 1.0) if len(daily) else 0.0
    },
    {
        "id": "code_1000",
        "title": "Code Warrior",
        "desc": "Write 1,000+ lines of Python code",
        "category": "Engineering",
        "icon": "💻",
        "rarity": "Common",
        "xp_reward": 250,
        "check": lambda daily, topics_a, topics_x, dads: daily["python_loc_written"].sum() >= 1000 if len(daily) else False,
        "progress": lambda daily, topics_a, topics_x, dads: min(daily["python_loc_written"].sum() / 1000.0, 1.0) if len(daily) else 0.0
    },
    {
        "id": "code_5000",
        "title": "Syntax Necromancer",
        "desc": "Write 5,000+ lines of Python code",
        "category": "Engineering",
        "icon": "🪄",
        "rarity": "Epic",
        "xp_reward": 750,
        "check": lambda daily, topics_a, topics_x, dads: daily["python_loc_written"].sum() >= 5000 if len(daily) else False,
        "progress": lambda daily, topics_a, topics_x, dads: min(daily["python_loc_written"].sum() / 5000.0, 1.0) if len(daily) else 0.0
    },
    {
        "id": "agentic_phase_3",
        "title": "Agentic Architect",
        "desc": "Advance to Phase 3 or higher in Agentic AI",
        "category": "Mastery",
        "icon": "🤖",
        "rarity": "Rare",
        "xp_reward": 500,
        "check": lambda daily, topics_a, topics_x, dads: topics_a.loc[topics_a.current_depth > 0, "phase"].max() >= 3 if len(topics_a) and (topics_a.current_depth > 0).any() else False,
        "progress": lambda daily, topics_a, topics_x, dads: min((topics_a.loc[topics_a.current_depth > 0, "phase"].max() if len(topics_a) and (topics_a.current_depth > 0).any() else 0) / 3.0, 1.0)
    },
    {
        "id": "x0_30",
        "title": "Neural Explorer",
        "desc": "Learn 30+ topics in ML Project X-0",
        "category": "Research",
        "icon": "🌌",
        "rarity": "Rare",
        "xp_reward": 600,
        "check": lambda daily, topics_a, topics_x, dads: (topics_x.current_depth > 0).sum() >= 30 if len(topics_x) else False,
        "progress": lambda daily, topics_a, topics_x, dads: min(((topics_x.current_depth > 0).sum() if len(topics_x) else 0) / 30.0, 1.0)
    },
    {
        "id": "deep_work_50",
        "title": "Monk Mode Veteran",
        "desc": "Accumulate 50+ hours of deep work during Winter Arc",
        "category": "Discipline",
        "icon": "🧘",
        "rarity": "Rare",
        "xp_reward": 500,
        "check": lambda daily, topics_a, topics_x, dads: daily["deep_work_hours"].sum() >= 50 if len(daily) else False,
        "progress": lambda daily, topics_a, topics_x, dads: min((daily["deep_work_hours"].sum() if len(daily) else 0) / 50.0, 1.0)
    },
    {
        "id": "level_25",
        "title": "Elite Hunter",
        "desc": "Reach Hunter Level 25 in the Solo Leveling system",
        "category": "Hunter",
        "icon": "🛡️",
        "rarity": "Epic",
        "xp_reward": 1000,
        "check": lambda daily, topics_a, topics_x, dads: calculate_hunter_profile(daily, topics_a, topics_x, dads)["level"] >= 25,
        "progress": lambda daily, topics_a, topics_x, dads: min(calculate_hunter_profile(daily, topics_a, topics_x, dads)["level"] / 25.0, 1.0)
    },
    {
        "id": "level_50",
        "title": "National Level Awakened",
        "desc": "Reach Hunter Level 50 in the Solo Leveling system",
        "category": "Hunter",
        "icon": "👑",
        "rarity": "Legendary",
        "xp_reward": 2500,
        "check": lambda daily, topics_a, topics_x, dads: calculate_hunter_profile(daily, topics_a, topics_x, dads)["level"] >= 50,
        "progress": lambda daily, topics_a, topics_x, dads: min(calculate_hunter_profile(daily, topics_a, topics_x, dads)["level"] / 50.0, 1.0)
    },
]

def calculate_row_xp(row):
    """Calculate total XP earned for a single daily log row."""
    xp = 0
    # Academics
    xp += row.get("m3_solved", 0) * XP_VALUES["m3_solved"]
    xp += row.get("coos_numericals", 0) * XP_VALUES["coos_numericals"]
    xp += row.get("coos_theory_learned", 0) * XP_VALUES["coos_theory_learned"]
    xp += row.get("coos_practicals", 0) * XP_VALUES["coos_practicals"]
    xp += row.get("python_tasks", 0) * XP_VALUES["python_tasks"]
    xp += (row.get("python_loc_written", 0) / 100.0) * XP_VALUES["python_loc_per_100"]
    xp += row.get("dsa_problems", 0) * XP_VALUES["dsa_problems"]
    xp += row.get("dsa_leetcode", 0) * XP_VALUES["dsa_leetcode"]
    xp += row.get("dsa_java_impl", 0) * XP_VALUES["dsa_java_impl"]
    xp += row.get("uhv_learned", 0) * XP_VALUES["uhv_learned"]

    # Mastery
    xp += row.get("agentic_topics_learned", 0) * XP_VALUES["agentic_topics_learned"]
    xp += row.get("agentic_topics_deepened", 0) * XP_VALUES["agentic_topics_deepened"]
    xp += row.get("agentic_requirements_solved", 0) * XP_VALUES["agentic_requirements_solved"]
    xp += row.get("agentic_projects", 0) * XP_VALUES["agentic_projects"]
    xp += row.get("agentic_deployments", 0) * XP_VALUES["agentic_deployments"]
    xp += row.get("agentic_bugs_fixed", 0) * XP_VALUES["agentic_bugs_fixed"]
    xp += row.get("x0_topics_learned", 0) * XP_VALUES["x0_topics_learned"]
    xp += row.get("x0_topics_deepened", 0) * XP_VALUES["x0_topics_deepened"]
    xp += row.get("x0_experiments", 0) * XP_VALUES["x0_experiments"]
    xp += row.get("x0_hypotheses", 0) * XP_VALUES["x0_hypotheses"]

    # Stamina & Deep Work
    xp += row.get("deep_work_hours", 0) * XP_VALUES["deep_work_hour"]

    return int(xp)

def get_row_xp_breakdown(row):
    """Categorized breakdown of XP for today or any specific row."""
    if row is None or (isinstance(row, pd.Series) and row.empty):
        return {"Academics": 0, "Agentic AI": 0, "Project X-0": 0, "Deep Work": 0}

    r = row.to_dict() if isinstance(row, pd.Series) else row
    
    acad_xp = (
        r.get("m3_solved", 0) * XP_VALUES["m3_solved"] +
        r.get("coos_numericals", 0) * XP_VALUES["coos_numericals"] +
        r.get("coos_theory_learned", 0) * XP_VALUES["coos_theory_learned"] +
        r.get("coos_practicals", 0) * XP_VALUES["coos_practicals"] +
        r.get("python_tasks", 0) * XP_VALUES["python_tasks"] +
        (r.get("python_loc_written", 0) / 100.0) * XP_VALUES["python_loc_per_100"] +
        r.get("dsa_problems", 0) * XP_VALUES["dsa_problems"] +
        r.get("dsa_leetcode", 0) * XP_VALUES["dsa_leetcode"] +
        r.get("dsa_java_impl", 0) * XP_VALUES["dsa_java_impl"] +
        r.get("uhv_learned", 0) * XP_VALUES["uhv_learned"]
    )

    agentic_xp = (
        r.get("agentic_topics_learned", 0) * XP_VALUES["agentic_topics_learned"] +
        r.get("agentic_topics_deepened", 0) * XP_VALUES["agentic_topics_deepened"] +
        r.get("agentic_requirements_solved", 0) * XP_VALUES["agentic_requirements_solved"] +
        r.get("agentic_projects", 0) * XP_VALUES["agentic_projects"] +
        r.get("agentic_deployments", 0) * XP_VALUES["agentic_deployments"] +
        r.get("agentic_bugs_fixed", 0) * XP_VALUES["agentic_bugs_fixed"]
    )

    x0_xp = (
        r.get("x0_topics_learned", 0) * XP_VALUES["x0_topics_learned"] +
        r.get("x0_topics_deepened", 0) * XP_VALUES["x0_topics_deepened"] +
        r.get("x0_experiments", 0) * XP_VALUES["x0_experiments"] +
        r.get("x0_hypotheses", 0) * XP_VALUES["x0_hypotheses"]
    )

    stamina_xp = r.get("deep_work_hours", 0) * XP_VALUES["deep_work_hour"]

    return {
        "Academics": int(round(acad_xp)),
        "Agentic AI": int(round(agentic_xp)),
        "Project X-0": int(round(x0_xp)),
        "Deep Work": int(round(stamina_xp))
    }

def calculate_streak(daily_df):
    """Calculates consecutive active days logged ending today or most recent day."""
    if daily_df is None or len(daily_df) == 0:
        return 0
    try:
        dates = pd.to_datetime(daily_df["dt"]).dt.date.drop_duplicates().sort_values(ascending=False).tolist()
        if not dates:
            return 0
        
        today = date.today()
        # If the most recent date is before yesterday, streak is broken
        if (today - dates[0]).days > 1:
            # Check if there is an unbroken chain ending at dates[0]
            chain = 1
            for i in range(len(dates) - 1):
                if (dates[i] - dates[i+1]).days == 1:
                    chain += 1
                else:
                    break
            return chain

        streak = 1
        for i in range(len(dates) - 1):
            if (dates[i] - dates[i+1]).days == 1:
                streak += 1
            else:
                break
        return streak
    except Exception:
        return len(daily_df)

def calculate_level_from_xp(total_xp):
    """
    RPG Level formula:
    Level 1 starts at 0 XP.
    XP required for level L = 150 * (L - 1)^1.4
    Inverts to find current level and progress to next.
    """
    total_xp = max(0, total_xp)
    level = 1
    while True:
        next_level_xp = int(180 * math.pow(level, 1.35))
        if total_xp < next_level_xp:
            prev_level_xp = int(180 * math.pow(level - 1, 1.35)) if level > 1 else 0
            cur_in_level = total_xp - prev_level_xp
            needed_in_level = max(1, next_level_xp - prev_level_xp)
            pct = min(100.0, (cur_in_level / needed_in_level) * 100.0)
            return {
                "level": level,
                "current_xp": total_xp,
                "next_level_xp": next_level_xp,
                "xp_in_level": cur_in_level,
                "xp_needed": next_level_xp - total_xp,
                "progress_pct": round(pct, 1)
            }
        level += 1
        if level >= 150: # Safeguard
            return {
                "level": level,
                "current_xp": total_xp,
                "next_level_xp": total_xp + 1000,
                "xp_in_level": 1000,
                "xp_needed": 1000,
                "progress_pct": 100.0
            }

def get_hunter_rank(level):
    """Returns hunter rank metadata based on level."""
    current = HUNTER_RANKS[0]
    for r in HUNTER_RANKS:
        if level >= r["min_level"]:
            current = r
    return current

def calculate_hunter_attributes(daily_df, agentic_df=None, x0_df=None, dads_df=None):
    """
    Computes 5-Dimensional Solo Leveling Hunter Attributes:
    INT: Academics (Math, COOS, DSA, Python logic)
    STR: Raw Output & Code Volume (LOC, problems, features)
    PER: Perception & Depth (X-0 topics, hypotheses, experiments)
    AGI: Agility & Autonomous Systems (Agentic AI topics, deployments, bug fixes)
    VIT: Endurance & Vitality (Deep work hours & stamina)
    """
    if daily_df is None or len(daily_df) == 0:
        return {"INT": 10, "STR": 10, "PER": 10, "AGI": 10, "VIT": 10}

    # Raw sums
    m3_solved = daily_df["m3_solved"].sum() if "m3_solved" in daily_df.columns else 0
    coos = (daily_df["coos_numericals"].sum() + daily_df["coos_theory_learned"].sum()) if "coos_numericals" in daily_df.columns else 0
    dsa = (daily_df["dsa_problems"].sum() + daily_df["dsa_leetcode"].sum()) if "dsa_problems" in daily_df.columns else 0
    loc = daily_df["python_loc_written"].sum() if "python_loc_written" in daily_df.columns else 0
    tasks = daily_df["python_tasks"].sum() if "python_tasks" in daily_df.columns else 0
    
    agentic_learned = daily_df["agentic_topics_learned"].sum() if "agentic_topics_learned" in daily_df.columns else 0
    agentic_deploys = daily_df["agentic_deployments"].sum() if "agentic_deployments" in daily_df.columns else 0
    agentic_bugs = daily_df["agentic_bugs_fixed"].sum() if "agentic_bugs_fixed" in daily_df.columns else 0
    
    x0_learned = daily_df["x0_topics_learned"].sum() if "x0_topics_learned" in daily_df.columns else 0
    x0_exp = daily_df["x0_experiments"].sum() if "x0_experiments" in daily_df.columns else 0
    x0_hyp = daily_df["x0_hypotheses"].sum() if "x0_hypotheses" in daily_df.columns else 0
    
    deep_work = daily_df["deep_work_hours"].sum() if "deep_work_hours" in daily_df.columns else 0

    # Base of 10 + log/linear scaled scores (0-100 scale for aesthetics)
    intel = 10 + int(min(90, (m3_solved * 0.4) + (coos * 0.5) + (dsa * 0.8) + (tasks * 0.5)))
    strength = 10 + int(min(90, (loc / 80.0) + (tasks * 1.5) + (m3_solved * 0.2)))
    perception = 10 + int(min(90, (x0_learned * 1.8) + (x0_exp * 3) + (x0_hyp * 2)))
    agility = 10 + int(min(90, (agentic_learned * 1.8) + (agentic_deploys * 5) + (agentic_bugs * 2)))
    vitality = 10 + int(min(90, deep_work * 2.2))

    return {
        "INT": max(10, min(100, intel)),
        "STR": max(10, min(100, strength)),
        "PER": max(10, min(100, perception)),
        "AGI": max(10, min(100, agility)),
        "VIT": max(10, min(100, vitality)),
    }

def calculate_hunter_profile(daily_df, agentic_df, x0_df, dads_df):
    """Aggregates all stats into a full Solo Leveling Hunter Profile."""
    total_xp = 0
    today_xp = 0
    
    today_str = str(date.today())
    today_row = None
    
    if daily_df is not None and len(daily_df) > 0:
        for _, row in daily_df.iterrows():
            row_xp = calculate_row_xp(row)
            total_xp += row_xp
            if str(row.get("dt")) == today_str:
                today_xp += row_xp
                today_row = row
        
        # If no entry for today, check last entered row for breakdown sample
        if today_row is None:
            today_row = daily_df.iloc[-1]
            today_xp = calculate_row_xp(today_row)

    lvl_info = calculate_level_from_xp(total_xp)
    rank_info = get_hunter_rank(lvl_info["level"])
    stats = calculate_hunter_attributes(daily_df, agentic_df, x0_df, dads_df)
    streak = calculate_streak(daily_df)
    
    # Calculate Winter Arc day (Oct 1 to Dec 31)
    start_date = date(2026, 10, 1)
    end_date = date(2026, 12, 31)
    today = date.today()
    total_days = (end_date - start_date).days + 1
    
    if today < start_date:
        day_num = 1
        days_left = total_days
        days_elapsed = 0
    elif today > end_date:
        day_num = total_days
        days_left = 0
        days_elapsed = total_days
    else:
        days_elapsed = (today - start_date).days + 1
        day_num = days_elapsed
        days_left = (end_date - today).days

    return {
        "level": lvl_info["level"],
        "rank": rank_info["rank"],
        "tier": rank_info["tier"],
        "rank_color": rank_info["color"],
        "rank_badge": rank_info["badge"],
        "rank_glow": rank_info["glow"],
        "total_xp": total_xp,
        "today_xp": today_xp,
        "next_level_xp": lvl_info["next_level_xp"],
        "xp_needed": lvl_info["xp_needed"],
        "progress_pct": lvl_info["progress_pct"],
        "streak": streak,
        "day_num": day_num,
        "total_days": total_days,
        "days_left": days_left,
        "days_elapsed": days_elapsed,
        "stats": stats,
        "today_row": today_row
    }

def evaluate_daily_quests(daily_row):
    """Evaluates completion of the daily quest objectives for a given daily row."""
    if daily_row is None:
        r = {}
    elif isinstance(daily_row, pd.Series):
        r = daily_row.to_dict()
    else:
        r = daily_row

    quests = []
    completed_count = 0
    
    for q in DEFAULT_DAILY_QUESTS:
        target = q["target"]
        if q["col"] == "topics_combo":
            actual = r.get("agentic_topics_learned", 0) + r.get("agentic_topics_deepened", 0) + r.get("x0_topics_learned", 0) + r.get("x0_topics_deepened", 0)
        elif q["col"] == "dsa_problems":
            actual = r.get("dsa_problems", 0) + r.get("dsa_leetcode", 0)
        else:
            actual = r.get(q["col"], 0)
            
        try:
            actual = float(actual)
        except Exception:
            actual = 0.0

        pct = min(100.0, (actual / target) * 100.0) if target > 0 else 100.0
        is_done = actual >= target
        if is_done:
            completed_count += 1
            
        quests.append({
            "key": q["key"],
            "title": q["title"],
            "domain": q["domain"],
            "icon": q["icon"],
            "target": target,
            "actual": actual,
            "unit": q["unit"],
            "completed": is_done,
            "progress_pct": round(pct, 1)
        })

    all_completed = (completed_count == len(DEFAULT_DAILY_QUESTS)) and len(DEFAULT_DAILY_QUESTS) > 0
    completion_pct = round((completed_count / len(DEFAULT_DAILY_QUESTS)) * 100.0, 1) if quests else 0.0

    return {
        "quests": quests,
        "completed_count": completed_count,
        "total_count": len(DEFAULT_DAILY_QUESTS),
        "completion_pct": completion_pct,
        "all_completed": all_completed,
    }

def evaluate_achievements(daily_df, agentic_df, x0_df, dads_df):
    """Evaluates all hunter achievements against database stats."""
    results = []
    unlocked_count = 0
    total_achievement_xp = 0
    
    for ach in ACHIEVEMENTS_LIST:
        try:
            unlocked = ach["check"](daily_df, agentic_df, x0_df, dads_df)
            prog = ach["progress"](daily_df, agentic_df, x0_df, dads_df)
        except Exception:
            unlocked = False
            prog = 0.0

        prog_pct = round(min(100.0, max(0.0, prog * 100.0)), 1)
        if unlocked:
            unlocked_count += 1
            total_achievement_xp += ach["xp_reward"]
            
        results.append({
            "id": ach["id"],
            "title": ach["title"],
            "desc": ach["desc"],
            "category": ach["category"],
            "icon": ach["icon"],
            "rarity": ach["rarity"],
            "xp_reward": ach["xp_reward"],
            "unlocked": unlocked,
            "progress_pct": prog_pct
        })
        
    return {
        "achievements": results,
        "unlocked_count": unlocked_count,
        "total_count": len(ACHIEVEMENTS_LIST),
        "pct_unlocked": round((unlocked_count / len(ACHIEVEMENTS_LIST)) * 100.0, 1),
        "total_achievement_xp": total_achievement_xp
    }
