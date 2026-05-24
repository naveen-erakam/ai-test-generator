import json


def parse_to_robot_format(test_cases: dict) -> str:
    """Converts generated JSON test cases into Robot Framework test file format."""
    lines = ["*** Settings ***",
             "Documentation    Auto-generated test cases by AI Test Generator",
             "Library    SeleniumLibrary", "",
             "*** Test Cases ***"]

    for tc in test_cases.get("test_cases", []):
        lines.append(f"{tc['id']} - {tc['title']}")
        lines.append(f"    [Documentation]    {tc['expected_result']}")
        lines.append(f"    [Tags]    {tc['type']}    {tc['priority']}    " +
                     "    ".join(tc.get("tags", [])))
        for step in tc.get("steps", []):
            lines.append(f"    Log    {step}")
        lines.append("")

    return "\n".join(lines)


def parse_to_pytest_format(test_cases: dict) -> str:
    """Converts generated JSON test cases into Pytest test file format."""
    lines = ['import pytest', '', '', f'class Test{test_cases["feature"].replace(" ", "")}:']

    for tc in test_cases.get("test_cases", []):
        method_name = tc["id"].lower() + "_" + tc["title"][:40].replace(" ", "_").replace("-", "_")
        lines.append(f'')
        lines.append(f'    def test_{method_name}(self):')
        lines.append(f'        """')
        lines.append(f'        {tc["title"]}')
        lines.append(f'        Type: {tc["type"]} | Priority: {tc["priority"]}')
        lines.append(f'        Expected: {tc["expected_result"]}')
        lines.append(f'        """')
        lines.append(f'        # TODO: Implement test steps')
        lines.append(f'        pass')

    return "\n".join(lines)
