#!/usr/bin/env python3
import json
import os
import subprocess
import time
from datetime import datetime

# Output directory for README files
OUTPUT_DIR = "repository_readmes"

def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def run_gh_command(cmd):
    """Run a GitHub CLI command and return the output"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e}")
        print(f"Error output: {e.stderr}")
        return None

def get_all_repos():
    """Get all repositories using GitHub CLI"""
    # Use GitHub API with pagination to get all repositories
    cmd = ["gh", "api", "user/repos", "--paginate", 
           "--jq", "[.[] | {name: .name, owner: .owner.login, url: .html_url}]"]
    
    result = run_gh_command(cmd)
    if not result:
        return []
    
    # Parse JSON results
    try:
        # The result might contain multiple JSON arrays (one per page)
        repos = []
        for line in result.strip().split('\n'):
            if line.strip():
                try:
                    page_repos = json.loads(line)
                    repos.extend(page_repos)
                except json.JSONDecodeError:
                    continue
        
        return repos
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return []

def get_org_repos(org):
    """Get repositories for a specific organization using GitHub CLI"""
    cmd = ["gh", "api", f"orgs/{org}/repos", "--paginate", 
           "--jq", "[.[] | {name: .name, owner: .owner.login, url: .html_url}]"]
    
    result = run_gh_command(cmd)
    if not result:
        return []
    
    # Parse JSON results
    try:
        # The result might contain multiple JSON arrays (one per page)
        repos = []
        for line in result.strip().split('\n'):
            if line.strip():
                try:
                    page_repos = json.loads(line)
                    repos.extend(page_repos)
                except json.JSONDecodeError:
                    continue
        
        return repos
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return []

def fetch_readme(owner, repo):
    """Fetch README file for a repository"""
    # Try to get the README content using GitHub API
    cmd = ["gh", "api", f"repos/{owner}/{repo}/readme", "--jq", ".content"]
    
    result = run_gh_command(cmd)
    if result:
        try:
            # GitHub API returns base64 encoded content
            import base64
            content = base64.b64decode(result.strip()).decode('utf-8')
            return content
        except Exception as e:
            print(f"Error decoding README for {owner}/{repo}: {e}")
    
    # If API fails, try to get README using GitHub CLI directly
    print(f"Could not fetch README via API for {owner}/{repo}, trying alternative method...")
    
    # Try common README filenames
    readme_filenames = [
        "README.md", "README", "README.txt", "README.markdown", 
        "Readme.md", "readme.md", "readme"
    ]
    
    for filename in readme_filenames:
        cmd = ["gh", "repo", "view", f"{owner}/{repo}", "--web"]
        
        # Just log that we're checking this repo
        print(f"Checking for {filename} in {owner}/{repo}...")
        
        # Use gh api to try to get the file content directly
        file_cmd = ["gh", "api", f"repos/{owner}/{repo}/contents/{filename}", "--jq", ".content"]
        file_result = run_gh_command(file_cmd)
        
        if file_result:
            try:
                import base64
                content = base64.b64decode(file_result.strip()).decode('utf-8')
                return content
            except Exception as e:
                print(f"Error decoding {filename} for {owner}/{repo}: {e}")
    
    # If we still can't find a README, return None
    return None

def save_readme(owner, repo, content):
    """Save README content to file"""
    if not content:
        return
    
    # Create directory for owner if it doesn't exist
    owner_dir = os.path.join(OUTPUT_DIR, owner)
    if not os.path.exists(owner_dir):
        os.makedirs(owner_dir)
    
    # Save README to file
    filename = os.path.join(owner_dir, f"{repo}_README.md")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# README for {owner}/{repo}\n\n")
        f.write(content)
    
    print(f"Saved README for {owner}/{repo} to {filename}")

def is_microservice(repo_name):
    """Check if a repository is likely a microservice based on its name"""
    microservice_keywords = [
        'service', 'api', 'backend', 'gateway', 'worker', 'engine',
        'server', 'middleware', 'core', 'processor', 'handler', 'router'
    ]
    
    # Check if any of the keywords are in the repo name
    return any(keyword in repo_name.lower() for keyword in microservice_keywords)

def create_summary_file(microservices):
    """Create a summary file with links to all microservices"""
    summary_path = os.path.join(OUTPUT_DIR, "microservices_summary.md")
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("# Microservices Summary\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total microservices found: {len(microservices)}\n\n")
        
        # Group by owner
        by_owner = {}
        for ms in microservices:
            owner = ms['owner']
            if owner not in by_owner:
                by_owner[owner] = []
            by_owner[owner].append(ms)
        
        # Write summary by owner
        for owner, repos in by_owner.items():
            f.write(f"## {owner} ({len(repos)} microservices)\n\n")
            
            for repo in sorted(repos, key=lambda x: x['name']):
                name = repo['name']
                url = repo['url']
                readme_path = f"{owner}/{name}_README.md"
                
                f.write(f"- [{name}]({url}) - [README]({readme_path})\n")
            
            f.write("\n")
    
    print(f"Summary file created at {summary_path}")

def main():
    """Main function to fetch READMEs from all repositories"""
    ensure_output_dir()
    
    # List of organizations to fetch repos from
    orgs = ["olivium-dev"]
    
    # Get user's own repositories
    print("Fetching your repositories...")
    user_repos = get_all_repos()
    print(f"Found {len(user_repos)} repositories for your account.")
    
    # Get repositories for each organization
    all_repos = user_repos.copy()
    for org in orgs:
        print(f"Fetching repositories for organization {org}...")
        org_repos = get_org_repos(org)
        print(f"Found {len(org_repos)} repositories for organization {org}.")
        all_repos.extend(org_repos)
    
    # Remove duplicates (in case user is member of org)
    unique_repos = []
    seen = set()
    for repo in all_repos:
        key = f"{repo['owner']}/{repo['name']}"
        if key not in seen:
            seen.add(key)
            unique_repos.append(repo)
    
    print(f"Total unique repositories: {len(unique_repos)}")
    
    # Filter for microservices
    microservices = [repo for repo in unique_repos if is_microservice(repo['name'])]
    print(f"Found {len(microservices)} potential microservices")
    
    # Fetch README for each microservice
    successful_microservices = []
    for i, repo in enumerate(microservices):
        owner = repo['owner']
        name = repo['name']
        print(f"[{i+1}/{len(microservices)}] Fetching README for {owner}/{name}...")
        
        readme_content = fetch_readme(owner, name)
        if readme_content:
            save_readme(owner, name, readme_content)
            successful_microservices.append(repo)
        else:
            print(f"No README found for {owner}/{name}")
        
        # Add a small delay to avoid rate limiting
        if i % 10 == 0 and i > 0:
            print("Pausing to avoid rate limiting...")
            time.sleep(2)
    
    # Create summary file
    create_summary_file(successful_microservices)
    
    print(f"\nCompleted! README files saved to {OUTPUT_DIR}/ directory.")

if __name__ == "__main__":
    main()
