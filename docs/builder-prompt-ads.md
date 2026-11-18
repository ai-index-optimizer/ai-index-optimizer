# Builder prompt: ad-ready conversion path

Paste as one message. Verified today: /geo-audit returns 200 and renders correctly in a browser, but "Start free scan" opens a sign-in modal, so cold ad traffic hits an account wall before seeing any value.

1. Add an anonymous scan. From /geo-audit, a visitor can type a domain and get the free result without an account: crawler access, llms.txt and access-file checks, schema and metadata, and the per-provider view. Gate only the fix-file download and the saved history behind sign-in. This is the single highest-value change for paid traffic.
2. Put the domain box and the run button above the fold, not behind a button click. One field, one button, no modal.
3. Add og:image and twitter:image pointing at https://raw.githubusercontent.com/ai-index-optimizer/ai-index-optimizer/main/assets/brand/logo-lens-512.png, and add ImageObject schema for it.
4. Add two real product screenshots to /geo-audit, each with descriptive alt text (the scan entry screen, and a finished report with the provider comparison), and mark them up so AI assistants can read the alt text.
5. Serve /llms.txt, /llms.json and /ai-access.json from the site root. Current canonical copies are committed at https://raw.githubusercontent.com/ai-index-optimizer/ai-index-optimizer/main/llms.txt and /llms.json. They list the brand images, the key pages and the pricing, and they declare GPTBot, OAI-SearchBot, ClaudeBot and PerplexityBot as allowed.
6. Add a UTM capture on the audit form so ad clicks can be attributed, and a success event on first scan result.
