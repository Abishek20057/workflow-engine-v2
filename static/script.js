async function loadWorkflows(){
let res = await fetch("/get_workflows")
let data = await res.json()

let table = document.getElementById("workflow_list")
table.innerHTML=""

for(let wf of data){
table.innerHTML += `
<tr>
<td>${wf.name}</td>
<td><button onclick="start('${wf.id}')">Start</button></td>
</tr>
`
}
}

async function createWorkflow(){
let name=document.getElementById("wf_name").value
await fetch(`/workflow?name=${name}`,{method:"POST"})
loadWorkflows()
}

function start(id){
document.getElementById("exec_wf").value=id
}

window.onload = loadWorkflows