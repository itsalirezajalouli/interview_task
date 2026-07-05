# I4Twins Technical Task Decision Record

## Commit A: Initial Commit - Sunday - 14:32

  The task was given to me at 11:33 AM but instead of baseline_rag.py and
  corpus.jsonl I was mistakenly given a private_eval.jsonl which looked like the
  evaluation set that I am tasked to craft. I informed the interviewers and I
  got corpus.jsonl and baseline_rag.py at 1:18 PM today.

  I'm gonna be honest, I have read those sample evaluations and they might have
  biased my thinking about how to solve this challenge,
  but I will try to find my own way to tackle this.

  Since then I have initialized project with uv, and placed required files and
  installed dependencies.

  This commit has no code/implementation value, I'm just going to record my
  initial thought process and decisions.

  I might be wrong and shoot myself in the foot.

### First Decision Record

  I want to start by implementing the evaluation set. I think I would implement
  them in unit test fashion with asserts everywhere (God help me), cause how can
  we diagnose the current baseline issues and improve it if we don't have a good
  evaluation test suit.

  I have some initial hunches but I don't want to get biased before testing.
  I used neovim to count longest documentation's character count (I use nvim btw!).

  The longest documentation is 342 characters and 53 words... Well that's our
  first weak point to fix, looking at baseline_rag.py CHUNK_SIZE equals to 400
  characters, sample corpus needs longer docs to evaluate the pipline
  better and certainly a character count chunking strategy will fail for longer
  docs and semantic coherence of chunks will lose quality.

  In fact that's why you had an extention_docs.jsonl in the files you mistakenly
  sent me(I guess).

  In next commit I will push an evaluation module skeleton and an evaluation
  data model.

---
