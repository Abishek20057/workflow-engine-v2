async function loadWorkflows() {
    let res = await fetch("/get_workflows");
    let data = await res.json();

    let table = document.getElementById("workflowTable");
    let exec = document.getElementById("execWorkflow");

    table.innerHTML = `
    <tr>
        <th>Name</th>
        <th>Action</th>
    </tr>`;

    exec.innerHTML = "";

    data.forEach(w => {
        table.innerHTML += `
        <tr>
            <td>${w.name}</td>
            <td>
                <button onclick="startWorkflow('${w.id}')">Start</button>
            </td>
        </tr>`;

        exec.innerHTML += `<option value="${w.id}">${w.name}</option>`;
    });
}

function startWorkflow(id) {
    showTab('start');
    document.getElementById("execWorkflow").value = id;

    loadDiagram(id);
}

function showTab(tab) {
    document.querySelectorAll(".tab").forEach(t => t.classList.add("hidden"));
    document.getElementById(tab).classList.remove("hidden");
}

function viewHistory() {
    window.location = "/history";
}

async function createWorkflow() {
    let name = document.getElementById("wfName").value;

    if (!name) {
        alert("Enter workflow name");
        return;
    }

    await fetch("/workflow?name=" + name, {method: "POST"});
    loadWorkflows();
}

function runWorkflow() {
    let wf = document.getElementById("execWorkflow").value;
    let amount = document.getElementById("amount").value;
    let country = document.getElementById("country").value;

    if (!wf) {
        alert("Select workflow!");
        return;
    }

    window.location = `/execute/${wf}?amount=${amount}&country=${country}`;
}

async function loadDiagram(wf_id) {
    let res = await fetch(`/get_steps/${wf_id}`);
    let data = await res.json();

    let diagram = document.getElementById("diagram");
    diagram.innerHTML = "";

    diagram.innerHTML += `<div class="node start">Start</div>`;

    data.forEach((step, index) => {
        diagram.innerHTML += `<div class="arrow">→</div>`;

        let cls = "node";
        if (index === 0) cls += " active";

        diagram.innerHTML += `<div class="${cls}">${step.name}</div>`;
    });
}

loadWorkflows();