#!/usr/bin/env python3
"""
RunLoop API Client Takehome Assessment - Task 1a: Create Devbox

This script creates a devbox using the RunLoop SDK as specified in Task 1.a:
- Use RunLoop SDK to create a devbox
- Name it with the email address: asad.shahid@berkeley.edu
- Record api-key, devbox-name, and devbox-id in answers.json

Author: Asad Shahid
Email: asad.shahid@berkeley.edu
"""

import os
import json
import sys
from typing import Dict, Any
from runloop_api_client import Runloop

class DevboxManager:
    """Manages devbox creation and configuration for RunLoop assessment."""
    
    def __init__(self):
        """Initialize the DevboxManager with API client."""
        # Read API key from answers.json instead of environment variables
        self.answers_file = "answers.json"
        self.load_answers()
        
        if not self.api_key:
            raise ValueError(
                "API key not found in answers.json. "
                "Please ensure 'api-key' is set in answers.json."
            )
        
        # Initialize RunLoop client
        self.client = Runloop(
            base_url="https://api.runloop.pro", 
            bearer_token=self.api_key
        )
        
        # Configuration
        self.devbox_name = "asad.shahid@berkeley.edu"
    
    def load_answers(self):
        """Load answers from answers.json file."""
        try:
            with open(self.answers_file, 'r') as f:
                answers = json.load(f)
            
            self.api_key = answers.get("api-key")
            if not self.api_key:
                raise ValueError("'api-key' not found in answers.json")
                
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find {self.answers_file}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in {self.answers_file}")
        except Exception as e:
            raise Exception(f"Error loading {self.answers_file}: {str(e)}")
    
    def create_devbox(self) -> Dict[str, Any]:
        """
        Create a new devbox with the specified configuration.
        
        Returns:
            Dict containing devbox information
        """
        try:
            print(f"Creating devbox with name: {self.devbox_name}")
            print(f"Using API endpoint: https://api.runloop.pro")
            print(f"API key (first 10 chars): {self.api_key[:10]}...")
            
            # Create devbox using RunLoop SDK with create_args
            print("Creating devbox...")
            running_devbox = self.client.devboxes.create_and_await_running(
                create_args={"name": self.devbox_name}
            )
            
            print(f"✅ Successfully created devbox!")
            print(f"   Name: {running_devbox.name}")
            print(f"   ID: {running_devbox.id}")
            print(f"   Status: {running_devbox.status}")
            
            return {
                "name": running_devbox.name,
                "id": running_devbox.id,
                "status": running_devbox.status
            }
            
        except Exception as e:
            print(f"❌ Error creating devbox: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            raise
    
    def update_answers_json(self, devbox_info: Dict[str, Any]) -> None:
        """
        Update the answers.json file with devbox information.
        
        Args:
            devbox_info: Dictionary containing devbox details
        """
        try:
            # Read existing answers.json
            with open(self.answers_file, 'r') as f:
                answers = json.load(f)
            
            # Update with new information
            answers["api-key"] = self.api_key
            answers["devbox-name"] = devbox_info["name"]
            answers["devbox-id"] = devbox_info["id"]
            
            # Write updated answers back to file
            with open(self.answers_file, 'w') as f:
                json.dump(answers, f, indent=2)
            
            print(f"✅ Updated {self.answers_file} with devbox information")
            
        except Exception as e:
            print(f"❌ Error updating answers.json: {str(e)}")
            raise
    
    def run(self) -> None:
        """Execute the complete devbox creation workflow."""
        print("🚀 Starting RunLoop Devbox Creation - Task 1a")
        print("=" * 50)
        
        try:
            # Step 1: Create devbox
            devbox_info = self.create_devbox()
            
            # Step 2: Update answers.json
            self.update_answers_json(devbox_info)
            
            print("\n✅ Task 1a completed successfully!")
            print(f"   Devbox Name: {devbox_info['name']}")
            print(f"   Devbox ID: {devbox_info['id']}")
            print(f"   Status: {devbox_info['status']}")
            print(f"   Updated: {self.answers_file}")
            
        except Exception as e:
            print(f"\n❌ Task 1a failed: {str(e)}")
            sys.exit(1)


def main():
    """Main entry point for the devbox creation script."""
    try:
        manager = DevboxManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()