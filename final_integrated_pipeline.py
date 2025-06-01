#!/usr/bin/env python3
"""
Final Integrated Pipeline: PubMed → Claude Analysis

A robust pipeline that:
1. Searches PubMed for papers
2. Downloads papers (trying multiple formats)
3. Extracts text properly
4. Analyzes with Claude

This version handles various download formats and edge cases.
"""

import os
import asyncio
from typing import List, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Verify API key
if not os.getenv("ANTHROPIC_API_KEY"):
    print("Error: Please set ANTHROPIC_API_KEY in your .env file")
    exit(1)

from pubmed_retriever import PubMedRetriever
import litellm
from bs4 import BeautifulSoup

# Configure LiteLLM
litellm.set_verbose = False


async def get_best_claude_model() -> str:
    """Get the best available Claude model, prioritizing recent Sonnet models."""
    # Order of preference: Claude 4 Sonnet > Claude 3.7 Sonnet > Claude 3.5 Sonnet (new) > Claude 3.5 Sonnet
    models_to_try = [
        "claude-sonnet-4-20250514",       # Claude 4 Sonnet (if available)
        "claude-3-7-sonnet-20241220",     # Claude 3.7 Sonnet (hypothetical)
        "claude-3-5-sonnet-20241022",     # Claude 3.5 Sonnet (new)
        "claude-3-5-sonnet-20240620",     # Claude 3.5 Sonnet (original)
        "claude-3-opus-20240229"          # Fallback to Claude 3 Opus
    ]
    
    for model in models_to_try:
        try:
            # Test with a minimal call
            response = await litellm.acompletion(
                model=model,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5
            )
            print(f"✓ Using Claude model: {model}")
            return model
        except Exception as e:
            continue
    
    # If none work, return the default
    print("⚠ No Claude models accessible, using default")
    return "claude-3-5-sonnet-20241022"


