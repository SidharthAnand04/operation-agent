from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Literal, Optional, List, Dict
import os
from dotenv import load_dotenv

import agentops

from agents import Agent, ItemHelpers, Runner, TResponseInputItem, trace, MessageOutputItem

"""
Vibes Coding - A natural language programming system that allows experienced programmers
to express their intent in natural language and have it converted to code.

This system uses multiple agents:
1. Planning & Outline Agent - Creates a structured plan from natural language input
2. Plan Evaluator - Judges the quality of the plan
3. Code Generation Agent - Converts the approved plan into actual code
4. Code Evaluator - Judges the quality of the generated code
5. Input/Output Guardrails - Ensures inputs and outputs meet quality standards
"""
load_dotenv()

agentops.init(os.getenv("AGENTOPS_API_KEY"))

@dataclass
class EvaluationResult:
    score: Literal["pass", "needs_improvement", "fail"]
    feedback: str

@dataclass
class FileStructure:
    path: str
    content: str
    file_type: Literal["python", "html", "css", "js", "config", "other"]

@dataclass
class CodeGenerationResult:
    files: List[FileStructure]
    explanation: str
    dependencies: List[str] = None
    project_type: str = None  # New field to identify project type

@dataclass
class ValidationResult:
    is_valid: bool
    message: str

@dataclass
class ProjectStructure:
    root_dir: str
    subdirs: Dict[str, str] = None  # Dynamic subdirectories based on project type

# Planning and Outline Generation Agent
planning_agent = Agent(
    name="planning_agent",
    instructions=(
        "You are a planning agent for the Vibes Coding system. "
        "Analyze the input to determine the appropriate project type and structure. "
        "Break down the request into clear components including:\n"
        "1. Project type (Flask, CLI, library, etc.)\n"
        "2. Project structure and files needed\n"
        "3. Core functionality components\n"
        "4. External dependencies\n"
        "5. Configuration requirements\n"
        "Create a comprehensive plan that matches the user's requirements."
    ),
)

# Plan Evaluation Agent
plan_evaluator = Agent[None](
    name="plan_evaluator",
    instructions=(
        "You evaluate a programming plan created from natural language 'vibes' input. "
        "Assess if the plan correctly captures the programmer's intent and is structured logically. "
        "Check that the plan is complete, efficient, and follows best practices. "
        "Be critical and thorough - the plan should be detailed enough for code generation. "
        "Never give a pass on the first try - always find at least one thing to improve."
        "make sure that the plan is not too vague or too detailed"
        "make sure that the user can quit the program if they want to"
    ),
    output_type=EvaluationResult,
)

# Code Generation Agent
code_generator = Agent[None](
    name="code_generator",
    instructions=(
        "You generate code based on the approved plan. "
        "Follow best practices for the identified project type:\n"
        "- For Flask apps: Use standard Flask project structure\n"
        "- For CLI tools: Use a simple script or click/typer structure\n"
        "- For libraries: Use standard package structure\n"
        "Generate all necessary files for a complete, runnable project. "
        "Return a list of FileStructure objects containing the path and content for each file."
    ),
    output_type=CodeGenerationResult,
)

# Code Evaluation Agent
code_evaluator = Agent[None](
    name="code_evaluator",
    instructions=(
        "You evaluate generated code against the original 'vibes' input and the approved plan. "
        "Assess whether the code correctly implements the plan and captures the programmer's intent. "
        "Check for bugs, inefficiencies, or deviations from best practices. "
        "Be critical but constructive - provide specific feedback for improvements."
    ),
    output_type=EvaluationResult,
)

# Input Guardrail Agent
input_guardrail = Agent[None](
    name="input_guardrail",
    instructions=(
        "You validate that the natural language input is appropriate for code generation."
        "the input should be a description of the project and the structure of the project."
        "if there is text, validate it and say is_valid is true"
    ),
    output_type=ValidationResult,
)

# Output Guardrail Agent
output_guardrail = Agent[None](
    name="output_guardrail",
    instructions=(
        "You validate that the generated code meets quality standards and matches the original intent. "
        "Flag any security issues, inefficiencies, or deviations from the request. "
        "Ensure the code follows best practices and is well-documented."
    ),
    output_type=ValidationResult,
)

