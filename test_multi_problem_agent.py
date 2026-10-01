from app.services import autonomous_agent


# Mock Gemini decisions so we can test the full
# autonomous self-healing loop without using
# the Gemini API quota.

decisions = [
    {
        "action": "tool",
        "tool": "inspect_workflow",
        "arguments": {},
    },
    {
        "action": "tool",
        "tool": "diagnose_workflow",
        "arguments": {},
    },
    {
        "action": "tool",
        "tool": "fix_workflow",
        "arguments": {},
    },
    {
        "action": "tool",
        "tool": "diagnose_workflow",
        "arguments": {},
    },
    {
        "action": "tool",
        "tool": "fix_workflow",
        "arguments": {},
    },
    {
        "action": "tool",
        "tool": "diagnose_workflow",
        "arguments": {},
    },
    {
        "action": "tool",
        "tool": "fix_workflow",
        "arguments": {},
    },
    {
        "action": "tool",
        "tool": "diagnose_workflow",
        "arguments": {},
    },
    {
        "action": "tool",
        "tool": "fix_workflow",
        "arguments": {},
    },
    {
        "action": "tool",
        "tool": "diagnose_workflow",
        "arguments": {},
    },
]


def mock_decision(
    goal,
    previous_results,
):
    decision = decisions.pop(0)

    print(
        f"\nNEXT ACTION: "
        f"{decision.get('tool', decision.get('action'))}"
    )

    return decision


# Replace the real Gemini decision function
# with our local mock.
autonomous_agent.decide_next_action = mock_decision


workflow = {
    "id": "workflow-001",
    "name": "Employee Data Workflow",
    "steps": [
        {
            "id": "trigger-1",
            "name": "Receive Employee Data",
            "type": "trigger",
            "config": {
                "path": "/employees"
            },
        },
        {
            "id": "validate-1",
            "name": "Validate Employee",
            "type": "validation",
            "config": {},
        },
        {
            "id": "db-1",
            "name": "Save Employee",
            "type": "database",
            "config": {},
        },
    ],
}


result = autonomous_agent.run_autonomous_agent(
    goal="Fix workflow configuration problems",
    workflow=workflow,
)


print("\n========================================")
print("FINAL RESULT")
print("========================================")

print("STATUS:", result["status"])
print("STEPS:", result["steps"])

print("\nFINAL DIAGNOSIS:")

for item in reversed(result["results"]):

    if item.get("tool") == "diagnose_workflow":

        print(
            item.get(
                "result"
            )
        )

        break
