import streamlit as st
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchAgent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:          #0a0d12;
    --surface:     #111520;
    --border:      #1e2535;
    --accent:      #4f8ef7;
    --accent2:     #a78bfa;
    --success:     #34d399;
    --warn:        #fbbf24;
    --text:        #e2e8f0;
    --muted:       #64748b;
    --mono:        'Space Mono', monospace;
    --sans:        'DM Sans', sans-serif;
}

/* Global reset */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--sans);
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero header ── */
.hero {
    padding: 2.5rem 0 1.5rem;
    text-align: center;
}
.hero h1 {
    font-family: var(--mono);
    font-size: 2.4rem;
    letter-spacing: -1px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.hero p {
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 0.4rem;
    letter-spacing: 0.5px;
}

/* ── Input card ── */
.input-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.6rem 2rem;
    margin-bottom: 2rem;
}

/* ── Step tracker ── */
.steps-row {
    display: flex;
    gap: 0;
    margin: 1.6rem 0;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--border);
}
.step-pill {
    flex: 1;
    text-align: center;
    padding: 0.7rem 0.5rem;
    font-family: var(--mono);
    font-size: 0.72rem;
    letter-spacing: 0.3px;
    background: var(--surface);
    color: var(--muted);
    border-right: 1px solid var(--border);
    transition: all .3s ease;
    position: relative;
}
.step-pill:last-child { border-right: none; }
.step-pill.active {
    background: rgba(79,142,247,.15);
    color: var(--accent);
}
.step-pill.done {
    background: rgba(52,211,153,.08);
    color: var(--success);
}
.step-pill .icon { font-size: 1rem; display: block; margin-bottom: 2px; }

/* ── Output section cards ── */
.section-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    transition: border-color .2s;
}
.section-card:hover { border-color: #2d3a55; }
.section-title {
    font-family: var(--mono);
    font-size: 0.78rem;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-title .badge {
    font-size: 0.65rem;
    padding: 2px 8px;
    border-radius: 20px;
    background: rgba(79,142,247,.15);
    color: var(--accent);
    letter-spacing: 0.8px;
}
.section-body {
    font-size: 0.9rem;
    line-height: 1.75;
    color: #c4cfe3;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Critique card accent ── */
.section-card.critique { border-left: 3px solid var(--accent2); }
.section-card.critique .section-title { color: var(--accent2); }
.section-card.critique .badge { background: rgba(167,139,250,.15); color: var(--accent2); }

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input {
    background: #0d1018 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
    font-size: 1rem !important;
    padding: 0.7rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,.15) !important;
}
.stTextInput label { color: var(--muted) !important; font-size: 0.82rem !important; }

.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-family: var(--mono) !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.5px !important;
    transition: opacity .2s, transform .1s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
    border-radius: 4px !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.8rem 0 !important; }

/* ── Toast-like status ── */
.status-bar {
    background: rgba(79,142,247,.1);
    border: 1px solid rgba(79,142,247,.25);
    border-radius: 8px;
    padding: 0.65rem 1.1rem;
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--accent);
    margin: 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🔬 ResearchAgent</h1>
    <p>Multi-agent pipeline · Search → Read → Write → Critique</p>
</div>
""", unsafe_allow_html=True)

# ── Input card ─────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. 'Agentic AI frameworks in 2025'",
        label_visibility="collapsed",
    )
with col2:
    run_btn = st.button("▶ Run", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Step tracker helper ─────────────────────────────────────────────────────────
STEPS = [
    ("🌐", "Search"),
    ("📄", "Reader"),
    ("✍️", "Writer"),
    ("🔍", "Critic"),
]

def render_steps(active: int):
    """active: 0-indexed step currently running, -1 = none, 4 = all done"""
    pills = ""
    for i, (icon, label) in enumerate(STEPS):
        cls = "done" if i < active else ("active" if i == active else "")
        pills += f'<div class="step-pill {cls}"><span class="icon">{icon if i >= active else "✓"}</span>{label}</div>'
    st.markdown(f'<div class="steps-row">{pills}</div>', unsafe_allow_html=True)

def render_section(title, badge, content, extra_class=""):
    st.markdown(f"""
    <div class="section-card {extra_class}">
        <div class="section-title">{title} <span class="badge">{badge}</span></div>
        <div class="section-body">{content}</div>
    </div>
    """, unsafe_allow_html=True)

# ── Pipeline execution ──────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        step_placeholder = st.empty()
        progress_bar = st.progress(0)
        status_placeholder = st.empty()

        results = {}

        try:
            from pipeline import research_pipeline

            # We wrap each stage with UI updates by monkey-patching
            # via a staged approach — call pipeline but capture state incrementally.

            # Stage indicators
            def show_status(msg):
                status_placeholder.markdown(
                    f'<div class="status-bar">⚡ {msg}</div>', unsafe_allow_html=True
                )

            with step_placeholder.container():
                render_steps(0)
            show_status("Search agent is scouring the web…")
            progress_bar.progress(10)

            # Run full pipeline (blocking)
            state = research_pipeline(topic)

            # Animate step progression after result (since pipeline is synchronous)
            for i in range(1, 5):
                with step_placeholder.container():
                    render_steps(i)
                progress_bar.progress(i * 25)
                time.sleep(0.35)

            status_placeholder.empty()
            progress_bar.empty()

            st.markdown("---")
            st.markdown(
                '<p style="font-family:\'Space Mono\',monospace;font-size:0.75rem;'
                'color:#64748b;letter-spacing:1px;text-transform:uppercase;margin-bottom:1rem;">'
                f'Results · {topic}</p>',
                unsafe_allow_html=True,
            )

            render_section("🌐 Search Results", "AGENT 1", state.get("search_results", "—"))
            render_section("📄 Scraped & Summarized Content", "AGENT 2", state.get("scraped_content", "—"))
            render_section("✍️ Generated Report", "WRITER CHAIN", state.get("report", "—"))
            render_section("🔍 Critique", "CRITIC CHAIN", state.get("critique", "—"), extra_class="critique")

        except ImportError as e:
            step_placeholder.empty()
            progress_bar.empty()
            status_placeholder.empty()
            st.error(f"Could not import pipeline: {e}")
        except Exception as e:
            step_placeholder.empty()
            progress_bar.empty()
            status_placeholder.empty()
            st.error(f"Pipeline error: {e}")

# ── Empty state ────────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div style="text-align:center;padding:3rem 0;color:#2d3a55;">
        <div style="font-size:3rem;margin-bottom:1rem;">⬆</div>
        <p style="font-family:'Space Mono',monospace;font-size:0.8rem;letter-spacing:1px;">
            ENTER A TOPIC AND HIT RUN
        </p>
    </div>
    """, unsafe_allow_html=True)
