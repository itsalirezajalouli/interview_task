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

## Commit B: add evaluation data model

  Nothing major to explain. Just added EvaluationTest and EvaluationResult
  BaseModels as abstractions for how to do the evaluations.

  Now I'm going to implement different evaluation unit tests for commit C.
  I'll use "green" and "unittest" for unit test, because I have previous experience with it.

---

## Commit C: add 2 evaluation tests (correctness + recall)

  I started writing correctness tests with unittest and "green" and after a
  single test I spotted one big problem in the baseline implementation, It only
  returns best-matching chunk!

  What if user query's answer was spread among 2 or 3 docs?
  We would never see anything from second or third document unless we wrote
  a very detailed query with a large similarity between query and target document.

  Here's the first diagnosis and the first point my implementation will diverge
  from your baseline.

  I created a module called my implementation and copy-pasted your functions.
  I modified them to have better type hinting and safety and also changed argmax
  logic to argpartition, I found argpartition in a stackoverflow thread from 14
  years ago:

  <https://stackoverflow.com/questions/6910641/how-do-i-get-indices-of-n-maximum-values-in-a-numpy-array>

### AI Usage

    I will be using claude for generating 2 other documents that common information
    about one single item, so DOC-16 and DOC-17 content are ai-generated, cause
    I'm lazy to write extention docs.

  Okay I know it's a large patch to push for a commit but it's okay, cause I
  diagnosed one issue and fixed it in my own implementation, now test number 2
  t02_multi_doc_direct_query goes red for baseline if you run following command
  but it goes green for my implementation.

  ```bash
    green -vvv evaluation
  ```
  
  This was just a minor implementation bug, next I'm going to fix the bigger
  issue: our chunking strategy!

  Probably will add 2 more docs with more than 400 chars and put the answer to
  user query in the exact chunk size threshold (400 characters).
  Splitting mid sentence and with no overlap will break semantic connections.

  In that case: even if you didn't have this previous bug and returned multiple
  chunks(docs) ONLY ONE OF THOSE two most related chunks would appear at the
  top of your results. This needs a kind of document that after 400 chars threshold
  is not that similar to first chunk.

---

## Commit D: precision
