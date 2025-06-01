#!/usr/bin/env python3
"""
Check setup and dependencies for the PubMed to PaperQA2 pipeline.
"""

import sys
import subprocess
import importlib.util

def check_module(module_name, package_name=None):
    """Check if a module is installed."""
    if package_name is None:
        package_name = module_name
    
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        return False, f"pip install {package_name}"
    return True, "Installed"

def main():
    print("PubMed to PaperQA2 Pipeline - Setup Check")
    print("="*50)
    
    # Core dependencies
    print("\nCore Dependencies:")
    core_deps = [
        ("requests", None),
        ("bs4", "beautifulsoup4"),
        ("lxml", None),
    ]
    
    all_good = True
    for module, package in core_deps:
        installed, msg = check_module(module, package)
        status = "✓" if installed else "✗"
        print(f"{status} {package or module}: {msg}")
        if not installed:
            all_good = False
    
    # PaperQA2 dependencies
    print("\nPaperQA2 Dependencies:")
    qa_deps = [
        ("paperqa", "paper-qa"),
        ("litellm", None),
        ("langchain", None),
        ("dotenv", "python-dotenv"),
        ("sentence_transformers", "sentence-transformers"),
    ]
    
    for module, package in qa_deps:
        installed, msg = check_module(module, package)
        status = "✓" if installed else "✗"
        print(f"{status} {package or module}: {msg}")
        if not installed:
            all_good = False
    
    # Check for API keys
    print("\nAPI Keys:")
    import os
    
    api_keys = {
        "ANTHROPIC_API_KEY": "Anthropic (Claude)",
        "OPENAI_API_KEY": "OpenAI (GPT)",
        "NCBI_EMAIL": "NCBI Email (optional)",
        "NCBI_API_KEY": "NCBI API Key (optional)",
    }
    
    for key, desc in api_keys.items():
        if os.getenv(key):
            print(f"✓ {desc}: Set")
        else:
            print(f"⚠ {desc}: Not set")
    
    # Summary
    print("\n" + "="*50)
    if all_good:
        print("✓ All dependencies are installed!")
        print("\nYou can run the pipeline with:")
        print("  python paperqa_pipeline.py [search_query] [question]")
    else:
        print("✗ Some dependencies are missing.")
        print("\nInstall all dependencies with:")
        print("  pip install -r requirements.txt")
    
    print("\nFor basic PubMed search (no API keys needed):")
    print("  python demo_pubmed_search.py")


if __name__ == "__main__":
    main()