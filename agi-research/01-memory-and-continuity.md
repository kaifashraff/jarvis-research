# OpenClaw AGI Memory Architecture — Research Report

## Memory & Continuity: From Chat Agent to Persistent Intelligence

**Date:** 2026-04-06  
**Author:** Agent 1 (Retry) — Memory & Continuity Architecture Research Team  
**For:** OpenClaw / R Company / Kaif Ashraf  
**Version:** 1.0 — Foundational Research

---

## Executive Summary

OpenClaw currently operates as a highly capable, session-bound chat agent with rudimentary file-based memory (`memory/YYYY-MM-DD.md` and `MEMORY.md`). To evolve into an AGI-like system — one that learns, reasons, plans, and acts with continuity across thousands of sessions — requires a fundamental re-architecture of its memory subsystem.

This report presents a comprehensive **Memory and Continuity Architecture** for OpenClaw, drawing from proven systems (MemGPT, LangChain, AutoGPT, LlamaIndex), cognitive science, and production-grade vector database patterns. The architecture covers ten research areas, from theoretical foundations to concrete implementation steps, all designed to be deployable within OpenClaw's existing infrastructure (EC2, Node.js runtime, Telegram/Browser channels, free-tier economics).

**Key thesis:** Memory is not storage. Memory is *retrieval architecture*. The difference between a chatbot and an AGI system is not the size of its database — it is the quality of its retrieval pathways, the selectivity of its encoding, and the intelligence of its forgetting.

---

## 1. Long-Term Memory Systems

### 1.1 The Tripartite Model: Episodic, Semantic, Procedural

Human memory is not one system. Neuroscience identifies at least three functionally distinct memory systems, each of which maps cleanly onto OpenClaw's evolving needs:

```
┌──────────────────────────────────────────────────────────────┐
│                 OPENCLAW MEMORY ARCHITECTURE                  │
├──────────────────┬──────────────────┬────────────────────────┤
│  EPISODIC        │  SEMANTIC        │  PROCEDURAL            │
│  (What happened) │  (What is true)  │  (How to do things)    │
├──────────────────┼──────────────────┼────────────────────────┤
│ • Raw session    │ • Facts,         │ • Skills, workflows,   │
│   logs           │   entities,      │   automation recipes   │
│ • Timestamped    │   relationships  │ • Learned patterns     │
│   events         │ • Business       │ • Heuristics           │
│ • Conversation   │   rules          │ • Response templates   │
│   snippets       │ • Kaif's         │ • Decision rules       │
│ • Decisions made │   preferences    │                        │
├──────────────────┼──────────────────┼────────────────────────┤
│  Storage:        │  Storage:        │  Storage:              │
│  Flat files +    │  Knowledge       │  SKILL.md +            │
│  session logs    │  Graph +         │  workflows/ +          │
│                  │  Vector DB       │  action_registry       │
└──────────────────┴──────────────────┴────────────────────────┘
```

**Episodic Memory** stores raw session data: what Kaif asked, what Jarvis replied, what decisions were made, what outcomes occurred. This is the "raw stream" of consciousness. Current implementation: `memory/YYYY-MM-DD.md`. This is adequate but unstructured.

**Semantic Memory** stores distilled, context-independent knowledge: "Kaif owns R Company," "Zari prices spike before Diwali," "Buyer X always pays 15 days late." This is the "what is true" layer. Current implementation: `MEMORY.md` is a flat-file approximation of semantic memory. It does not scale.

**Procedural Memory** stores "how to do things": how to format a quotation, how to check heartbeat, how to respond to a buyer inquiry. This maps to OpenClaw's Skill system — and is the most mature subsystem.

### 1.2 Vector Databases for Semantic Search

Semantic memory cannot be stored in flat files alone. When OpenClaw needs to answer "What did we learn about Buyer X last month?" or "Has Kaif ever dealt with this supplier before?", flat-file grep is insufficient. Semantic similarity search over vector embeddings is required.

**Production-ready options for OpenClaw's constraints (free/low-cost, EC2-hosted):**

| Option | Cost | Self-host? | Complexity | Fit for OpenClaw |
|--------|------|-----------|------------|------------------|
| **LanceDB** | Free | Yes | Low | ★★★★★ Best fit — embedded, no server, disk-based, supports vector + full-text |
| **Chroma** | Free | Yes | Medium | ★★★★☆ Popular, good JS client, needs separate process |
| **Qdrant** | Free tier | Yes | High | ★★★★☆ Production-grade, Rust-based, has free cloud tier |
| **pgvector (PostgreSQL)** | Free | Yes | Medium-High | ★★★★☆ If Postgres already in use; adds operational weight |
| **Faiss (Facebook)** | Free | Yes | High | ★★★☆☆ Fast but complex; no native JS bindings |
| **Pinecone** | Free tier | No | Low | ★★☆☆☆ Vendor lock-in, free tier very limited |

**Recommendation: LanceDB.** It is:
- **Embedded**: No separate server process. Runs inside the Node.js runtime via its JS/TypeScript bindings.
- **Disk-based**: Persistent storage without memory pressure. Ideal for EC2 instances with limited RAM.
- **No external dependencies**: Just `npm install lancedb`.
- **Vector + hybrid search**: Supports ANN (approximate nearest neighbor) search and metadata filtering.
- **Free and open-source**: Apache 2.0 license.

### 1.3 Knowledge Graphs for Relational Memory

Vector search finds *similar* items. Knowledge graphs find *related* items. These are complementary.

Example: "Kaif spoke to Supplier A about Zari thread. Supplier A also supplies Buyer B's factory. Buyer B pays late." A vector search for "Supplier A" finds relevant passages. A knowledge graph reveals the **path**: Kaif → spoke to → Supplier A → supplies → Factory B → owned by → Buyer B → pays late.

