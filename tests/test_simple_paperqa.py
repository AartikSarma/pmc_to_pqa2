#!/usr/bin/env python3
"""
Test basic PaperQA2 functionality
"""

import asyncio
from paperqa import Docs, Settings

async def test_basic():
    # Test basic Docs creation
    print("Testing basic PaperQA2...")
    
    # Try creating Docs without settings first
    try:
        docs = Docs()
        print("✓ Basic Docs created successfully")
    except Exception as e:
        print(f"✗ Failed to create basic Docs: {e}")
        
    # Try with settings
    try:
        settings = Settings(
            llm="claude-3-opus-20240229",
            summary_llm="claude-3-haiku-20240307"
        )
        print(f"✓ Settings created: {settings}")
        
        # Check how to pass settings to Docs
        import inspect
        sig = inspect.signature(Docs.__init__)
        print(f"\nDocs.__init__ signature: {sig}")
        
    except Exception as e:
        print(f"✗ Failed with settings: {e}")

if __name__ == "__main__":
    asyncio.run(test_basic())