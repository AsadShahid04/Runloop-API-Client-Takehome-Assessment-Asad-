#!/usr/bin/env python3
"""
Devbox Operations Script for Runloop API Client Takehome
Task 1.b: Operations on the devbox
"""

import os
import sys
import json
from typing import Dict, Any
from runloop_api_client import Runloop


class DevboxOperations:
    """Class to handle devbox operations for Task 1.b."""
    
    def __init__(self):
        """Initialize the DevboxOperations class."""
        self.config = self._load_config()
        self.api_key = self.config.get("api-key")
        self.devbox_name = self.config.get("devbox-name")
        self.devbox_id = self.config.get("devbox-id")
        
        if not self.api_key:
            raise ValueError("API key not found in answers.json")
        
        # Initialize Runloop client
        self.client = Runloop(
            base_url="https://api.runloop.pro",
            bearer_token=self.api_key
        )
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from answers.json."""
        try:
            with open("answers.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ answers.json not found. Please ensure it exists.")
            sys.exit(1)
        except json.JSONDecodeError:
            print("❌ Invalid JSON in answers.json")
            sys.exit(1)
    
    def list_devboxes(self):
        """List all devboxes to find the one with our name."""
        print("🔍 Listing devboxes to find our devbox...")
        try:
            devboxes = self.client.devboxes.list()
            print(f"Found {len(devboxes)} devboxes:")
            
            for devbox in devboxes:
                print(f"  - {devbox.name} (ID: {devbox.id})")
                if devbox.name == self.devbox_name:
                    print(f"✅ Found our devbox: {devbox.name} (ID: {devbox.id})")
                    self.devbox_id = devbox.id
                    # Update answers.json with the devbox ID
                    self._update_answers_json("devbox-id", devbox.id)
                    return True
            
            print(f"❌ Devbox with name '{self.devbox_name}' not found")
            return False
            
        except Exception as e:
            print(f"❌ Error listing devboxes: {e}")
            return False
    
    def _update_answers_json(self, key: str, value: str):
        """Update answers.json with a new key-value pair."""
        try:
            with open("answers.json", "r") as f:
                data = json.load(f)
            
            data[key] = value
            
            with open("answers.json", "w") as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Updated answers.json: {key} = {value}")
        except Exception as e:
            print(f"❌ Error updating answers.json: {e}")
    
    def copy_resources_to_devbox(self):
        """Copy the resources folder to the devbox."""
        print("📁 Copying resources folder to devbox...")
        try:
            # First, let's try to upload the files individually
            # We'll need to read each file and upload it
            resources_dir = "./resources"
            if not os.path.exists(resources_dir):
                print(f"❌ Resources directory {resources_dir} not found")
                return False
            
            # Upload each file individually
            for filename in os.listdir(resources_dir):
                file_path = os.path.join(resources_dir, filename)
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Upload to devbox
                    result = self.client.devboxes.write_file(
                        devbox_id=self.devbox_id,
                        path=f"/workspace/resources/{filename}",
                        content=content
                    )
                    print(f"✅ Uploaded {filename}: {result}")
            
            return True
        except Exception as e:
            print(f"❌ Error copying resources: {e}")
            return False
    
    def edit_me_txt(self):
        """Edit me.txt and replace the email with the user's own."""
        print("✏️  Editing me.txt file...")
        try:
            # Read the current me.txt content
            with open("resources/me.txt", "r") as f:
                content = f.read()
            
            # Replace the email with the user's own
            new_content = content.replace(
                "asad.shahid@berkeley.edu", 
                "asad.shahid@berkeley.edu"  # This is already correct
            )
            
            # Write the updated content to the devbox
            result = self.client.devboxes.write_file(
                devbox_id=self.devbox_id,
                path="/workspace/resources/me.txt",
                content=new_content
            )
            print(f"✅ me.txt updated successfully: {result}")
            return True
        except Exception as e:
            print(f"❌ Error editing me.txt: {e}")
            return False
    
    def execute_test_script(self, script_name: str = "test.py"):
        """Execute either test.js or test.py on the devbox."""
        print(f"🚀 Executing {script_name} on devbox...")
        try:
            if script_name == "test.py":
                result = self.client.devboxes.execute_command(
                    devbox_id=self.devbox_id,
                    command="python3 /workspace/resources/test.py"
                )
            elif script_name == "test.js":
                result = self.client.devboxes.execute_command(
                    devbox_id=self.devbox_id,
                    command="node /workspace/resources/test.js"
                )
            else:
                print(f"❌ Unsupported script: {script_name}")
                return False
            
            print(f"✅ {script_name} executed successfully")
            print(f"Output: {result.output}")
            return True
        except Exception as e:
            print(f"❌ Error executing {script_name}: {e}")
            return False
    
    def run_all_operations(self):
        """Run all required operations for Task 1.b."""
        print("🚀 Starting Task 1.b: Operations on the devbox")
        print("=" * 50)
        
        # Step 0: Get devbox ID if we don't have it
        if not self.devbox_id or self.devbox_id == "YOUR_DEVBOX_ID":
            if not self.list_devboxes():
                print("❌ Could not find devbox. Stopping.")
                return False
        
        # Step 1: Copy resources
        if not self.copy_resources_to_devbox():
            print("❌ Failed to copy resources. Stopping.")
            return False
        
        # Step 2: Edit me.txt
        if not self.edit_me_txt():
            print("❌ Failed to edit me.txt. Stopping.")
            return False
        
        # Step 3: Execute test script (default to test.py)
        if not self.execute_test_script("test.py"):
            print("❌ Failed to execute test script. Stopping.")
            return False
        
        print("=" * 50)
        print("✅ Task 1.b completed successfully!")
        return True


def main():
    """Main function to run the devbox operations."""
    try:
        operations = DevboxOperations()
        operations.run_all_operations()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 