**Implementation approach for OpenClaw:**

```typescript
// Conceptual: Knowledge Graph node and edge types
interface KGNode {
  id: string;          // e.g., "kaif", "r_company", "buyer_x", "zari_supplier_a"
  type: 'person' | 'company' | 'supplier' | 'buyer' | 'material' | 'event' | 'location';
  properties: Record<string, string | number | Date>;
}

interface KGEdge {
  source: string;      // source node id
  target: string;      // target node id
  relation: 'owns' | 'supplies' | 'buys_from' | 'pays_late' | 'spoke_to' | 'located_in';
  weight: number;      // 0-1 confidence/relevance
  timestamp: Date;     // when this relationship was observed
}
```

For a lightweight, self-hosted knowledge graph, use **SQLite** with adjacency lists, or **Neo4j Community** if willing to run a separate JVM process. For OpenClaw's constraints, I recommend a **simple SQLite-based graph**:

```sql
CREATE TABLE kg_nodes (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  properties TEXT  -- JSON
);

CREATE TABLE kg_edges (
  source TEXT REFERENCES kg_nodes(id),
  target TEXT REFERENCES kg_nodes(id),
  relation TEXT NOT NULL,
  weight REAL DEFAULT 1.0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (source, target, relation)
);

CREATE INDEX idx_edges_source ON kg_edges(source);
CREATE INDEX idx_edges_target ON kg_edges(target);
CREATE INDEX idx_edges_relation ON kg_edges(relation);
```

This is trivially queryable from Node.js with `better-sqlite3`, requires zero external processes, and scales to millions of edges on a single EC2 instance.

**Libraries to consider:**
- **LangChain GraphMemory**: Built-in graph memory integration.
- **LlamaIndex KnowledgeGraphIndex**: For RAG over graph structures.
- **Custom**: For OpenClaw, a custom lightweight implementation is preferable — less dependency bloat.

### 1.4 The Combined Architecture: Vector + Graph + File

```
┌─────────────────────────────────────────────────────────────────┐
│              OPENCLAW LONG-TERM MEMORY LAYERS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐    ┌──────────────┐    ┌────────────────┐   │
│   │   EPISODIC   │    │   SEMANTIC   │    │  PROCEDURAL    │   │
│   │              │    │              │    │                │   │
│   │ memory/      │───▶│ LanceDB      │───▶│ skills/        │   │
│   │ YYYY-MM-DD   │    │ (vectors)    │    │ workflows/     │   │
│   │ (raw logs)   │    │              │    │ action_        │   │
│   │              │    │ kg_nodes     │    │ registry/      │   │
│   │              │    │ kg_edges     │    │ (learned       │   │
│   │              │    │ (SQLite)     │    │  procedures)   │   │
│   └──────────────┘    └──────────────┘    └────────────────┘   │
│         │                     │                     │           │
│         │   MEMORY.md ────────┘                     │           │
│         │   (human-curated                          │           │
│         │    semantic layer)                        │           │
│         └───────────────────────────────────────────┘           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Context Persistence: 1000s of Sessions Without Loss

The core challenge: LLMs have finite context windows (even qwen3.6-plus:free has a limited input token budget per call). OpenClaw cannot stuff 1000 sessions into every prompt.

### 2.1 The Tiered Context Strategy

Proven systems (MemGPT, AutoMem, CAMEL) use a **multi-tier retrieval architecture**:

```
┌──────────────────────────────────────────────────────────────┐
│              TIERED CONTEXT RETRIEVAL                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Tier 1: IMMEDIATE CONTEXT (~2-4K tokens)                   │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ • Last 5-10 messages (conversation window)             │  │
│  │ • Active task summary                                  │  │
│  │ • Relevant skill context (if a skill is active)        │  │
│  └────────────────────────────────────────────────────────┘  │
│                      ▲                                       │
│                      │ retrieved on-demand                    │
│  Tier 2: SHORT-TERM MEMORY (~10-20K tokens)                 │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ • Today's session log (memory/YYYY-MM-DD.md)           │  │
│  │ • Yesterday's session (if relevant)                    │  │
│  │ • Top-5 vector search results from LanceDB             │  │
│  │ • 3-hop KG neighbors of key entities                   │  │
│  └────────────────────────────────────────────────────────┘  │
│                      ▲                                       │
│                      │ distilled & cached                     │
│  Tier 3: LONG-TERM MEMORY (unbounded, external)             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ • Full LanceDB corpus (all episodic memory)            │  │
│  │ • Full knowledge graph                                 │  │
│  │ • MEMORY.md (human-curated core truths)                │  │
│  │ • Skill definitions, workflows                         │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

**How it works in practice:**

1. When Kaif sends a message, OpenClaw extracts key entities (names, dates, topics).
2. It queries LanceDB for the top-K most relevant episodic memories.
3. It queries the KG for relationships involving those entities.
4. It loads today's session log.
5. It assembles Tier 1 + Tier 2 context (staying within token budget).
6. Tier 3 remains external — queried only when needed for deeper research.

### 2.2 Context Compression

Not all messages are equally important. MemGPT uses a **memory manager** — a smaller LLM call that compresses conversation history into a summary.

For OpenClaw:

```typescript
interface ContextCompressor {
  /**
   * Compress raw messages into a structured summary.
   * Called at end of each session or when context overflows.
   */
  compress(
    messages: Message[],
    existingSummary?: string
  ): Promise<SessionSummary>;
}

interface SessionSummary {
  sessionId: string;
  date: string;
  keyTopics: string[];
  decisions: string[];
  actionItems: string[];
  entitiesMentioned: string[];
  summaryText: string;     // 200-500 word compressed narrative
  embedding: number[];     // vector for retrieval
}
```

**Compression trigger:** Every 50 messages in a session, or at session end (detected by 30+ minutes of inactivity).

