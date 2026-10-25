---
title: "1.1 · Dataset and preprocessing"
linkTitle: "1.1 Dataset and preprocessing"
weight: 1
math: true
---
<div class="nb-proto">

<em><span>Prototypical example for this section:</span> the validation sentence <em>“Eine Gruppe von Männern lädt Baumwolle auf einen Lastwagen”</em>, which becomes $11$ token ids with <em>Baumwolle</em> mapped to `<unk>`.</em>

</div>

## 1.1.i Source and splits {#s1-1-i}

The data is the Hugging Face dataset `bentrevett/multi30k`, loaded with `load_dataset` at `dataset.py:96`. Each example is a pair of fields `de` and `en`: one image caption in German and its English counterpart.

| Split | Pairs | German tokens<br>mean | max | English tokens<br>mean | max | `<unk>` rate (de / en) |
|:--|--:|--:|--:|--:|--:|--:|
| train | 29,000 | 14.44 | 46 | 15.11 | 43 | 3.00% / 1.03% |
| validation | 1,014 | 14.63 | 35 | 15.24 | 34 | 4.47% / 1.94% |
| test | 1,000 | 14.10 | 33 | 15.06 | 35 | 3.75% / 1.68% |

Lengths count the added `<sos>` and `<eos>`; `<unk>` rates are over real tokens only. These statistics are my re-computation with the project’s own tokeniser and vocabulary. $178$ of the $1{,}000$ English test references contain at least one `<unk>` after this preprocessing; that number matters in [Section What the BLEU numbers really measure](../implementation/#sec-a3-bleu-caveat).

## 1.1.ii Tokenisation {#s1-1-ii}

Both languages are split into words with spaCy’s rule-based tokenisers from the small pipelines `de_core_news_sm` and `en_core_web_sm` (`dataset.py:101-102`), and every token is <em>lower-cased</em> (`dataset.py:111-123`). Only the tokeniser is called, as `spacy_de.tokenizer(text)` rather than `spacy_de(text)`. That skips the tagger, parser and entity recogniser, which are not needed here.

<div class="nb nb-remark" id="remark-1-1-1">

<strong>Remark 1.1.1</strong> (Why word-level tokens) — The spec only allows spaCy for preprocessing, so the standard alternative for translation, a learned sub-word vocabulary such as BPE, was not an option. The price is the `<unk>` rate above: a word seen only once in training cannot be translated at all. Lower-casing merges forms like <em>Ein</em> and <em>ein</em>, which helps a 29k-sentence dataset, but the model can then never produce capital letters.

</div>

## 1.1.iii Vocabulary {#s1-1-iii}

The `Vocab` class (`dataset.py:20-73`) is written by hand; torchtext is not used.

```python {filename="dataset.py, lines 20–48",linenos=table,linenostart=20}
class Vocab:

    # These 4 special tokens must always be at fixed positions
    SPECIALS = ['<unk>', '<pad>', '<sos>', '<eos>']

    def __init__(self, counter, min_freq=2):
        super(Vocab, self).__init__()

        # Start building index-to-string list with the special tokens first
        self.itos = []
        for special in self.SPECIALS:
            self.itos.append(special)

        # Now add regular words that appear often enough in the corpus
        # We sort by frequency (most_common gives highest freq first)
        for word, freq in counter.most_common():
            if freq >= min_freq:
                # Make sure we don't accidentally add a special token again
                if word not in self.SPECIALS:
                    self.itos.append(word)

        # Build the reverse mapping: string -> index, for fast token lookup
        self.stoi = {}
        for idx in range(len(self.itos)):
            word = self.itos[idx]
            self.stoi[word] = idx

        # Index of unknown token for handling out-of-vocabulary words
        self._unk_idx = self.stoi['<unk>']
```

- The four special tokens always get the first four indices: `<unk>` $=0$, `<pad>` $=1$, `<sos>` $=2$, `<eos>` $=3$. The mask helpers in `model.py` rely on this, since their default is `pad_idx=1`.
- Words are added in decreasing frequency, keeping only those seen at least `min_freq` $=2$ times.
- Looking up a word that is not in the vocabulary returns `<unk>` (`dataset.py:53-58`).

The vocabularies are built from the <em>training split only</em> (`dataset.py:125-141`); the validation and test datasets are given the training vocabularies before `process_data` runs (`train.py:311-319`), so no information leaks from the evaluation data. The resulting sizes, printed in every training log and stored in the checkpoint, are

$$
V_{\text{src}} = 7{,}853 \quad \text{(German)}, \qquad V_{\text{tgt}} = 5{,}893 \quad \text{(English)}.
$$

## 1.1.iv From sentences to batches {#s1-1-iv}

`process_data` (`dataset.py:143-177`) turns every pair into two lists of ids, each wrapped as $[\texttt{<sos>}, w_1, \dots, w_n, \texttt{<eos>}]$. Batches are built by a collate function that pads every sequence to the longest one in the batch with `<pad>` (`train.py:329-338`):

- training and validation: batch size $128$, training data shuffled every epoch;
- test: batch size $1$, because greedy decoding runs one sentence at a time.

With $29{,}000$ training pairs, one epoch is $\lceil 29000/128 \rceil = 227$ optimiser steps; this number returns several times below.

## 1.1.v What is not done {#s1-1-v}

There is no normalisation or augmentation: neither applies to token ids. There is also no random seed anywhere in the code or the notebooks: data order, dropout masks and the initial weights differ from run to run. [Section 1.4.iv](../experiments/#sec-a3-noise) measures how much that matters.

<div class="nb nb-example nb-block" id="example-1-1-2">

<strong>Example 1.1.2</strong> (The attention sample, end to end)

The first validation pair is <em>“Eine Gruppe von Männern lädt Baumwolle auf einen Lastwagen”</em> / <em>“A group of men are loading cotton onto a truck”</em>. After tokenisation and lower-casing the German side becomes

`<sos> eine gruppe von männern lädt <unk> auf einen lastwagen <eos>`,

$11$ ids, because <em>baumwolle</em> (cotton) occurs fewer than twice in training. In the first validation batch the longest German sentence has $35$ tokens, so this sentence is padded with $24$ `<pad>` ids.

</div>
