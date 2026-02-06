"""
Automation System
Provides automated operations similar to Claude Desktop
"""

import time
import pyautogui
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import platform


class AutomationAction(Enum):
    """Types of automation actions"""
    CLICK = "click"
    TYPE = "type"
    PRESS_KEY = "press_key"
    MOVE_MOUSE = "move_mouse"
    SCROLL = "scroll"
    SCREENSHOT = "screenshot"
    WAIT = "wait"
    OPEN_APP = "open_app"
    CLOSE_APP = "close_app"


@dataclass
class AutomationStep:
    """Single step in automation"""
    action: AutomationAction
    parameters: Dict[str, Any]
    description: str = ""
    delay_after: float = 0.5  # seconds


@dataclass
class AutomationTask:
    """A complete automation task"""
    name: str
    description: str
    steps: List[AutomationStep]
    repeatable: bool = False


class AutomationEngine:
    """Core automation engine"""
    
    def __init__(self):
        # Safety settings
        pyautogui.FAILSAFE = True  # Move mouse to corner to stop
        pyautogui.PAUSE = 0.5  # Default pause between actions
        self.is_running = False
    
    def execute_step(self, step: AutomationStep) -> bool:
        """Execute a single automation step"""
        try:
            if step.action == AutomationAction.CLICK:
                x = step.parameters.get("x")
                y = step.parameters.get("y")
                clicks = step.parameters.get("clicks", 1)
                button = step.parameters.get("button", "left")
                
                if x is not None and y is not None:
                    pyautogui.click(x, y, clicks=clicks, button=button)
                else:
                    pyautogui.click(clicks=clicks, button=button)
            
            elif step.action == AutomationAction.TYPE:
                text = step.parameters.get("text", "")
                interval = step.parameters.get("interval", 0.05)
                pyautogui.write(text, interval=interval)
            
            elif step.action == AutomationAction.PRESS_KEY:
                key = step.parameters.get("key")
                presses = step.parameters.get("presses", 1)
                pyautogui.press(key, presses=presses)
            
            elif step.action == AutomationAction.MOVE_MOUSE:
                x = step.parameters.get("x")
                y = step.parameters.get("y")
                duration = step.parameters.get("duration", 0.5)
                pyautogui.moveTo(x, y, duration=duration)
            
            elif step.action == AutomationAction.SCROLL:
                clicks = step.parameters.get("clicks", 1)
                pyautogui.scroll(clicks)
            
            elif step.action == AutomationAction.SCREENSHOT:
                region = step.parameters.get("region")
                filepath = step.parameters.get("filepath", "screenshot.png")
                if region:
                    pyautogui.screenshot(filepath, region=region)
                else:
                    pyautogui.screenshot(filepath)
            
            elif step.action == AutomationAction.WAIT:
                duration = step.parameters.get("duration", 1.0)
                time.sleep(duration)
            
            elif step.action == AutomationAction.OPEN_APP:
                app_name = step.parameters.get("app_name")
                self._open_application(app_name)
            
            # Delay after action
            if step.delay_after > 0:
                time.sleep(step.delay_after)
            
            return True
            
        except Exception as e:
            print(f"Error executing step: {e}")
            return False
    
    def execute_task(self, task: AutomationTask, on_progress: Optional[Callable] = None) -> bool:
        """Execute a complete automation task"""
        self.is_running = True
        
        try:
            for i, step in enumerate(task.steps):
                if not self.is_running:
                    return False
                
                if on_progress:
                    on_progress(i, len(task.steps), step.description)
                
                success = self.execute_step(step)
                if not success:
                    return False
            
            return True
            
        except Exception as e:
            print(f"Error executing task: {e}")
            return False
        finally:
            self.is_running = False
    
    def stop(self):
        """Stop current automation"""
        self.is_running = False
    
    def _open_application(self, app_name: str):
        """Open an application (platform-specific)"""
        system = platform.system()
        
        if system == "Windows":
            import subprocess
            subprocess.Popen(app_name)
        elif system == "Darwin":  # macOS
            import subprocess
            subprocess.Popen(["open", "-a", app_name])
        elif system == "Linux":
            import subprocess
            subprocess.Popen([app_name])