### 2.3 The `context_window` Budget

OpenClaw should maintain a **context budget calculator**:

```typescript
const CONTEXT_BUDGET = {
  system_prompt: 800,       // AGENTS.md, SOUL.md, IDENTITY.md combined
  session_log: 2000,        // today's session so far
  short_term_retrieval: 4000, // vector search results + KG neighbors
  skill_context: 1500,      // active skill's SKILL.md
  conversation: 3000,       // last N messages
  reserved: 500,            // safety margin
  total_limit: 12800,       // adjust for model's actual limit
};
```

If total exceeds `total_limit`, drop from least important first: `short_term_retrieval` (reduce K), then `session_log` (use compressed summary), then `conversation` (truncate older messages).

---

## 3. Memory Distillation: Raw Data → Curated Intelligence

Raw logs are noise. Intelligence is distilled signal.

### 3.1 The Distillation Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  RAW LOGS   │────▶│  EXTRACTOR   │────▶│  CURATED ENTRY  │
│ (episodic)  │     │  (LLM-based) │     │  (semantic)     │
└─────────────┘     └──────────────┘     └─────────────────┘
     │                       │                    │
     │                 What happened?             │
     │                 Who was involved?          │
     │                 What was decided?          │
     │                 What was learned?          │
     │                                            │
     └────────────────────────────────────────────┘
```

**Extractor prompt (conceptual):**

```
You are OpenClaw's memory distiller. Given this raw session log,
extract structured intelligence for long-term storage.

INPUT: {{full_session_log}}

OUTPUT FORMAT (JSON):
{
  "key_entities": ["entity1", "entity2"],
  "decisions_made": ["decision1 with context", "decision2"],
  "lessons_learned": ["lesson1", "lesson2"],
  "facts_discovered": ["fact1", "fact2"],
  "action_items_created": ["action1 assigned to X", "action2"],
  "patterns_observed": ["pattern1"],
  "summary": "3-5 sentence distilled summary of what mattered"
}

RULES:
- Only extract what is genuinely new or important
- Do NOT extract greetings, casual chatter, or already-known facts
- For decisions: include the reasoning or context
- For facts: state them as assertions, not questions
- For patterns: describe trends, not one-offs
```

**Where distilled memory goes:**
1. Insert into **LanceDB** as a new episodic document (with metadata tags).
2. Upsert into **MEMORY.md** if it meets a "high-importance" threshold (decisions, lessons, new entities).
3. Create or update **KG nodes/edges** for entities and relationships.

### 3.2 Automated Distillation Triggers

| Trigger | Frequency | What Happens |
|---------|-----------|--------------|
| Session end | Per session | Distill the session into summary + structured entries |
| Daily cron | 02:00 IST | Review all `memory/YYYY-MM-DD.md` files from the past 7 days, distill any missed insights |
| Heartbeat | Every 4-8h | Run lightweight distillation on new messages since last heartbeat |
| Manual | On command `/distill` | Force distillation of a specific date range |

### 3.3 The MEMORY.md Auto-Updater

`MEMORY.md` is currently manually curated. It should be **semi-automated**:

```typescript
interface MemoryUpdateProposal {
  type: 'add' | 'update' | 'delete';
  section: string;
  content: string;
  confidence: number;    // 0-1, how certain the LLM is
  source: string;        // which session/date this came from
  requiresApproval: boolean; // true if confidence < 0.85
}

// Proposed workflow:
// 1. Distillation pipeline generates MemoryUpdateProposal[]
// 2. High-confidence proposals (>=0.85) are auto-applied
// 3. Low-confidence proposals are queued for Kaif's review
//    (shown in Telegram as approval cards)
// 4. Kaif approves/rejects → MEMORY.md is updated
```

---

## 4. Cross-Session Shared Memory

When OpenClaw spans multiple agents (Jarvis main session, subagents for research, content, analytics), they must share a **single knowledge base**.

### 4.1 The Shared Memory Bus

```
┌──────────────────────────────────────────────────────┐
│            SHARED MEMORY BUS ARCHITECTURE             │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐         │
│  │  Jarvis  │   │ Subagent │   │ Subagent │         │
│  │  (main)  │   │   #1     │   │   #2     │         │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘         │
│       │              │              │                 │
│       │   ┌──────────▼──────────────▼──────────┐     │
│       │   │       MEMORY BUS (LanceDB +        │     │
│       │   │       SQLite KG + MEMORY.md)       │     │
│       │   └──────────┬──────────────┬──────────┘     │
│       │              │              │                 │
│       ▼              ▼              ▼                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐         │
│  │ Read     │   │ Write    │   │ Subscribe │         │
│  │ context  │   │ distilled│   │ to events │         │
│  └──────────┘   │ memory   │   └──────────┘         │
│                 └──────────┘                         │
└──────────────────────────────────────────────────────┘
```

**Implementation:**

1. **LanceDB is the canonical store.** All agents read from and write to the same LanceDB tables (`episodic_memory`, `semantic_memory`).
2. **SQLite KG is shared.** All agents read and update the same `kg_nodes` and `kg_edges` tables.
3. **MEMORY.md is the golden source for high-level truths.** Subagents should NOT write to `MEMORY.md` directly. Instead, they emit `MemoryUpdateProposal` events to the Memory Bus. The main agent (Jarvis) reviews and applies them.

### 4.2 Memory Bus Events

```typescript
type MemoryBusEvent =
  | { type: 'EPISODIC_WRITE'; sessionId: string; content: string; entities: string[] }
  | { type: 'SEMANTIC_UPSERT'; facts: string[]; confidence: number; source: string }
  | { type: 'KG_NODE_CREATE'; node: KGNode }
  | { type: 'KG_EDGE_CREATE'; edge: KGEdge }
  | { type: 'MEMORY_UPDATE_PROPOSAL'; proposal: MemoryUpdateProposal }
  | { type: 'CONTEXT_QUERY'; entities: string[]; maxTokens: number };
