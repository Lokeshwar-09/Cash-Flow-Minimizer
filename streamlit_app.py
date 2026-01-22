import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from greedy_algorithm import greedy_minimize
from graph_flow_algorithm import graph_flow_minimize  # your existing function

# ───────────── Page config ─────────────
st.set_page_config(
    page_title="Cash Flow Minimization",
    page_icon="💰",
    layout="wide"
)

# ───────────── Title & Intro ─────────────
st.title("💰 Cash Flow Minimization in Financial Transactions")
st.markdown("""
**M.Gowtham (24018) & N.Lokeshwar (24020)**  
Expense splitting, UPI settlements, business payments — minimize transactions using **Greedy** + **Graph-Based Flow** algorithms.
""")

# ───────────── Input Section ─────────────
st.subheader("Enter Transactions (one per line)")
st.caption("Format: payer payee amount   Example: Alice Bob 1200")

transactions_input = st.text_area(
    label="Transactions",
    height=180,
    placeholder="Alice Bob 1000\nBob Charlie 400\nCharlie Alice 200\nDavid Alice 150",
    help="Enter one transaction per line. Click 'Minimize' when ready."
)

if st.button("🚀 Minimize Transactions", type="primary", use_container_width=True):
    if not transactions_input.strip():
        st.error("Please enter at least one transaction.")
    else:
        # Parse input
        lines = [line.strip() for line in transactions_input.split("\n") if line.strip()]
        transactions = []
        error = None

        for line in lines:
            parts = line.split()
            if len(parts) != 3:
                error = f"Invalid format: {line}"
                break
            try:
                payer, payee, amt = parts[0], parts[1], int(parts[2])
                if amt <= 0:
                    error = f"Amount must be positive: {line}"
                    break
                transactions.append((payer, payee, amt))
            except:
                error = f"Invalid amount: {line}"
                break

        if error:
            st.error(error)
        else:
            with st.spinner("Minimizing transactions..."):
                # Run algorithms
                greedy_result = greedy_minimize(transactions)
                flow_result = graph_flow_minimize(transactions)

                # ───────────── Results Layout ─────────────
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Greedy Algorithm")
                    st.markdown(f"**Reduced to {len(greedy_result)} transactions**")
                    if greedy_result:
                        for fr, to, amt in greedy_result:
                            st.write(f"**{fr} → {to}** : ₹{amt}")
                    else:
                        st.success("Already balanced — no payments needed!")

                with col2:
                    st.subheader("Graph-Based Flow")
                    st.markdown(f"**Reduced to {len(flow_result)} transactions**")
                    if flow_result:
                        for fr, to, amt in flow_result:
                            st.write(f"**{fr} → {to}** : ₹{amt}")
                    else:
                        st.success("No additional optimization needed.")

                # ───────────── Graphs ─────────────
                st.subheader("Visualizations")

                def draw_graph(data, title):
                    if not data:
                        st.info("No data to visualize")
                        return
                    fig, ax = plt.subplots(figsize=(10, 7))
                    G = nx.DiGraph()
                    for a, b, amt in data:
                        G.add_edge(a, b, weight=amt)
                    pos = nx.spring_layout(G, seed=42)
                    nx.draw(G, pos, ax=ax, with_labels=True, node_color='#a8e6cf',
                            node_size=3000, font_size=12, font_weight='bold',
                            arrows=True, arrowstyle='->', arrowsize=20)
                    labels = nx.get_edge_attributes(G, 'weight')
                    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=11, ax=ax)
                    ax.set_title(title)
                    st.pyplot(fig)

                tab1, tab2, tab3 = st.tabs(["Original", "Greedy", "Graph Flow"])

                with tab1:
                    draw_graph(transactions, "Original Debt Graph")

                with tab2:
                    draw_graph(greedy_result, "After Greedy Minimization")

                with tab3:
                    draw_graph(flow_result, "After Graph Flow Optimization")

st.markdown("---")
st.caption("Project uses Greedy for fast settlement + Graph Flow (min-cost) for optimality validation. Scalable for UPI, expense splitting, business settlements.")