# Tests Directory

This directory contains all test files and utilities for the PubMed to Claude Analysis Pipeline.

## Test Files

### Setup & Verification
- `check_setup.py` - Verify dependencies and API keys are working
- `inspect_paperqa.py` - Analyze PaperQA2 configuration and structure

### Pipeline Tests
- `test_working_pipeline.py` - Working end-to-end test with Claude
- `test_full_pipeline.py` - Full pipeline test (needs PaperQA2 fixes)
- `test_minimal_pipeline.py` - Minimal PaperQA2 test
- `test_simple_paperqa.py` - Basic PaperQA2 functionality test
- `test_with_litellm.py` - LiteLLM integration test
- `test_pipeline.py` - Original pipeline test suite

## Usage

Run setup check first:
```bash
python tests/check_setup.py
```

Run working pipeline test:
```bash
python tests/test_working_pipeline.py
```

## Notes

- Most tests require ANTHROPIC_API_KEY in .env file
- Some tests may download papers for testing
- PaperQA2 integration tests may need additional configuration