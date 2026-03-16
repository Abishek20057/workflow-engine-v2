async function createWorkflow(){

let name=document.getElementById("workflowName").value

await fetch("/workflow",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({name:name})
})

location.reload()

}



async function createStep(){

let workflow_id=document.getElementById("workflowSelect").value
let name=document.getElementById("stepName").value
let step_type=document.getElementById("stepType").value
let order=parseInt(document.getElementById("stepOrder").value)

await fetch("/step",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
workflow_id,
name,
step_type,
order
})
})

location.reload()

}



async function createRule(){

let step_id=document.getElementById("ruleStepId").value
let condition=document.getElementById("condition").value
let next_step_id=document.getElementById("nextStep").value
let priority=parseInt(document.getElementById("priority").value)

await fetch("/rule",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
step_id,
condition,
next_step_id,
priority
})
})

alert("Rule added")

}



async function runWorkflow(){

let workflow_id=document.getElementById("execWorkflow").value
let amount=document.getElementById("amount").value

let res=await fetch("/execute/"+workflow_id,{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
data:{amount:Number(amount)}
})
})

let data=await res.json()

localStorage.setItem("logs", data.logs.join("\n"))

window.location.href="/result"

}



function showHistory(){

window.location.href="/history"

}