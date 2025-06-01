#!/usr/bin/env python3
"""
Example analysis using the integrated pipeline
"""

import asyncio
from final_integrated_pipeline import FinalIntegratedPipeline

async def run_example():
    """Run an example analysis on CRISPR research."""
    pipeline = FinalIntegratedPipeline(
        # model=None,  # Auto-detect best available Claude model
        output_dir="./crispr_analysis"
    )
    
    # Search for CRISPR clinical trials
    results = await pipeline.run_pipeline(
        search_query="CRISPR gene editing clinical trials safety efficacy",
        question="What are the main safety concerns and efficacy results from CRISPR gene editing clinical trials? Include specific outcomes and adverse events reported.",
        max_papers=3
    )
    
    pipeline.display_results(results)

if __name__ == "__main__":
    print("Running example analysis on CRISPR clinical trials...")
    asyncio.run(run_example())