from langgraph.graph import (
    StateGraph,
    START,
    END
)

from state import SupportState

from nodes import (
    classify_node,
    sales_node,
    technical_node,
    billing_node,
    account_node,
    memory_node,
    approval_node,
    supervisor_node,
    router
)

#from memory import get_memory


# -----------------------------------------
# Create Graph
# -----------------------------------------

builder = StateGraph(SupportState)


# -----------------------------------------
# Add Nodes
# -----------------------------------------

builder.add_node(
    "classifier",
    classify_node
)

builder.add_node(
    "sales",
    sales_node
)

builder.add_node(
    "technical",
    technical_node
)

builder.add_node(
    "billing",
    billing_node
)

builder.add_node(
    "account",
    account_node
)

builder.add_node(
    "memory",
    memory_node
)

builder.add_node(
    "approval",
    approval_node
)

builder.add_node(
    "supervisor",
    supervisor_node
)


# -----------------------------------------
# Entry Point
# -----------------------------------------

builder.add_edge(
    START,
    "classifier"
)


# -----------------------------------------
# Intent Routing
# -----------------------------------------

builder.add_conditional_edges(
    "classifier",
    router,
    {
        "sales": "sales",
        "technical": "technical",
        "billing": "billing",
        "account": "account",
        "memory": "memory"
    }
)


# -----------------------------------------
# Agent Flow
# -----------------------------------------

builder.add_edge(
    "sales",
    "approval"
)

builder.add_edge(
    "technical",
    "approval"
)

builder.add_edge(
    "billing",
    "approval"
)

builder.add_edge(
    "account",
    "approval"
)


# -----------------------------------------
# Approval Flow
# -----------------------------------------

builder.add_edge(
    "approval",
    "supervisor"
)


# -----------------------------------------
# Memory Flow
# -----------------------------------------

builder.add_edge(
    "memory",
    END
)


# -----------------------------------------
# Final Response
# -----------------------------------------

builder.add_edge(
    "supervisor",
    END
)


# -----------------------------------------
# Compile Graph
# -----------------------------------------

#memory = get_memory()

graph = builder.compile()