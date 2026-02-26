#!/usr/bin/env python3
"""
Automated GitHub deployment script for warinfo project
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class GitHubDeployer:
    def __init__(self, github_token=None, github_username=None, repo_name="warinfo"):
        self.github_token = github_token or os.environ.get('GITHUB_TOKEN')
        self.github_username = github_username or os.environ.get('GITHUB_USERNAME')
        self.repo_name = repo_name
        self.project_dir = Path(__file__).parent.absolute()
        
    def setup_github_repo(self):
        """Setup GitHub repository with proper configuration"""
        if not self.github_token or not self.github_username:
            print("Error: GITHUB_TOKEN and GITHUB_USERNAME must be set")
            print("Please set them as environment variables or provide them as arguments")
            return False
            
        # Create remote URL with token
        remote_url = f"https://{self.github_username}:{self.github_token}@github.com/{self.github_username}/{self.repo_name}.git"
        
        try:
            # Initialize git if not already done
            if not (self.project_dir / ".git").exists():
                subprocess.run(["git", "init"], cwd=self.project_dir, check=True)
                subprocess.run(["git", "add", "."], cwd=self.project_dir, check=True)
                subprocess.run(["git", "config", "user.name", "warinfo-deployer"], cwd=self.project_dir, check=True)
                subprocess.run(["git", "config", "user.email", "deploy@warinfo.local"], cwd=self.project_dir, check=True)
                subprocess.run(["git", "commit", "-m", "Initial commit: warinfo project"], cwd=self.project_dir, check=True)
            
            # Add remote repository
            subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=self.project_dir, check=False)
            
            # Push to GitHub
            subprocess.run(["git", "push", "-u", "origin", "master", "--force"], cwd=self.project_dir, check=True)
            
            print(f"✅ Successfully deployed to https://github.com/{self.github_username}/{self.repo_name}")
            print(f"🌐 GitHub Pages URL: https://{self.github_username}.github.io/{self.repo_name}/global_conflict_heatmap.html")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Deployment failed: {e}")
            return False
    
    def setup_github_pages(self):
        """Setup GitHub Pages via API (requires admin permissions)"""
        # This would require additional GitHub API calls
        # For now, user needs to enable GitHub Pages manually
        print("ℹ️  Please enable GitHub Pages manually in your repository settings:")
        print("   Settings → Pages → Source: master branch / root folder")
    
    def create_config_file(self):
        """Create a configuration file template"""
        config = {
            "github_username": self.github_username,
            "repo_name": self.repo_name,
            "update_schedule": "0 2 * * *",  # Daily at 2 AM UTC
            "data_sources": ["sample_data"]  # Can be extended to real APIs
        }
        
        config_file = self.project_dir / "deployment_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"📝 Configuration saved to {config_file}")

def main():
    # Try to get credentials from environment variables first
    github_token = os.environ.get('GITHUB_TOKEN')
    github_username = os.environ.get('GITHUB_USERNAME')
    
    if not github_token or not github_username:
        print("🔐 GitHub deployment requires credentials")
        print("\nOption 1: Set environment variables")
        print("   export GITHUB_TOKEN='your_personal_access_token'")
        print("   export GITHUB_USERNAME='your_github_username'")
        print("   python deploy_to_github.py")
        print("\nOption 2: Run with arguments")
        print("   python deploy_to_github.py --token YOUR_TOKEN --username YOUR_USERNAME")
        print("\nOption 3: Create a config file")
        print("   Create deployment_config.json with your credentials")
        return
    
    deployer = GitHubDeployer(github_token, github_username)
    if deployer.setup_github_repo():
        deployer.create_config_file()
        deployer.setup_github_pages()

if __name__ == "__main__":
    main()