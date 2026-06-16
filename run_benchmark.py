"""Run the 20-case golden dataset benchmark.

Usage:
    python run_benchmark.py
"""

from __future__ import annotations

from benchmark_dataset import build_golden_dataset, mock_agent
from solution.solution import BenchmarkRunner, RAGASEvaluator


def main() -> None:
    qa_pairs = build_golden_dataset()
    evaluator = RAGASEvaluator()
    runner = BenchmarkRunner()
    results = runner.run(qa_pairs, mock_agent, evaluator)
    report = runner.generate_report(results)

    print("=== 20 QA Benchmark Results ===")
    print(f"Total: {report['total']}")
    print(f"Passed: {report['passed']}")
    print(f"Pass rate: {report['pass_rate']:.0%}")
    print(f"Avg faithfulness: {report['avg_faithfulness']:.2f}")
    print(f"Avg relevance: {report['avg_relevance']:.2f}")
    print(f"Avg completeness: {report['avg_completeness']:.2f}")
    print(f"Failure types: {report['failure_types']}")
    print()

    print("| ID | Level | Faithfulness | Relevance | Completeness | Overall | Passed | Failure Type |")
    print("|----|-------|--------------|-----------|--------------|---------|--------|--------------|")
    for result in results:
        qa_id = result.qa_pair.metadata["id"]
        level = result.qa_pair.metadata["difficulty"]
        failure_type = result.failure_type or "-"
        passed = "Yes" if result.passed else "No"
        print(
            f"| {qa_id} | {level} | {result.faithfulness:.2f} | "
            f"{result.relevance:.2f} | {result.completeness:.2f} | "
            f"{result.overall_score():.2f} | {passed} | {failure_type} |"
        )

    print("\n=== Worst 3 ===")
    for result in sorted(results, key=lambda item: item.overall_score())[:3]:
        qa_id = result.qa_pair.metadata["id"]
        print(
            f"{qa_id}: overall={result.overall_score():.2f}, "
            f"failure={result.failure_type}, answer={result.actual_answer}"
        )


if __name__ == "__main__":
    main()
