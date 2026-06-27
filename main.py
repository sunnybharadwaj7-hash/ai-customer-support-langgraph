from graph import graph

from memory import   save_conversation



def main():

    print("=" * 60)
    print("ABC Technologies Customer Support Automation System")
    print("=" * 60)

    customer_id = input("Customer ID : ")

    customer_name = input("Customer Name : ")

    while True:

        query = input("\nCustomer : ")

        if query.lower() == "exit":
            print("\nThank you for using ABC Technologies Support.")
            break

        state = {

            "customer_id": customer_id,

            "customer_name": customer_name,

            "query": query,

            "intent": "",

            "retrieved_context": "",

            "approval_required": False,

            "approval_status": "",

            "final_response": "",

            "conversation_history": []

        }

        result = graph.invoke(
            state
        )

        print("\n" + "=" * 60)
        print("Customer Support Response")
        print("=" * 60)

        print(result["final_response"])

        print("=" * 60)

        # Save conversation into SQLite
        save_conversation(
            customer_id,
            customer_name,
            query,
            result["final_response"]
        )


if __name__ == "__main__":
    main()