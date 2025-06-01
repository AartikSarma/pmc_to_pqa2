#!/usr/bin/env python3
"""
Inspect PaperQA2 configuration to understand how to integrate properly
"""

import inspect
from paperqa import Docs, Settings
import paperqa
import pprint

print("PaperQA2 Configuration Analysis")
print("="*50)

# Check Settings attributes
print("\n1. Settings class attributes:")
settings = Settings()
for attr in dir(settings):
    if not attr.startswith('_'):
        try:
            value = getattr(settings, attr)
            if not callable(value):
                print(f"  {attr}: {type(value).__name__} = {str(value)[:50]}...")
        except:
            pass

# Check Docs initialization
print("\n2. Docs initialization signature:")
print(inspect.signature(Docs.__init__))

# Check what Docs accepts
print("\n3. Docs class attributes after creation:")
docs = Docs()
relevant_attrs = ['llm', 'summary_llm', 'embedding', '_llm_model', '_summary_llm_model']
for attr in relevant_attrs:
    if hasattr(docs, attr):
        value = getattr(docs, attr)
        print(f"  {attr}: {type(value).__name__}")

# Check paperqa.llms module
print("\n4. paperqa.llms module contents:")
if hasattr(paperqa, 'llms'):
    llms_module = paperqa.llms
    for item in dir(llms_module):
        if not item.startswith('_'):
            print(f"  {item}")

# Try to understand model configuration
print("\n5. Default LLM model configuration:")
if hasattr(docs, 'llm_model'):
    print(f"  Model name: {docs.llm_model.name if hasattr(docs.llm_model, 'name') else 'N/A'}")
    print(f"  Model config: {docs.llm_model.config if hasattr(docs.llm_model, 'config') else 'N/A'}")

print("\n6. How to properly set models:")
print("  Docs accepts these parameters directly:")
print("  - llm: str (model name)")
print("  - summary_llm: str (model name)")
print("  - llm_model: LLMModel instance")
print("  - summary_llm_model: LLMModel instance")