```

**Subagent lifecycle integration:**

```
Subagent Spawned
       │
       ▼
┌──────────────────┐
│ Read shared      │ ◄─── Context injection via Memory Bus
│ context (entities│
│ relevant to task)│
└────────┬─────────┘
         │
         ▼
   [Subagent works]
         │
         ▼
┌──────────────────┐
│ Write results to │ ◄─── Distilled findings emitted as
│ Memory Bus       │     EPISODIC_WRITE + SEMANTIC_UPSERT
└──────────────────┘
         │
         ▼
  Subagent Terminates
       (results pushed
        to main agent)
```

### 4.3 Conflict Resolution

What if two subagents write conflicting facts?

**Rule:** The Memory Bus applies a **last-write-wins with source tracking** policy. Each `SEMANTIC_UPSERT` carries:
- `source`: which agent/session wrote it
- `timestamp`: when it was written
- `confidence`: 0-1 confidence score

When a conflict is detected (same entity, contradictory fact), the system:
1. Keeps the higher-confidence entry.
2. If confidence is tied, keeps the newer entry.
3. Logs the conflict in `memory/conflicts/YYYY-MM-DD.md` for later review.

---

## 5. Memory Decay and Prioritization

Forgetting is a feature, not a bug. An AGI system that remembers everything remembers nothing.

### 5.1 The Forgetting Curve

Human memory follows Ebbinghaus's forgetting curve: information decays exponentially unless reinforced.

```
Recall Probability
    1.0 ┤
        │ ╲
        │  ╲
    0.5 ┤   ╲
        │    ╲
        │     ╲
    0.1 ┤      ╲
        │       ╲
        │        ╲
    0.0 └─────────┴───
        0   1   7   30   Days
```

### 5.2 Weighted Memory Scoring

Every memory item in LanceDB and the KG should have a **relevance score**:

```typescript
interface MemoryScore {
  recency: number;       // 0-1, decays over time (1.0 = just created)
  importance: number;    // 0-1, assigned at creation (decisions = 0.9, chatter = 0.1)
  frequency: number;     // how often this memory has been retrieved
  reinforcement: number; // how many times this fact has been re-confirmed
  decayRate: number;     // how fast this memory decays (0.01-0.1 per day)
}

function computeRelevance(score: MemoryScore, daysSinceCreation: number): number {
  const recencyDecay = Math.exp(-score.decayRate * daysSinceCreation);
  const usageBoost = Math.log(1 + score.frequency) * 0.1;
  const reinforcementBoost = Math.min(score.reinforcement * 0.05, 0.3);

  return score.importance * recencyDecay + usageBoost + reinforcementBoost;
}
```

### 5.3 Memory Tiers and Archival

```
┌──────────────────────────────────────────────────────┐
│              MEMORY TIER SYSTEM                        │
├──────────────────────────────────────────────────────┤
│                                                      │
│  TIER 1: HOT MEMORY (relevance > 0.7)               │
│  • Always loaded into LanceDB active index           │
│  • Included in default context retrieval             │
│  • MEMORY.md entries                                 │
│                                                      │
│  TIER 2: WARM MEMORY (0.3 < relevance <= 0.7)       │
│  • Stored in LanceDB but not in active index         │
│  • Retrieved only on specific entity/match queries   │
│  • Archived after 90 days of inactivity              │
│                                                      │
│  TIER 3: COLD MEMORY (relevance <= 0.3)             │
│  • Archived to compressed flat files                │
│  • Not searched in normal retrieval                  │
│  • Still queryable via explicit deep-search command  │
│  • Purged after 365 days unless manually preserved   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Automated decay job (daily cron):**

```bash
# Runs at 03:00 IST daily
0 3 * * * /usr/bin/node /home/ubuntu/.openclaw/workspace/scripts/memory-decay.js
```

The `memory-decay.js` script:
1. Reads all LanceDB entries and KG edges.
2. Recalculates relevance scores.
3. Downgrades entries that fall below tier thresholds.
4. Archives cold entries to `memory/archived/YYYY/`.
5. Purges entries older than 365 days with relevance < 0.1.
6. Logs summary to `memory/decay-YYYY-MM-DD.log`.

### 5.4 What to Forget vs. Preserve

| Preserve (High Importance) | Forget / Archive (Low Importance) |
|---------------------------|-----------------------------------|
| Business decisions and reasoning | Casual greetings, small talk |
| Buyer/supplier payment histories | Weather discussions (unless relevant) |
| Zari price trends and supplier contacts | Temporary task statuses (completed > 7 days) |
| Kaif's stated preferences | One-off chat jokes |
| Lessons from failed orders | Redundant confirmations |
| Recurring patterns (seasonal trends) | Duplicate or near-duplicate messages |

---

## 6. Self-Updating Knowledge

A static knowledge base is a dead knowledge base. The system must detect when facts change and update accordingly.

### 6.1 Contradiction Detection

When a new fact contradicts an existing fact, flag it:

```typescript
interface Contradiction {
  existingFact: string;
  newFact: string;
  existingSource: string;
  newSource: string;
  confidence: number;
  detectedAt: Date;
  status: 'pending_review' | 'resolved_new_wins' | 'resolved_old_wins' | 'merged';
}

// Example:
// Existing: "Supplier X charges ₹500/kg for Zari thread" (from 2025-12-01)
// New: "Supplier X now charges ₹550/kg for Zari thread" (from 2026-04-01)
// → Flag as contradiction, update with new fact, preserve old fact in history
```

### 6.2 Temporal Knowledge Graph

Standard KGs are atemporal. For self-updating knowledge, edges need **validity windows**:

