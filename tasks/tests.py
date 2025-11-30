from django.test import TestCase, Client
from .scoring import calculate_scores
from datetime import date, timedelta

class ScoringTests(TestCase):
    def test_overdue_has_higher_score(self):
        today = date.today()
        t1 = {"id":1,"title":"old","due_date": (today - timedelta(days=2)).strftime("%Y-%m-%d"), "importance":5, "estimated_hours":2, "dependencies":[]}
        t2 = {"id":2,"title":"future","due_date": (today + timedelta(days=5)).strftime("%Y-%m-%d"), "importance":5, "estimated_hours":2, "dependencies":[]}
        res,meta = calculate_scores([t1,t2])
        self.assertTrue(res[0]['id']==1)

    def test_quick_task_preferred_in_fastest_strategy(self):
        today = date.today()
        t1 = {"id":1,"title":"long work","due_date": (today + timedelta(days=5)).strftime("%Y-%m-%d"), "importance":5, "estimated_hours":10, "dependencies":[]}
        t2 = {"id":2,"title":"quick","due_date": (today + timedelta(days=5)).strftime("%Y-%m-%d"), "importance":5, "estimated_hours":1, "dependencies":[]}
        res,meta = calculate_scores([t1,t2], strategy="fastest")
        self.assertTrue(res[0]['id']==2)

    def test_cycle_detection(self):
        t1 = {"id":1,"dependencies":[2]}
        t2 = {"id":2,"dependencies":[1]}
        res,meta = calculate_scores([t1,t2])
        self.assertTrue(len(meta['cycles'])>0)
