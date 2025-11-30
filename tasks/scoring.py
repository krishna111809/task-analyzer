from datetime import datetime, date
from typing import List, Dict, Tuple, Any, Set

def parse_date(d):
    if not d:
        return None
    if isinstance(d, date):
        return d
    try:
        return datetime.strptime(d, "%Y-%m-%d").date()
    except Exception:
        return None

def detect_cycles(tasks: List[Dict]) -> List[List[int]]:
    graph = {}
    for t in tasks:
        tid = t.get("id")
        deps = t.get("dependencies") or []
        graph[tid] = deps
    visited = set()
    stack = set()
    cycles = []

    def dfs(node, path):
        if node in stack:
            idx = path.index(node)
            cycles.append(path[idx:])
            return
        if node in visited:
            return
        visited.add(node)
        stack.add(node)
        for nei in graph.get(node, []):
            if nei in graph: 
                dfs(nei, path + [nei])
        stack.remove(node)

    for n in graph:
        if n not in visited:
            dfs(n, [n])
    return cycles

def calculate_scores(tasks: List[Dict], strategy: str = "smart") -> Tuple[List[Dict], Dict]:
    today = date.today()
    id_map = {t.get("id"): t for t in tasks}
    blocks_count = {t.get("id"): 0 for t in tasks}
    for t in tasks:
        for dep in (t.get("dependencies") or []):
            if dep in blocks_count:
                blocks_count[dep] += 1

    cycles = detect_cycles(tasks)

    results = []
    for t in tasks:
        explanation_parts = []
        score = 0
        importance = int(t.get("importance") or 5)
        estimated = int(t.get("estimated_hours") or 1)
        due = parse_date(t.get("due_date"))
        tid = t.get("id")

        if due is None:
            explanation_parts.append("no due date")
            score += 5
        else:
            days_until = (due - today).days
            if days_until < 0:
                score += 200
                explanation_parts.append("OVERDUE")
            elif days_until <= 3:
                score += 80
                explanation_parts.append(f"due in {days_until}d")
            elif days_until <= 7:
                score += 40
                explanation_parts.append(f"due in {days_until}d")
            else:
                score += max(0, 20 - min(days_until, 20) // 1)
                explanation_parts.append(f"due in {days_until}d")

        score += importance * 10
        explanation_parts.append(f"importance {importance}/10")

        if estimated <= 2:
            score += 20
            explanation_parts.append(f"quick {estimated}h")
        else:
            score -= min(estimated, 30)
            explanation_parts.append(f"{estimated}h est")

        blocked_by_count = blocks_count.get(tid, 0)
        if blocked_by_count:
            score += blocked_by_count * 30
            explanation_parts.append(f"blocks {blocked_by_count} task(s)")

        unmet_deps = [d for d in (t.get("dependencies") or []) if d in id_map]
        if unmet_deps:
            score -= len(unmet_deps) * 15
            explanation_parts.append(f"blocked by {len(unmet_deps)}")

        in_cycle = any(tid in cycle for cycle in cycles)
        if in_cycle:
            score -= 100
            explanation_parts.append("in circular dependency")

        if strategy == "fastest":
            score += max(0, 10 - estimated)
        elif strategy == "highimpact":
            score += importance * 5 
        elif strategy == "deadline":
            if due:
                days_until = (due - today).days
                score += max(0, 50 - days_until)

        t_copy = t.copy()
        t_copy["score"] = int(score)
        t_copy["explanation"] = "; ".join(explanation_parts)
        t_copy["in_cycle"] = in_cycle
        results.append(t_copy)

    results.sort(key=lambda x: x["score"], reverse=True)
    meta = {"cycles": cycles}
    return results, meta
