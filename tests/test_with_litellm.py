#!/usr/bin/env python3
"""
Test pipeline with proper LiteLLM configuration for Claude
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure LiteLLM to use Claude
import litellm
litellm.drop_params = True  # Drop unsupported params
litellm.set_verbose = False

from pubmed_retriever import PubMedRetriever
from paperqa import Docs, Settings

async def test_with_claude():
    """Test pipeline with Claude models via LiteLLM."""
    print("Testing Pipeline with Claude 4 via LiteLLM")
    print("="*50)
    
    # Verify API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not found!")
        return
    
    print("✓ Anthropic API key found")
    
    # Step 1: Download papers
    print("\n1. Downloading papers...")
    retriever = PubMedRetriever(output_dir="./test_claude_papers")
    
    # Search and download one paper for quick test
    pmc_ids = retriever.search_pubmed("COVID-19 vaccine effectiveness", max_results=1)
    
    downloaded = []
    for pmc_id in pmc_ids:
        info = retriever.get_pmc_info(pmc_id)
        if info:
            print(f"  Downloading: {info['title'][:60]}...")
            file_path = retriever.download_fulltext(pmc_id, info['title'])
            if file_path:
                downloaded.append(file_path)
    
    if not downloaded:
        print("No papers downloaded!")
        return
    
    print(f"\n  Downloaded {len(downloaded)} paper(s)")
    
    # Step 2: Configure PaperQA2 with Claude
    print("\n2. Configuring PaperQA2 with Claude...")
    
    # Create minimal settings that work with Claude
    settings = Settings(
        llm="anthropic/claude-sonnet-4-20250514",
        summary_llm="anthropic/claude-sonnet-4-20250514",
        # Disable embeddings for now to avoid OpenAI dependency
        answer_max_sources=3,
        llm_config={
            "model": "anthropic/claude-sonnet-4-20250514",
            "temperature": 0.1,
        }
    )
    
    print("  Settings configured for Claude Sonnet 4")
    
    # Create Docs with settings
    docs = Docs(
        llm=settings.llm,
        summary_llm=settings.summary_llm,
        answer_max_sources=settings.answer_max_sources,
    )
    
    # Step 3: Add papers
    print("\n3. Adding papers to Docs...")
    for paper in downloaded:
        try:
            print(f"  Adding: {Path(paper).name[:60]}...")
            await docs.aadd(paper, settings=settings)
            print("    ✓ Added successfully")
        except Exception as e:
            print(f"    ✗ Error: {str(e)[:100]}...")
    
    # Step 4: Query
    question = "What is the effectiveness of COVID-19 vaccines?"
    print(f"\n4. Querying: {question}")
    
    try:
        # Test basic LiteLLM call first
        print("\n  Testing LiteLLM directly...")
        test_response = await litellm.acompletion(
            model="anthropic/claude-sonnet-4-20250514",
            messages=[{"role": "user", "content": "Say 'Hello from Claude!'"}],
            temperature=0.1
        )
        print(f"  ✓ LiteLLM test: {test_response.choices[0].message.content}")
        
        # Now query through PaperQA2
        print("\n  Querying through PaperQA2...")
        answer = await docs.aquery(question, settings=settings)
        
        print("\n5. Results:")
        print("="*50)
        print(f"Answer: {answer.answer[:300]}..." if len(answer.answer) > 300 else f"Answer: {answer.answer}")
        
        if answer.contexts:
            print(f"\n✓ Used {len(answer.contexts)} sources")
        
        print("\n✓ Pipeline test completed successfully!")
            
    except Exception as e:
        print(f"\n✗ Error during query: {str(e)[:200]}...")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_with_claude())