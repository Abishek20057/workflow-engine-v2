function goHome() {
    window.location = "/";
}

function viewHistory() {
    window.location = "/history";
}

// LOAD WORKFLOWS
async function loadWorkflows() {
    let res = await fetch("/get_workflows");
    let data = await res.json();

    let table = document.getElementById("workflowTable");
    let select = document.getElementById("wfSelect");
    let exec = document.getElementById("execWorkflow");

    table.innerHTML = "<tr><th>Name</th><th>Action</th></tr>";
    select.innerHTML = "";
    exec.innerHTML = "";

    data.forEach(w => {
        table.innerHTML += `
        <tr>
            <td>${w.name}</td>
            <td><button onclick="start('${w.id}')">Start</button></td>
        </tr>`;

        select.innerHTML += `<option value="${w.id}">${w.name}</option>`;
        exec.innerHTML += `<option value="${w.id}">${w.name}</option>`;
    });
}

// CREATE
async function createWorkflow() {
    let name = document.getElementById("wfName").value;
    await fetch("/workflow?name=" + name, {method: "POST"});
    loadWorkflows();
}

// STEP
async function addStep() {
    let wf = document.getElementById("wfSelect").value;
    let name = document.getElementById("stepName").value;
    let type = document.getElementById("stepType").value;
    let order = document.getElementById("stepOrder").value;

    await fetch(`/step?workflow_id=${wf}&name=${name}&step_type=${type}&order=${order}`, {
        method: "POST"
    });

    alert("Step Added");
}

// RULE
async function addRule() {
    let step = document.getElementById("ruleStep").value;
    let condition = document.getElementById("condition").value;
    let next = document.getElementById("nextStep").value;
    let priority = document.getElementById("priority").value;

    await fetch(`/rule?step_id=${step}&condition=${condition}&next_step_id=${next}&priority=${priority}`, {
        method: "POST"
    });

    alert("Rule Added");
}

// RUN
function runWorkflow() {
    let wf = document.getElementById("execWorkflow").value;
    let amount = document.getElementById("amount").value;
    let country = document.getElementById("country").value;

    window.location = `/execute/${wf}?amount=${amount}&country=${country}`;
}

loadWorkflows();