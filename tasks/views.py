import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .scoring import calculate_scores

@csrf_exempt
def analyze_tasks(request):
    if request.method != "POST":
        return HttpResponseBadRequest(json.dumps({"error": "POST required"}), content_type="application/json")
    try:
        body = json.loads(request.body.decode("utf-8") or "[]")
    except Exception as e:
        return HttpResponseBadRequest(json.dumps({"error": "Invalid JSON", "detail": str(e)}), content_type="application/json")

    if not isinstance(body, list):
        return HttpResponseBadRequest(json.dumps({"error": "Expected a JSON array of tasks"}), content_type="application/json")
    strategy = request.GET.get("strategy", "smart")
    scored, meta = calculate_scores(body, strategy=strategy)
    return JsonResponse({"tasks": scored, "meta": meta}, safe=False)

def suggest_tasks(request):
    import json
    data_str = request.GET.get("data")
    strategy = request.GET.get("strategy", "smart")
    if not data_str:
        return JsonResponse({"error": "Provide tasks via ?data=<json array> or POST to /analyze/"}, status=400)
    try:
        tasks = json.loads(data_str)
    except Exception as e:
        return JsonResponse({"error": "Invalid JSON in data param", "detail": str(e)}, status=400)
    scored, meta = calculate_scores(tasks, strategy=strategy)
    top3 = scored[:3]
    suggestions = []
    for t in top3:
        suggestions.append({
            "id": t.get("id"),
            "title": t.get("title"),
            "score": t.get("score"),
            "reason": t.get("explanation")
        })
    return JsonResponse({"suggestions": suggestions, "meta": meta})
