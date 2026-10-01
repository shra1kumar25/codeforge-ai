from app.services.agent_executor import execute_agent_tool
from app.services.decision_service import decide_next_action
from app.workflow.workflow_schema import Workflow


MAX_STEPS = 10


def run_autonomous_agent(
    goal: str,
    workflow=None,
):
    results = []

    # Convert incoming workflow dictionary into Workflow model
    if workflow is not None and isinstance(workflow, dict):
        workflow = Workflow(**workflow)

    # Keep the latest workflow state throughout
    # the complete agent lifecycle.
    current_workflow = workflow

    for _ in range(MAX_STEPS):

        next_action = decide_next_action(
            goal=goal,
            previous_results=results,
        )

        # --------------------------------
        # FINISH
        # --------------------------------

        if next_action.get("action") == "finish":

            # Check the latest diagnosis before
            # allowing the agent to claim completion.
            latest_diagnosis = None

            for previous_result in reversed(results):

                if previous_result.get(
                    "tool"
                ) == "diagnose_workflow":

                    latest_diagnosis = previous_result.get(
                        "result",
                        {},
                    )

                    break

            # Do not report completed if unresolved
            # workflow problems still exist.
            if (
                latest_diagnosis is not None
                and latest_diagnosis.get("healthy") is False
            ):
                return {
                    "status": "incomplete",
                    "reason": "Workflow still has unresolved issues",
                    "goal": goal,
                    "steps": len(results),
                    "results": results,
                }

            return {
                "status": "completed",
                "goal": goal,
                "steps": len(results),
                "results": results,
            }

        # --------------------------------
        # PAUSE
        # --------------------------------

        if next_action.get("action") == "pause":
            return {
                "status": "paused",
                "reason": next_action.get(
                    "reason",
                    "Agent execution paused",
                ),
                "retry_after": next_action.get(
                    "retry_after",
                ),
                "results": results,
            }

        # --------------------------------
        # TOOL
        # --------------------------------

        if next_action.get("action") == "tool":

            arguments = next_action.get(
                "arguments",
                {},
            )

            tool_name = next_action.get("tool")

            # --------------------------------
            # INSPECT WORKFLOW
            # --------------------------------

            if (
                tool_name == "inspect_workflow"
                and current_workflow is not None
            ):
                arguments["workflow"] = current_workflow

            # --------------------------------
            # DIAGNOSE WORKFLOW
            # --------------------------------

            if tool_name == "diagnose_workflow":

                workflow_data = None

                # Always diagnose the latest workflow state.
                if current_workflow is not None:
                    workflow_data = current_workflow

                # Fallback: use the latest fixed workflow.
                if workflow_data is None:

                    for previous_result in reversed(results):

                        if previous_result.get(
                            "tool"
                        ) == "fix_workflow":

                            fixed_result = previous_result.get(
                                "result",
                                {},
                            )

                            workflow_data = fixed_result.get(
                                "workflow"
                            )

                            if workflow_data is not None:
                                break

                # Fallback: use the inspected workflow.
                if workflow_data is None:

                    for previous_result in reversed(results):

                        if previous_result.get(
                            "tool"
                        ) == "inspect_workflow":

                            workflow_data = previous_result.get(
                                "result"
                            )

                            if workflow_data is not None:
                                break

                if workflow_data is not None:

                    # Convert Pydantic Workflow into the
                    # dictionary structure expected by
                    # the diagnosis tool.
                    if isinstance(
                        workflow_data,
                        Workflow,
                    ):
                        workflow_data = {
                            "workflow_id": workflow_data.id,
                            "workflow_name": workflow_data.name,
                            "step_count": len(
                                workflow_data.steps
                            ),
                            "steps": [
                                {
                                    "id": step.id,
                                    "name": step.name,
                                    "type": step.type,
                                    "config": step.config,
                                }
                                for step in workflow_data.steps
                            ],
                        }

                    arguments["workflow_data"] = workflow_data

            # --------------------------------
            # FIX WORKFLOW
            # --------------------------------

            if tool_name == "fix_workflow":

                workflow_data = None
                issue = None

                # Get the latest diagnosis.
                for previous_result in reversed(results):

                    if previous_result.get(
                        "tool"
                    ) == "diagnose_workflow":

                        diagnosis = previous_result.get(
                            "result",
                            {},
                        )

                        issues = diagnosis.get(
                            "issues",
                            [],
                        )

                        if issues:
                            issue = issues[0]

                        break

                # Use the current workflow state.
                if current_workflow is not None:

                    workflow_data = {
                        "workflow_id": current_workflow.id,
                        "workflow_name": current_workflow.name,
                        "step_count": len(
                            current_workflow.steps
                        ),
                        "steps": [
                            {
                                "id": step.id,
                                "name": step.name,
                                "type": step.type,
                                "config": step.config,
                            }
                            for step in current_workflow.steps
                        ],
                    }

                if workflow_data is not None:
                    arguments["workflow_data"] = workflow_data

                if issue is not None:
                    arguments["issue"] = issue

            # --------------------------------
            # EXECUTE TOOL
            # --------------------------------

            result = execute_agent_tool(
                tool_name=tool_name,
                arguments=arguments,
            )

            results.append(result)

            # --------------------------------
            # IMMEDIATE HEALTH CHECK
            # --------------------------------

            # If diagnosis confirms that the workflow
            # is healthy, self-healing is complete.
            if (
                tool_name == "diagnose_workflow"
                and result.get(
                    "verification",
                    {},
                ).get("verified")
            ):
                diagnosis_result = result.get(
                    "result",
                    {},
                )

                if diagnosis_result.get(
                    "healthy"
                ) is True:
                    return {
                        "status": "completed",
                        "goal": goal,
                        "steps": len(results),
                        "results": results,
                    }

            # --------------------------------
            # UPDATE WORKFLOW STATE
            # --------------------------------

            if (
                tool_name == "fix_workflow"
                and result.get(
                    "verification",
                    {},
                ).get("verified")
            ):

                fixed_workflow = result.get(
                    "result",
                    {},
                ).get(
                    "workflow"
                )

                if fixed_workflow is not None:

                    # Rebuild the Workflow model from
                    # the fixed workflow dictionary.
                    current_workflow = Workflow(
                        id=fixed_workflow.get(
                            "workflow_id"
                        ),
                        name=fixed_workflow.get(
                            "workflow_name"
                        ),
                        steps=fixed_workflow.get(
                            "steps",
                            [],
                        ),
                    )

    # --------------------------------
    # MAX STEPS
    # --------------------------------

    return {
        "status": "max_steps_reached",
        "goal": goal,
        "steps": len(results),
        "results": results,
    }
