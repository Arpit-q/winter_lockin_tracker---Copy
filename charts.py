"""
Solo Leveling Visual Charts & Analytics Module
Provides custom styled dark futuristic Plotly charts and visual indicators.
Signature Theme: Electric Blue (#00d2ff) & Deep Purple (#7c3aed / #9333ea) on Pitch Black and Charcoal.
Fonts: Michroma (Geometric Futuristic Sci-Fi Sans) & Plus Jakarta Sans (Clean Modern Rounded Sans).
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Solo Leveling Anime Power & Aura Palette
SL_ELECTRIC_BLUE = "#00d2ff"
SL_ELECTRIC_CYAN = "#38e1ff"
SL_DEEP_PURPLE = "#7c3aed"
SL_ROYAL_PURPLE = "#9333ea"
SL_SHADOW_PURPLE = "#6d28d9"
SL_VIOLET_AURA = "#a855f7"
SL_EMERALD_CLEARED = "#10b981"
SL_GOLD_RANK = "#fbbf24"
SL_ROSE_CALAMITY = "#f43f5e"

DARK_BG = "rgba(9, 13, 22, 0.85)"
BORDER_COLOR = "rgba(0, 210, 255, 0.3)"

PALETTE = [
    SL_ELECTRIC_BLUE,
    SL_DEEP_PURPLE,
    SL_ELECTRIC_CYAN,
    SL_ROYAL_PURPLE,
    SL_VIOLET_AURA,
    SL_EMERALD_CLEARED,
    SL_GOLD_RANK,
    SL_ROSE_CALAMITY,
    "#60a5fa",
    "#c084fc"
]

def apply_hunter_theme(fig, title="", height=360):
    """Applies authentic Solo Leveling Anime HUD styling to any Plotly figure."""
    fig.update_layout(
        title={
            "text": f"<b>{title}</b>" if title else "",
            "font": {"size": 13, "color": "#f1f5f9", "family": "Michroma, Chakra Petch, sans-serif"},
            "x": 0.02,
            "xanchor": "left"
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin={"l": 25, "r": 25, "t": 48 if title else 20, "b": 25},
        font={"color": "#94a3b8", "family": "Plus Jakarta Sans, sans-serif", "size": 12},
        legend={
            "font": {"color": "#cbd5e1", "family": "Plus Jakarta Sans, sans-serif", "size": 11},
            "bgcolor": "rgba(9, 13, 22, 0.75)",
            "bordercolor": "rgba(0, 210, 255, 0.25)",
            "borderwidth": 1
        },
        hoverlabel={
            "bgcolor": "#070a11",
            "bordercolor": SL_ELECTRIC_BLUE,
            "font": {"color": "#ffffff", "family": "Plus Jakarta Sans, sans-serif"}
        }
    )
    return fig

def create_radar_stat_chart(stats_dict):
    """Generates 5-Dimensional Solo Leveling Hunter Stat Polygon."""
    categories = ["INT (Academics)", "STR (Execution)", "PER (Research)", "AGI (Agentic AI)", "VIT (Stamina)"]
    values = [
        stats_dict.get("INT", 10),
        stats_dict.get("STR", 10),
        stats_dict.get("PER", 10),
        stats_dict.get("AGI", 10),
        stats_dict.get("VIT", 10),
    ]
    # Close the polygon loop
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure()
    
    # Outer baseline max 100 ring
    fig.add_trace(go.Scatterpolar(
        r=[100]*6,
        theta=categories,
        mode="lines",
        line=dict(color="rgba(255,255,255,0.08)", width=1, dash="dot"),
        hoverinfo="none",
        showlegend=False
    ))
    
    # Hunter Current Stats with Electric Blue Aura & Deep Purple Nodes
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill="toself",
        fillcolor="rgba(0, 210, 255, 0.22)",
        line=dict(color=SL_ELECTRIC_BLUE, width=2.5),
        marker=dict(size=8, color=SL_DEEP_PURPLE, symbol="diamond", line=dict(color=SL_ELECTRIC_CYAN, width=1.5)),
        name="Hunter Stats"
    ))

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(8, 12, 20, 0.6)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                linecolor="rgba(255, 255, 255, 0.12)",
                gridcolor="rgba(0, 210, 255, 0.18)"
            ),
            angularaxis=dict(
                linecolor="rgba(0, 210, 255, 0.3)",
                gridcolor="rgba(124, 58, 237, 0.15)",
                tickfont=dict(size=10, color=SL_ELECTRIC_CYAN, family="Michroma, Chakra Petch, sans-serif")
            )
        ),
        showlegend=False
    )
    return apply_hunter_theme(fig, "HUNTER ATTRIBUTE RADAR (5-D RADAR)", height=350)

def create_effort_pie_chart(daily_df):
    """Donut chart showing cumulative distribution of output across core tracks."""
    if daily_df is None or len(daily_df) == 0:
        labels = ["No Data Logged Yet"]
        values = [1]
        fig = px.pie(names=labels, values=values, hole=0.55, color_discrete_sequence=["#1e293b"])
        return apply_hunter_theme(fig, "DOMAIN OUTPUT DISTRIBUTION", height=320)

    # Compute domain output metrics
    acad_weight = (daily_df["m3_solved"].sum() if "m3_solved" in daily_df.columns else 0) + \
                  (daily_df["coos_numericals"].sum() if "coos_numericals" in daily_df.columns else 0) + \
                  (daily_df["dsa_problems"].sum() if "dsa_problems" in daily_df.columns else 0) + \
                  ((daily_df["python_loc_written"].sum() / 50.0) if "python_loc_written" in daily_df.columns else 0)
    agentic_weight = ((daily_df["agentic_topics_learned"].sum() * 5) if "agentic_topics_learned" in daily_df.columns else 0) + \
                     ((daily_df["agentic_deployments"].sum() * 10) if "agentic_deployments" in daily_df.columns else 0) + \
                     (daily_df["agentic_bugs_fixed"].sum() if "agentic_bugs_fixed" in daily_df.columns else 0)
    x0_weight = ((daily_df["x0_topics_learned"].sum() * 5) if "x0_topics_learned" in daily_df.columns else 0) + \
                ((daily_df["x0_experiments"].sum() * 8) if "x0_experiments" in daily_df.columns else 0) + \
                ((daily_df["x0_hypotheses"].sum() * 6) if "x0_hypotheses" in daily_df.columns else 0)
    deep_work_weight = (daily_df["deep_work_hours"].sum() * 5) if "deep_work_hours" in daily_df.columns else 0

    data = {
        "Academics (INT)": max(0, acad_weight),
        "Agentic AI (AGI)": max(0, agentic_weight),
        "ML Project X-0 (PER)": max(0, x0_weight),
        "Deep Work (VIT)": max(0, deep_work_weight)
    }

    # Filter zero values if at least one nonzero exists
    nonzero_data = {k: v for k, v in data.items() if v > 0}
    if not nonzero_data:
        nonzero_data = {"Awaiting Daily Grind": 1}

    df = pd.DataFrame({"Domain": list(nonzero_data.keys()), "Weight": list(nonzero_data.values())})
    
    fig = px.pie(
        df,
        names="Domain",
        values="Weight",
        hole=0.55,
        color_discrete_sequence=PALETTE
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hoverinfo="label+percent+value",
        marker=dict(line=dict(color="#060910", width=2))
    )
    return apply_hunter_theme(fig, "TOTAL WINTER ARC OUTPUT SPLIT", height=320)

def create_academic_pie_chart(daily_df):
    """Donut chart for Academic problem solving breakdown."""
    if daily_df is None or len(daily_df) == 0:
        fig = px.pie(names=["No Data"], values=[1], hole=0.55, color_discrete_sequence=["#1e293b"])
        return apply_hunter_theme(fig, "ACADEMIC SUBJECT ALLOCATION", height=320)

    m3 = daily_df["m3_solved"].sum()
    coos = daily_df["coos_numericals"].sum() + daily_df["coos_practicals"].sum()
    py = daily_df["python_tasks"].sum()
    dsa = daily_df["dsa_problems"].sum() + daily_df["dsa_leetcode"].sum()
    uhv = daily_df["uhv_learned"].sum()

    data = {
        "Mathematics III": m3,
        "COOS": coos,
        "Python Tasks": py,
        "DSA / LeetCode": dsa,
        "UHV-II": uhv
    }
    nonzero = {k: v for k, v in data.items() if v > 0}
    if not nonzero:
        nonzero = {"Pending First Session": 1}

    df = pd.DataFrame({"Subject": list(nonzero.keys()), "Count": list(nonzero.values())})
    fig = px.pie(
        df,
        names="Subject",
        values="Count",
        hole=0.55,
        color_discrete_sequence=[SL_ELECTRIC_BLUE, SL_DEEP_PURPLE, SL_EMERALD_CLEARED, SL_GOLD_RANK, SL_ROSE_CALAMITY]
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(line=dict(color="#060910", width=2))
    )
    return apply_hunter_theme(fig, "ACADEMIC SUBJECT PROBLEM SPLIT", height=320)

def create_daily_quest_donut(completed, total):
    """Donut chart indicating daily quest completion with glowing center."""
    remaining = max(0, total - completed)
    pct = round((completed / total) * 100) if total > 0 else 0
    
    labels = ["Completed", "Remaining"]
    values = [completed, remaining]
    colors = [SL_EMERALD_CLEARED if pct == 100 else SL_ELECTRIC_BLUE, "rgba(255, 255, 255, 0.08)"]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.68,
        sort=False,
        marker=dict(colors=colors, line=dict(color="#060910", width=2)),
        textinfo="none",
        hoverinfo="label+value"
    )])

    # Add central indicator in Michroma font
    fig.add_annotation(
        text=f"<b>{pct}%</b><br><span style='font-size:10px;color:#94a3b8;letter-spacing:1px;'>CLEARED</span>",
        x=0.5, y=0.5,
        font=dict(size=18, color=SL_EMERALD_CLEARED if pct == 100 else "#ffffff", family="Michroma, Plus Jakarta Sans, sans-serif"),
        showarrow=False
    )

    fig.update_layout(showlegend=False)
    return apply_hunter_theme(fig, "DAILY QUEST COMPLETION", height=240)

def create_today_xp_pie(breakdown_dict):
    """Pie chart showing breakdown of XP gained today."""
    nonzero = {k: v for k, v in breakdown_dict.items() if v > 0}
    if not nonzero:
        nonzero = {"No XP Earned Yet": 1}

    df = pd.DataFrame({"Source": list(nonzero.keys()), "XP": list(nonzero.values())})
    fig = px.pie(
        df,
        names="Source",
        values="XP",
        hole=0.52,
        color_discrete_sequence=[SL_ELECTRIC_BLUE, SL_DEEP_PURPLE, SL_ELECTRIC_CYAN, SL_ROYAL_PURPLE, SL_GOLD_RANK, SL_EMERALD_CLEARED]
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(line=dict(color="#060910", width=2))
    )
    return apply_hunter_theme(fig, "TODAY'S EXP FORGE BREAKDOWN", height=300)

def create_skill_depth_pie(agentic_df, x0_df):
    """Pie chart showing distribution of depth (0-5) across topics."""
    depth_counts = {f"Depth {i} ({'Master' if i==5 else 'Expert' if i==4 else 'Adept' if i==3 else 'Apprentice' if i==2 else 'Novice' if i==1 else 'Unstarted'})": 0 for i in range(6)}
    
    if agentic_df is not None and len(agentic_df) > 0 and "current_depth" in agentic_df.columns:
        for d, count in agentic_df["current_depth"].value_counts().items():
            if 0 <= d <= 5:
                key = list(depth_counts.keys())[int(d)]
                depth_counts[key] += int(count)

    if x0_df is not None and len(x0_df) > 0 and "current_depth" in x0_df.columns:
        for d, count in x0_df["current_depth"].value_counts().items():
            if 0 <= d <= 5:
                key = list(depth_counts.keys())[int(d)]
                depth_counts[key] += int(count)

    nonzero = {k: v for k, v in depth_counts.items() if v > 0}
    if not nonzero:
        nonzero = {"Depth 0 (Unstarted)": 1}

    df = pd.DataFrame({"Depth": list(nonzero.keys()), "Topics": list(nonzero.values())})
    fig = px.pie(
        df,
        names="Depth",
        values="Topics",
        hole=0.52,
        color_discrete_sequence=["#334155", "#38bdf8", "#818cf8", "#a855f7", "#fbbf24", "#10b981"]
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(line=dict(color="#060910", width=2))
    )
    return apply_hunter_theme(fig, "SKILL DEPTH MASTERY (AGENTIC + X-0)", height=320)

def create_task_type_donut(daily_df):
    """Donut chart for functional task output types."""
    if daily_df is None or len(daily_df) == 0:
        fig = px.pie(names=["No Data"], values=[1], hole=0.55, color_discrete_sequence=["#1e293b"])
        return apply_hunter_theme(fig, "TASK TYPE FOCUS", height=320)

    code_units = ((daily_df["python_loc_written"].sum() / 20.0) if "python_loc_written" in daily_df.columns else 0) + \
                 ((daily_df["python_tasks"].sum() * 5) if "python_tasks" in daily_df.columns else 0)
    problem_solving = (daily_df["m3_solved"].sum() if "m3_solved" in daily_df.columns else 0) + \
                      (daily_df["coos_numericals"].sum() if "coos_numericals" in daily_df.columns else 0) + \
                      (daily_df["dsa_problems"].sum() if "dsa_problems" in daily_df.columns else 0)
    theory_topics = (
        (daily_df["agentic_topics_learned"].sum() if "agentic_topics_learned" in daily_df.columns else 0) + 
        (daily_df["x0_topics_learned"].sum() if "x0_topics_learned" in daily_df.columns else 0) + 
        (daily_df["coos_theory_learned"].sum() if "coos_theory_learned" in daily_df.columns else 0) + 
        (daily_df["uhv_learned"].sum() if "uhv_learned" in daily_df.columns else 0)
    )
    deep_work = (daily_df["deep_work_hours"].sum() * 5) if "deep_work_hours" in daily_df.columns else 0

    data = {
        "Code Shipped (LOC & Tasks)": max(0, code_units),
        "Problem Solving (Math & DSA)": max(0, problem_solving),
        "Theory & Research Topics": max(0, theory_topics),
        "Deep Work & Stamina": max(0, deep_work)
    }
    nonzero = {k: v for k, v in data.items() if v > 0}
    if not nonzero:
        nonzero = {"Awaiting Daily Input": 1}

    df = pd.DataFrame({"TaskType": list(nonzero.keys()), "Value": list(nonzero.values())})
    fig = px.pie(
        df,
        names="TaskType",
        values="Value",
        hole=0.55,
        color_discrete_sequence=[SL_ELECTRIC_BLUE, SL_DEEP_PURPLE, SL_GOLD_RANK, SL_EMERALD_CLEARED]
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(line=dict(color="#060910", width=2))
    )
    return apply_hunter_theme(fig, "FUNCTIONAL OUTPUT TYPE SPLIT", height=320)

def create_winter_arc_pace_gauge(days_elapsed, total_days, current_xp, target_xp=50000):
    """Gauge showing Winter Arc timeline progress vs EXP progress."""
    time_pct = min(100.0, (days_elapsed / total_days) * 100.0) if total_days > 0 else 0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_xp,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "<b>WINTER ARC LOCK-IN EXP GAUGE</b>", 'font': {'size': 13, 'color': '#f1f5f9', 'family': 'Michroma, sans-serif'}},
        delta={'reference': target_xp * (time_pct / 100.0), 'increasing': {'color': SL_EMERALD_CLEARED}, 'decreasing': {'color': SL_ROSE_CALAMITY}},
        gauge={
            'axis': {'range': [None, target_xp], 'tickcolor': "rgba(255,255,255,0.2)", 'tickwidth': 1},
            'bar': {'color': SL_ELECTRIC_BLUE, 'thickness': 0.3},
            'bgcolor': "rgba(8, 12, 20, 0.75)",
            'borderwidth': 1,
            'bordercolor': "rgba(0, 210, 255, 0.35)",
            'steps': [
                {'range': [0, target_xp * 0.4], 'color': 'rgba(0, 210, 255, 0.12)'},
                {'range': [target_xp * 0.4, target_xp * 0.8], 'color': 'rgba(56, 189, 248, 0.16)'},
                {'range': [target_xp * 0.8, target_xp], 'color': 'rgba(124, 58, 237, 0.25)'}
            ],
            'threshold': {
                'line': {'color': SL_GOLD_RANK, 'width': 3},
                'thickness': 0.8,
                'value': target_xp
            }
        }
    ))
    return apply_hunter_theme(fig, "", height=250)

def create_xp_cumulative_chart(daily_df, xp_calculator_func):
    """Cumulative EXP Area chart with Solo Leveling electric blue & deep purple aura aesthetic."""
    if daily_df is None or len(daily_df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No logs recorded yet. Start your daily grind!", showarrow=False, font=dict(color="#64748b"))
        return apply_hunter_theme(fig, "CUMULATIVE HUNTER EXP TRAJECTORY", height=320)

    df = daily_df.copy()
    df["Date"] = pd.to_datetime(df["dt"])
    df = df.sort_values("Date")
    
    df["daily_xp"] = df.apply(xp_calculator_func, axis=1)
    df["cum_xp"] = df["daily_xp"].cumsum()

    fig = go.Figure()
    
    # Area gradient fill
    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=df["cum_xp"],
        mode="lines+markers",
        name="Hunter EXP",
        line=dict(color=SL_ELECTRIC_BLUE, width=3),
        marker=dict(size=7, color=SL_DEEP_PURPLE, symbol="diamond-dot", line=dict(color="#ffffff", width=1)),
        fill="tozeroy",
        fillcolor="rgba(0, 210, 255, 0.14)"
    ))

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255, 255, 255, 0.06)",
        linecolor="rgba(0, 210, 255, 0.25)"
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255, 255, 255, 0.06)",
        linecolor="rgba(0, 210, 255, 0.25)",
        title="Total EXP"
    )

    return apply_hunter_theme(fig, "CUMULATIVE HUNTER EXP TRAJECTORY", height=320)

def create_weekly_output_comparison(daily_df):
    """Weekly aggregated multi-metric bar chart."""
    if daily_df is None or len(daily_df) < 1:
        fig = go.Figure()
        fig.add_annotation(text="Log at least 1 day to see weekly progression", showarrow=False, font=dict(color="#64748b"))
        return apply_hunter_theme(fig, "WEEKLY OUTPUT COMPARISON", height=320)

    df = daily_df.copy()
    df["Date"] = pd.to_datetime(df["dt"])
    df["Week"] = df["Date"].dt.to_period("W").astype(str)
    
    agg = df.groupby("Week").agg(
        Math_Solved=("m3_solved", "sum"),
        DSA_Problems=("dsa_problems", "sum"),
        Python_Tasks=("python_tasks", "sum"),
        Topics=("agentic_topics_learned", "sum")
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=agg["Week"], y=agg["Math_Solved"], name="Math Solved", marker_color=SL_ELECTRIC_BLUE))
    fig.add_trace(go.Bar(x=agg["Week"], y=agg["DSA_Problems"], name="DSA Problems", marker_color=SL_DEEP_PURPLE))
    fig.add_trace(go.Bar(x=agg["Week"], y=agg["Python_Tasks"], name="Python Tasks", marker_color=SL_EMERALD_CLEARED))
    fig.add_trace(go.Bar(x=agg["Week"], y=agg["Topics"], name="Topics Learned", marker_color=SL_GOLD_RANK))

    fig.update_layout(barmode="group")
    fig.update_xaxes(showgrid=False, linecolor="rgba(0, 210, 255, 0.2)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255, 255, 255, 0.06)", linecolor="rgba(0, 210, 255, 0.2)")

    return apply_hunter_theme(fig, "WEEKLY CORE METRICS COMPARISON", height=320)
