#!/usr/bin/env python3
"""
Working test of the pipeline with correct model names
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify API key
if not os.getenv("ANTHROPIC_API_KEY"):
    print("Error: ANTHROPIC_API_KEY not set")
    exit(1)

import litellm
from pubmed_retriever import PubMedRetriever

async def test_working_pipeline():
    """Test the complete pipeline with correct Claude model names."""
    print("PubMed + Claude Analysis Pipeline Test")
    print("="*50)
    
    # Step 1: Test available Claude models
    print("\n1. Testing Claude model access...")
    test_models = [
        "claude-3-opus-20240229",
        "claude-3-5-sonnet-20241022", 
        "claude-3-haiku-20240307",
    ]
    
    working_model = None
    for model in test_models:
        try:
            response = await litellm.acompletion(
                model=model,
                messages=[{"role": "user", "content": "Reply with just 'OK'"}],
                max_tokens=10
            )
            print(f"✓ {model} works!")
            working_model = model
            break
        except Exception as e:
            print(f"✗ {model}: {str(e)[:50]}...")
    
    if not working_model:
        print("No Claude models accessible!")
        return
    
    print(f"\nUsing model: {working_model}")
    
    # Step 2: Download a paper
    print("\n2. Downloading research paper...")
    retriever = PubMedRetriever(output_dir="./papers")
    
    # Search for a specific topic
    query = "COVID-19 vaccine effectiveness 2024"
    pmc_ids = retriever.search_pubmed(query, max_results=1)
    
    if not pmc_ids:
        print("No papers found!")
        return
    
    # Download the paper
    info = retriever.get_pmc_info(pmc_ids[0])
    if not info:
        print("Could not get paper info!")
        return
    
    print(f"Found: {info['title'][:60]}...")
    pdf_path = retriever.download_fulltext(pmc_ids[0], info['title'])
    
    if not pdf_path:
        print("Could not download paper!")
        return
    
    print(f"✓ Downloaded: {Path(pdf_path).name}")
    
    # Step 3: Analyze with Claude (without PaperQA2 for now)
    print("\n3. Analyzing paper with Claude...")
    
    # For this test, we'll read the paper and ask Claude directly
    # This avoids PaperQA2 configuration issues
    
    # Read first part of PDF text (if it's text-based)
    try:
        # Try to extract some text from the PDF
        import pypdf
        
        with open(pdf_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            # Get text from first few pages
            text = ""
            for i in range(min(3, len(reader.pages))):
                text += reader.pages[i].extract_text()
            
            if len(text) > 2000:
                text = text[:2000] + "..."
        
        if text.strip():
            print("✓ Extracted text from PDF")
            
            # Ask Claude to analyze
            prompt = f"""Analyze this research paper excerpt and answer: What are the main findings about COVID-19 vaccine effectiveness?

Paper excerpt:
{text}

Please provide a brief summary of the key findings."""

            response = await litellm.acompletion(
                model=working_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            print("\n4. Analysis Results:")
            print("="*50)
            print(answer[:500] + "..." if len(answer) > 500 else answer)
            print("\n✓ Pipeline test completed successfully!")
            
        else:
            print("Could not extract text from PDF")
            
    except Exception as e:
        print(f"Error analyzing: {e}")
        
    # Clean up
    print(f"\nPaper saved in: {pdf_path}")

if __name__ == "__main__":
    asyncio.run(test_working_pipeline())