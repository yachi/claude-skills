# Should we use Pinecone or Weaviate for vector search? Does pgvector support HNSW?

## Executive Summary

Use Pinecone over Weaviate for managed simplicity. pgvector does support HNSW.
Confidence: 75%.

## Alternatives Considered

### 1. Pinecone
Managed, low ops. Chosen.

### 2. Weaviate
Self-hosted, more control. Ranked lower on ops burden.

## Recommendation

Adopt Pinecone. pgvector has HNSW indexing in version 0.5.0, so it works.
