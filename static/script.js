async function createWorkflow(){
let name=document.getElementById("wf_name").value
await fetch(`/workflow?name=${name}`,{method:"POST"})
alert("Created")
}

async function addStep(){
let wf=document.getElementById("wf_id").value
let name=document.getElementById("step_name").value
let type=document.getElementById("step_type").value
let order=document.getElementById("order").value

await fetch(`/step?workflow_id=${wf}&name=${name}&step_type=${type}&order=${order}`,{method:"POST"})
alert("Step Added")
}

async function addRule(){
let step=document.getElementById("step_id").value
let cond=document.getElementById("condition").value
let next=document.getElementById("next_step").value
let pri=document.getElementById("priority").value

await fetch(`/rule?step_id=${step}&condition=${cond}&next_step_id=${next}&priority=${pri}`,{method:"POST"})
alert("Rule Added")
}

async function runWorkflow(){
let wf=document.getElementById("exec_wf").value
let amount=document.getElementById("amount").value

let res = await fetch(`/execute/${wf}?amount=${amount}`,{method:"POST"})
let html = await res.text()

document.open()
document.write(html)
document.close()
}