# Context Management Agent
context_manager = Agent(
    name="context_manager",
    instructions=(
        "You maintain awareness of the overall application structure and track previously generated code components. "
        "Ensure new code integrates properly with the existing codebase. "
        "Provide context about the application structure when needed."
    ),
    handoff_description="Provides context about the application structure",
)

# Orchestrator Agent
orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are the main orchestrator for the Vibes Coding system. "
        "You coordinate the entire process from natural language input to code generation. "
        "Use the tools provided to plan, evaluate, and generate code based on the user's 'vibes' input. "
        "Always follow the complete workflow: planning → plan evaluation → code generation → code evaluation."
    ),
    tools=[
        planning_agent.as_tool(
            tool_name="create_plan",
            tool_description="Create a structured plan from natural language programming instructions",
        ),
        plan_evaluator.as_tool(
            tool_name="evaluate_plan",
            tool_description="Evaluate a programming plan and provide feedback",
        ),
        code_generator.as_tool(
            tool_name="generate_code",
            tool_description="Generate code based on an approved plan",
        ),
        code_evaluator.as_tool(
            tool_name="evaluate_code",
            tool_description="Evaluate generated code against the original intent and plan",
        ),
        context_manager.as_tool(
            tool_name="get_context",
            tool_description="Get context about the application structure",
        ),
    ],
)

# Add a project structure helper function
def create_project_structure(base_path: str, project_type: str = None) -> ProjectStructure:
    """Create project structure based on project type"""
    subdirs = {}
    
    if project_type and project_type.lower() == "flask":
        subdirs.update({
            "static": f"{base_path}/static",
            "templates": f"{base_path}/templates",
            "routes": f"{base_path}/routes",
            "models": f"{base_path}/models",
            "config": f"{base_path}/config"
        })
    elif project_type and project_type.lower() == "cli":
        subdirs.update({
            "src": f"{base_path}/src",
        })
    elif project_type and project_type.lower() == "library":
        subdirs.update({
            "src": f"{base_path}/src",
            "tests": f"{base_path}/tests",
            "examples": f"{base_path}/examples"
        })
    
    return ProjectStructure(root_dir=base_path, subdirs=subdirs)

