#!/usr/bin/env python3
"""
Minimal test of the pipeline with correct PaperQA2 usage
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up LiteLLM to use Anthropic
os.environ["LITELLM_DEFAULT_PROVIDER"] = "anthropic"

from pubmed_retriever import PubMedRetriever
from paperqa import Docs

async def test_minimal():
    """Test minimal pipeline functionality."""
    print("Testing Minimal Pipeline")
    print("="*40)
    
    # Step 1: Download papers
    print("\n1. Downloading papers...")
    retriever = PubMedRetriever(output_dir="./test_minimal_papers")
    
    # Search and auto-download
    pmc_ids = retriever.search_pubmed("COVID-19 vaccine effectiveness", max_results=2)
    
    downloaded = []
    for pmc_id in pmc_ids:
        info = retriever.get_pmc_info(pmc_id)
        if info:
            print(f"  Downloading: {info['title'][:60]}...")
            file_path = retriever.download_fulltext(pmc_id, info['title'])
            if file_path:
                downloaded.append(file_path)
    
    print(f"\n  Downloaded {len(downloaded)} papers")
    
    # Step 2: Analyze with PaperQA2
    print("\n2. Analyzing papers with PaperQA2...")
    
    # Create Docs with minimal configuration
    # Let PaperQA2 use its defaults and configure models via environment
    os.environ["PAPERQA_LLM"] = "claude-sonnet-4-20250514"
    os.environ["PAPERQA_SUMMARY_LLM"] = "claude-sonnet-4-20250514"
    
    docs = Docs()
    
    # Add papers
    print("  Adding papers to Docs...")
    for paper in downloaded:
        try:
            await docs.aadd(paper)
            print(f"    Added: {Path(paper).name}")
        except Exception as e:
            print(f"    Error adding {Path(paper).name}: {e}")
    
    # Query
    question = "What is the reported effectiveness of COVID-19 vaccines against hospitalization?"
    print(f"\n  Querying: {question}")
    
    try:
        answer = await docs.aquery(question)
        
        print("\n3. Results:")
        print("="*40)
        print(f"Answer: {answer.answer[:500]}..." if len(answer.answer) > 500 else f"Answer: {answer.answer}")
        
        if answer.contexts:
            print(f"\nUsed {len(answer.contexts)} sources")
            
    except Exception as e:
        print(f"\nError during query: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_minimal())