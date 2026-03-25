import os
import sys
import time
import logging
import shutil
from pathlib import Path
from datetime import datetime, timezone
from bytez import Bytez
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
log_level = logging.DEBUG if DEBUG_MODE else logging.INFO

logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/orchestrator_bronze.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BronzeOrchestrator:
    """Production-grade Bronze Tier AI Employee Orchestrator"""
    
    def __init__(self, vault_path: str = "./obsidian_vault"):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / "Inbox"
        self.needs_action = self.vault_path / "Needs_Action"
        self.plans = self.vault_path / "Plans"
        self.done = self.vault_path / "Done"
        self.errors = self.vault_path / "Errors"
        self.skills_dir = self.vault_path / "Skills"
        
        # Core Files
        self.dashboard_file = self.vault_path / "Dashboard.md"
        self.handbook_file = self.vault_path / "Company_Handbook.md"
        
        # Security Requirements
        self.api_key = os.getenv('BYTEZ_API_KEY')
        if not self.api_key:
            logger.warning("BYTEZ_API_KEY not found in environment variables. Set it to run the AI features.")
        else:
            self.bytez = Bytez(self.api_key)
            
        self.model_name = "anthropic/claude-haiku-4-5"
        
        # Verify Constraints & Create Boilerplate Files
        self._ensure_directories()
        self._ensure_required_files()
        
        # Load Bronze Tier rules and skills
        self.handbook_content = self.handbook_file.read_text(encoding='utf-8')
        
        # Caching
        self.cache = {}
        
        logger.info(f"🥉 Bronze Tier AI Employee Orchestrator Initialized")
        if self.api_key:
            logger.info(f"   Model: {self.model_name}")
        self._update_dashboard()
    
    def _ensure_directories(self):
        """Ensure Hackathon requested filesystem structure strictly exists."""
        for folder in [self.inbox, self.needs_action, self.plans, self.done, self.errors, self.skills_dir, Path("logs")]:
            folder.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured folder exists: {folder}")
            
    def _ensure_required_files(self):
        """Auto-create required Dashboard, Handbook, and Skills if missing."""
        # 1. Dashboard
        if not self.dashboard_file.exists():
            self._update_dashboard(initial=True)
            logger.info("Created default Dashboard.md")
            
        # 2. Company Handbook
        if not self.handbook_file.exists():
            handbook_content = """# Company Handbook

## System Role & Behavior
- You are an autonomous AI employee. You act independently but strictly within these bounds.
- **Tone Guidelines**: Always maintain a professional, concise, and helpful tone.
- **Safety First**: Engage in ZERO harmful, destructive, or unsafe actions.
- **Assumptions**: Ask for clarification if user instructions are fundamentally unclear or missing critical paths.

## Approval Guidelines
- Any action modifying sensitive data or sending outwards communications requires explicit Human-In-The-Loop approval.

## Task Handling Instructions
- When receiving a task, strictly follow the provided output structure. 
- Ensure plans are actionable and logical.
"""
            self.handbook_file.write_text(handbook_content, encoding='utf-8')
            logger.info("Created Company_Handbook.md")
            
        # 3. Default Planning Skill
        planning_skill = self.skills_dir / "planning_skill.md"
        if not planning_skill.exists():
            skill_content = """# Skill: Planning

## Purpose
To break down complex or vague operational requests into clear, actionable steps.

## Input Format
Raw unstructured text or task descriptions containing specific goals and constraints.

## Output Format
A structured markdown action plan containing Objectives, Steps, and Notes.

## Instructions for AI
1. Read and analyze the core goal of the input request.
2. Outline exactly 3 to 5 logical, sequential steps to resolve the task.
3. Ensure every single step is actionable, distinct, and clearly defined.
4. Output the result perfectly formatted as per the system's requested markdown layout.
"""
            planning_skill.write_text(skill_content, encoding='utf-8')
            logger.info("Created default planning_skill.md in Skills/")

        # 4. Marketing Skill
        marketing_skill = self.skills_dir / "marketing_skill.md"
        if not marketing_skill.exists():
            marketing_content = """# Skill: Marketing

## Purpose
To generate creative and structured marketing campaigns or ideas based on a given topic.

## Input Format
Topic, target audience, or raw idea that needs to be expanded into a marketing plan.

## Output Format
A structured markdown action plan containing Objectives, Steps, and Notes focused on marketing execution.

## Instructions for AI
1. Analyze the input to understand the core marketing goals and target audience.
2. Formulate 3 to 5 clear marketing steps (e.g., channel selection, content creation, distribution).
3. Ensure the tone is engaging but professional.
4. Provide the final output adhering perfectly to the standardized plan format.
"""
            marketing_skill.write_text(marketing_content, encoding='utf-8')
            logger.info("Created default marketing_skill.md in Skills/")

    def _update_dashboard(self, initial=False):
        """Update system overview and activity tracking in Dashboard.md."""
        try:
            pending = len(self.check_needs_action())
            completed = len(list(self.done.glob("*.*"))) - len(list(self.done.glob(".gitkeep")))
            inbox_count = len(list(self.inbox.glob("*.*"))) - len(list(self.inbox.glob(".gitkeep")))
            error_count = len(list(self.errors.glob("*.*"))) - len(list(self.errors.glob(".gitkeep")))
            
            content = f"""# AI Employee Dashboard

**Last Updated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
**Last Run:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

## System Overview
- **Inbox (/Inbox)**: {inbox_count} file(s) pending triage
- **Pending Tasks (/Needs_Action)**: {pending} file(s) waiting for AI Processing
- **Completed Tasks (/Done)**: {completed} file(s) finalized
- **Errors (/Errors)**: {error_count} file(s) failed processing

## Recent Activity
- Monitoring `Inbox/` for new raw tasks.
- Processing tasks linearly from `Needs_Action/`.
- Dead-Letter Queue (DLQ) actively catching failures in `Errors/`.
- Background orchestrator active: YES
"""
            self.dashboard_file.write_text(content, encoding='utf-8')
        except Exception as e:
            logger.error(f"Failed to update dashboard: {e}")

    def _trigger_inbox_to_needs_action(self):
        """Move any newly arrived tasks in Inbox/ straight to Needs_Action/ implicitly filtering invalid files."""
        inbox_files = list(self.inbox.iterdir())
        if not inbox_files:
            return

        for task_file in inbox_files:
            # Safe File Filter
            if task_file.name.startswith('.') or task_file.suffix not in ['.md', '.txt']:
                continue

            try:
                dest = self.needs_action / task_file.name
                shutil.move(str(task_file), str(dest))
                logger.info(f"Pipeline: Moved task {task_file.name} to Needs_Action/")
            except Exception as e:
                logger.error(f"Failed to move {task_file.name} to Needs_Action/: {e}")

    def _detect_relevant_skills(self, task_content: str) -> str:
        """Analyze task and pull in relevant skill contexts based on folder/files."""
        task_lower = task_content.lower()
        skills_added = []
        context = ""
        
        for skill_file in self.skills_dir.glob("*.md"):
            name = skill_file.stem.lower().replace("_skill", "")
            # If the skill name (like 'planning', 'marketing') is in the text, or default to 'planning'
            if name in task_lower or name == "planning":
                try:
                    skill_text = skill_file.read_text(encoding='utf-8')
                    context += f"\n\n--- SKILL DEFINITION: {skill_file.name} ---\n{skill_text}"
                    skills_added.append(skill_file.name)
                except Exception as e:
                    logger.warning(f"Could not read skill file {skill_file}: {e}")
                    
        if skills_added:
            logger.info(f"Context enriched with skills: {', '.join(skills_added)}")
        else:
            logger.debug("No specific skills detected. Using general logic.")
            
        return context
    
    def _parse_response(self, result) -> str:
        """Safely extract text from multiple possible Bytez response formats."""
        try:
            error_msg = getattr(result, 'error', None)
            if error_msg:
                logger.error(f"Bytez API Error: {error_msg}")

            output = getattr(result, 'output', result)
            if not output: return ""
            
            content = None
            if isinstance(output, dict):
                content = output.get('content')
                provider = getattr(result, 'provider', None) or output.get('provider', {})
                usage = provider.get('usage', {}) if isinstance(provider, dict) else {}
                if usage:
                    logger.info(f"Token usage: Input={usage.get('input_tokens', 0)}, Output={usage.get('output_tokens', 0)}")
                elif 'usage' in output:
                    logger.info(f"Token usage: Input={output['usage'].get('prompt_tokens', 0)}, Output={output['usage'].get('completion_tokens', 0)}")
            else:
                content = output

            if isinstance(content, str): return content.strip()
            elif isinstance(content, list):
                text_parts = [item['text'] if isinstance(item, dict) and 'text' in item else str(item) for item in content]
                return " ".join(text_parts).strip()
            return str(content).strip()

        except Exception as e:
            logger.error(f"Error parsing response: {e}")
            return ""

    def _call_bytez_api(self, system_prompt: str, user_prompt: str, max_retries: int = 3) -> str:
        """Reliable API wrapper loop with automated exponential backoff."""
        if not hasattr(self, 'bytez'):
            logger.error("Bytez client not initialized. Cannot process task.")
            return ""
            
        model = self.bytez.model(self.model_name)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        for attempt in range(1, max_retries + 1):
            try:
                logger.debug(f"API Request (Attempt {attempt}/{max_retries}) using {self.model_name}")
                result = model.run(messages)
                
                response_text = self._parse_response(result)
                if response_text:
                    logger.info("API Response received and successfully parsed.")
                    return response_text
                else:
                    logger.warning(f"Empty content received on attempt {attempt}.")
                    
            except Exception as e:
                logger.error(f"API Request failed on attempt {attempt}: {e}")
                
            if attempt < max_retries:
                sleep_time = 2 ** attempt
                logger.info(f"Waiting {sleep_time}s before retrying...")
                time.sleep(sleep_time)
                
        # Skip task if complete repeated failure occurs
        logger.error("All API retries exhausted. Returning empty to trigger failure.")
        return ""

    def _generate_plan(self, task_file: Path, task_content: str) -> str | None:
        """Use the LLM to analyze the task and output the perfectly structured plan."""
        task_id = task_file.stem
        
        relevant_skills_context = self._detect_relevant_skills(task_content)

        system_prompt = f"""You are an autonomous AI employee. 

COMPANY RULES AND GUIDELINES (From Company_Handbook.md):
{self.handbook_content}

YOUR AVAILABLE SKILLS:
{relevant_skills_context}

CRITICAL OUTPUT REQUIREMENT:
You MUST generate a structured 3-5 step action plan exactly matching the format below. Do NOT output anything else before or after the plan. Do NOT wrap it in a code block.

---
# Plan

## Objective
[Write 1-2 concise sentences summarizing what you will achieve]

## Steps
- [ ] [Step 1 description]
- [ ] [Step 2 description]
- [ ] [Step 3 description]

## Notes
[Add any relevant observations, considerations, or warnings here]

---
"""
        
        response_text = self._call_bytez_api(system_prompt, task_content)
        if not response_text:
            return None

        # Clean any accidental conversational artifacts or code blocks
        response_text = response_text.replace("```markdown\\n", "").replace("```\\n", "").replace("```", "").strip()

        # Output Validation
        if "## Steps" not in response_text:
            logger.error("Invalid AI output format")
            return None

        # Add tracking metadata frontmatter
        plan = f"""---
task_id: {task_id}
created: {datetime.now(timezone.utc).isoformat()}
tier: bronze
model: {self.model_name}
---

{response_text}
"""
        return plan

    def _handle_failure(self, task_file: Path, reason: str):
        """Move failed files to DLQ and log appropriately."""
        logger.error(f"Task failure: {task_file.name}. Reason: {reason}")
        try:
            error_file = self.errors / f"{task_file.name}"
            shutil.move(str(task_file), str(error_file))
            logger.info(f"Task moved to DLQ (/Errors/): {error_file.name}")
        except Exception as e:
            logger.error(f"Failed to move damaged task {task_file.name} to /Errors/: {e}")
        self._update_dashboard()

    def _archive_task(self, task_file: Path):
        """Move the processed task to the Done folder archive."""
        try:
            done_file = self.done / task_file.name
            shutil.move(str(task_file), str(done_file))
            logger.info(f"Task successfully archived to Done/: {done_file.name}")
        except Exception as e:
            logger.error(f"Failed to archive task {task_file.name}: {e}")

    def _save_plan(self, task_id: str, plan_content: str) -> bool:
        """Save the generated result back to the Obsidian Vault."""
        try:
            plan_file = self.plans / f"{task_id}_plan.md"
            plan_file.write_text(plan_content, encoding='utf-8')
            logger.info(f"Output saved safely to vault at Plans/: {plan_file.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to save output for task {task_id}: {e}")
            return False

    def process_task(self, task_file: Path) -> bool:
        """Core AI Processing pipeline: Read -> Process -> Write -> Move Loop."""
        logger.info(f"Task started: {task_file.name}")
        
        try:
            task_content = task_file.read_text(encoding='utf-8')
            
            # 1. Empty File Check
            if not task_content.strip():
                self._handle_failure(task_file, "File is empty or contains only whitespace")
                return False

            # 2. File Size Limit (Token Safety)
            if len(task_content) > 10000:
                self._handle_failure(task_file, "File too large (exceeds 10,000 characters limit)")
                return False

            logger.info(f"Task read successfully ({len(task_content)} characters).")
            
            plan = self._generate_plan(task_file, task_content)
            
            # 3. Output validation & Failure Handling
            if plan and self._save_plan(task_file.stem, plan):
                self._archive_task(task_file)
                logger.info(f"Task success: {task_file.name}")
                self._update_dashboard()
                return True
            else:
                # E.g. API completely retried 3 times and failed, or invalid format
                self._handle_failure(task_file, "AI processing failed or invalid output format generated")
                return False
                
        except Exception as e:
            self._handle_failure(task_file, f"Critical processing exception: {e}")
            return False

    def check_needs_action(self):
        """Scan Needs_Action/ for tasks ready for AI processing while safely ignoring system files."""
        valid_tasks = []
        for task in self.needs_action.iterdir():
            if not task.name.startswith('.') and task.suffix in ['.md', '.txt']:
                valid_tasks.append(task)
        return valid_tasks

    def run_cycle(self):
        """Single orchestration workflow cycle executing the required pipeline."""
        # 1. Pipeline: Check Inbox and move to Needs_Action automatically
        self._trigger_inbox_to_needs_action()
        
        # 2. Process tasks from Needs_Action
        new_tasks = self.check_needs_action()
        if new_tasks:
            logger.info(f"Found {len(new_tasks)} task(s) in Needs_Action/")
            for task_file in new_tasks[:1]:  # Process single task per cycle 
                self.process_task(task_file)
        else:
            logger.debug("No new tasks to process in Needs_Action/")
            
        self._update_dashboard()
        
    def start(self):
        """Start the orchestrator continuous watcher loop."""
        logger.info("🥉 BRONZE TIER AI EMPLOYEE ACTIVE")
        logger.info("Press Ctrl+C to stop.\n")
        
        while True:
            try:
                self.run_cycle()
                time.sleep(15)
            except KeyboardInterrupt:
                logger.info("\n🛑 Orchestrator stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(15)


if __name__ == "__main__":
    orchestrator = BronzeOrchestrator()
    orchestrator.start()
