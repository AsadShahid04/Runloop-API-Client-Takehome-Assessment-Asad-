#!/usr/bin/env python3
"""
Blueprint Creation Script for Runloop API Client Takehome
Task 2: Create blueprint with cowsay installed
"""

import os
import sys
import json
from typing import Dict, Any
from runloop_api_client import Runloop


class BlueprintCreator:
    """Class to handle blueprint creation for Task 2."""
    
    def __init__(self):
        """Initialize the BlueprintCreator class."""
        self.config = self._load_config()
        self.api_key = self.config.get("api-key")
        
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
    
    def create_blueprint(self):
        """Create a blueprint with cowsay installed."""
        print("🔧 Creating blueprint with cowsay...")
        try:
            # Create blueprint with cowsay installation
            blueprint = self.client.blueprints.create(
                name="cowsay-blueprint",
                description="Blueprint with cowsay utility installed",
                # Add installation commands for cowsay
                commands=[
                    "apt-get update",
                    "apt-get install -y cowsay"
                ]
            )
            
            print(f"✅ Blueprint created successfully!")
            print(f"  Name: {blueprint.name}")
            print(f"  ID: {blueprint.id}")
            
            # Update answers.json
            self._update_answers_json("blueprint-name", blueprint.name)
            self._update_answers_json("blueprint-id", blueprint.id)
            
            return blueprint
            
        except Exception as e:
            print(f"❌ Error creating blueprint: {e}")
            return None
    
    def boot_devbox_from_blueprint(self, blueprint_id: str):
        """Boot a devbox from the created blueprint."""
        print("🚀 Booting devbox from blueprint...")
        try:
            devbox = self.client.devboxes.create(
                name="cowsay-test-devbox",
                blueprint_id=blueprint_id
            )
            
            print(f"✅ Devbox created from blueprint!")
            print(f"  Name: {devbox.name}")
            print(f"  ID: {devbox.id}")
            
            # Update answers.json
            self._update_answers_json("devbox-from-blueprint-name", devbox.name)
            self._update_answers_json("devbox-from-blueprint-id", devbox.id)
            
            return devbox
            
        except Exception as e:
            print(f"❌ Error booting devbox from blueprint: {e}")
            return None
    
    def test_cowsay(self, devbox_id: str):
        """Test cowsay on the devbox."""
        print("🐄 Testing cowsay on devbox...")
        try:
            result = self.client.devboxes.execute_command(
                devbox_id=devbox_id,
                command="cowsay 'Hello from Runloop!'"
            )
            
            print(f"✅ Cowsay executed successfully!")
            print(f"Output: {result.output}")
            return True
            
        except Exception as e:
            print(f"❌ Error testing cowsay: {e}")
            return False
    
    def run_all_operations(self):
        """Run all required operations for Task 2."""
        print("🚀 Starting Task 2: Create blueprint with cowsay")
        print("=" * 50)
        
        # Step 1: Create blueprint
        blueprint = self.create_blueprint()
        if not blueprint:
            print("❌ Failed to create blueprint. Stopping.")
            return False
        
        # Step 2: Boot devbox from blueprint
        devbox = self.boot_devbox_from_blueprint(blueprint.id)
        if not devbox:
            print("❌ Failed to boot devbox from blueprint. Stopping.")
            return False
        
        # Step 3: Test cowsay
        if not self.test_cowsay(devbox.id):
            print("❌ Failed to test cowsay. Stopping.")
            return False
        
        print("=" * 50)
        print("✅ Task 2 completed successfully!")
        print("📸 Don't forget to take a screenshot of cowsay running!")
        return True


def main():
    """Main function to run the blueprint creation."""
    try:
        creator = BlueprintCreator()
        creator.run_all_operations()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 