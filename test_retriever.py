import pytest
from loaders import loader_chromadb, loader_weaviate, loader_graphdb

def test_chroma_query():
    retriever = loader_chromadb.init()
    results = retriever.query("What is a trade confirmation?", top_k=2)
    assert isinstance(results, list)
    assert len(results) > 0

def test_weaviate_query():
    retriever = loader_weaviate.init()
    results = retriever.query("List trade statuses", top_k=2)
    assert isinstance(results, list)

def test_graph_query():
    retriever = loader_graphdb.init()
    results = retriever.query("Which tables link trades and events?", top_k=2)
    assert isinstance(results, list)
