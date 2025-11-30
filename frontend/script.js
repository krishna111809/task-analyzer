async function analyzeTasks() {
  const txt = document.getElementById('taskInput').value;
  let tasks;
  try {
    tasks = JSON.parse(txt);
  } catch(e) {
    alert("Invalid JSON input");
    return;
  }
  const strategy = document.getElementById('strategy').value;
  try {
    const resp = await fetch(`/api/tasks/analyze/?strategy=${strategy}`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(tasks)
    });
    if (!resp.ok) {
      const err = await resp.json();
      alert("Error: " + JSON.stringify(err));
      return;
    }
    const data = await resp.json();
    displayResults(data.tasks);
  } catch(e) {
    alert("Network error: " + e);
  }
}

function displayResults(tasks){
  const container = document.getElementById('results');
  container.innerHTML = '';
  tasks.forEach(t=>{
    const div = document.createElement('div');
    const cls = t.score >= 150 ? 'high' : (t.score >= 80 ? 'medium' : 'low');
    div.className = 'card ' + cls;
    div.innerHTML = `<strong>${t.title}</strong> (id:${t.id})<br/>
      Score: ${t.score} — ${t.explanation}<br/>
      Due: ${t.due_date || "n/a"} • Est: ${t.estimated_hours}h • Importance: ${t.importance}`;
    container.appendChild(div);
  });
}
