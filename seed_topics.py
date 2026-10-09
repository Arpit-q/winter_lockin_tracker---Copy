"""
Curriculum and Sample Data Seeder for Winter Arc Command Center
Seeds realistic Agentic AI topics, X-0 ML topics, and optional sample lock-in history.
"""
from datetime import date, timedelta
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "winter_lockin.db"

AGENTIC_CURRICULUM = [
    ("A01-01", "LLM Foundations & Prompt Engineering", 1, "Core", "High", 3, 3, "Mastered"),
    ("A01-02", "Context Window Management & Chunking", 1, "Core", "High", 3, 3, "Mastered"),
    ("A01-03", "Structured Outputs & JSON Schema Validation", 1, "Core", "High", 3, 2, "In progress"),
    ("A02-01", "Vector Databases & Dense Embeddings", 2, "RAG", "High", 3, 2, "In progress"),
    ("A02-02", "Hybrid Search & Re-ranking Strategies", 2, "RAG", "Medium", 3, 1, "In progress"),
    ("A02-03", "RAG Evaluation Frameworks (Ragas / TruLens)", 2, "RAG", "Medium", 3, 1, "In progress"),
    ("A03-01", "Tool Definition & Function Calling APIs", 3, "Tool Use", "High", 4, 2, "In progress"),
    ("A03-02", "Safe Tool Execution & Sandbox Environments", 3, "Tool Use", "Medium", 3, 1, "In progress"),
    ("A04-01", "ReAct Framework & Observation Loops", 4, "Reasoning", "High", 4, 1, "In progress"),
    ("A04-02", "Self-Consistency & Chain-of-Thought", 4, "Reasoning", "Medium", 3, 1, "In progress"),
    ("A05-01", "Memory Systems: Short-term vs Long-term", 5, "Architecture", "High", 4, 0, "Not started"),
    ("A05-02", "State Management & Checkpointing (LangGraph)", 5, "Architecture", "High", 4, 0, "Not started"),
    ("A06-01", "Multi-Agent Collaboration & Supervisor Pattern", 6, "Multi-Agent", "High", 4, 0, "Not started"),
    ("A06-02", "Subagent Delegation & Consensus Protocols", 6, "Multi-Agent", "Medium", 3, 0, "Not started"),
    ("A07-01", "Agent Observability (Langfuse / Phoenix)", 7, "Production", "High", 3, 0, "Not started"),
    ("A07-02", "Latency & Token Cost Optimization", 7, "Production", "High", 3, 0, "Not started"),
    ("A08-01", "Local Model Serving (vLLM / Ollama)", 8, "Deployment", "Medium", 3, 0, "Not started"),
    ("A08-02", "Model Quantization (GGUF, AWQ, EXL2)", 8, "Deployment", "Medium", 3, 0, "Not started"),
    ("A09-01", "Autonomous Coding Agent Workflows", 9, "Autonomous", "High", 5, 0, "Not started"),
    ("A09-02", "Self-Healing Test & Debug Loops", 9, "Autonomous", "High", 5, 0, "Not started"),
]

