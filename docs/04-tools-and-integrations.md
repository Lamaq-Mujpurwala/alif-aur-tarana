# 04 · Tools & Integrations

The companions need to reach beyond the LLM's own memory. Your brief named four: **(i) conversation history, (ii) web search, (iii) YouTube transcription, (iv) Rekhta.** Each is exposed to the LLM as a **function-callable tool** (plain Python functions + JSON schemas — no LangChain; see [`05`](05-tech-stack.md)).

---

## 1. Rekhta — the hard truth and the workaround

**You asked specifically whether Rekhta has an API. It does not.** Rekhta.org is the largest online Urdu-poetry repository (30,000+ ghazals/nazms, 2,500+ poets) run by the **not-for-profit Rekhta Foundation** ([about/FAQ](https://www.rekhta.org/CMS/FAQ), [rekhta.org](https://www.rekhta.org/)), but there is **no public developer API** and **no documented integration program**. (They do have neat tools like **Taqti** for meter/*behr* scansion, but no API.)

### Options for Rekhta-grade content

| Option | What | Free? | Pros | Cons / risk |
|--------|------|-------|------|-------------|
| **A. Open community datasets** ✅ recommended | Pre-scraped, cleaned poetry corpora, e.g. [amir9ume/urdu_ghazals_rekhta](https://github.com/amir9ume/urdu_ghazals_rekhta) (Urdu + Hindi + Roman transliteration) | Free | No live scraping, already tri-script, instant, legal-cleaner | Snapshot (not live), must **credit Rekhta Foundation**, finite coverage |
| **B. Curated local corpus** ✅ recommended | We hand-pick + store the poets/ghazals you love (Faiz, Faraz, Jaun Elia, Gulzar, Ghalib…) in our DB | Free | Highest quality, full control, fast retrieval, offline | Manual effort to build/expand |
| **C. Scrape Rekhta live** ⚠️ avoid for MVP | Selenium/BeautifulSoup against rekhta.org ([example](https://saadsohail5104.medium.com/preserving-the-soul-of-urdu-poetry-scraping-rekhta-org-using-selenium-and-beautifulsoup-40403843362e)) | Free | Live, complete | Fragile, **ToS/ethical issues** scraping a non-profit, slow, breaks on redesign |
| **D. LLM's own knowledge + web verify** | Ask Gemini for the couplet, verify via web search | Free | Zero data infra | Hallucination risk on exact wording — **dangerous for beloved poetry** |

> **Recommendation:** Build a **local "poetry corpus" tool** = open datasets (A) + a growing curated set (B), stored in our DB with tri-script + poet metadata, **always crediting Rekhta Foundation** in the UI. Expose it as `rekhta.lookup(query, poet?, theme?)`. Treat live scraping (C) as a last resort and, if ever used, do it politely (rate-limited, cached) and revisit licensing. Never rely on D alone for exact text.
>
> **Relationship note:** Since Rekhta is a mission-aligned non-profit, the *right* long-term move is to **email Rekhta Foundation** about a partnership/data-access for an educational, non-commercial Urdu-learning tool. Worth doing early — best case, official blessing; worst case, a polite no and we proceed with A+B.

### The tool contract
```
rekhta.lookup(query: str, poet: str | None, theme: str | None, limit: int = 3)
  -> list[{ couplet_urdu, couplet_devanagari, couplet_roman,
            poet, ghazal_title, meaning_hint?, source_attribution }]
```

---

## 2. YouTube — songs, interviews, the living archive

So much Urdu lives on YouTube: film songs, mushairas, poet interviews, Rekhta's own channel. The companions need to pull a video's words.

| Option | Free? | Needs key? | Reliability | Notes |
|--------|-------|------------|-------------|-------|
| **`youtube-transcript-api`** (Python) ✅ primary | Free | No | ⚠️ uses undocumented internals; can break; rate-limited ~100–500 req/hr | v1.2.4 (Jan 2026), Py 3.8–3.14, pulls existing captions ([repo](https://github.com/jdepoix/youtube-transcript-api), [guide](https://www.notelm.ai/blog/youtube-transcript-api)) |
| **Whisper fallback** (local/Groq) ✅ | Free | No | High | For videos with **no captions**: `yt-dlp` audio → faster-whisper/Groq → transcript |
| **Supadata** | Free 100 req/mo | Yes | High (AI fallback) | Managed; "only YT transcript API with AI fallback" ([supadata](https://supadata.ai/youtube-transcript-api)) |
| **Firecrawl** | Free tier | Yes | High | Transcript *or* raw MP3; MCP-capable ([firecrawl](https://www.firecrawl.dev/blog/best-youtube-transcript-extractors)) |
| **YouTube Data API** (official) | Free quota | Yes | High (for search/metadata) | Use for **search**, not transcripts (captions endpoint is restricted) |

> **Recommendation:** `youtube-transcript-api` first; if it returns nothing (no captions) or errors, fall back to **`yt-dlp` + local/Groq Whisper**. Add **Supadata** (100/mo free) as a managed safety net. Use the official **YouTube Data API** only for *searching* videos ("find a Jaun Elia interview"). Cache transcripts by video ID (they don't change).

### The tool contract
```
youtube.search(query)        -> list[{video_id, title, channel, duration}]
youtube.transcript(video_id) -> { lang, segments:[{start, dur, text}], full_text }
```

---

## 3. Web search — reaching beyond the model

For poet biographies, song trivia, "who wrote this", current facts.

| Option | Free tier | LLM-optimised? | Notes |
|--------|-----------|----------------|-------|
| **Tavily** ✅ recommended | **1,000 searches/mo free** | ✅ ranked snippets + citations, built for agents | Easiest drop-in for agent context ([brave roundup](https://brave.com/learn/best-search-api-2026/), [agentic search benchmark](https://aimultiple.com/agentic-search)) |
| **Brave Search API** | ❌ no free tier (but **$5 credit/mo**) | structured SERP | Best agent score & latency in benchmarks, but raw results need formatting; pay-as-you-go |
| **Exa / Parallel** | small free | ✅ semantic | Good alternatives; Exa is neural-search-first |
| **DuckDuckGo (ddgs lib)** | free, unofficial | ❌ | Zero-cost stopgap, less reliable |
| **Google Programmable Search (CSE)** | 100 queries/day free | ❌ | Official-ish, low free quota |

> **Recommendation:** **Tavily** — 1,000 free searches/month is plenty for MVP, and it returns LLM-ready, cited snippets so the companion can say "Rekhta ke mutabik…" with a source. Keep **DuckDuckGo (`ddgs`)** wired as a free fallback if Tavily quota runs out.

### The tool contract
```
web.search(query, max_results=5) -> list[{title, url, snippet, score}]
```

---

## 4. Conversation memory — "it remembers us"

This is requirement (c) and a huge part of *why it feels like a friend*. Two layers:

- **Short-term (session):** the running transcript in context — handled by the agent loop, trimmed to a token budget.
- **Long-term (across sessions):** who you are, words you've learned, poets you love, your Urdu-density level, inside jokes. This is what makes Alif say "yaad hai 'firaaq' seekha tha?".

| Option | Free / self-host | Model | Best for | Notes |
|--------|------------------|-------|----------|-------|
| **mem0** ✅ recommended | ✅ open-source, self-host (48k+ stars) | Passive extraction + semantic search; Python & JS SDK | Personalization, chat/assistant memory | "Memory layer, not a runtime" — drop into our own agent ([mem0 vs Letta](https://vectorize.io/articles/mem0-vs-letta)) |
| **Plain SQLite/Postgres + pgvector** ✅ | ✅ | You define schema + embeddings | Maximum control, minimal deps | The truly barebones route; ~no new framework |
| **Letta (MemGPT)** | ✅ self-host | Tiered self-editing memory, full runtime | Long-horizon agents | Heavier — it wants to *be* the agent runtime; more than we need |
| **Zep** | partial | Temporal knowledge graph | Highest recall in benchmarks | More infra; revisit at scale |

> **Recommendation:** **mem0** over a Postgres+pgvector store. It gives "remember the user" cheaply, has Python+JS SDKs (matches FastAPI + Next.js), and stays out of the way of our own Pipecat agent loop — unlike Letta which would want to own orchestration. If we want zero new dependencies, **Postgres + pgvector with a tiny memory module** is a perfectly good barebones alternative.

### What we deliberately store (the schema sketch)
```
user_profile:   name, languages, urdu_density_dial, preferred_companion, goals
learned_vocab:  word_urdu, gloss, first_seen, last_surfaced, times_used, example_line
loved_content:  poets[], ghazals[], songs[], themes[]
session_recaps: date, summary, new_words[], highlight_line
relationship:   inside_jokes[], tone_notes  (e.g. "user enjoys sarcasm")
```

### The tool contract
```
memory.recall(query, kinds=[...]) -> relevant memories
memory.write(kind, payload)       -> persists (also auto-extracted post-session)
```

---

## 5. How the tools combine — a worked example

> You: *"Alif, woh Gulzar wala gaana… 'mera kuchh saamaan'… samjhao."*
> 1. `memory.recall("Gulzar, songs user likes")` → confirms you love Gulzar.
> 2. `youtube.search("Mera Kuch Samaan Gulzar")` → finds the track → `youtube.transcript(id)` → lyrics.
> 3. LLM (Gemini Flash) translates + picks 2 teaching words, in Alif's voice, tri-script.
> 4. `web.search("Mera Kuch Samaan Gulzar Ijaazat meaning")` → a fact to enrich ("RD Burman set this *free verse* to music — unheard of").
> 5. `memory.write(learned_vocab, "saamaan→belongings/in this poem, emotional baggage")`.
> 6. TTS (ElevenLabs, with `[softly]`) speaks it; audio cached.

Six tools, one fluid, in-character answer that *teaches* and *remembers*. That's the product.

---

## 6. Tool summary

| Tool | MVP choice | Free | Fallback |
|------|-----------|------|----------|
| Poetry (Rekhta) | Local corpus (open datasets + curated) | ✅ | (email Rekhta for partnership) |
| YouTube | `youtube-transcript-api` | ✅ | yt-dlp + Whisper; Supadata |
| Web search | Tavily (1k/mo) | ✅ | DuckDuckGo `ddgs` |
| Memory | mem0 (self-host) | ✅ | Postgres + pgvector |

Next: how it's all built → [`05-tech-stack.md`](05-tech-stack.md).

---

### Sources for this document
- Rekhta: [rekhta.org](https://www.rekhta.org/) · [FAQ](https://www.rekhta.org/CMS/FAQ) · [open ghazal dataset](https://github.com/amir9ume/urdu_ghazals_rekhta) · [scraping example/ethics](https://saadsohail5104.medium.com/preserving-the-soul-of-urdu-poetry-scraping-rekhta-org-using-selenium-and-beautifulsoup-40403843362e)
- YouTube: [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) · [free options guide](https://www.notelm.ai/blog/youtube-transcript-api) · [Supadata](https://supadata.ai/youtube-transcript-api) · [Firecrawl extractors](https://www.firecrawl.dev/blog/best-youtube-transcript-extractors)
- Web search: [Brave best search APIs 2026](https://brave.com/learn/best-search-api-2026/) · [agentic search benchmark](https://aimultiple.com/agentic-search) · [Tavily alternatives](https://websearchapi.ai/blog/tavily-alternatives)
- Memory: [mem0 vs Letta](https://vectorize.io/articles/mem0-vs-letta) · [agent memory frameworks 2026](https://atlan.com/know/best-ai-agent-memory-frameworks-2026/)
