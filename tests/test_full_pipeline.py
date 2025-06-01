#!/usr/bin/env python3
"""
Test the full pipeline with a simple query.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from paperqa_pipeline_litellm import PaperQAPipelineLiteLLM

async def test_pipeline():
    """Test the pipeline with a simple search and analysis."""
    try:
        # Initialize pipeline with LiteLLM
        print("Initializing pipeline...")
        pipeline = PaperQAPipelineLiteLLM(
            llm_provider="anthropic",
            embedding_model="local",  # Use local embeddings
            output_dir="./test_papers_full"
        )
        print("✓ Pipeline initialized successfully")
        
        # Test with a simple query
        print("\nRunning pipeline test...")
        results = await pipeline.run_pipeline(
            search_query="COVID-19 vaccine effectiveness",
            analysis_question="What is the reported effectiveness of COVID-19 vaccines against hospitalization?",
            max_results=2,  # Small number for testing
            auto_download=True
        )
        
        # Display results
        print("\n" + "="*60)
        print("TEST RESULTS")
        print("="*60)
        
        if "error" in results:
            print(f"Error: {results['error']}")
        else:
            print(f"Question: {results.get('question', 'N/A')}")
            print(f"Papers analyzed: {results.get('papers_analyzed', 0)}")
            print(f"\nAnswer preview (first 500 chars):")
            answer = results.get('answer', 'No answer generated')
            print(answer[:500] + "..." if len(answer) > 500 else answer)
            
            if results.get('sources'):
                print(f"\nNumber of sources used: {len(results['sources'])}")
        
        print("\n✓ Pipeline test completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Pipeline test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing PubMed to PaperQA2 Pipeline")
    print("="*40)
    asyncio.run(test_pipeline())