# RAAR: Retrieval Augmented Agentic Reasoning for Cross-Domain Misinformation Detection

[RAAR paper](https://arxiv.org/abs/2601.04853)

The code is being organized and will be released soon... 

## News

📢 *Jan. 2026* New preprint paper "RAAR: Retrieval Augmented Agentic Reasoning for Cross-Domain Misinformation Detection" [arXiv](https://arxiv.org/abs/2601.04853).


## Models in RAAR

There are a series of RAAR models, including RAAR-8b, RAAR-14b, MisSFT-8b, and MisSFT-14b.

- RAAR-8b: The 8b model for cross-domain misinformation detection after two stages of optimization (SFT+RL).
- RAAR-14b: The 14b model for cross-domain misinformation detection after two stages of optimization (SFT+RL).
- MisSFT-8b: The 8b model for cross-domain misinformation detection after SFT.
- MisSFT-14b: The 14b model for cross-domain misinformation detection after SFT.

All models can be found at [RAAR collection](https://huggingface.co/collections/lzw1008/raar)

## Usage

The processed data are in the datasets folder. 

NOTE: The datasets in this project are just for review. If you would like to use the datasets, please make sure to comply with the original data's license or obtain authorization from the author of the original data.

Original data link: [AMTCele](https://aclanthology.org/C18-1287/), [PHEME](https://aclanthology.org/C18-1288/), [COCO](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10071453/).

### Stage 1: Retrieval Augmented Data Building

```python
cd Stage1
- Follow 1.ObtainEmbeddings.ipynb to obtain the embeddings of sentiment, semantic, and style.
- Follow 2.Retrieval.ipynb to retrieval samples.
- Follow 3.ConstructDatasets.ipynb to construct the RA data
```

### Stage 2: Multi-agent Collaborated Reasoning Path Building

```python
# Construct the reasoning paths, you need to first add the api key in call_llm.py and subagents.py
cd Stage2
python cot_build.py
```

### Stage 3: Two-step model optimization

- SFT: We use the mature LLama-factory framework for SFT training. Please refer to the [LLama-factory code](https://github.com/hiyouga/LlamaFactory).
- RL: We use the mature open-r1 framework for SFT training. Please refer to the [openr1 code](https://github.com/huggingface/open-r1).

