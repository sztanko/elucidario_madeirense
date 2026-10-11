def generate_mermaid_graph(workflow):
    lines = ["graph TD"]
    step_names = {step.name for step in workflow}
    for step in workflow:
        for dep in step.depends_on:
            if dep in step_names:
                lines.append(f"    {dep} --> {step.name}")
        if not step.depends_on:
            lines.append(f"    {step.name}")
    return "\n".join(lines)
