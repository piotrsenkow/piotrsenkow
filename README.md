# Piotr Senkow

Senior full-stack engineer based in Chicago. I build production systems end-to-end — currently focused on **Realytica**, a self-hosted real-estate investment-analytics platform for Chicagoland investors.

Most of my professional work isn't open-source. This profile mainly hosts older side-project source; this README is where I describe what I build and the architectural calls I make along the way.

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

Realytica's source isn't public; the platform serves real users and the codebase stays private. Happy to walk through architecture, decisions, and tradeoffs in interview conversations.

---

## AI / Local Inference Homelab

A multi-node local-inference stack on my LAN — used as my daily dev assistant and for experimentation. Mix of NVIDIA GPUs and AMD Ryzen AI hardware. All endpoints OpenAI-compatible HTTP. Day-to-day usage via terminal coding agents (OpenCode, Claude Code) and direct Python SDK.

---

## Reach out

- **Realytica:** [realytica.com](https://www.realytica.com) — the live product
- **Real-estate work:** [piotrsenkow.com](https://www.piotrsenkow.com) — I'm also a licensed Illinois broker; the "engineer who reads buildings like code" angle is real
- **LinkedIn:** [piotr-senkow](https://www.linkedin.com/in/piotr-senkow/)
- **Email:** piotrsenkow@gmail.com
