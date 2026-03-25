"""
Filesystem Watcher - BRONZE TIER
Monitors obsidian_vault/Inbox/ and moves files to Needs_Action/

Bronze Tier Flow:
1. User drops file in /Inbox
2. Watcher detects it
3. Creates markdown task in /Needs_Action
4. Orchestrator processes from there

Simple, clean, minimal.
"""

import os
import time
import logging
from pathlib import Path
from datetime import datetime, timezone
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BronzeFilesystemWatcher(FileSystemEventHandler):
    """Watches Inbox/ and moves files to Needs_Action/"""
    
    def __init__(self, vault_path: str = "./obsidian_vault"):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / "Inbox"
        self.needs_action = self.vault_path / "Needs_Action"
        
        # Ensure directories exist
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.needs_action.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🥉 Bronze Tier Filesystem Watcher initialized")
        logger.info(f"   Monitoring: {self.inbox}")
        logger.info(f"   Output: {self.needs_action}")
    
    def on_created(self, event):
        """Handle new file in Inbox - move to Needs_Action"""
        if event.is_directory:
            return
        
        file_path = Path(str(event.src_path))
        
        # Ignore hidden files and system files
        if file_path.name.startswith('.') or file_path.name.startswith('~'):
            return
        
        # Ignore temporary files
        if file_path.name.endswith('.tmp') or file_path.name.endswith('.swp'):
            return
        
        logger.info(f"📄 New file in Inbox: {file_path.name}")
        
        try:
            # Wait for file to be fully written (stability check)
            time.sleep(1.0)
            
            # Verify file still exists
            if not file_path.exists():
                logger.warning(f"File {file_path.name} disappeared before processing")
                return
            
            # Check file size stability (wait up to 3 seconds)
            prev_size = -1
            current_size = file_path.stat().st_size
            
            for _ in range(3):
                if current_size == prev_size:
                    break
                prev_size = current_size
                time.sleep(0.5)
                if file_path.exists():
                    current_size = file_path.stat().st_size
                else:
                    return
            
            # Read file content
            try:
                content = file_path.read_text(encoding='utf-8')
                # Truncate large files
                if len(content) > 50000:
                    logger.warning(f"File {file_path.name} is large ({len(content)} chars), truncating to 50KB")
                    content = content[:50000] + "\n\n[... Content truncated at 50KB ...]"
            except UnicodeDecodeError:
                content = f"[Binary file - {file_path.stat().st_size} bytes]\n\nCannot display content (not a text file)"
            
            # Create task filename
            timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
            task_filename = f"{file_path.stem}_{timestamp}.md"
            task_file = self.needs_action / task_filename
            
            # Create simple task document for Needs_Action
            task_content = f"""# Task: {file_path.name}

**Created:** {datetime.now(timezone.utc).isoformat()}  
**Original File:** {file_path.name}  
**Size:** {file_path.stat().st_size} bytes  
**Type:** {file_path.suffix or 'text'}

---

## Content

{content}

---

## Instructions for AI

Please analyze this content and create a detailed action plan (3-5 steps).
"""
            
            # Write task file to Needs_Action
            task_file.write_text(task_content, encoding='utf-8')
            
            logger.info(f"✅ Task created in Needs_Action: {task_filename}")
            
            # Remove from Inbox (Bronze Tier: clean transfer)
            file_path.unlink()
            logger.info(f"📦 Removed from Inbox: {file_path.name}")
            
        except Exception as e:
            logger.error(f"Error processing file {file_path.name}: {e}")
    
    def start(self):
        """Start watching the Inbox folder"""
        observer = Observer()
        observer.schedule(self, str(self.inbox), recursive=False)
        observer.start()
        
        logger.info(f"")
        logger.info(f"👀 Monitoring: {self.inbox}")
        logger.info(f"📤 Output: {self.needs_action}")
        logger.info(f"")
        logger.info(f"🥉 BRONZE TIER - Drop files in Inbox/ to create tasks")
        logger.info(f"Press Ctrl+C to stop")
        logger.info(f"")
        
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            observer.stop()
            logger.info("\n🛑 Filesystem watcher stopped")
        
        observer.join()


if __name__ == "__main__":
    watcher = BronzeFilesystemWatcher()
    watcher.start()