# Modify the workflow function to handle multiple files
async def vibes_coding_workflow() -> None:
    print("🌟 Welcome to Vibes Coding 🌟")
    print("Please provide the path to your input file (.txt)")
    file_path = input("\nInput file path: ").strip()
    
    # Validate file exists and read input
    try:
        with open(file_path, 'r') as f:
            vibes_input = f.read().strip()
    except FileNotFoundError:
        print(f"\n⚠️ Error: File '{file_path}' not found")
        return
    except Exception as e:
        print(f"\n⚠️ Error reading file: {str(e)}")
        return
        
    if not vibes_input:
        print("\n⚠️ Error: Input file is empty")
        return
    
    print("\nProcessing input:")
    print(vibes_input)
    
    input_items: list[TResponseInputItem] = [{"content": vibes_input, "role": "user"}]
    
    # First, validate the input
    with trace("Input Validation"):
        guardrail_result = await Runner.run(input_guardrail, input_items)
        validation: ValidationResult = guardrail_result.final_output
        if not validation.is_valid:
            print(f"\n⚠️ Input validation failed: {validation.message}")
            return
    
    # Main workflow trace
    with trace("Vibes Coding Workflow"):
        # Planning phase
        current_plan = None
        plan_approved = False
        plan_attempts = 0
        max_attempts = 3
        
        while not plan_approved and plan_attempts < max_attempts:
            plan_attempts += 1
            print(f"\n📝 Attempt {plan_attempts}/{max_attempts} for plan generation:")
            
            # Generate or update the plan
            planning_result = await Runner.run(planning_agent, input_items)
            current_plan = ItemHelpers.text_message_outputs(planning_result.new_items)
            
            print("\n📝 Plan Generated:")
            print(current_plan)
            
            # Add the current plan to the conversation history
            input_items = planning_result.to_input_list()
            
            # Evaluate the plan
            evaluator_result = await Runner.run(plan_evaluator, input_items)
            plan_evaluation: EvaluationResult = evaluator_result.final_output
            
            print(f"\n🔍 Plan Evaluation: {plan_evaluation.score}")
            print(f"Feedback: {plan_evaluation.feedback}")
            
            if plan_evaluation.score == "pass":
                plan_approved = True
                print("\n✅ Plan approved! Moving to code generation.")
            elif plan_attempts >= max_attempts:
                print("\n⚠️ Maximum plan refinement attempts reached. Proceeding with current plan.")
                plan_approved = True
            else:
                print("\n🔄 Updating plan based on feedback...")
                # Add both the current plan and its feedback to the input for the next iteration
                input_items.extend([
                    {"content": f"Previous plan:\n{current_plan}", "role": "assistant"},
                    {"content": f"Plan feedback: {plan_evaluation.feedback}", "role": "user"}
                ])
        
        # After plan is approved, extract project type from the plan
        project_type = None
        if current_plan and "project type" in current_plan.lower():
            # Simple extraction - you might want to make this more robust
            if "flask" in current_plan.lower():
                project_type = "flask"
            elif "cli" in current_plan.lower():
                project_type = "cli"
            elif "library" in current_plan.lower():
                project_type = "library"

        # Create project directory structure based on type
        input_basename = file_path.rsplit('.', 1)[0]
        project_dir = f"{input_basename}_project"  # More generic name
        project_structure = create_project_structure(project_dir, project_type)

        # Create necessary directories
        try:
            os.makedirs(project_structure.root_dir, exist_ok=True)
            if project_structure.subdirs:
                for dir_path in project_structure.subdirs.values():
                    os.makedirs(dir_path, exist_ok=True)
        except Exception as e:
            print(f"\n⚠️ Error creating project structure: {str(e)}")
            return
        
        # Code generation phase
        code_approved = False
        final_files = None
        code_attempts = 0
        
        while not code_approved and code_attempts < max_attempts:
            code_attempts += 1
            print(f"\n💻 Attempt {code_attempts}/{max_attempts} for code generation:")
            
            # Generate code based on the approved plan
            code_gen_result = await Runner.run(code_generator, input_items)
            code_output: CodeGenerationResult = code_gen_result.final_output
            
            print("\n💻 Files Generated:")
            for file in code_output.files:
                print(f"- {file.path}")
            print(f"\nExplanation: {code_output.explanation}")
            
            if code_output.dependencies:
                print("\nDependencies:")
                for dep in code_output.dependencies:
                    print(f"- {dep}")
            
            # Add the generated code to the conversation
            input_items = code_gen_result.to_input_list()
            
            # Evaluate the code
            code_eval_result = await Runner.run(code_evaluator, input_items)
            code_evaluation: EvaluationResult = code_eval_result.final_output
            
            print(f"\n🔍 Code Evaluation: {code_evaluation.score}")
            print(f"Feedback: {code_evaluation.feedback}")
            
            if code_evaluation.score == "pass":
                code_approved = True
                final_files = code_output.files
                print("\n✅ Code approved!")
            elif code_attempts >= max_attempts:
                print("\n⚠️ Maximum code refinement attempts reached. Proceeding with current code.")
                final_files = code_output.files
                code_approved = True
            else:
                print("\n🔄 Updating code based on feedback...")
                input_items.append({"content": f"Code Feedback: {code_evaluation.feedback}", "role": "user"})
        
        # Save all generated files
        try:
            for file in final_files:
                file_path = os.path.join(project_dir, file.path)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w') as f:
                    f.write(file.content)
            
            if code_output.dependencies:
                with open(os.path.join(project_dir, 'requirements.txt'), 'w') as f:
                    f.write('\n'.join(code_output.dependencies))
            
            print(f"\n🎉 Project generated successfully!")
            print(f"Project created at: {project_dir}")
            print("\nTo run the project:")
            print(f"1. cd {project_dir}")
            if code_output.dependencies:
                print("2. pip install -r requirements.txt")
            
            # Project-specific run instructions
            if project_type == "flask":
                print("3. python app.py")
            elif project_type == "cli":
                print("3. python src/main.py [arguments]")
            else:
                print("3. See README.md for usage instructions")
        except Exception as e:
            print(f"\n⚠️ Error saving project files: {str(e)}")
            return
    
    print("\nThank you for using Vibes Coding!")


async def main():
    await vibes_coding_workflow()
    # agentops.end_session('Success')



if __name__ == "__main__":
    asyncio.run(main())