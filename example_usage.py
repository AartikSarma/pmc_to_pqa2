#!/usr/bin/env python3
"""
Example usage scripts for the PubMed to PaperQA2 pipeline.

This file demonstrates various ways to use the pipeline for different research tasks.
"""

import asyncio
import os
from pathlib import Path
from paperqa_pipeline import PaperQAPipeline
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def example_basic_usage():
    """Basic example: Search, download, and analyze papers on a topic."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Usage")
    print("="*60)
    
    pipeline = PaperQAPipeline()
    
    # Run the complete pipeline
    results = await pipeline.run_pipeline(
        search_query="COVID-19 long term effects",
        analysis_question="What are the most common symptoms of long COVID?",
        max_results=5,
        auto_download=True
    )
    
    print(f"\nAnswer: {results['answer']}")
    print(f"Papers analyzed: {results['papers_analyzed']}")


async def example_multiple_questions():
    """Example: Download papers once, ask multiple questions."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Multiple Questions on Same Papers")
    print("="*60)
    
    pipeline = PaperQAPipeline()
    
    # Download papers on machine learning in medicine
    papers = pipeline.search_and_download("machine learning diagnosis", max_results=3)
    
    if papers:
        questions = [
            "What types of machine learning algorithms are most commonly used for medical diagnosis?",
            "What are the main challenges in implementing ML systems in clinical practice?",
            "How do these ML systems compare to human doctors in terms of accuracy?"
        ]
        
        for question in questions:
            print(f"\nQuestion: {question}")
            results = await pipeline.analyze_papers(question, paper_paths=papers)
            print(f"Answer: {results['answer'][:500]}...")  # Truncate for readability


async def example_comparative_analysis():
    """Example: Compare findings across different search queries."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Comparative Analysis")
    print("="*60)
    
    pipeline = PaperQAPipeline(output_dir="./comparative_papers")
    
    # Search for papers on two different treatments
    treatment_searches = [
        ("immunotherapy melanoma", "immunotherapy_papers"),
        ("targeted therapy melanoma", "targeted_therapy_papers")
    ]
    
    all_papers = []
    
    for search_query, folder_name in treatment_searches:
        print(f"\nSearching for: {search_query}")
        # Create subdirectory for each treatment type
        treatment_dir = Path(pipeline.output_dir) / folder_name
        treatment_dir.mkdir(exist_ok=True)
        
        # Temporarily change output directory
        pipeline.retriever.output_dir = str(treatment_dir)
        
        papers = pipeline._auto_download(search_query, max_results=3)
        all_papers.extend(papers)
    
    # Analyze all papers together
    comparison_question = (
        "Compare the effectiveness and side effects of immunotherapy "
        "versus targeted therapy for melanoma treatment."
    )
    
    results = await pipeline.analyze_papers(comparison_question, paper_paths=all_papers)
    print(f"\nComparative Analysis:")
    print(f"{results['answer']}")


async def example_research_synthesis():
    """Example: Create a research synthesis from multiple papers."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Research Synthesis")
    print("="*60)
    
    pipeline = PaperQAPipeline()
    
    # Download papers on a research topic
    papers = pipeline._auto_download("CRISPR gene therapy clinical trials", max_results=5)
    
    if papers:
        # Ask synthesis questions
        synthesis_questions = [
            "What are the main therapeutic areas where CRISPR is being tested in clinical trials?",
            "What safety concerns have been identified in CRISPR clinical trials?",
            "What are the reported success rates and outcomes from completed trials?"
        ]
        
        synthesis = {}
        for question in synthesis_questions:
            results = await pipeline.analyze_papers(question, paper_paths=papers)
            synthesis[question] = results['answer']
        
        # Create a summary
        print("\nRESEARCH SYNTHESIS: CRISPR Gene Therapy Clinical Trials")
        print("-" * 50)
        for question, answer in synthesis.items():
            print(f"\n{question}")
            print(f"→ {answer}\n")
        
        # Save the synthesis
        pipeline.save_results(synthesis, "crispr_synthesis.json")


async def example_custom_analysis():
    """Example: Custom analysis with specific paper selection."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Custom Analysis Workflow")
    print("="*60)
    
    pipeline = PaperQAPipeline()
    
    # Step 1: Search for papers
    print("Step 1: Searching for papers on 'artificial intelligence radiology'")
    pmc_ids = pipeline.retriever.search_pubmed("artificial intelligence radiology", max_results=10)
    
    # Step 2: Get paper information
    print("\nStep 2: Retrieving paper information...")
    papers_info = []
    for pmc_id in pmc_ids[:5]:  # Limit to first 5
        info = pipeline.retriever.get_pmc_info(pmc_id)
        if info:
            papers_info.append(info)
            print(f"  - {info['title'][:80]}...")
    
    # Step 3: Download specific papers (e.g., only recent ones)
    print("\nStep 3: Downloading selected papers...")
    downloaded = []
    for info in papers_info[:3]:  # Download top 3
        file_path = pipeline.retriever.download_fulltext(info['pmc_id'], info['title'])
        if file_path:
            downloaded.append(file_path)
    
    # Step 4: Analyze with specific focus
    if downloaded:
        print("\nStep 4: Analyzing papers...")
        results = await pipeline.analyze_papers(
            "What specific radiology tasks has AI shown the most promise in, "
            "and what are the reported accuracy metrics?",
            paper_paths=downloaded
        )
        
        print(f"\nAnalysis Result:")
        print(f"{results['answer']}")
        
        # Show sources
        print(f"\nSources ({len(results['sources'])}):")
        for i, source in enumerate(results['sources'][:3], 1):
            print(f"{i}. {source['source']}")


async def main():
    """Run all examples."""
    examples = [
        example_basic_usage,
        example_multiple_questions,
        example_comparative_analysis,
        example_research_synthesis,
        example_custom_analysis
    ]
    
    print("\nPubMed to PaperQA2 Pipeline - Examples")
    print("======================================")
    
    for example in examples:
        try:
            await example()
        except Exception as e:
            print(f"\nError in {example.__name__}: {str(e)}")
            print("Continuing with next example...")
        
        # Pause between examples
        await asyncio.sleep(2)
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)


if __name__ == "__main__":
    # Check for Anthropic API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: Please set your ANTHROPIC_API_KEY environment variable")
        print("You can do this by creating a .env file with:")
        print("ANTHROPIC_API_KEY=your_api_key_here")
        exit(1)
    
    # Run examples
    asyncio.run(main())