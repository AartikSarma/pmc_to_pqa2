#!/usr/bin/env python3
"""
Demo script showing PubMed search and download functionality.
This can run without API keys to demonstrate the retrieval capabilities.
"""

from pubmed_retriever import PubMedRetriever
import sys

def demo_search_only():
    """Demo search functionality without downloading."""
    print("="*60)
    print("PubMed Search Demo")
    print("="*60)
    
    # Initialize retriever
    retriever = PubMedRetriever(output_dir="./demo_papers")
    
    # Search for papers
    query = "CRISPR gene therapy"
    print(f"\nSearching PubMed for: '{query}'")
    print("-"*40)
    
    pmc_ids = retriever.search_pubmed(query, max_results=5)
    
    if not pmc_ids:
        print("No results found.")
        return
    
    print(f"Found {len(pmc_ids)} papers\n")
    
    # Get info for each paper
    for i, pmc_id in enumerate(pmc_ids, 1):
        article_info = retriever.get_pmc_info(pmc_id)
        if article_info:
            print(f"{i}. PMC{pmc_id}")
            print(f"   Title: {article_info['title']}")
            print(f"   URL: {article_info['url']}")
            print()


def demo_download_single():
    """Demo downloading a single paper."""
    print("\n" + "="*60)
    print("PubMed Download Demo")
    print("="*60)
    
    retriever = PubMedRetriever(output_dir="./demo_papers")
    
    # Search for a specific topic
    query = "COVID-19 mRNA vaccine"
    print(f"\nSearching for: '{query}'")
    
    pmc_ids = retriever.search_pubmed(query, max_results=1)
    
    if not pmc_ids:
        print("No results found.")
        return
    
    pmc_id = pmc_ids[0]
    article_info = retriever.get_pmc_info(pmc_id)
    
    if article_info:
        print(f"\nFound: {article_info['title']}")
        print(f"PMC ID: {pmc_id}")
        
        response = input("\nDownload this paper? (y/n): ")
        if response.lower() == 'y':
            print("\nDownloading...")
            file_path = retriever.download_fulltext(pmc_id, article_info['title'])
            if file_path:
                print(f"✓ Successfully downloaded to: {file_path}")
            else:
                print("✗ Download failed")


def main():
    """Run demo based on user choice."""
    print("\nPubMed Retrieval Demo")
    print("====================")
    print("\nThis demo shows the PubMed search and retrieval functionality.")
    print("No API keys required for basic search!\n")
    
    print("Options:")
    print("1. Search papers (no download)")
    print("2. Search and download one paper")
    print("3. Exit")
    
    choice = input("\nSelect option (1-3): ")
    
    if choice == "1":
        demo_search_only()
    elif choice == "2":
        demo_download_single()
    elif choice == "3":
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice. Please run again.")


if __name__ == "__main__":
    main()