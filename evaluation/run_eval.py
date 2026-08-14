import sys
import os
import json
import time
 
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app", "retrieval"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app", "generation"))
 
from reranker import search_with_rerank
from llm_generator import generate_answer
 
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "eval_questions.json")
RESULTS_FILE = os.path.join(os.path.dirname(__file__), "eval_results.md")
 
 
def run_evaluation():
    with open(QUESTIONS_FILE, "r") as f:
        questions = json.load(f)
 
    results = []
 
    for q in questions:
        print(f"Running question {q['id']}: {q['question']}")

        start_time = time.time()
        try:
            chunks = search_with_rerank(q["question"], retrieve_k=10, final_k=5)

            if not chunks:
                answer = "I couldn't find relevant information for that question."
            else:
                answer = generate_answer(q["question"], chunks)
        except Exception as e:
            chunks = []
            answer = f"ERROR: {e}"

        elapsed = time.time() - start_time
 
        results.append({
            "id": q["id"],
            "question": q["question"],
            "difficulty": q["difficulty"],
            "expected_topic": q["expected_topic"],
            "answer": answer,
            "num_chunks_retrieved": len(chunks),
            "time_seconds": round(elapsed, 2),
        })
 
        print(f"  Done in {elapsed:.2f}s\n")
 
    return results
 
 
def write_report(results):
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        f.write("# RAG System Evaluation Results\n\n")
        f.write(f"Total questions tested: {len(results)}\n\n")
 
        avg_time = sum(r["time_seconds"] for r in results) / len(results)
        f.write(f"Average response time: {avg_time:.2f}s\n\n")
 
        f.write("---\n\n")
 
        for r in results:
            f.write(f"## Q{r['id']} ({r['difficulty']}): {r['question']}\n\n")
            f.write(f"**Expected topic:** {r['expected_topic']}\n\n")
            f.write(f"**Chunks retrieved:** {r['num_chunks_retrieved']} | **Time:** {r['time_seconds']}s\n\n")
            f.write(f"**Answer:**\n\n{r['answer']}\n\n")
            f.write("**Manual verdict:** [ ] Correct  [ ] Partially correct  [ ] Incorrect\n\n")
            f.write("---\n\n")
 
    print(f"\nReport saved to: {RESULTS_FILE}")
 
 
if __name__ == "__main__":
    results = run_evaluation()
    write_report(results)
 