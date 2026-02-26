#!/usr/bin/env python3
"""
Daily update script for warinfo project
This script should be run daily via cron job
"""

import os
import sys
import subprocess
from datetime import datetime

def main():
    """Main update function"""
    print(f"Starting daily update at {datetime.now()}")
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    try:
        # Update conflict data
        print("Updating conflict data...")
        result = subprocess.run([sys.executable, "conflict_data.py"], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"Error updating data: {result.stderr}")
            return False
        
        # Create heatmap
        print("Creating heatmap...")
        result = subprocess.run([sys.executable, "create_heatmap.py"], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            print(f"Error creating heatmap: {result.stderr}")
            return False
        
        # Commit and push to GitHub (if configured)
        print("Committing changes...")
        try:
            # Add files
            subprocess.run(["git", "add", "conflict_data.json", "global_conflict_heatmap.html"], 
                          check=True, timeout=60)
            
            # Check if there are changes to commit
            result = subprocess.run(["git", "status", "--porcelain"], 
                                  capture_output=True, text=True, timeout=60)
            if result.stdout.strip():
                # Commit with timestamp
                commit_message = f"Daily update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                subprocess.run(["git", "commit", "-m", commit_message], 
                              check=True, timeout=60)
                print(f"Committed: {commit_message}")
                
                # Push to remote (optional - requires authentication setup)
                # subprocess.run(["git", "push"], check=True, timeout=120)
                # print("Pushed to GitHub")
            else:
                print("No changes to commit")
                
        except subprocess.CalledProcessError as e:
            print(f"Git operation failed: {e}")
            # Continue even if git fails
        
        print("Daily update completed successfully!")
        return True
        
    except Exception as e:
        print(f"Daily update failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)