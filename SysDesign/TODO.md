## Directory: System_Design
## Topics that must be covered
- Requirements Gathering: Defining Functional vs. Non-functional requirements (latency, throughput, availability)
- Recommendation Systems: Collaborative Filtering (user-user/item-item), Content-based filtering, Hybrid approaches, Two-Tower neural models, Ranking (LambdaMART)
- Search Engines: Inverted Indexing (BM25) vs. Dense Retrieval (vector search), Hybrid search (combining sparse + dense), Reranking
- Conversational Chatbots: Dialogue state management, Memory (short-term vs. long-term), Tool integration, Graceful fallback strategies
- Inference Architectures: Batch inference (offline, nightly jobs) vs. Real-time/Online inference (sub-100ms latency)
- Data Pipelines: ETL (Extract, Transform, Load) vs. ELT, Streaming pipelines using Kafka/Kinesis for feeding real-time features
