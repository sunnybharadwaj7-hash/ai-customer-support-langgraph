from typing import TypedDict, List


class SupportState(TypedDict):
    customer_name: str
    customer_id: str

    query: str
    intent: str

    retrieved_context: str

    approval_required: bool
    approval_status: str

    final_response: str

    conversation_history: List[str]