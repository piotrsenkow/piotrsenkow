# Piotr Senkow

Senior full-stack engineer based in Chicago. I build production systems end-to-end — currently focused on **Realytica**, a self-hosted real-estate investment-analytics platform for Chicagoland investors.

Most of my professional work isn't open-source — Realytica included — but I've carved a couple of production-hardened pieces of its stack out into standalone, general-purpose tools ([below](#open-source)). This README is where I describe what I build and the architectural calls I make along the way.

---

## Featured: Realytica

**[realytica.com](https://www.realytica.com)** — solo-built, self-hosted, in active use by agents and buyers.

A real-estate analytics platform that ingests every MLS-Grid listing in the MRED feed (Chicagoland + adjacent IA/WI/IN counties), fuses it with 12 Cook County public datasets (parcels, assessments, sales, etc.), and serves search + comps + investor underwriting on top.

### Scale (June 2026)

- **6.66M** total property records on PostgreSQL 17 + PostGIS
- **2.96M** lifetime IDX records, **21K** currently active across all counties
- **4.22M** photos with BlurHash placeholders, **~2 TB** in self-hosted object storage
- **12** Cook County public datasets fused with the MLS feed
- Fully self-hosted, behind Cloudflare with zero open ingress ports

### Architecture (at a glance)

Polyglot backend — Go for the API and supporting services, C++23 for the in-memory spatial index. TypeScript / Next.js 16 / React 19 / Mapbox GL on the frontend.

The spatial layer is a custom in-memory index built on [Google S2](http://s2geometry.io/) and exposed over gRPC. It serves bounding-box, polygon, radius, and k-nearest queries. S2's hierarchical cell decomposition gives uniform cell area, good clustering of nearby geometry, and battle-tested containment / nearest-neighbor primitives — fundamentally different ergonomics from running the same queries through PostGIS, especially for k-NN comps lookup on a working set of a couple hundred thousand listings.

### Deal Mode

Investor underwriting workspace: persistence, sensitivity analysis, side-by-side deal comparison, PDF export. Backed by k-NN spatial queries for live comps lookup.

### Source

Realytica's source isn't public; the platform serves real users and the codebase stays private. Two general-purpose pieces of its ingestion + query layer *are* public, though — see [Open Source](#open-source). Happy to walk through architecture, decisions, and tradeoffs in interview conversations.

---

## Open Source

Two production-hardened pieces of the Realytica stack, rebuilt clean-room as general-purpose tools anyone with an MLS Grid license can run:

```
MLS Grid API ──▶ mlsgrid-sync ──▶ PostgreSQL ──▶ mlsgrid-mcp ──▶ your AI agent
                 (replication)     (your data)    (query tools)
```

- **[mlsgrid-sync](https://github.com/piotrsenkow/mlsgrid-sync)** — a single Go binary that replicates MLS Grid (RESO Web API / OData) feeds into PostgreSQL: resumable backfill, cursor-based incremental sync, reconcile sweeps, media download to S3-compatible storage, and configurable field scopes — all inside the feed's rate limits. The database schema is a versioned, documented contract.
- **[mlsgrid-mcp](https://github.com/piotrsenkow/mlsgrid-mcp)** — a read-only [Model Context Protocol](https://modelcontextprotocol.io) server that lets AI agents query that database: search listings, pull comps, price history, market stats, open houses. Pins the sync project's schema contract so the two release independently.

Both are Apache-2.0 and ship no MLS data or credentials — you bring your own licensed feed.

---

## AI / Local Inference Homelab

A multi-node local-inference stack on my LAN — used as my daily dev assistant and for experimentation. Mix of NVIDIA GPUs and AMD Ryzen AI hardware. All endpoints OpenAI-compatible HTTP. Day-to-day usage via terminal coding agents (OpenCode, Claude Code) and direct Python SDK.

---

## Reach out

- **Realytica:** [realytica.com](https://www.realytica.com) — the live product
- **Real-estate work:** [piotrsenkow.com](https://www.piotrsenkow.com) — I'm also a licensed Illinois broker; the "engineer who reads buildings like code" angle is real
- **LinkedIn:** [piotr-senkow](https://www.linkedin.com/in/piotr-senkow/)
- **Email:** piotrsenkow@gmail.com
