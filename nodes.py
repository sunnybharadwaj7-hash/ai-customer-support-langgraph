from langchain_ollama import ChatOllama

from prompts import (
    CLASSIFIER_PROMPT,
    SUPERVISOR_PROMPT
)

from rag import retrieve_context

from memory import get_previous_issue


# --------------------------------------------------
# LLM
# --------------------------------------------------

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


# --------------------------------------------------
# Intent Classification Node
# --------------------------------------------------

def classify_node(state):

    prompt = CLASSIFIER_PROMPT.format(
        query=state["query"]
    )

    response = llm.invoke(prompt)

    state["intent"] = response.content.strip()
    print(f"\nIntent Detected: {state['intent']}")

    return state


# --------------------------------------------------
# Sales Support Agent
# --------------------------------------------------

def sales_node(state):

    context = retrieve_context(
        state["query"]
    )

    state["retrieved_context"] = context

    prompt = f"""
You are the Sales Support Agent.

Answer only using the company information below.

Company Information:

{context}

Customer Query:

{state['query']}

Generate a professional response.
"""

    response = llm.invoke(prompt)

    state["final_response"] = response.content

    print(f"\nSales Support Response: {state['final_response']}")

    return state


# --------------------------------------------------
# Technical Support Agent
# --------------------------------------------------

def technical_node(state):

    context = retrieve_context(
        state["query"]
    )

    state["retrieved_context"] = context

    prompt = f"""
You are the Technical Support Agent.

Use the technical documentation below.

Technical Manual:

{context}

Customer Query:

{state['query']}

Provide troubleshooting steps.
"""

    response = llm.invoke(prompt)

    state["final_response"] = response.content
    print(f"\nTechnical Support Response: {state['final_response']}")

    return state


# --------------------------------------------------
# Billing Support Agent
# --------------------------------------------------

def billing_node(state):

    context = retrieve_context(
        state["query"]
    )

    state["retrieved_context"] = context

    prompt = f"""
You are the Billing Support Agent.

Use the billing policy below.

Company Policy:

{context}

Customer Query:

{state['query']}

If this is a refund request,
mention that supervisor approval is required.

Generate a professional response.
"""

    response = llm.invoke(prompt)

    state["final_response"] = response.content
    print(f"\nBilling Support Response: {state['final_response']}")

    return state


# --------------------------------------------------
# Account Support Agent
# --------------------------------------------------

def account_node(state):

    context = retrieve_context(
        state["query"]
    )

    state["retrieved_context"] = context

    prompt = f"""
You are the Account Support Agent.

Use the information below.

Context:

{context}

Customer Query:

{state['query']}

Generate a helpful response.
"""

    response = llm.invoke(prompt)

    state["final_response"] = response.content
    print(f"\nAccount Support Response: {state['final_response']}")
    return state
# --------------------------------------------------
# Memory Recall Node
# --------------------------------------------------

def memory_node(state):

    previous_issue = get_previous_issue(
        state["customer_id"]
    )

    state["final_response"] = (
        f"Your previous support issue was:\n\n{previous_issue}"
    )

    return state


# --------------------------------------------------
# Human Approval Node
# --------------------------------------------------

HIGH_RISK = [
    "refund",
    "refund request",
    "cancel subscription",
    "subscription cancellation",
    "account closure",
    "close account",
    "compensation",
    "management",
    "escalation"
]


def approval_node(state):

    query = state["query"].lower()

    state["approval_required"] = any(
        keyword in query
        for keyword in HIGH_RISK
    )

    if state["approval_required"]:

        print("\n" + "=" * 60)
        print("HUMAN APPROVAL REQUIRED")
        print("=" * 60)

        print("\nCustomer Query:")
        print(state["query"])

        print("\nDraft Response:")
        print(state["final_response"])

        approval = input(
            "\nApprove? (yes/no): "
        )

        if approval.lower() == "yes":
            state["approval_status"] = "approved"
        else:
            state["approval_status"] = "rejected"

            state["final_response"] = (
                "Your request has been forwarded "
                "to a human supervisor."
            )

    else:
        state["approval_status"] = "approved"

    return state


# --------------------------------------------------
# Supervisor Node
# --------------------------------------------------

def supervisor_node(state):

    prompt = SUPERVISOR_PROMPT.format(
        query=state["query"],
        context=state["retrieved_context"],
        response=state["final_response"]
    )

    response = llm.invoke(prompt)

    state["final_response"] = response.content

    return state


# --------------------------------------------------
# Router
# --------------------------------------------------

def router(state):

    intent = state["intent"].strip().lower()
    routes={
        "sales":"sales",
        "technical":"technical",
        "billing":"billing",
        "account":"account",
        "memory":"memory"
    }
    print(f"\nRouting to: {intent}")
    return routes.get(intent,"sales")