```sql
CREATE TABLE kg_edges_temporal (
  source TEXT,
  target TEXT,
  relation TEXT,
  weight REAL,
  valid_from TIMESTAMP,
  valid_until TIMESTAMP,   -- NULL if still valid
  superseded_by TEXT,      -- reference to the edge that replaced this one
  PRIMARY KEY (source, target, relation, valid_from)
);
```

When a fact is updated:
1. The old edge gets `valid_until = NOW()` and `superseded_by = new_edge_id`.
2. The new edge gets `valid_from = NOW()` and `valid_until = NULL`.
3. Queries default to `WHERE valid_until IS NULL` (current state).
4. Historical queries can reconstruct past states.

### 6.3 Automated Fact Validation

Scheduled jobs that cross-check stored facts against external sources:

| Fact Type | Validation Source | Frequency |
|-----------|------------------|-----------|
| Zari prices | Web search / supplier APIs | Daily |
| Festival dates | Calendar API | Weekly |
| Supplier contact info | Email/phone verification | Monthly |
| Buyer payment patterns | Payment records analysis | Weekly |

When a validation check finds a discrepancy, it emits a `MEMORY_UPDATE_PROPOSAL` for review.

---

## 7. External Memory Augmentation

Even with vector databases, token limits are real. External augmentation offloads data from the LLM's context window.

### 7.1 The External Memory Pattern (from MemGPT)

MemGPT pioneered the concept of **paging memory in and out** of context. OpenClaw can implement this as:

```typescript
interface ExternalMemoryStore {
  /**
   * Read a chunk of memory by ID or query.
   * Returns text that can be injected into context.
   */
  read(query: string | MemoryId, maxTokens: number): Promise<string>;

  /**
   * Write memory to external store.
   * Does NOT add to LLM context — caller decides when to retrieve.
   */
  write(content: string, metadata: MemoryMetadata): Promise<MemoryId>;

  /**
   * Search for relevant memories. Returns IDs and snippets, not full content.
   */
  search(query: string, topK: number): Promise<MemorySnippet[]>;

  /**
   * Delete or archive memory.
   */
  archive(id: MemoryId): Promise<void>;
}
```

### 7.2 File-Based External Memory (Low-Cost Option)

For OpenClaw's zero-cost philosophy, the simplest external memory is **structured files**:

```
memory/
├── episodic/
│   ├── 2025-01/
│   │   ├── 2025-01-15.jsonl   # One JSON per line
│   │   └── 2025-01-16.jsonl
│   ├── 2025-02/
│   └── ...
├── semantic/
│   ├── buyers.json            # Structured buyer profiles
│   ├── suppliers.json         # Structured supplier profiles
│   ├── materials.json         # Zari thread types, prices
│   └── projects.json          # Ongoing/completed orders
├── procedural/
│   └── workflows/             # Skill definitions
├── archived/
│   └── 2025/                  # Compressed old data
└── MEMORY.md                  # Human-curated summary
```

**JSONL format for episodic memory:**

```jsonl
{"id":"ep_20260406_001","timestamp":"2026-04-06T17:20:00Z","type":"message","role":"user","content":"Check if buyer X paid last invoice","entities":["buyer_x"],"embedding_id":"emb_abc123"}
{"id":"ep_20260406_002","timestamp":"2026-04-06T17:21:00Z","type":"message","role":"assistant","content":"Buyer X's last invoice (INV-2026-045) was paid on 2026-03-28. Next payment due 2026-04-28.","entities":["buyer_x","INV-2026-045"],"embedding_id":"emb_def456"}
```

### 7.3 API-Based Augmentation

For real-time data, external APIs extend memory without storing it:

| Data Type | API | Cost |
|-----------|-----|------|
| Current zari/gold prices | IndiaMART API, commodity APIs | Free tier |
| Festival calendar | Google Calendar API, DharmaCalendar API | Free |
| Weather (for delivery planning) | OpenWeatherMap | Free tier |
| Exchange rates | exchangerate-api.com | Free tier |

**Pattern:** When context requires real-time data, the agent calls the API, injects the result into context for *that turn only*, and optionally stores a summary in episodic memory.

---

## 8. Pattern Recognition Across Time

Memory without pattern detection is just storage. AGI requires **trend detection**, **anomaly detection**, and **predictive inference**.

### 8.1 Time-Series Pattern Detection

```typescript
interface PatternDetector {
  /**
   * Detect trends in numeric time-series data.
   */
  detectTrend(
    series: { timestamp: Date; value: number }[],
    window: '7d' | '30d' | '90d'
  ): TrendAnalysis;

  /**
   * Detect anomalies: values significantly different from expected.
   */
  detectAnomalies(
    series: { timestamp: Date; value: number }[],
    sensitivity: number  // 0-1, higher = more sensitive
  ): Anomaly[];

  /**
   * Detect recurring patterns in categorical events.
   */
  detectRecurringPatterns(
    events: { timestamp: Date; category: string; metadata: Record<string, string> }[],
    minOccurrences: number
  ): RecurringPattern[];
}

interface TrendAnalysis {
  direction: 'up' | 'down' | 'stable';
  slope: number;           // rate of change per day
  rSquared: number;        // confidence in the linear fit
  startValue: number;
  endValue: number;
  periodDays: number;
}

interface Anomaly {
  timestamp: Date;
  value: number;
  expectedValue: number;
  deviation: number;       // standard deviations from mean
  possibleExplanation: string; // LLM-generated hypothesis
}
```

### 8.2 Practical Use Cases for R Company