X0_CURRICULUM = [
    ("X0-001", "Matrix Decompositions (SVD & Eigendecomposition)", "0", "Math", "High", 4, 3, "In progress"),
    ("X0-002", "Multivariate Calculus & Jacobians/Hessians", "0", "Math", "High", 4, 3, "In progress"),
    ("X0-003", "Probability Distributions & Maximum Likelihood", "0", "Math", "High", 3, 2, "In progress"),
    ("X0-004", "Convex Optimization & Gradient Descent Variants", "0", "Optimization", "High", 4, 3, "In progress"),
    ("X0-005", "Loss Surfaces, Saddles & Momentum Dynamics", "0", "Optimization", "Medium", 3, 2, "In progress"),
    ("X0-006", "PyTorch Tensor Internals & Autograd Engine", "0", "Deep Learning", "High", 4, 3, "In progress"),
    ("X0-007", "Custom Autograd Functions & Memory Layouts", "0", "Deep Learning", "Medium", 3, 2, "In progress"),
    ("X0-008", "Scaled Dot-Product Attention Implementation", "0", "Transformers", "High", 5, 3, "In progress"),
    ("X0-009", "Multi-Head & Grouped-Query Attention (GQA)", "0", "Transformers", "High", 5, 2, "In progress"),
    ("X0-010", "RoPE (Rotary Position Embeddings) Derivation", "0", "Transformers", "High", 4, 2, "In progress"),
    ("X0-011", "FlashAttention & GPU SRAM Tiling Concepts", "0", "Transformers", "High", 4, 1, "In progress"),
    ("X0-012", "LayerNorm vs RMSNorm & Residual Connections", "0", "Transformers", "Medium", 3, 2, "In progress"),
    ("X0-013", "BPE & SentencePiece Tokenizer Implementation", "0", "NLP", "Medium", 3, 2, "In progress"),
    ("X0-014", "Pretraining Loss Formulations & Perplexity", "0", "Training", "High", 4, 1, "In progress"),
    ("X0-015", "Cosine Annealing with Warmup Schedules", "0", "Training", "Medium", 3, 2, "In progress"),
    ("X0-016", "LoRA (Low-Rank Adaptation) Matrix Mechanics", "0", "Fine-Tuning", "High", 4, 2, "In progress"),
    ("X0-017", "QLoRA & 4-Bit NormalFloat Quantization", "0", "Fine-Tuning", "High", 4, 1, "In progress"),
    ("X0-018", "DPO (Direct Preference Optimization) Mathematics", "0", "Alignment", "High", 4, 1, "In progress"),
    ("X0-019", "KV Cache Architecture & PagedAttention", "0", "Inference", "High", 4, 1, "In progress"),
    ("X0-020", "Speculative Decoding & Draft Models", "0", "Inference", "Medium", 3, 0, "Not started"),
]

def seed_topics_master(con=None):
    close_con = False
    if con is None:
        con = sqlite3.connect(DB_PATH)
        close_con = True
    cur = con.cursor()
    
    for row in AGENTIC_CURRICULUM:
        cur.execute("""
            INSERT OR REPLACE INTO agentic_topics(
                topic_id, topic, phase, category, importance, target_depth, current_depth, status
            ) VALUES(?,?,?,?,?,?,?,?)
        """, row)

    for row in X0_CURRICULUM:
        cur.execute("""
            INSERT OR REPLACE INTO x0_topics(
                topic_id, topic, phase, category, importance, target_depth, current_depth, status
            ) VALUES(?,?,?,?,?,?,?,?)
        """, row)

    con.commit()
    if close_con:
        con.close()
    return len(AGENTIC_CURRICULUM), len(X0_CURRICULUM)

