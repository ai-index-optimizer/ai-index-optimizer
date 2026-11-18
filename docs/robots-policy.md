# Crawler policy the product generates

Named rules, not a wildcard. Account and admin paths are closed to every crawler; public marketing pages are open.

```
User-agent: *
Allow: /
Disallow: /Admin
Disallow: /Billing
Disallow: /Settings
Disallow: /Account
Disallow: /Profile
Disallow: /DataExport

User-agent: GPTBot
Allow: /
Disallow: /Admin
Disallow: /Billing
Disallow: /Settings
Disallow: /Account
Disallow: /Profile
Disallow: /DataExport
```

The same block is repeated for `OAI-SearchBot`, `ChatGPT-User`, `ClaudeBot`, `PerplexityBot` and `Google-Extended`.

Why named rules: a crawler that is only covered by `User-agent: *` inherits whatever exception another tool writes later. Naming each crawler keeps the decision explicit and auditable.

Note: `Google-Extended` controls Gemini and Vertex training use, not Googlebot indexing. Blocking it does not remove a page from Google Search.