| Pattern | Data Source | Action |
|---------|-------------|--------|
| Zari price increasing | Supplier quotations over time | Alert Kaif: "Lock prices with Supplier X before Diwali spike" |
| Buyer paying later each month | Payment history timestamps | Flag: "Buyer X payment delay trending up — average 5 days late, was 2 days" |
| Order volume seasonal | Order dates | Auto-prep: "Diwali orders start 6 weeks early. Begin outreach on {{date}}" |
| Supplier quality declining | Defect reports/rework frequency | Alert: "Supplier Y defect rate increased 3x in last month" |
| Content engagement rising | YouTube/Reels analytics | Double down: "Last 3 Reels using Format A averaged 2x views" |

### 8.3 Implementation: The Pattern Engine

```javascript
// scripts/pattern-detect.js — runs daily via heartbeat or cron

const lance = require('lancedb');
const db = await lance.connect('/path/to/lancedb');
const episodicTable = await db.openTable('episodic_memory');

// Extract zari price mentions from last 90 days
const prices = await episodicTable
  .search('zari price')
  .where("metadata.type = 'fact' AND metadata.entity = 'zari'")
  .limit(100)
  .execute();

// Parse prices and detect trend
const timeSeries = prices.map(p => ({
  timestamp: new Date(p.timestamp),
  value: parseFloat(p.content.match(/₹(\d+)/)?.[1] || 0)
})).filter(p => p.value > 0);

const trend = detectTrend(timeSeries, '90d');
if (trend.direction === 'up' && trend.slope > 2) {
  await memoryBus.emit({
    type: 'ALERT',
    message: `Zari prices trending up: ₹${trend.startValue} → ₹${trend.endValue} over ${trend.periodDays} days`,
    confidence: trend.rSquared
  });
}
```

---

## 9. Human Memory vs. AI Memory: Lessons from Neuroscience

Cognitive science offers design principles for better AI memory systems.

### 9.1 Key Insights from Neuroscience

| Human Memory Principle | AI Implementation Lesson |
|------------------------|--------------------------|
| **Encoding specificity**: Memory is better retrieved in the same context it was encoded | Tag episodic memories with rich contextual metadata (channel, time, mood, active task) |
| **Spaced repetition**: Information reviewed at increasing intervals is retained longer | Re-surface important memories at 1d, 3d, 7d, 30d intervals to reinforce |
| **Chunking**: Working memory holds ~7±2 chunks, not raw items | Compress related facts into chunks (e.g., "Buyer X profile" instead of 50 separate facts) |
| **Cue-dependent retrieval**: Memory needs cues to be retrieved | Build multi-cue indices: entity, topic, date, sentiment, outcome |
| **Consolidation during sleep**: Memories are reorganized and strengthened offline | Run nightly distillation/consolidation jobs during low-activity hours |
| **Emotional salience**: Emotionally charged events are remembered better | Weight memories with sentiment scores; high-sentiment events get higher importance |
| **Interference**: Similar memories compete and cause forgetting | Deduplicate near-similar memories; merge overlapping entries |
| **Reconstructive memory**: Recall is reconstruction, not playback | Accept that retrieved context may be imperfect; provide source citations |

### 9.2 The Sleep Cycle Analogy

Human brains consolidate memory during sleep. OpenClaw should emulate this:

```
┌──────────────────────────────────────────────────┐
│         OPENCLAW "SLEEP" CYCLE (02:00-04:00 IST)  │
├──────────────────────────────────────────────────┤
│                                                  │
│  Phase 1: REPLAY (02:00-02:30)                  │
│  • Review all episodic memory from today         │
│  • Re-encode salient events with richer metadata  │
│                                                  │
│  Phase 2: CONSOLIDATE (02:30-03:00)              │
│  • Run distillation pipeline on raw logs         │
│  • Update semantic memory (LanceDB + KG)         │
│  • Update MEMORY.md with high-confidence entries  │
│                                                  │
│  Phase 3: PRUNE (03:00-03:30)                    │
│  • Apply decay scores to all memories             │
│  • Downgrade/ archive low-relevance entries       │
│  • Detect and resolve contradictions              │
│                                                  │
│  Phase 4: PLAN (03:30-04:00)                     │
│  • Review action items and deadlines             │
│  • Generate next-day priority list               │
│  • Schedule proactive checks (heartbeat)          │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 10. Concrete Implementation Plan for OpenClaw

### 10.1 Phase 1: Foundation (Week 1-2)

**Goal:** Add LanceDB-based episodic memory and basic vector search.

```bash
# Step 1: Install LanceDB
cd /home/ubuntu/.openclaw/workspace
npm install lancedb
npm install @xenova/transformers  # for local embeddings

# Step 2: Initialize LanceDB tables
mkdir -p data/lancedb
```

```typescript
// scripts/init-lancedb.ts
import * as lancedb from 'lancedb';
import { pipeline } from '@xenova/transformers';

const db = await lancedb.connect('data/lancedb');

// Create episodic memory table
const episodicSchema = {
  id: 'string',
  timestamp: 'string',
  content: 'string',
  role: 'string',       // 'user' | 'assistant' | 'system'
  sessionId: 'string',
  channel: 'string',    // 'telegram' | 'browser'
  entities: 'string',   // JSON array of entities
  importance: 'float32', // 0-1
  embedding: 'vector',   // 384-dim (all-MiniLM-L6-v2)
};

await db.createTable('episodic_memory', [], { schema: episodicSchema });

// Create semantic memory table
const semanticSchema = {
  id: 'string',
  fact: 'string',
  sourceSessionId: 'string',
  confidence: 'float32',
  createdAt: 'string',
  lastVerifiedAt: 'string',
  embedding: 'vector',
};

await db.createTable('semantic_memory', [], { schema: semanticSchema });

console.log('LanceDB initialized.');
```

```typescript
// scripts/embed.ts — generate embeddings locally
import { pipeline } from '@xenova/transformers';

const embedder = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');

