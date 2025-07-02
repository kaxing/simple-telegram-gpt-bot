# OpenAI GPT Models Research Findings - December 2024

## Latest Available Models

Based on research conducted on December 27, 2024, here are the current OpenAI GPT models available via API:

### Flagship Models

#### GPT-4.1 Series
- **gpt-4.1** - Advanced flagship model with enhanced capabilities
  - Context window: 1,047,576 tokens (~1M tokens)
  - Max output: 32,768 tokens
  - Pricing: $2.00 per million input tokens, $8.00 per million output tokens
  - Release: April 14, 2025 (recently released)
  - Optimized for: Advanced instruction following, real-world software engineering, long-context reasoning
  - Performance: 54.6% on SWE-bench Verified, 87.4% on IFEval
  - Knowledge cutoff: June 2024

- **gpt-4.1-mini** - Smaller version of GPT-4.1
- **gpt-4.1-nano** - Ultra-compact version of GPT-4.1

#### GPT-4o Series  
- **gpt-4o** - Multimodal flagship model
- **gpt-4o-mini** - Compact multimodal model with low latency
- **chatgpt-4o-latest** - Latest ChatGPT version
- **gpt-4o-2024-11-20** - Specific version release
- **gpt-4o-2024-08-06** - Earlier specific version release

#### GPT-4 Series
- **gpt-4** - Original GPT-4 model
- **gpt-4-turbo** - Enhanced version with larger context
- **gpt-4-32k** - Extended context version

### Reasoning Models (o-series)

#### o4 Series
- **o4-mini** - Newest small reasoning model
  - Context window: 200,000 tokens
  - Max output: 100,000 tokens
  - Pricing: $1.16 per million input tokens, $4.62 per million output tokens
  - Performance: 83.2% MMLU, 92.7% AIME mathematics
  - Features: Multimodal capabilities, tool integration, Python execution

#### o3 Series
- **o3** - Advanced reasoning model with precise, context-aware answers
- **o3-mini** - Smaller version of o3

#### o1 Series
- **o1** - Reasoning-focused model
- **o1-mini** - Compact reasoning model
- **o1-preview** - Preview version
- **o1-pro** - Professional version with enhanced capabilities

### Legacy Models
- **gpt-3.5-turbo** - Cost-effective model for simpler tasks
- **gpt-3.5-turbo-instruct** - Instruction-tuned version
- **gpt-3.5-turbo-16k** - Extended context version

### Preview/Experimental Models
- **gpt-4.5-preview** - Preview of upcoming GPT-4.5

## Key Capabilities and Features

### Multimodal Support
Most newer models (GPT-4o series, o4-mini, etc.) support:
- Text and image inputs
- Vision understanding
- Diagram and chart analysis
- Multimodal reasoning

### Tool Integration
Advanced models support:
- Function calling
- Python code execution
- Web browsing capabilities
- API integrations

### Context Windows
- **GPT-4.1**: Up to 1M tokens
- **o4-mini**: 200K tokens
- **GPT-4o series**: Varies by model
- **o3/o1 series**: Typically 200K tokens

## Pricing Summary (per million tokens)

| Model | Input Cost | Output Cost |
|-------|------------|-------------|
| GPT-4.1 | $2.00 | $8.00 |
| o4-mini | $1.16 | $4.62 |
| GPT-4o | Varies | Varies |
| GPT-3.5-turbo | Lower cost | Lower cost |

## Performance Benchmarks

### GPT-4.1
- SWE-bench Verified: 54.6%
- IFEval (Instruction Following): 87.4%
- MMLU: 90.2%

### o4-mini  
- MMLU: 83.2%
- AIME (Mathematics): 92.7%
- Codeforces: ELO 2719

## Recommendations for Configuration Update

1. **Add new flagship models**: GPT-4.1, GPT-4.1-mini, GPT-4.1-nano
2. **Add o4-mini**: Latest efficient reasoning model
3. **Add o1-pro**: Professional reasoning model
4. **Add gpt-4o-mini**: Compact multimodal model
5. **Add gpt-4.5-preview**: Preview model
6. **Update vision models list**: Include all new multimodal-capable models

## Sources
- OpenRouter API documentation
- AI/ML API documentation  
- Third-party AI model comparison sites
- Research conducted on December 27, 2024