# Project Specification: Commercial Cloud Deployment (Monetized)

## 1. Objective
Transform the **Fretboard Compass Music Theory Suite** into a professional SaaS (Software as a Service) hosted on **Cloudflare Pages + Workers**, featuring usage-based throttling and newsletter/payment integration.

---

## 2. Commercial Tech Stack

### **Computing: Cloudflare Workers (TypeScript)**
- **Edge Runtime:** Migrate Python engine.py logic to a high-performance TypeScript theory.ts module.
- **Benefits:** Sub-millisecond execution, native integration with Cloudflare KV, and superior cold-start performance.

### **Database & Throttling: Cloudflare KV (Key-Value)**
- **Session Management:** Store encrypted session tokens for user authentication.
- **Usage Throttling:** Track generations per user email (e.g., user:limit:2024-04-14).
- **Gatekeeping:** Return HTMX "Upsell" partials when daily limits are reached.

### **Monetization Engine: Stripe + Newsletter Hooks**
- **Stripe Checkout:** Handle "Pro" subscriptions ($5/mo) for unlimited generations and advanced Jazz voicings.
- **Newsletter Webhooks:** Automatically grant "Subscriber" tier access (10 generations/day) when a user joins the mailing list (Substack/Beehiiv).

---

## 3. Deployment Architecture

### **Frontend: Cloudflare Pages**
- **Assets:** Pre-compiled Tailwind CSS, static HTML, and local HTMX library.
- **Performance:** Global CDN delivery with zero-latency asset serving.

### **Security: Custom Auth Worker**
- **Authentication:** Passwordless "Magic Link" (Email OTP) system.
- **Identity:** Direct integration with Cloudflare Access for Admin functions.

---

## 4. Porting Strategy

### **Phase 1: Theory Port**
- Translate SCALES, CHORD_TYPES, and PROGRESSION_PRESETS constants to TypeScript.
- Implement TriadBuilder class to replace get_chord_from_degree with identical mathematical logic.

### **Phase 2: UI Adaptation**
- Update index.html to point to /api/generate.
- Replace Flask Jinja2 templates with Worker-compatible template literals or pre-rendered partials.

### **Phase 3: Launch**
- Connect custom domain (e.g., sheets.guitarpractice.com).
- Enable Cloudflare WAF "Bot Fight Mode" to protect SVG assets.

## Documentation Standards
- **Emoji Usage:** NEVER use emojis in any output documentation (README.md, GEMINI.md, etc.) except for the README.md which has a sign of the horns (🤘) after the last line "...for guitarists ..."
- application code may use specific music symbols if they are standard and best practice, but not emojies for general header/comment text output, which should always appear as professional output.
- applicaiton code should prefer svg icons from free font awesome resources if needed (the star for favorites), and should avoid smart quotes, em dashes, and other use of emojies not already specified.