export async function embed(text: string): Promise<number[]> {
  const output = await embedder(text, { pooling: 'mean', normalize: true });
  return Array.from(output.data);
}
```

**Config changes in OpenClaw gateway:**

```yaml
# ~/.openclaw/config.yaml — add memory section
memory:
  episodic:
    enabled: true
    store: lancedb
    path: /home/ubuntu/.openclaw/workspace/data/lancedb
    retention_days: 365
  semantic:
    enabled: true
    store: lancedb
    auto_distill: true
    distillation_confidence_threshold: 0.85
  knowledge_graph:
    enabled: false  # Phase 2
  decay:
    enabled: true
    schedule: "0 3 * * *"  # daily at 03:00 IST
```

### 10.2 Phase 2: Knowledge Graph (Week 3-4)

**Goal:** Add SQLite-based KG with entity extraction.

```bash
npm install better-sqlite3
npm install natural   # for basic NLP / entity extraction
```

```typescript
// scripts/init-kg.ts
import Database from 'better-sqlite3';

const kg = new Database('data/knowledge_graph.db');

kg.exec(`
  CREATE TABLE IF NOT EXISTS kg_nodes (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    properties TEXT
  );
  CREATE TABLE IF NOT EXISTS kg_edges (
    source TEXT REFERENCES kg_nodes(id),
    target TEXT REFERENCES kg_nodes(id),
    relation TEXT NOT NULL,
    weight REAL DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (source, target, relation)
  );
  CREATE INDEX IF NOT EXISTS idx_edges_source ON kg_edges(source);
  CREATE INDEX IF NOT EXISTS idx_edges_target ON kg_edges(target);
`);

console.log('Knowledge Graph initialized.');
```

```typescript
// scripts/entity-extractor.ts — extract entities from text
import natural from 'natural';

export function extractEntities(text: string): string[] {
  // Simple: extract proper nouns and known entity patterns
  const tokens = natural.WordTokenizer().tokenize(text);
  const nouns = tokens.filter(t => /^[A-Z]/.test(t) && t.length > 2);
  // Deduplicate
  return [...new Set(nouns)];
}

// Better: use an NER model via Transformers.js
import { pipeline } from '@xenova/transformers';

const ner = await pipeline('token-classification', 'Xenova/bert-base-NER');

export async function extractEntitiesNER(text: string): Promise<string[]> {
  const result = await ner(text);
  const entities = result
    .filter((r: any) => r.entity.startsWith('B-'))
    .map((r: any) => r.word);
  return [...new Set(entities)];
}
```

### 10.3 Phase 3: Distillation Pipeline (Week 5-6)

**Goal:** Automated session distillation and MEMORY.md updates.

```typescript
// scripts/distill-session.ts
import { generate } from './llm-client'; // OpenClaw's LLM interface
import { embed } from './embed';
import * as lancedb from 'lancedb';

interface DistilledSession {
  summary: string;
  entities: string[];
  decisions: string[];
  facts: string[];
  importance: number;
}

export async function distillSession(sessionId: string): Promise<DistilledSession> {
  // 1. Load raw session log
  const sessionLog = await fs.readFile(`memory/${sessionId}.md`, 'utf-8');

  // 2. Call LLM to distill
  const prompt = `You are OpenClaw's memory distiller...
INPUT: ${sessionLog}...`;

  const response = await generate({
    model: 'openrouter/qwen/qwen3.6-plus:free',
    prompt: prompt,
    maxTokens: 1000
  });

  // 3. Parse JSON response
  const distilled: DistilledSession = JSON.parse(response);

  // 4. Generate embedding for the summary
  const vector = await embed(distilled.summary);

  // 5. Insert into LanceDB
  const db = await lancedb.connect('data/lancedb');
  const table = await db.openTable('episodic_memory');
  await table.insert([{
    id: `ep_${sessionId}`,
    timestamp: new Date().toISOString(),
    content: distilled.summary,
    role: 'system',
    sessionId: sessionId,
    channel: ' distilled',
    entities: JSON.stringify(distilled.entities),
    importance: distilled.importance,
    embedding: vector
  }]);

  // 6. If high importance, propose MEMORY.md update
  if (distilled.importance > 0.85) {
    await proposeMemoryUpdate(distilled);
  }

  return distilled;
}
```

### 10.4 Phase 4: Pattern Engine (Week 7-8)

**Goal:** Trend detection and anomaly alerts.

```typescript
// scripts/pattern-engine.ts
import * as lancedb from 'lancedb';
import simpleStat from 'simple-statistics';

