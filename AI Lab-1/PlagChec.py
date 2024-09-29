import heapq
import re
from typing import List, Tuple

class State:
    def __init__(self, pos1: int, pos2: int, cost: int, path: List[Tuple[int, int]]):
        self.pos1 = pos1
        self.pos2 = pos2
        self.cost = cost
        self.path = path

    def __lt__(self, other):
        return self.cost < other.cost

def preprocess_text(text: str) -> List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.lower().strip() for s in sentences]

def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def heuristic(doc1: List[str], doc2: List[str], pos1: int, pos2: int) -> int:
    remaining_doc1 = doc1[pos1:]
    remaining_doc2 = doc2[pos2:]
    
    if not remaining_doc1 and not remaining_doc2:
        return 0
    elif not remaining_doc1:
        return sum(len(s) for s in remaining_doc2)
    elif not remaining_doc2:
        return sum(len(s) for s in remaining_doc1)
    
    return sum(min(levenshtein_distance(s1, s2) for s2 in remaining_doc2)
               for s1 in remaining_doc1)

def astar_alignment(doc1: List[str], doc2: List[str]) -> List[Tuple[int, int]]:
    start_state = State(0, 0, 0, [])
    heap = [(0, start_state)]
    visited = set()

    while heap:
        _, current_state = heapq.heappop(heap)

        if current_state.pos1 == len(doc1) and current_state.pos2 == len(doc2):
            return current_state.path

        if (current_state.pos1, current_state.pos2) in visited:
            continue

        visited.add((current_state.pos1, current_state.pos2))

        if current_state.pos1 < len(doc1) and current_state.pos2 < len(doc2):
            cost = levenshtein_distance(doc1[current_state.pos1], doc2[current_state.pos2])
            new_cost = current_state.cost + cost
            new_path = current_state.path + [(current_state.pos1, current_state.pos2)]
            new_state = State(current_state.pos1 + 1, current_state.pos2 + 1, new_cost, new_path)
            f = new_cost + heuristic(doc1, doc2, new_state.pos1, new_state.pos2)
            heapq.heappush(heap, (f, new_state))

        if current_state.pos1 < len(doc1):
            new_cost = current_state.cost + len(doc1[current_state.pos1])
            new_state = State(current_state.pos1 + 1, current_state.pos2, new_cost, current_state.path)
            f = new_cost + heuristic(doc1, doc2, new_state.pos1, new_state.pos2)
            heapq.heappush(heap, (f, new_state))

        if current_state.pos2 < len(doc2):
            new_cost = current_state.cost + len(doc2[current_state.pos2])
            new_state = State(current_state.pos1, current_state.pos2 + 1, new_cost, current_state.path)
            f = new_cost + heuristic(doc1, doc2, new_state.pos1, new_state.pos2)
            heapq.heappush(heap, (f, new_state))

    return []

def detect_plagiarism(doc1: List[str], doc2: List[str], alignment: List[Tuple[int, int]], threshold: float = 0.8) -> List[Tuple[str, str, float]]:
    plagiarism_cases = []
    for i, j in alignment:
        if i < len(doc1) and j < len(doc2):
            similarity = 1 - levenshtein_distance(doc1[i], doc2[j]) / max(len(doc1[i]), len(doc2[j]))
            if similarity >= threshold:
                plagiarism_cases.append((doc1[i], doc2[j], similarity))
    return plagiarism_cases

def main():
    test_cases = [
        ("This is a test. It has multiple sentences. We want to detect plagiarism.",
         "This is a test. It has many sentences. We want to find copying."),
        ("The quick brown fox jumps over the lazy dog.",
         "The fast brown fox leaps over the sleepy canine."),
        ("This is a completely different text. It has no similarity to the other one.",
         "We are discussing various topics here. None of them relate to the previous text."),
        ("Partial overlap exists in this text. Some sentences are copied.",
         "This text is mostly unique. However, some sentences are copied from elsewhere.")
    ]

    for i, (text1, text2) in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        doc1 = preprocess_text(text1)
        doc2 = preprocess_text(text2)

        alignment = astar_alignment(doc1, doc2)
        plagiarism_cases = detect_plagiarism(doc1, doc2, alignment)

        print("Aligned sentences:")
        for i, j in alignment:
            if i < len(doc1) and j < len(doc2):
                print(f"'{doc1[i]}' <-> '{doc2[j]}'")

        print("\nPotential plagiarism detected:")
        for s1, s2, similarity in plagiarism_cases:
            print(f"Similarity: {similarity:.2f}")
            print(f"  Doc1: '{s1}'")
            print(f"  Doc2: '{s2}'")

if __name__ == "__main__":
    main()