def seed_sample_daily_logs(con=None):
    """Inserts a realistic 7-day Winter Arc Lock-In sequence to showcase leveling, pie charts, and growth."""
    close_con = False
    if con is None:
        con = sqlite3.connect(DB_PATH)
        close_con = True
    cur = con.cursor()

    # Clear existing daily logs for clean demonstration
    cur.execute("DELETE FROM daily_log")
    
    # 7 consecutive days of lock-in grind leading up to today
    today = date.today()
    start_date = today - timedelta(days=6)
    
    sample_records = [
        # Day 1: Awakening
        {
            "dt": str(start_date),
            "m3_attempted": 12, "m3_solved": 10, "m3_correct": 9, "m3_chapter": "Linear Differential Equations", "m3_topic": "Cauchy-Euler Equations",
            "coos_numericals": 6, "coos_correct": 5, "coos_theory_learned": 3, "coos_theory_revised": 2, "coos_practicals": 1,
            "python_tasks": 2, "python_loc_written": 240, "python_loc_read": 500, "python_topics_learned": 2, "python_topics_applied": 2,
            "dsa_theory": 2, "dsa_problems": 4, "dsa_leetcode": 2, "dsa_java_impl": 2, "dsa_revision": 1,
            "uhv_learned": 1, "uhv_revised": 0,
            "agency_prospects": 0, "agency_contacted": 0, "agency_outreach": 0, "agency_followups": 0,
            "agency_replies": 0, "agency_conversations": 0, "agency_calls": 0, "agency_proposals": 0, "agency_deals": 0,
            "agency_new_mrr": 0.0, "agency_current_mrr": 0.0,
            "linkedin_posts": 1, "instagram_posts": 0, "other_content": 0,
            "agentic_topics_learned": 1, "agentic_topics_revised": 0, "agentic_topics_deepened": 1,
            "agentic_requirements_solved": 1, "agentic_projects": 0, "agentic_features": 1, "agentic_deployments": 0,
            "agentic_bugs_fixed": 2, "agentic_capabilities": 1,
            "x0_topics_learned": 2, "x0_topics_revised": 1, "x0_topics_deepened": 1,
            "x0_experiments": 1, "x0_hypotheses": 1, "x0_questions_resolved": 1, "x0_sources": 3, "x0_milestones": 0,
            "dads_investigated": 0, "dads_implementing": 0, "dads_improved": 0, "dads_independent": 0,
            "dads_tech_impl": 0, "dads_tech_knowledge": 0.0, "dads_ops_knowledge": 0.0,
            "deep_work_hours": 3.5, "notes": "Day 1 of Winter Arc. Locked in hard."
        },
        # Day 2
        {
            "dt": str(start_date + timedelta(days=1)),
            "m3_attempted": 15, "m3_solved": 14, "m3_correct": 13, "m3_chapter": "Linear Differential Equations", "m3_topic": "Method of Variation of Parameters",
            "coos_numericals": 8, "coos_correct": 7, "coos_theory_learned": 2, "coos_theory_revised": 1, "coos_practicals": 1,
            "python_tasks": 3, "python_loc_written": 380, "python_loc_read": 700, "python_topics_learned": 2, "python_topics_applied": 2,
            "dsa_theory": 1, "dsa_problems": 5, "dsa_leetcode": 3, "dsa_java_impl": 2, "dsa_revision": 2,
            "uhv_learned": 1, "uhv_revised": 1,
            "agency_prospects": 0, "agency_contacted": 0, "agency_outreach": 0, "agency_followups": 0,
            "agency_replies": 0, "agency_conversations": 0, "agency_calls": 0, "agency_proposals": 0, "agency_deals": 0,
            "agency_new_mrr": 0.0, "agency_current_mrr": 0.0,
            "linkedin_posts": 1, "instagram_posts": 1, "other_content": 0,
            "agentic_topics_learned": 2, "agentic_topics_revised": 1, "agentic_topics_deepened": 1,
            "agentic_requirements_solved": 2, "agentic_projects": 0, "agentic_features": 2, "agentic_deployments": 1,
            "agentic_bugs_fixed": 3, "agentic_capabilities": 2,
            "x0_topics_learned": 2, "x0_topics_revised": 1, "x0_topics_deepened": 1,
            "x0_experiments": 2, "x0_hypotheses": 1, "x0_questions_resolved": 2, "x0_sources": 4, "x0_milestones": 1,
            "dads_investigated": 0, "dads_implementing": 0, "dads_improved": 0, "dads_independent": 0,
            "dads_tech_impl": 0, "dads_tech_knowledge": 0.0, "dads_ops_knowledge": 0.0,
            "deep_work_hours": 4.5, "notes": "Momentum building. Math pace is solid."
        },
        # Day 3
        {
            "dt": str(start_date + timedelta(days=2)),
            "m3_attempted": 18, "m3_solved": 16, "m3_correct": 15, "m3_chapter": "Partial Differential Equations", "m3_topic": "Lagrange Linear PDE",
            "coos_numericals": 10, "coos_correct": 9, "coos_theory_learned": 2, "coos_theory_revised": 2, "coos_practicals": 1,
            "python_tasks": 3, "python_loc_written": 420, "python_loc_read": 600, "python_topics_learned": 1, "python_topics_applied": 2,
            "dsa_theory": 2, "dsa_problems": 6, "dsa_leetcode": 4, "dsa_java_impl": 3, "dsa_revision": 2,
            "uhv_learned": 0, "uhv_revised": 1,
            "agency_prospects": 0, "agency_contacted": 0, "agency_outreach": 0, "agency_followups": 0,
            "agency_replies": 0, "agency_conversations": 0, "agency_calls": 0, "agency_proposals": 0, "agency_deals": 0,
            "agency_new_mrr": 0.0, "agency_current_mrr": 0.0,
            "linkedin_posts": 1, "instagram_posts": 0, "other_content": 1,
            "agentic_topics_learned": 1, "agentic_topics_revised": 2, "agentic_topics_deepened": 2,
            "agentic_requirements_solved": 2, "agentic_projects": 1, "agentic_features": 3, "agentic_deployments": 1,
            "agentic_bugs_fixed": 1, "agentic_capabilities": 2,
            "x0_topics_learned": 1, "x0_topics_revised": 2, "x0_topics_deepened": 2,
            "x0_experiments": 1, "x0_hypotheses": 2, "x0_questions_resolved": 2, "x0_sources": 2, "x0_milestones": 0,
            "dads_investigated": 0, "dads_implementing": 0, "dads_improved": 0, "dads_independent": 0,
            "dads_tech_impl": 0, "dads_tech_knowledge": 0.0, "dads_ops_knowledge": 0.0,
            "deep_work_hours": 5.0, "notes": "First Agentic mini-project shipped."
        },
        # Day 4: Deep focus sprint
        {
            "dt": str(start_date + timedelta(days=3)),
            "m3_attempted": 12, "m3_solved": 11, "m3_correct": 10, "m3_chapter": "Partial Differential Equations", "m3_topic": "Charpit's Method",
            "coos_numericals": 7, "coos_correct": 6, "coos_theory_learned": 2, "coos_theory_revised": 1, "coos_practicals": 0,
            "python_tasks": 4, "python_loc_written": 550, "python_loc_read": 800, "python_topics_learned": 2, "python_topics_applied": 3,
            "dsa_theory": 1, "dsa_problems": 5, "dsa_leetcode": 3, "dsa_java_impl": 3, "dsa_revision": 1,
            "uhv_learned": 1, "uhv_revised": 0,
            "agency_prospects": 0, "agency_contacted": 0, "agency_outreach": 0, "agency_followups": 0,
            "agency_replies": 0, "agency_conversations": 0, "agency_calls": 0, "agency_proposals": 0, "agency_deals": 0,
            "agency_new_mrr": 0.0, "agency_current_mrr": 0.0,
            "linkedin_posts": 1, "instagram_posts": 1, "other_content": 0,
            "agentic_topics_learned": 2, "agentic_topics_revised": 1, "agentic_topics_deepened": 1,
            "agentic_requirements_solved": 3, "agentic_projects": 0, "agentic_features": 2, "agentic_deployments": 1,
            "agentic_bugs_fixed": 4, "agentic_capabilities": 2,
            "x0_topics_learned": 2, "x0_topics_revised": 1, "x0_topics_deepened": 1,
            "x0_experiments": 2, "x0_hypotheses": 1, "x0_questions_resolved": 1, "x0_sources": 3, "x0_milestones": 1,
            "dads_investigated": 0, "dads_implementing": 0, "dads_improved": 0, "dads_independent": 0,
            "dads_tech_impl": 0, "dads_tech_knowledge": 0.0, "dads_ops_knowledge": 0.0,
            "deep_work_hours": 6.0, "notes": "Deep focus sprint. Agentic workflow deployed."
        },
        # Day 5
        {
            "dt": str(start_date + timedelta(days=4)),
            "m3_attempted": 20, "m3_solved": 18, "m3_correct": 17, "m3_chapter": "Vector Calculus", "m3_topic": "Gradient, Divergence & Curl",
            "coos_numericals": 9, "coos_correct": 8, "coos_theory_learned": 3, "coos_theory_revised": 2, "coos_practicals": 2,
            "python_tasks": 3, "python_loc_written": 480, "python_loc_read": 650, "python_topics_learned": 2, "python_topics_applied": 2,
            "dsa_theory": 2, "dsa_problems": 7, "dsa_leetcode": 5, "dsa_java_impl": 3, "dsa_revision": 2,
            "uhv_learned": 1, "uhv_revised": 1,
            "agency_prospects": 0, "agency_contacted": 0, "agency_outreach": 0, "agency_followups": 0,
            "agency_replies": 0, "agency_conversations": 0, "agency_calls": 0, "agency_proposals": 0, "agency_deals": 0,
            "agency_new_mrr": 0.0, "agency_current_mrr": 0.0,
            "linkedin_posts": 1, "instagram_posts": 0, "other_content": 0,
            "agentic_topics_learned": 2, "agentic_topics_revised": 2, "agentic_topics_deepened": 2,
            "agentic_requirements_solved": 2, "agentic_projects": 0, "agentic_features": 3, "agentic_deployments": 1,
            "agentic_bugs_fixed": 2, "agentic_capabilities": 3,
            "x0_topics_learned": 2, "x0_topics_revised": 2, "x0_topics_deepened": 2,
            "x0_experiments": 2, "x0_hypotheses": 2, "x0_questions_resolved": 3, "x0_sources": 4, "x0_milestones": 1,
            "dads_investigated": 0, "dads_implementing": 0, "dads_improved": 0, "dads_independent": 0,
            "dads_tech_impl": 0, "dads_tech_knowledge": 0.0, "dads_ops_knowledge": 0.0,
            "deep_work_hours": 5.5, "notes": "Strong focus across all subjects."
        },
        # Day 6
        {
            "dt": str(start_date + timedelta(days=5)),
            "m3_attempted": 22, "m3_solved": 20, "m3_correct": 19, "m3_chapter": "Vector Calculus", "m3_topic": "Green's and Gauss Theorems",
            "coos_numericals": 12, "coos_correct": 11, "coos_theory_learned": 3, "coos_theory_revised": 2, "coos_practicals": 1,
            "python_tasks": 4, "python_loc_written": 620, "python_loc_read": 900, "python_topics_learned": 2, "python_topics_applied": 3,
            "dsa_theory": 2, "dsa_problems": 8, "dsa_leetcode": 5, "dsa_java_impl": 4, "dsa_revision": 2,
            "uhv_learned": 1, "uhv_revised": 1,
            "agency_prospects": 0, "agency_contacted": 0, "agency_outreach": 0, "agency_followups": 0,
            "agency_replies": 0, "agency_conversations": 0, "agency_calls": 0, "agency_proposals": 0, "agency_deals": 0,
            "agency_new_mrr": 0.0, "agency_current_mrr": 0.0,
            "linkedin_posts": 2, "instagram_posts": 1, "other_content": 1,
            "agentic_topics_learned": 3, "agentic_topics_revised": 1, "agentic_topics_deepened": 2,
            "agentic_requirements_solved": 3, "agentic_projects": 1, "agentic_features": 4, "agentic_deployments": 2,
            "agentic_bugs_fixed": 3, "agentic_capabilities": 3,
            "x0_topics_learned": 3, "x0_topics_revised": 2, "x0_topics_deepened": 2,
            "x0_experiments": 3, "x0_hypotheses": 2, "x0_questions_resolved": 3, "x0_sources": 5, "x0_milestones": 1,
            "dads_investigated": 0, "dads_implementing": 0, "dads_improved": 0, "dads_independent": 0,
            "dads_tech_impl": 0, "dads_tech_knowledge": 0.0, "dads_ops_knowledge": 0.0,
            "deep_work_hours": 6.5, "notes": "Mathematical proofs mastered and high velocity code."
        },
        # Day 7: Today
        {
            "dt": str(today),
            "m3_attempted": 25, "m3_solved": 22, "m3_correct": 21, "m3_chapter": "Vector Calculus", "m3_topic": "Stokes' Theorem & Surface Integrals",
            "coos_numericals": 10, "coos_correct": 10, "coos_theory_learned": 2, "coos_theory_revised": 2, "coos_practicals": 2,
            "python_tasks": 4, "python_loc_written": 580, "python_loc_read": 750, "python_topics_learned": 3, "python_topics_applied": 3,
            "dsa_theory": 2, "dsa_problems": 8, "dsa_leetcode": 6, "dsa_java_impl": 4, "dsa_revision": 3,
            "uhv_learned": 1, "uhv_revised": 1,
            "agency_prospects": 0, "agency_contacted": 0, "agency_outreach": 0, "agency_followups": 0,
            "agency_replies": 0, "agency_conversations": 0, "agency_calls": 0, "agency_proposals": 0, "agency_deals": 0,
            "agency_new_mrr": 0.0, "agency_current_mrr": 0.0,
            "linkedin_posts": 1, "instagram_posts": 1, "other_content": 0,
            "agentic_topics_learned": 2, "agentic_topics_revised": 2, "agentic_topics_deepened": 2,
            "agentic_requirements_solved": 3, "agentic_projects": 0, "agentic_features": 3, "agentic_deployments": 1,
            "agentic_bugs_fixed": 2, "agentic_capabilities": 3,
            "x0_topics_learned": 3, "x0_topics_revised": 2, "x0_topics_deepened": 2,
            "x0_experiments": 2, "x0_hypotheses": 2, "x0_questions_resolved": 2, "x0_sources": 4, "x0_milestones": 1,
            "dads_investigated": 0, "dads_implementing": 0, "dads_improved": 0, "dads_independent": 0,
            "dads_tech_impl": 0, "dads_tech_knowledge": 0.0, "dads_ops_knowledge": 0.0,
            "deep_work_hours": 6.0, "notes": "7-day streak locked in. Solo Leveling Monarch rising."
        }
    ]

    for rec in sample_records:
        cols = ", ".join(rec.keys())
        placeholders = ", ".join(["?"] * len(rec))
        cur.execute(f"INSERT INTO daily_log({cols}) VALUES({placeholders})", tuple(rec.values()))

    # Sample M3 Topic Ledger entries
    m3_topics = [
        (str(start_date), "Linear Differential Equations", "Cauchy-Euler Equations", 12, 10, 9, 0, "Solved tutorial sheet"),
        (str(start_date + timedelta(days=1)), "Linear Differential Equations", "Method of Variation of Parameters", 15, 14, 13, 1, "Formula memorized"),
        (str(start_date + timedelta(days=2)), "Partial Differential Equations", "Lagrange Linear PDE", 18, 16, 15, 0, "Quasi-linear equations solved"),
        (str(start_date + timedelta(days=3)), "Partial Differential Equations", "Charpit's Method", 12, 11, 10, 0, "Auxiliary equations practiced"),
        (str(start_date + timedelta(days=4)), "Vector Calculus", "Gradient, Divergence & Curl", 20, 18, 17, 1, "Directional derivatives clear"),
        (str(start_date + timedelta(days=5)), "Vector Calculus", "Green's and Gauss Theorems", 22, 20, 19, 1, "Volume integrals checked"),
        (str(today), "Vector Calculus", "Stokes' Theorem & Surface Integrals", 25, 22, 21, 0, "Line vs Surface equivalence verified"),
    ]
    cur.execute("DELETE FROM m3_topic_log")
    for row in m3_topics:
        cur.execute("""
            INSERT INTO m3_topic_log(dt, chapter, topic, attempted, solved, correct, revision, notes)
            VALUES(?,?,?,?,?,?,?,?)
        """, row)

    # Sample Projects
    sample_projects = [
        ("PRJ-01", "Solo Leveling AI Agent Platform", "Agentic AI", str(start_date), "", "Active", "Full-Stack System", 0, 1, "A01, A03, A04", "LangGraph, Streamlit, SQLite", "A01", "Python, Streamlit, Plotly", "GitHub Repo", "Active production deployment", "Autonomous tracking engine"),
        ("PRJ-02", "Multi-Agent Code Reviewer", "Agentic AI", str(start_date + timedelta(days=1)), str(start_date + timedelta(days=3)), "Completed", "Developer Tool", 0, 1, "A01, A03, A05", "Static analysis, AST parsing, LLM verification", "A02", "Python, FastAPI, Tree-sitter", "GitHub PR Bot", "Reduced PR review latency by 60%", "Production-ready automated reviewer"),
        ("PRJ-03", "Attention Mechanism From Scratch", "X-0 ML", str(start_date + timedelta(days=2)), "", "Active", "Research Sandbox", 0, 0, "X0-008, X0-009", "PyTorch, CUDA Tensors, GQA", "X0-006", "PyTorch, NumPy", "Colab Notebook", "Passing unit tests with PyTorch SDPA", "Clean math derivation and code")
    ]
    cur.execute("DELETE FROM projects")
    for prj in sample_projects:
        cur.execute("""
            INSERT INTO projects(
                project_id, project_name, domain, start_date, completion_date, status, project_type,
                real_client, production, topics_used, topics_learned, topics_revised, technologies, evidence, outcome, notes
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, prj)

    con.commit()
    if close_con:
        con.close()
    return len(sample_records)

if __name__ == "__main__":
    init_cnt_a, init_cnt_x = seed_topics_master()
    logs_cnt = seed_sample_daily_logs()
    print(f"Seeded {init_cnt_a} Agentic topics, {init_cnt_x} X-0 topics, and {logs_cnt} sample daily lock-in days.")