export async function detectPriceTrends(): Promise<void> {
  const db = await lancedb.connect('data/lancedb');
  const table = await db.openTable('semantic_memory');

  const facts = await table
    .search('price')
    .where("fact LIKE '%₹%'")
    .limit(200)
    .execute();

  // Group by entity, detect trends
  // ... (time-series analysis as shown in Section 8.3)
}
```

### 10.5 File Structure (Final State)

```
/home/ubuntu/.openclaw/workspace/
├── AGENTS.md
├── SOUL.md
├── IDENTITY.md
├── USER.md
├── TOOLS.md
├── MEMORY.md                    # Human-curated semantic layer
├── memory/
│   ├── 2026-04-05.md            # Daily raw logs
│   ├── 2026-04-06.md
│   ├── episodic/                # Structured episodic memory (JSONL)
│   │   └── 2026-04/
│   ├── semantic/                # Structured semantic data
│   │   ├── buyers.json
│   │   ├── suppliers.json
│   │   ├── materials.json
│   │   └── projects.json
│   ├── archived/                # Compressed old data
│   │   └── 2025/
│   ├── conflicts/               # Contradiction logs
│   ├── decay-YYYY-MM-DD.log     # Daily decay job output
│   └── heartbeat-state.json
├── data/
│   ├── lancedb/                 # LanceDB vector database
│   │   ├── episodic_memory/
│   │   └── semantic_memory/
│   └── knowledge_graph.db       # SQLite KG
├── scripts/
│   ├── init-lancedb.ts
│   ├── init-kg.ts
│   ├── embed.ts
│   ├── entity-extractor.ts
│   ├── distill-session.ts
│   ├── memory-decay.js          # Daily cron job
│   ├── pattern-engine.ts
│   └── consolidate-nightly.ts  # "Sleep cycle" job
├── skills/                      # Procedural memory (existing)
├── agi-research/                # This report
│   └── 01-memory-and-continuity.md
└── HEARTBEAT.md
```

---

## OpenClaw AGI Memory Architecture — Implementation Checklist

### Phase 1: Foundation (Week 1-2)
- [ ] Install `lancedb` and `@xenova/transformers` via npm
- [ ] Create `data/lancedb/` directory
- [ ] Run `scripts/init-lancedb.ts` to create `episodic_memory` and `semantic_memory` tables
- [ ] Implement `scripts/embed.ts` using `Xenova/all-MiniLM-L6-v2`
- [ ] Modify OpenClaw's message pipeline to log every message to LanceDB (with embedding)
- [ ] Add `memory.episodic.enabled = true` config in `~/.openclaw/config.yaml`
- [ ] Test: Send a message, verify it appears in LanceDB with correct embedding
- [ ] Implement basic vector search: `/search <query>` command
- [ ] Document the LanceDB schema in `data/lancedb/SCHEMA.md`

### Phase 2: Knowledge Graph (Week 3-4)
- [ ] Install `better-sqlite3` and `natural`
- [ ] Run `scripts/init-kg.ts` to create `kg_nodes` and `kg_edges` tables
- [ ] Implement `scripts/entity-extractor.ts` with NER
- [ ] Hook entity extraction into the message pipeline: extract entities → create KG nodes
- [ ] Implement KG query: `/kg query <entity>` command (3-hop neighborhood)
- [ ] Implement edge creation from detected relationships (LLM-based)
- [ ] Test: Mention a buyer and supplier in the same message → verify KG edge created
- [ ] Document KG schema in `data/SCHEMA.md`

### Phase 3: Distillation Pipeline (Week 5-6)
- [ ] Implement `scripts/distill-session.ts`
- [ ] Add session-end detection (30 min inactivity → trigger distillation)
- [ ] Implement `proposeMemoryUpdate()` for MEMORY.md auto-updates
- [ ] Create Telegram approval flow for low-confidence memory updates
- [ ] Hook distillation into heartbeat: daily review of unprocessed logs
- [ ] Test: Complete a session → verify distilled summary in LanceDB
- [ ] Test: High-importance fact → verify MEMORY.md proposal generated

### Phase 4: Decay and Archival (Week 7)
- [ ] Implement `scripts/memory-decay.js` with relevance scoring
- [ ] Add daily cron entry: `0 3 * * * node scripts/memory-decay.js`
- [ ] Implement tiered storage: HOT → WARM → COLD transitions
- [ ] Implement archival to `memory/archived/YYYY/` with gzip compression
- [ ] Implement purge: delete entries > 365 days with relevance < 0.1
- [ ] Test: Run decay job manually, verify downgrades and archivals
- [ ] Document decay formula and thresholds

### Phase 5: Pattern Engine (Week 8)
- [ ] Implement `scripts/pattern-engine.ts` with trend detection
- [ ] Implement `detectPriceTrends()` for zari/supplier pricing
- [ ] Implement `detectPaymentPattern()` for buyer payment delays
- [ ] Implement `detectSeasonalPattern()` for order volume
- [ ] Hook pattern engine into heartbeat: run analysis 2x/week
- [ ] Implement alert emission: when trend threshold exceeded, notify Kaif via Telegram
- [ ] Test: Feed synthetic price data, verify trend detection

### Phase 6: Cross-Session Memory Bus (Week 9-10)
- [ ] Implement `MemoryBusEvent` type and event emitter
- [ ] Modify subagent spawn to read shared context from Memory Bus
- [ ] Modify subagent termination to emit results to Memory Bus
- [ ] Implement conflict resolution for contradictory facts
- [ ] Implement temporal KG edges (`kg_edges_temporal`)
- [ ] Test: Spawn two subagents, both write facts → verify conflict handling
- [ ] Document Memory Bus API in `docs/MEMORY-BUS.md`

### Phase 7: External Augmentation & APIs (Week 11)
- [ ] Implement `ExternalMemoryStore` interface
- [ ] Add zari price API integration (IndiaMART or web scraping)
- [ ] Add festival calendar API (Google Calendar or DharmaCalendar)
- [ ] Implement API data injection into context on demand
- [ ] Test: Query "What's the current zari price?" → API call → context injection → response

### Phase 8: Evaluation and Tuning (Week 12)
- [ ] Benchmark vector search latency (target: <500ms for top-5)
- [ ] Benchmark distillation cost (target: <₹1/session in API costs)
- [ ] Audit MEMORY.md quality: are auto-updates helpful?
- [ ] Tune decay parameters: is too much being forgotten? too little?
- [ ] Gather feedback from Kaif: what's useful, what's noise?
- [ ] Document final architecture in `docs/ARCHITECTURE.md`
- [ ] Write migration script for existing `memory/YYYY-MM-DD.md` → LanceDB

---

**End of Report.**

This architecture transforms OpenClaw from a session-bound chat agent into a persistent, learning, evolving intelligence system. The core insight: **memory is retrieval architecture**. Every component — LanceDB, knowledge graph, decay engine, pattern detector — exists to ensure the right information appears in the right context at the right time.

The implementation is phased, incremental, and fully compatible with OpenClaw's free-tier, EC2-hosted constraints. No vendor lock-in. No expensive cloud services. No black-box dependencies.

The result: Jarvis becomes not just a respondent, but a **continuously learning operational mind** for R Company.
