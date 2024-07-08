<p align="center">
  <a href="https://www.citeme.ai/">
    <img src="assets/banner.png" alt="citeme.ai" />
  </a>
</p>


<p align="center">
  <a href="https://citeme.ai"><strong>Website & Dataset Download </strong></a>&nbsp; | &nbsp;
  <a href="https://citeme.ai/paper"><strong>Preprint</strong></a>
</p>

**CiteME is a dataset that tests Language Models in their ability to find papers cited by scientific texts.**

## 📝 tl;dr
CiteME is a benchmark designed to test the abilities of language models in finding papers that are cited in scientific texts.

## ❓ What's the task?
Each question in CiteME is made up of a text excerpt (taken from a research paper) that cites a single paper. The cited paper is marked with the word [CITATION]. For each excerpt, the goal is to find the title of the cited paper.

## 📊 CiteME Evaluation
We enable language models to search for papers, read them, and then pick the paper it thinks is cited. In addition to the 3 LMs tested, we also test two SPECTER models.

## 🏆 Leaderboard
|           | GPT-4o | LLaMa-3-70B | Claude 3 Opus | SPECTER2 | SPECTER1 |
|-----------|--------|-------------|---------------|----------|----------|
| Accuracy [%] | **35.3** | 21.0 | 27.7 | 0 | 0 |

## 🚀 CiteAgent in Action
We enable language models to search for papers, read them, and then pick the paper it thinks is cited. We refer to this combination of commands and LMs as "CiteAgents". To see CiteAgents in action, [click here](https://www.citeme.ai/trajectories.html).



## Dataset

**The hand curated version of the dataset can be found on [citeme.ai](https://www.citeme.ai).**  
It contains following columns:
- `id`: A unique id that is used in all our experiments to reference a specific paper.
- `excerpt`: The text excerpt describing the target paper.
- `target_paper_title`: The title of the paper described by the excerpt.
- `target_paper_url`: The URL to the paper described by the excerpt.
- `source_paper_title`: The title of the paper the excerpt was taken from.
- `source_paper_url`: The URL to the paper the excerpt was taken from.
- `year`: The year the source paper was published.
- `split`: Indicates if the sample is from the `train` or `test` split.

## CiteAgent

### Environment variables

CiteAgent requires following environment variables to function properly:
- `S2_API_KEY`: Your semantic scholar api key
- `OPENAI_API_KEY`: Your openai api key (for gpt-4 models)
- `ANTHROPIC_API_KEY`: Your anthropic api key (for claude models)
- `TOGETHER_API_KEY`: Your together api key (for llama models)

### Run
1. Install the required python packages listed in the `requirements.txt`.
   ```
   pip install -r requirements.txt
   ```

2. Download the dataset from [citeme.ai](https://www.citeme.ai) and place it in the project folder as `DATASET.csv`.

3. Run the `main.py` file.
   ```
   python src/main.py
   ```

### Configuration

To modify the run parameters open `src/main.py` and update the `metadata` dict.

To run different models adjust the `model` entry (e.g. `gpt-4o`, `claude-3-opus-20240229` or `meta-llama/Llama-3-70b-chat-hf`).

To run the agent without actions change the executor from `LLMSelfAskAgentPydantic` to `LLMNoSearch` and adjust the `prompt_name` to a `*_no_search` prompt.



## 📚Citation
### If you find our work helpful, please use the following citation:
```
@misc{press2024citeme,
    title={CiteME: Can Language Models Accurately Cite Scientific Claims?},
    author={Ori Press and Andreas Hochlehnert and Ameya Prabhu and Vishaal Udandarao and Ofir Press and Matthias Bethge},
    year={2024},
    eprint={},
    archivePrefix={arXiv},
    primaryClass={cs.ML}
}
```
