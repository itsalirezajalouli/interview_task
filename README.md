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

## Commit D: add 1 baseline evaluation test (precision)

  Let's pick a random document from existing docs in corpus.jsonl: I picked DOC-03.
  I will extend the corpus with 2 documents‍ that have similar contents to DOC-03
  but this time they don't act as documents but CHUNKS! to test CHUNK_SIZE
  chunking strategy one document will be 400 character (DOC-19-chunk1) and next
  one will be the rest of that document simulating the split effect (DOC-19-chunk2).

### AI Usage

    Of course, I used AI to generate the new document.

  For test #3 even if we ignore the previous bug and use my implementation instead
  We get bad results.

  I printed to see where in the results chunk 2 of "DOC-19" appears:

  ```python
    > ['DOC-19'(chunk 1), 'DOC-03', 'DOC-12', 'DOC-19'(chunk 1)]
  ```

  As you see in the 4th result with generous threshold of 0.3!
  We predicted DOC-03 got there sooner than DOC-19 (chunk 2) and it happend.

  Solution? using recursive chunking with overlap.
  In next commit I will implement the recursive chunking with overlap.
  Right now for baseline we have two tests that fail:
  F   test02_multi_doc_direct_query
  F   test03_multi_chunk_direct_query
  They are supposed to fail!

---

## Commit E: add recursive chunking + evaluation (precision)

  Chunking strategy quietly controls retrieval quality, so it's an important
  design decision, recursive chunking might not even be best strategy here but
  we should exhaust all the possible strategies.

  I added a new python module to my_implementation called recursive_chunking.py.
  It's a simple implemetation of recursive chunking

  It's logic follows something like this:
      Try splitting by paragraph (\n\n)
      If chunk too large → split by line (\n)
      If still too large → split by sentence (.,!?;...)
      If still too large → split by word
      If still too large → split by character (CHUNK_SIZE)

  In ingestion.py, in build_index_w_doc_model function i commented previous
  chunk_text(d.text) and changed it to recursive_chunking(d.text), then added
  a test to my_pipeline_evaluation.py called test03_multi_chunk_direct_query
  which even has EXACT STRING MATCHING COMPARISON between expected answer and
  retrieved document and guess what? the test goes green!

  The sentence that was cut in middle by CHUNK_SIZE now gets retrieved completely
  in this new pipeline because overlap and recursive chunking by seperators exists!

  I experimented with threshold and lowered it to 0.3 to see what are the other
  docs it retrieves:

```python
[(Chunk(id='DOC-19', title='Compressor C-100 — Separator Element Replacement', text='The air-oil separator element on this unit should be replaced every 4000 operating hours to maintain separation efficiency. '), 0.7995917797088623), (Chunk(id='DOC-03', title='Compressor C-100 — Specifications', text='It includes an integrated air-oil separator and an after-cooler. Ambient operating temperature should stay below 40 degrees Celsius. Condensate must be drained daily.'), 0.43372634053230286), (Chunk(id='DOC-19', title='Compressor C-100 — Separator Element Replacement', text='The C-100 compressor undergoes extended maintenance checks beyond the standard schedule. Technicians should verify belt tension, inspect the intake filter for fouling, '), 0.40845930576324463), (Chunk(id='DOC-03', title='Compressor C-100 — Specifications', text='The C-100 is a rotary screw air compressor. Rated output is 6 m3/min at 8 bar. Motor power is 37 kW. It includes an integrated air-oil separator and an after-cooler. '), 0.38761916756629944), (Chunk(id='DOC-12', title='Preventive Maintenance Intervals', text='Pumps are serviced every 2000 hours and compressors every 4000 hours. Keep a record of every intervention with date and technician.'), 0.36556902527809143)]
```

  The query is now responsed by 80% score, next best option is 43%.

  We improved retrieval quality with simplest chunking strategy (actually second
  simplest after your fixed CHUNK_SIZE chunking) possible.
  What we did here was improving "Structural Precision".

  I was thinking here I could try and implement semantic chunking and try to look
  like a know-it-all rag developer but why? this is a technical documentation corpus
  each sentence is already semantically dense... It's not a corpus of fictional
  books!

  If you ask about little dogs in "animal farm" your response is some lines from
  first pages of the book and some lines in the end of the book where they grew
  up by pigs and came back and semantic chunking would place those chunks grouped
  together but here we are not talking about stories spread between different
  lines in different places of the corpus so recursive chunking is good enough
  and I decided not to implement semantic chunking!

---

## Commit F: add negation evaluation test (MRR/Ranking quality)

  There is a solid metric for rag evaluation called "Mean Reciprocal Rank" which
  is 1 / position_of_correct_answer.
  It measures how we rank the correct answer?
  Like we expect the correct answer to be number 1 but if it appears number
  2 -> then 1/2 = 0.5, and if appears number 3 then 1/3 = 0.34.

  What we have here currently is a bi-encoder implementation, meaning query
  gets embeded and also docs. Common issue with this implementations is NEGATION!

  Not going to elaborate more till we have a test, and then I will show you what
  it is.

  I extended documents with 2 new docs: DOC-20 and DOC-21

### AI Usage

    I asked claude to generate 2 new docs resembeling DOC-03 but with negating
    conflicts. One of them talk about how to start C-100 compressor and one of
    of them talks about how it should NOT to strated!
    I got a little evil here and told claude to fill DOC-21 (wrong doc) with
    words in the test query:  C-100 compressor, started, conditions,
    starting, start.

  Test user query:
  "Under what conditions should the C-100 compressor not be started?"

  Added a test number 4 to baseline_evaluation.py and it got red:

  > AssertionError: 'DOC-21' not found in ['DOC-20'] : Retrieved document should be in expected documents.
  
  As expected it returned wrong document. But I went further and lifted the issue
  with one best match to see where in results we see the correct answer to measure
  our MRR:

```python
  [(Chunk(id='DOC-21', title='Compressor C-100 — Startup Conditions', text='The C-100 compressor should only be started when all operating conditions are confirmed within range. '), 0.8941630721092224), (Chunk(id='DOC-21', title='Compressor C-100 — Startup Conditions', text='Before starting the C-100 compressor, operators must verify that compressor start conditions are satisfied. Check all C-100 startup conditions before each start to confirm the unit is ready to run.'), 0.8186443448066711), (Chunk(id='DOC-19', title='Compressor C-100 — Separator Element Replacement', text='The C-100 compressor undergoes extended maintenance checks beyond the standard schedule. Technicians should verify belt tension, inspect the intake filter for fouling, '), 0.6730542778968811), (Chunk(id='DOC-03', title='Compressor C-100 — Specifications', text='The C-100 is a rotary screw air compressor. Rated output is 6 m3/min at 8 bar. Motor power is 37 kW. It includes an integrated air-oil separator and an after-cooler. '), 0.5356651544570923), (Chunk(id='DOC-20', title='Compressor C-100 — Inhibited Start States', text='Energisation of the C-100 drive motor is prohibited under any of the following inhibiting states: oil sight glass below minimum, thermostat reading above 45°C, '), 0.4197276532649994)]
```

  Brah! AMAZING! DOC-20 is in 5th rank!!!!!!!
  BASELINE's MRR IS 1/5 = 20 %
  HILLARITY XD!!!

  We definitely need a re-ranker to fix this.
  And that's what I'm going to implement in next commit.
