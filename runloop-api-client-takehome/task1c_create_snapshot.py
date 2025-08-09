#!/usr/bin/env python3
"""
Snapshot Creation Script for Runloop API Client Takehome
Task 1.c: Create snapshot of devbox after operations
"""

import os
import sys
import json
from typing import Dict, Any
from runloop_api_client import Runloop


class SnapshotCreator:
    """Class to handle devbox snapshot creation for Task 1.c."""
    
    def __init__(self):
        """Initialize the SnapshotCreator class."""
        self.config = self._load_config()
        self.api_key = self.config.get("api-key")
        self.devbox_name = self.config.get("devbox-name")
        self.devbox_id = self.config.get("devbox-id")
        
        if not self.api_key:
            raise ValueError("API key not found in answers.json")
        
        if not self.devbox_id or self.devbox_id == "YOUR_DEVBOX_ID":
            raise ValueError("Devbox ID not found in answers.json. Please run Task 1.a first.")
        
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
    
    def create_snapshot(self):
        """Create a snapshot of the devbox after operations."""
        print("📸 Creating snapshot of devbox...")
        try:
            # Create snapshot
            snapshot = self.client.devboxes.create_snapshot(
                devbox_id=self.devbox_id,
                name=f"snapshot-after-operations-{self.devbox_name}"
            )
            
            print(f"✅ Snapshot created successfully!")
            print(f"  Name: {snapshot.name}")
            print(f"  ID: {snapshot.id}")
            
            # Update answers.json
            self._update_answers_json("snapshot-id", snapshot.id)
            
            return snapshot
            
        except Exception as e:
            print(f"❌ Error creating snapshot: {e}")
            return None
    
    def run_all_operations(self):
        """Run all required operations for Task 1.c."""
        print("🚀 Starting Task 1.c: Create snapshot")
        print("=" * 50)
        
        # Step 1: Create snapshot
        snapshot = self.create_snapshot()
        if not snapshot:
            print("❌ Failed to create snapshot. Stopping.")
            return False
        
        print("=" * 50)
        print("✅ Task 1.c completed successfully!")
        print(f"📸 Snapshot created: {snapshot.name} (ID: {snapshot.id})")
        return True


def main():
    """Main function to run the snapshot creation."""
    try:
        creator = SnapshotCreator()
        creator.run_all_operations()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 