class TaskLibrary:
    """Library of pre-defined automation tasks"""
    
    @staticmethod
    def get_common_tasks() -> List[AutomationTask]:
        """Get list of common automation tasks"""
        return [
            AutomationTask(
                name="Take Screenshot",
                description="Take a screenshot of the current screen",
                steps=[
                    AutomationStep(
                        action=AutomationAction.SCREENSHOT,
                        parameters={"filepath": "screenshot.png"},
                        description="Capturing screen"
                    )
                ]
            ),
            AutomationTask(
                name="Copy Text",
                description="Select all and copy text",
                steps=[
                    AutomationStep(
                        action=AutomationAction.PRESS_KEY,
                        parameters={"key": "ctrl+a" if platform.system() != "Darwin" else "command+a"},
                        description="Select all"
                    ),
                    AutomationStep(
                        action=AutomationAction.PRESS_KEY,
                        parameters={"key": "ctrl+c" if platform.system() != "Darwin" else "command+c"},
                        description="Copy"
                    )
                ]
            ),
            AutomationTask(
                name="Search Web",
                description="Open browser and search",
                steps=[
                    AutomationStep(
                        action=AutomationAction.PRESS_KEY,
                        parameters={"key": "ctrl+t" if platform.system() != "Darwin" else "command+t"},
                        description="Open new tab"
                    ),
                    AutomationStep(
                        action=AutomationAction.WAIT,
                        parameters={"duration": 0.5},
                        description="Wait for tab"
                    )
                ]
            )
        ]
    
    @staticmethod
    def create_custom_task(
        name: str,
        description: str,
        steps: List[Dict[str, Any]]
    ) -> AutomationTask:
        """Create a custom automation task"""
        automation_steps = []
        
        for step_data in steps:
            action = AutomationAction[step_data["action"].upper()]
            automation_steps.append(
                AutomationStep(
                    action=action,
                    parameters=step_data.get("parameters", {}),
                    description=step_data.get("description", ""),
                    delay_after=step_data.get("delay_after", 0.5)
                )
            )
        
        return AutomationTask(
            name=name,
            description=description,
            steps=automation_steps
        )


class AutomationAssistant:
    """High-level automation assistant"""
    
    def __init__(self):
        self.engine = AutomationEngine()
        self.library = TaskLibrary()
        self.task_history: List[Dict[str, Any]] = []
    
    def get_available_tasks(self) -> List[str]:
        """Get list of available task names"""
        tasks = self.library.get_common_tasks()
        return [task.name for task in tasks]
    
    def execute_task_by_name(self, task_name: str) -> bool:
        """Execute a task by its name"""
        tasks = self.library.get_common_tasks()
        
        for task in tasks:
            if task.name.lower() == task_name.lower():
                result = self.engine.execute_task(task)
                
                # Record in history
                self.task_history.append({
                    "task_name": task_name,
                    "timestamp": time.time(),
                    "success": result
                })
                
                return result
        
        return False
    
    def suggest_automation(self, context: Dict[str, Any]) -> Optional[str]:
        """Suggest automation based on context"""
        # Simple suggestion logic
        if "activity_type" in context:
            activity = context["activity_type"]
            
            if activity == "coding":
                return "I can help automate code formatting or run tests."
            elif activity == "writing":
                return "I can help with text formatting or grammar checking."
            elif activity == "web_browsing":
                return "I can help automate form filling or data extraction."
        
        return None
    
    def create_macro(
        self,
        name: str,
        description: str,
        recorded_actions: List[Dict[str, Any]]
    ) -> AutomationTask:
        """Create a macro from recorded actions"""
        return self.library.create_custom_task(name, description, recorded_actions)
