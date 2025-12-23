import sys

# Allow importing from ai_agents_hospitality-api/
sys.path.append("ai_agents_hospitality-api")

from agents.hotel_rag_agent import answer_hotel_question_rag


def run_test(name: str, question: str):
    print("\n" + "=" * 60)
    print(f"🧪 {name}")
    print("-" * 60)
    print(f"Q: {question}\n")
    ans = answer_hotel_question_rag(question)
    print("A:\n")
    print(ans)
    return ans


if __name__ == "__main__":
    print("🧪 Testing Exercise 1: RAG Agent (Hotels knowledge base)")

    # Basic retrieval sanity checks
    run_test("Test 1/3: List hotels & locations", "List 5 hotels and their locations")
    run_test("Test 2/3: Ask about rooms", "Tell me about the rooms available in 2 hotels")
    run_test("Test 3/3: Ask about meal plans", "What meal plans are available across the hotels?")

    print("\n✅ Exercise 1 tests executed.")
