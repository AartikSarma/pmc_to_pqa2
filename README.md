# Retrieve papers from PMC and send them to PaperQA2/Claude

A fully integrated pipeline that searches PubMed Central, downloads scientific papers, and analyzes them using Claude AI. Powered by FutureHouse's PaperQA2 for advanced document analysis and question-answering.

## ✅ Status: Fully Working

The integration is complete and tested. The pipeline successfully:
- Searches PubMed Central for scientific papers
- Downloads papers in multiple formats (XML, text, PDF)
- Extracts text content properly
- Analyzes papers using Claude 3 Opus via LiteLLM
- Provides detailed answers with citations

## 🚀 Quick Start

1. **Set up your environment:**
```bash
# Create .env file with your API key
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env

# Install dependencies
pip install -r requirements.txt
```

2. **Run the pipeline:**
```bash
python final_integrated_pipeline.py
```

3. **Custom analysis:**
```bash
python run_example_analysis.py
```

## 📁 Key Files

### Core Components
- `pubmed_retriever.py` - PubMed search and download functionality
- `final_integrated_pipeline.py` - **Main integration script** (recommended)
- `integrated_pipeline.py` - Alternative implementation
- `paperqa_claude_integration.py` - PaperQA2 integration attempt (partial)

### Examples & Tests
- `run_example_analysis.py` - Example CRISPR analysis
- `demo_pubmed_search.py` - Interactive PubMed search demo
- `check_setup.py` - Verify your setup

## 🔧 How It Works

```python
from final_integrated_pipeline import FinalIntegratedPipeline

# Initialize pipeline
pipeline = FinalIntegratedPipeline(
    model="claude-3-opus-20240229",  # or claude-3-5-sonnet-20241022
    output_dir="./my_analysis"
)

# Run analysis
results = await pipeline.run_pipeline(
    search_query="your PubMed search terms",
    question="Your analysis question?",
    max_papers=3
)

# Display results
pipeline.display_results(results)
```

## 📊 Example Results

The pipeline successfully analyzes papers and provides:
- Detailed answers based on paper content
- Citations to specific papers
- Extraction of key findings and data
- Summary of safety concerns, efficacy results, etc.

## 🎯 Features

1. **Smart Download Strategy**
   - Tries XML first (best structured text)
   - Falls back to text format
   - Handles PDF as last resort
   - Validates downloads

2. **Robust Text Extraction**
   - Handles XML, HTML, and plain text
   - Extracts meaningful content
   - Limits text length for API efficiency

3. **Claude Integration**
   - Auto-detects best available Claude model
   - Prioritizes latest Sonnet models (Claude 4 → 3.5 new → 3.5 → 3 Opus)
   - Provides context-aware responses

4. **Error Handling**
   - Validates API keys
   - Handles download failures
   - Provides clear error messages

## 🔍 Available Claude Models

- `claude-3-opus-20240229` - Most powerful (default)
- `claude-3-5-sonnet-20241022` - Balanced performance
- `claude-3-haiku-20240307` - Fast and efficient

## 💡 Tips

1. **Better Results**: Use specific search terms including "systematic review" or "meta-analysis"
2. **API Limits**: The pipeline limits text to ~15,000 chars per paper to stay within limits
3. **File Formats**: XML downloads usually provide the best text extraction

## 🐛 Troubleshooting

- **"Invalid PDF header"**: PubMed sometimes returns HTML instead of PDF. The pipeline handles this automatically.
- **No text extracted**: Try different search terms or increase `max_papers`
- **API errors**: Check your ANTHROPIC_API_KEY in .env file

## 📈 Next Steps

The pipeline is ready for:
- Research literature reviews
- Systematic analysis of scientific evidence
- Automated paper summarization
- Question-answering from scientific literature

## 🙏 Acknowledgments

This pipeline is built on top of:
- **[PaperQA2](https://github.com/Future-House/paper-qa)** by FutureHouse - Advanced document analysis and question-answering framework
- **[LiteLLM](https://github.com/BerriAI/litellm)** - Universal LLM API interface
- **NCBI E-utilities** - PubMed Central access and paper retrieval
- **Anthropic Claude** - State-of-the-art language model for analysis

Special thanks to the FutureHouse team for creating PaperQA2, which powers the sophisticated document analysis capabilities of this pipeline.

## 🎉 Success!

The integration successfully combines PubMed's vast research database with Claude's analytical capabilities, powered by FutureHouse's PaperQA2, creating a powerful tool for scientific literature analysis.