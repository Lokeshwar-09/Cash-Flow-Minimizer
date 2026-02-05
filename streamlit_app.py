import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from greedy_algorithm import greedy_minimize
from graph_flow_algorithm import graph_flow_minimize

st.set_page_config(page_title="Cash Flow Minimization", page_icon="💰", layout="wide")

# ───────────── Modern CSS + Theme Support ─────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    .main { background-color: #0f1117; color: #e0e0e0; }
    .stApp { background-color: #0f1117; }
    .block-container { padding-top: 2rem !important; }
    
    h1 { color: #6366f1 !important; font-weight: 700; }
    h2, h3 { color: #a5b4fc !important; }
    
    .card {
        background: #1e293b;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        border: 1px solid #334155;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .place-header {
        font-size: 24px;
        font-weight: 700;
        color: #818cf8;
        margin-bottom: 8px;
    }
    
    .payer-tag {
        font-size: 18px;
        font-weight: 600;
        color: #34d399;
        background: rgba(52, 211, 153, 0.15);
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
    }
    
    .debt-line {
        color: #f87171;
        font-weight: 500;
    }
    
    .summary-box {
        background: #1e293b;
        border-radius: 12px;
        padding: 20px;
        margin: 24px 0;
        border-left: 5px solid #6366f1;
    }
    
    .progress { height: 10px !important; }
    .stProgress > div > div > div { background-color: #6366f1 !important; }
    
    .stButton > button {
        background: #6366f1;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: #4f46e5;
    }
    
    hr { border-color: #334155; margin: 32px 0; }
    </style>
""", unsafe_allow_html=True)

st.title("💰 Cash Flow Minimization")
st.markdown("**M.Gowtham (24018) & N.Lokeshwar (24020)**")
st.caption("Smart expense splitting & transaction minimization for groups")

# ───────────── Progress ─────────────
progress = st.progress(0)
if st.session_state.get('step', 1) == 1:
    progress.progress(0.25)
elif st.session_state.get('step', 1) == 2:
    progress.progress(0.50)
elif st.session_state.get('step', 1) == 3:
    progress.progress(0.85)
else:
    progress.progress(1.0)

# ───────────── Session State ─────────────
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'group_members' not in st.session_state:
    st.session_state.group_members = []
if 'situations' not in st.session_state:
    st.session_state.situations = []

# ───────────── Step 1 ─────────────
if st.session_state.step == 1:
    st.markdown("### Step 1: Group Size")
    num = st.number_input("How many people are in the group?", min_value=2, max_value=12, value=3, step=1)

    if st.button("Continue to Names"):
        if num >= 2:
            st.session_state.group_size = num
            st.session_state.group_members = [""] * num
            st.session_state.step = 2
            st.rerun()

# ───────────── Step 2 ─────────────
if st.session_state.step == 2:
    st.markdown("### Step 2: Enter Group Member Names")
    cols = st.columns(3)
    for i in range(st.session_state.group_size):
        name = cols[i % 3].text_input(f"Member {i+1}", key=f"name_{i}")
        st.session_state.group_members[i] = name.strip()

    if st.button("Save Group → Add Expenses"):
        valid = [n.strip() for n in st.session_state.group_members if n.strip()]
        if len(valid) >= 2:
            st.session_state.group_members = list(set(valid))
            st.success(f"Group created: {', '.join(st.session_state.group_members)}")
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("Please enter at least 2 valid names")

# ───────────── Step 3: Add Expenses ─────────────
if st.session_state.step == 3:
    st.markdown("### Step 3: Add Expenses / Places")
    st.caption("Add one expense at a time – form resets after each addition")

    with st.form(key=f"expense_form_{len(st.session_state.situations)}"):
        place = st.text_input("Expense / Place", placeholder="Cafe Bill, Juice Shop, Hotel, Auto...")
        payer = st.selectbox("Who paid the full amount", options=st.session_state.group_members)
        total = st.number_input("Total Amount Paid (₹)", min_value=1.0, step=10.0, format="%.2f")

        st.markdown("**Who participated?** (select all)")
        participants = []
        cols = st.columns(3)
        for i, p in enumerate(st.session_state.group_members):
            if cols[i % 3].checkbox(p, key=f"chk_{p}_{len(st.session_state.situations)}_{i}"):
                participants.append(p)

        if st.form_submit_button("➕ Add Expense", type="primary"):
            if not place.strip() or not participants or total <= 0:
                st.error("Please complete all fields")
            else:
                per = total / len(participants)
                st.session_state.situations.append({
                    'name': place.strip(),
                    'payer': payer,
                    'total': total,
                    'participants': participants,
                    'per_person': per
                })
                st.success("Expense added!")
                st.rerun()

    # ───────────── Display Added Expenses ─────────────
    if st.session_state.situations:
        st.markdown("### Added Expenses")
        
        total_debt = 0
        for sit in st.session_state.situations:
            with st.container():
                st.markdown(f'<div class="card">', unsafe_allow_html=True)
                st.markdown(f'<div class="place-title">{sit["name"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="payer">Paid by {sit["payer"]} – ₹{sit["total"]:.2f}</div>', unsafe_allow_html=True)
                st.caption(f'For: {", ".join(sit["participants"])}')
                
                for p in sit['participants']:
                    if p != sit['payer']:
                        amt = sit['per_person']
                        total_debt += amt
                        st.markdown(f'<span class="debt">→ {p} owes {sit["payer"]} ₹{amt:.2f}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # Summary
        st.markdown(f'<div class="summary-box">'
                    f'<strong>Total Expenses:</strong> ₹{sum(s["total"] for s in st.session_state.situations):.2f}<br>'
                    f'<strong>Total Debts Before Minimization:</strong> ₹{total_debt:.2f}<br>'
                    f'<strong>Group Size:</strong> {len(st.session_state.group_members)} people'
                    f'</div>', unsafe_allow_html=True)

        # Minimize
        if st.button("🔄 Minimize All Transactions", type="primary"):
            all_tx = []
            for sit in st.session_state.situations:
                for p in sit['participants']:
                    if p != sit['payer']:
                        all_tx.append((p, sit['payer'], sit['per_person']))

            greedy = greedy_minimize(all_tx)
            flow = graph_flow_minimize(all_tx)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Greedy Result (Fast & Practical)")
                for fr, to, a in greedy:
                    st.markdown(f"**{fr} → {to}** : ₹{a:.2f}")

            with col2:
                st.subheader("Graph Flow Result (Optimal)")
                for fr, to, a in flow:
                    st.markdown(f"**{fr} → {to}** : ₹{a:.2f}")

            # Graphs
            st.divider()
            st.subheader("Visual Comparison")

            def plot(data, title):
                fig, ax = plt.subplots(figsize=(9, 6))
                G = nx.DiGraph()
                for a, b, w in data:
                    G.add_edge(a, b, weight=round(w, 2))
                pos = nx.spring_layout(G, seed=42)
                nx.draw(G, pos, ax=ax, with_labels=True, node_color='#6366f1', node_size=2400,
                        font_size=10, font_weight='bold', arrows=True, arrowsize=18)
                nx.draw_networkx_edge_labels(G, pos, edge_labels={e: f"₹{d['weight']:.2f}" for e,d in G.edges(data=True)}, font_size=9, ax=ax)
                ax.set_title(title, color='white')
                fig.patch.set_facecolor('#0f1117')
                ax.set_facecolor('#0f1117')
                ax.tick_params(colors='white')
                st.pyplot(fig)

            tab1, tab2, tab3 = st.tabs(["Original", "Greedy", "Graph Flow"])
            with tab1: plot(all_tx, "Original Debts")
            with tab2: plot(greedy, "After Greedy")
            with tab3: plot(flow, "After Graph Flow")

# ───────────── Reset ─────────────
if st.button("🗑️ Reset & Start New"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()