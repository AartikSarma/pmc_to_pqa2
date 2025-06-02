# PubMed to PaperQA2 Analysis Pipeline

A streamlined pipeline that searches PubMed Central, downloads scientific papers, and analyzes them using Claude AI through FutureHouse's PaperQA2 framework.

## ✅ Status: Fully Working

This pipeline successfully handles PMC's anti-bot protection and delivers comprehensive scientific analysis:
- ✅ Searches PubMed Central for research papers
- ✅ Downloads papers (handles PDF blocking with XML fallback)
- ✅ Converts XML to text for optimal analysis
- ✅ Analyzes papers using Claude 3.5 Sonnet via PaperQA2
- ✅ Provides detailed answers with proper citations
- ✅ Saves results to JSON files

## 🚀 Quick Start

1. **Set up your environment:**
```bash
# Copy and configure environment variables
cp .env.example .env
# Edit .env to add your ANTHROPIC_API_KEY

# Install dependencies
pip install -r requirements.txt
```

2. **Run the pipeline:**
```bash
python paperqa2_simple.py
```

This will automatically:
- Search for ARDS molecular phenotype papers
- Download and convert them to text format
- Analyze them with PaperQA2
- Save results to `simple_papers/ards_analysis_results_[timestamp].json`

## 📁 Key Files

### Core Components
- `paperqa2_simple.py` - **Main pipeline script** (recommended)
- `pubmed_retriever.py` - Enhanced PubMed search and download with anti-bot handling
- `example_usage.py` - Original usage example for the retriever
- `requirements.txt` - All required dependencies
- `.env.example` - Template for API configuration

## 🔧 How It Works

The pipeline handles PMC's modern anti-bot protection by:

1. **Smart Download Strategy**
   - Attempts PDF download first
   - Detects PMC's "Proof of Work" challenge pages
   - Falls back to XML format via E-utilities API
   - Converts XML to clean text for analysis

2. **PaperQA2 Integration**
   - Uses the latest PaperQA2 `ask()` function
   - Leverages Claude 3.5 Sonnet for analysis
   - Provides evidence-based answers with citations
   - Saves comprehensive results including contexts

## 📊 Example Results

Recent analysis of ARDS molecular phenotypes found:

**Two Main ARDS Phenotypes:**
1. **Hyperinflammatory**: Higher cytokines, lower bicarbonate, higher mortality
2. **Hypoinflammatory**: Lower cytokines, higher bicarbonate, better outcomes

**Key Biomarkers:**
- Endothelial damage markers (angiopoietin-2)
- Inflammatory markers (IL-6, IL-8, TNF-α)
- Coagulation markers (protein C, D-dimer)

## 🎯 Key Features

### Advanced PDF Handling
- Detects PMC's anti-bot "Proof of Work" challenges
- Automatically falls back to XML when PDFs are blocked
- Maintains full scientific content through E-utilities API

### Robust Text Processing
- Converts PMC XML to clean, structured text
- Extracts titles, authors, abstracts, and body content
- Preserves scientific formatting and citations

### PaperQA2 Integration
- Uses latest PaperQA2 framework for sophisticated analysis
- Leverages Claude 3.5 Sonnet for state-of-the-art reasoning
- Provides evidence-based answers with proper citations
- Saves detailed results including source contexts

## 🔧 Customization

You can modify the pipeline for different research questions:

```python
# In paperqa2_simple.py, change the search query:
query = "your research topic keywords"

# Change the analysis question:
question = "Your specific research question?"

# Adjust number of papers:
pmc_ids = retriever.search_pubmed(query, max_results=10)
```

## 💡 Tips for Better Results

1. **Search Strategy**: Use specific medical/scientific terms
2. **Paper Quality**: Include terms like "systematic review" or "meta-analysis"
3. **Recent Research**: PMC typically has the latest peer-reviewed content
4. **Question Formulation**: Ask specific, focused questions for better analysis

## 🐛 Troubleshooting

### Common Issues
- **"Proof of Work challenge"**: Normal - pipeline automatically uses XML fallback
- **Rate limiting (429 errors)**: Reduce `max_results` or add delays
- **No papers found**: Try broader search terms
- **API errors**: Verify `ANTHROPIC_API_KEY` in `.env` file

### PMC Access Notes
- PMC now uses JavaScript-based anti-bot protection for PDFs
- XML format via E-utilities API remains fully accessible
- Pipeline automatically handles this transition transparently

## 🌟 Success Story

This pipeline successfully analyzed ARDS research papers and identified distinct molecular phenotypes with their clinical implications, demonstrating its capability for serious scientific literature analysis.

## 🙏 Acknowledgments

Built with:
- **[PaperQA2](https://github.com/Future-House/paper-qa)** by FutureHouse - Advanced document Q&A framework
- **[NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25497/)** - Programmatic access to PubMed Central
- **[Anthropic Claude](https://www.anthropic.com/)** - State-of-the-art language model
- **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)** - XML/HTML parsing

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.