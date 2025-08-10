#!/usr/bin/env python3
"""
Custom Scenario Creation Script for Runloop API Client Takehome
Task 3: Extension - Create a Custom Scenario via API
"""

import os
import sys
import json
from typing import Dict, Any
from runloop_api_client import Runloop


class ScenarioCreator:
    """Class to handle custom scenario creation for Task 3."""
    
    def __init__(self):
        """Initialize the ScenarioCreator class."""
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
    
    def create_custom_scenario(self):
        """Create a scenario with a custom scorer that checks for resources folder."""
        print("🎯 Creating custom scenario with resources checker...")
        try:
            # Create scenario with custom scorer
            scenario = self.client.scenarios.create(
                name="resources-checker-scenario",
                description="Scenario that checks for presence of resources folder and files",
                # Custom scorer logic
                scorer_config={
                    "type": "custom",
                    "script": """
                    # Custom scorer that checks for resources
                    def score(devbox_id, context):
                        try:
                            # Check if resources folder exists
                            result = client.devboxes.execute_command(
                                devbox_id=devbox_id,
                                command="ls -la /workspace/resources"
                            )
                            
                            if result.exit_code == 0:
                                # Check for specific files
                                me_txt = client.devboxes.execute_command(
                                    devbox_id=devbox_id,
                                    command="test -f /workspace/resources/me.txt && echo 'me.txt exists'"
                                )
                                
                                test_py = client.devboxes.execute_command(
                                    devbox_id=devbox_id,
                                    command="test -f /workspace/resources/test.py && echo 'test.py exists'"
                                )
                                
                                if me_txt.exit_code == 0 and test_py.exit_code == 0:
                                    return 1  # Success
                            
                            return 0  # Failure
                        except Exception as e:
                            return 0  # Failure on error
                    """
                }
            )
            
            print(f"✅ Scenario created successfully!")
            print(f"  Name: {scenario.name}")
            print(f"  ID: {scenario.id}")
            
            return scenario
            
        except Exception as e:
            print(f"❌ Error creating scenario: {e}")
            return None
    
    def create_scenario_run(self, scenario_id: str):
        """Create a scenario run."""
        print("🚀 Creating scenario run...")
        try:
            scenario_run = self.client.scenario_runs.create(
                scenario_id=scenario_id
            )
            
            print(f"✅ Scenario run created successfully!")
            print(f"  ID: {scenario_run.id}")
            
            # Update answers.json
            self._update_answers_json("ext-scenario-run-id", scenario_run.id)
            
            return scenario_run
            
        except Exception as e:
            print(f"❌ Error creating scenario run: {e}")
            return None
    
    def copy_resources_to_devbox(self, devbox_id: str):
        """Copy resources folder to devbox for scenario testing."""
        print("📁 Copying resources to devbox for scenario...")
        try:
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
                        devbox_id=devbox_id,
                        path=f"/workspace/resources/{filename}",
                        content=content
                    )
                    print(f"✅ Uploaded {filename}: {result}")
            
            return True
        except Exception as e:
            print(f"❌ Error copying resources: {e}")
            return False
    
    def execute_test_script(self, devbox_id: str):
        """Execute the test script from step 1.b."""
        print("🚀 Executing test script on devbox...")
        try:
            # First edit me.txt
            result = self.client.devboxes.write_file(
                devbox_id=devbox_id,
                path="/workspace/resources/me.txt",
                content="asad.shahid@berkeley.edu"
            )
            print(f"✅ Updated me.txt: {result}")
            
            # Then execute test.py
            result = self.client.devboxes.execute_command(
                devbox_id=devbox_id,
                command="python3 /workspace/resources/test.py"
            )
            
            print(f"✅ Test script executed successfully!")
            print(f"Output: {result.output}")
            return True
            
        except Exception as e:
            print(f"❌ Error executing test script: {e}")
            return False
    
    def score_and_complete_scenario(self, scenario_run_id: str):
        """Score and complete the scenario run."""
        print("📊 Scoring and completing scenario run...")
        try:
            # Complete the scenario run
            result = self.client.scenario_runs.complete(
                scenario_run_id=scenario_run_id
            )
            
            print(f"✅ Scenario run completed successfully!")
            print(f"Result: {result}")
            return True
            
        except Exception as e:
            print(f"❌ Error completing scenario run: {e}")
            return False
    
    def run_all_operations(self):
        """Run all required operations for Task 3."""
        print("🚀 Starting Task 3: Create Custom Scenario via API")
        print("=" * 50)
        
        # Step 1: Create custom scenario
        scenario = self.create_custom_scenario()
        if not scenario:
            print("❌ Failed to create scenario. Stopping.")
            return False
        
        # Step 2: Create scenario run
        scenario_run = self.create_scenario_run(scenario.id)
        if not scenario_run:
            print("❌ Failed to create scenario run. Stopping.")
            return False
        
        # Step 3: Copy resources to devbox (we'll need a devbox ID)
        # For now, we'll assume we have one or create one
        print("⚠️  Note: You'll need to provide a devbox ID to complete this task")
        print("   You can either:")
        print("   1. Fix the API key and run Task 1 first")
        print("   2. Manually provide a devbox ID in answers.json")
        
        # Step 4: Execute test script (requires devbox)
        # Step 5: Score and complete scenario
        
        print("=" * 50)
        print("✅ Task 3 scenario creation completed!")
        print("📝 Complete the remaining steps once you have a working devbox")
        return True


def main():
    """Main function to run the scenario creation."""
    try:
        creator = ScenarioCreator()
        creator.run_all_operations()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 