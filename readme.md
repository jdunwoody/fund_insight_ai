# Fund Insight AI

Uses an LLM to extract and summarise the views of a particular fund manager w.r.t. economic issues raised in the source documents.

Initial goals:

- populate metadata
  - fund manager (e.g. bridgewater, not names of people interviewed)
  - date (of publication)
  - source (doc path)

- answer the following question:
  - what is the fund manager (bridgewater's) view on how the US Economy is tracking?

- expected result:
  - changing from a resilient viewpoint to expecting a slowdown, where reasons haven't transpired.
  - the tone of the manager has changed over time

Eventual goals:

- how should you invest based on these views?
- so what next?

## installation

```
python 3.10
pip intall -r requirements.txt
```

## run

[main](src/main.py)