class FinalIntegratedPipeline:
    """Robust pipeline for paper analysis."""
    
    def __init__(self, 
                 model: Optional[str] = None,
                 output_dir: str = "./papers_analysis"):
        """Initialize the pipeline."""
        self.model = model  # Will be set during pipeline run if None
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Custom retriever that prioritizes text formats
        self.retriever = PubMedRetriever(output_dir=str(self.output_dir))
        
        print(f"Pipeline initialized")
        if self.model:
            print(f"Model: {self.model}")
        else:
            print("Model: Will auto-detect best available Claude model")
        print(f"Output directory: {self.output_dir}")
    
    def search_papers(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search PubMed and get paper info."""
        print(f"\nSearching PubMed for: {query}")
        pmc_ids = self.retriever.search_pubmed(query, max_results)
        
        papers = []
        for pmc_id in pmc_ids:
            info = self.retriever.get_pmc_info(pmc_id)
            if info:
                papers.append(info)
        
        return papers
    
    def download_papers_smart(self, papers: List[Dict]) -> List[Dict]:
        """Download papers trying different formats intelligently."""
        results = []
        
        for paper in papers:
            pmc_id = paper['pmc_id']
            title = paper['title']
            
            print(f"\nDownloading: {title[:60]}...")
            
            # Try XML first (usually has good structured text)
            file_path = None
            
            # Try different methods
            methods = [
                ('XML', self.retriever.try_download_xml),
                ('Text', self.retriever.try_download_text),
                ('PDF', self.retriever.try_download_pdf)
            ]
            
            for format_name, download_method in methods:
                try:
                    temp_path = download_method(pmc_id, title)
                    if temp_path and self._validate_download(temp_path):
                        file_path = temp_path
                        print(f"  ✓ Downloaded as {format_name}: {Path(file_path).name}")
                        break
                except Exception as e:
                    print(f"  - {format_name} failed: {str(e)[:50]}")
            
            if file_path:
                results.append({
                    'pmc_id': pmc_id,
                    'title': title,
                    'file_path': file_path,
                    'url': paper['url']
                })
            else:
                print(f"  ✗ Could not download in any format")
        
        return results
    
    def _validate_download(self, file_path: str) -> bool:
        """Check if download is valid and contains content."""
        try:
            file_size = Path(file_path).stat().st_size
            if file_size < 1000:  # Too small, probably error page
                return False
            
            # Check if it's actually HTML error page
            with open(file_path, 'rb') as f:
                header = f.read(200)
                if b'403 Forbidden' in header or b'Access Denied' in header:
                    return False
            
            return True
        except:
            return False
    
    def extract_text(self, file_path: str) -> Optional[str]:
        """Extract text from any file format."""
        file_path = Path(file_path)
        
        try:
            # Read file content
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Try to decode as text
            try:
                text_content = content.decode('utf-8')
            except:
                text_content = content.decode('latin-1', errors='ignore')
            
            # Check if it's XML
            if file_path.suffix == '.xml' or '<?xml' in text_content[:100]:
                soup = BeautifulSoup(text_content, 'xml')
                
                # Extract article body
                article_body = soup.find('body')
                if article_body:
                    # Get all paragraphs
                    paragraphs = article_body.find_all(['p', 'sec'])
                    text = '\n\n'.join(p.get_text(strip=True) for p in paragraphs)
                    return text
                else:
                    # Fallback: get all text
                    return soup.get_text()
            
            # Check if it's HTML
            elif '<html' in text_content[:500].lower():
                soup = BeautifulSoup(text_content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text from paragraphs
                paragraphs = soup.find_all('p')
                if paragraphs:
                    text = '\n\n'.join(p.get_text(strip=True) for p in paragraphs)
                    return text
                else:
                    return soup.get_text()
            
            # Plain text
            else:
                return text_content
                
        except Exception as e:
            print(f"  Error extracting text: {str(e)[:100]}")
            return None
    
    async def analyze_with_claude(self, papers_data: List[Dict], question: str) -> Dict:
        """Analyze papers using Claude."""
        if not papers_data:
            return {"error": "No papers to analyze"}
        
        print(f"\n{'='*60}")
        print("Analyzing papers with Claude")
        print(f"{'='*60}")
        
        # Prepare paper contents
        paper_contents = []
        for paper in papers_data:
            text = self.extract_text(paper['file_path'])
            if text and len(text) > 500:  # Must have meaningful content
                # Limit text length
                max_chars = 20000
                if len(text) > max_chars:
                    text = text[:max_chars] + "\n[... truncated ...]"
                
                paper_contents.append({
                    'title': paper['title'],
                    'pmc_id': paper['pmc_id'],
                    'text': text,
                    'chars': len(text)
                })
                print(f"✓ {paper['title'][:50]}... ({len(text)} chars)")
        
        if not paper_contents:
            return {"error": "Could not extract meaningful text from papers"}
        
        # Build prompt
        prompt = f"You are analyzing {len(paper_contents)} research papers to answer a specific question.\n\n"
        prompt += f"QUESTION: {question}\n\n"
        
        for i, paper in enumerate(paper_contents, 1):
            prompt += f"\n{'='*50}\n"
            prompt += f"PAPER {i}: {paper['title']}\n"
            prompt += f"PMC ID: PMC{paper['pmc_id']}\n"
            prompt += f"{'='*50}\n\n"
            prompt += paper['text'][:15000]  # Limit per paper
            prompt += "\n\n"
        
        prompt += "\n\nBased on these papers, please provide a detailed answer to the question. "
        prompt += "Be specific with numbers, percentages, and confidence intervals where available. "
        prompt += "Cite which paper(s) support each claim."
        
        # Call Claude
        print("\nSending to Claude...")
        try:
            response = await litellm.acompletion(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a medical research analyst. Provide detailed, evidence-based answers citing specific papers."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2500
            )
            
            answer = response.choices[0].message.content
            
            return {
                "question": question,
                "answer": answer,
                "papers_analyzed": len(paper_contents),
                "total_chars_analyzed": sum(p['chars'] for p in paper_contents),
                "model": self.model,
                "timestamp": datetime.now().isoformat(),
                "papers": [
                    {
                        "title": p['title'],
                        "pmc_id": p['pmc_id'],
                        "chars_analyzed": p['chars']
                    }
                    for p in paper_contents
                ]
            }
            
        except Exception as e:
            return {"error": f"Claude API error: {str(e)}"}
    
    async def run_pipeline(self, search_query: str, question: str, max_papers: int = 3) -> Dict:
        """Run the complete pipeline."""
        print("\n" + "="*70)
        print("FINAL INTEGRATED PIPELINE: PubMed → Claude Analysis")
        print("="*70)
        
        # Auto-detect best Claude model if not specified
        if not self.model:
            print("\nDetecting best available Claude model...")
            self.model = await get_best_claude_model()
        
        # Step 1: Search
        papers = self.search_papers(search_query, max_papers)
        if not papers:
            return {"error": "No papers found in PubMed"}
        
        print(f"\nFound {len(papers)} papers")
        
        # Step 2: Download
        downloaded = self.download_papers_smart(papers)
        if not downloaded:
            return {"error": "Could not download any papers"}
        
        print(f"\nSuccessfully downloaded {len(downloaded)} papers")
        
        # Step 3: Analyze
        results = await self.analyze_with_claude(downloaded, question)
        
        # Add search metadata
        results['search_query'] = search_query
        results['papers_found'] = len(papers)
        results['papers_downloaded'] = len(downloaded)
        
        return results
    
    def display_results(self, results: Dict):
        """Display results in a nice format."""
        print("\n" + "="*70)
        print("ANALYSIS RESULTS")
        print("="*70)
        
        if "error" in results:
            print(f"\nError: {results['error']}")
            return
        
        print(f"\nSearch Query: {results.get('search_query', 'N/A')}")
        print(f"Question: {results.get('question', 'N/A')}")
        print(f"\nPapers analyzed: {results.get('papers_analyzed', 0)}")
        print(f"Total text analyzed: {results.get('total_chars_analyzed', 0):,} characters")
        
        print("\nPapers included:")
        for i, paper in enumerate(results.get('papers', []), 1):
            print(f"{i}. {paper['title'][:70]}...")
            print(f"   PMC{paper['pmc_id']} ({paper['chars_analyzed']:,} chars)")
        
        print(f"\n{'='*70}")
        print("ANSWER:")
        print("="*70)
        print(results.get('answer', 'No answer generated'))
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_{timestamp}.json"
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n\nResults saved to: {output_path}")


async def main():
    """Example usage."""
    pipeline = FinalIntegratedPipeline()
    
    # Example query
    results = await pipeline.run_pipeline(
        search_query="COVID-19 vaccine effectiveness systematic review meta-analysis",
        question="What is the effectiveness of COVID-19 vaccines against severe outcomes (hospitalization and death) based on systematic reviews and meta-analyses? Include specific effectiveness percentages.",
        max_papers=3
    )
    
    pipeline.display_results(results)


if __name__ == "__main__":
    asyncio.run(main())