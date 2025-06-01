#!/usr/bin/env python3
"""
Test script for the PubMed to PaperQA2 pipeline.
This tests basic functionality without requiring API keys.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import requests
        print("✓ requests")
    except ImportError as e:
        print(f"✗ requests: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✓ beautifulsoup4")
    except ImportError as e:
        print(f"✗ beautifulsoup4: {e}")
        return False
    
    try:
        import lxml
        print("✓ lxml")
    except ImportError as e:
        print(f"✗ lxml: {e}")
        return False
    
    try:
        from pubmed_retriever import PubMedRetriever
        print("✓ pubmed_retriever module")
    except ImportError as e:
        print(f"✗ pubmed_retriever: {e}")
        return False
    
    print("\nAll imports successful!")
    return True


def test_pubmed_retriever():
    """Test PubMedRetriever functionality."""
    print("\nTesting PubMedRetriever...")
    
    try:
        from pubmed_retriever import PubMedRetriever
        
        # Create test directory
        test_dir = "./test_papers"
        retriever = PubMedRetriever(output_dir=test_dir)
        
        print(f"✓ PubMedRetriever initialized with output dir: {test_dir}")
        
        # Test search functionality (without downloading)
        print("\nTesting PubMed search...")
        query = "COVID-19 vaccine"
        results = retriever.search_pubmed(query, max_results=3)
        
        if results:
            print(f"✓ Search returned {len(results)} results for '{query}'")
            print(f"  PMC IDs: {', '.join(results[:3])}")
            
            # Test getting article info
            print("\nTesting article info retrieval...")
            article_info = retriever.get_pmc_info(results[0])
            if article_info:
                print(f"✓ Retrieved info for PMC{results[0]}:")
                print(f"  Title: {article_info['title'][:80]}...")
            else:
                print(f"⚠ Could not retrieve info for PMC{results[0]}")
        else:
            print(f"⚠ No search results returned for '{query}'")
        
        # Clean up test directory
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
            
        return True
        
    except Exception as e:
        print(f"✗ Error testing PubMedRetriever: {e}")
        return False


def test_pipeline_initialization():
    """Test pipeline initialization without API keys."""
    print("\nTesting pipeline initialization...")
    
    # Test basic pipeline import
    try:
        from paperqa_pipeline import PaperQAPipeline
        print("✓ paperqa_pipeline module imported")
    except ImportError as e:
        print(f"✗ paperqa_pipeline import failed: {e}")
        return False
    
    # Test LiteLLM pipeline import
    try:
        from paperqa_pipeline_litellm import PaperQAPipelineLiteLLM
        print("✓ paperqa_pipeline_litellm module imported")
    except ImportError as e:
        print(f"✗ paperqa_pipeline_litellm import failed: {e}")
        return False
    
    print("\nChecking for API keys...")
    if os.getenv("ANTHROPIC_API_KEY"):
        print("✓ ANTHROPIC_API_KEY found in environment")
    else:
        print("⚠ ANTHROPIC_API_KEY not found - pipeline will require this to run")
    
    return True


def test_dependencies_check():
    """Check if lxml is properly installed."""
    print("\nTesting lxml dependency...")
    
    try:
        from pubmed_retriever import check_dependencies
        if check_dependencies():
            print("✓ All dependencies properly installed")
            return True
        else:
            print("✗ Missing dependencies")
            return False
    except Exception as e:
        print(f"✗ Error checking dependencies: {e}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("PubMed to PaperQA2 Pipeline Test Suite")
    print("="*60)
    
    all_passed = True
    
    # Run tests
    tests = [
        test_imports,
        test_dependencies_check,
        test_pubmed_retriever,
        test_pipeline_initialization
    ]
    
    for test in tests:
        if not test():
            all_passed = False
        print()
    
    print("="*60)
    if all_passed:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed. Please check the output above.")
    print("="*60)
    
    # Provide setup instructions if needed
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\nTo run the full pipeline, you need to set up your API key:")
        print("1. Create a .env file in this directory")
        print("2. Add: ANTHROPIC_API_KEY=your_api_key_here")
        print("\nOr export it in your shell:")
        print("export ANTHROPIC_API_KEY=your_api_key_here")


if __name__ == "__main__":
    main()