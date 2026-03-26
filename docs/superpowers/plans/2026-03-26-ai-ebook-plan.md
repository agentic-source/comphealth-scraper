# AI for the Rest of Us — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Write and prepare for launch a 12-chapter beginner e-book on AI/automation, with all marketing assets and platform setup guides.

**Architecture:** The manuscript is written as structured Markdown files (one per chapter + front/back matter), then assembled into a single manuscript. Marketing assets and guides are separate Markdown files. All content lives in a `book/` directory tree.

**Tech Stack:** Markdown for all content. User converts to DOCX via Pandoc, to PDF via Pandoc or print-to-PDF, and to EPUB for Kindle via KDP's built-in DOCX converter or Calibre (free tool).

**Spec:** `docs/superpowers/specs/2026-03-26-ai-ebook-design.md`

---

## File Structure

```
book/
├── manuscript/
│   ├── 00-front-matter.md          # Title page, copyright, disclaimer, TOC placeholder
│   ├── 01-what-even-is-ai.md
│   ├── 02-the-big-names.md
│   ├── 03-how-to-talk-to-ai.md
│   ├── 04-good-at-and-terrible-at.md
│   ├── 05-automation-vs-ai.md
│   ├── 06-free-tools-today.md
│   ├── 07-will-ai-take-my-job.md
│   ├── 08-ai-at-home.md
│   ├── 09-ai-at-work.md
│   ├── 10-agentic-ai.md
│   ├── 11-privacy-and-safety.md
│   ├── 12-thirty-day-starter-plan.md
│   └── 13-back-matter.md           # About the Author, Resources & Links, What's Next
├── marketing/
│   ├── amazon-description.md        # KDP listing: description, keywords, categories
│   ├── gumroad-sales-page.md        # Full Gumroad sales page copy
│   ├── email-sequence.md            # 3-email post-purchase drip
│   ├── launch-announcement.md       # Social media / network post
│   ├── review-request-template.md   # Ask for reviews message
│   ├── author-bio.md                # Short + long versions
│   └── canva-cover-brief.md         # Cover design direction for Canva
├── guides/
│   ├── manuscript-conversion.md     # How to convert Markdown → DOCX → EPUB/PDF
│   ├── kdp-setup-guide.md           # Step-by-step KDP account + upload
│   ├── gumroad-setup-guide.md       # Step-by-step Gumroad setup
│   └── mailchimp-drip-guide.md      # Setting up the 3-email automation
└── assembled-manuscript.md          # Final combined file (all chapters in order)
```

---

## Phase 1: Content Creation

### Task 1: Front Matter

**Files:**
- Create: `book/manuscript/00-front-matter.md`

- [ ] **Step 1: Write title page**
  Title, subtitle, author name placeholder (`[Your Name]`).

- [ ] **Step 2: Write copyright page**
  Year, author name placeholder, "All rights reserved," standard e-book copyright language.

- [ ] **Step 3: Write legal disclaimer**
  Cover career advice (Ch. 7) and privacy/safety guidance (Ch. 11) — informational content, not professional advice. Keep it short and reader-friendly.

- [ ] **Step 4: Write table of contents**
  Hyperlinked Markdown headings for all 12 chapters plus back matter sections.

- [ ] **Step 5: Commit**
  ```bash
  git add book/manuscript/00-front-matter.md
  git commit -m "content: add front matter — title, copyright, disclaimer, TOC"
  ```

---

### Task 2: Chapter 1 — What Even Is AI?

**Files:**
- Create: `book/manuscript/01-what-even-is-ai.md`

- [ ] **Step 1: Write opening scenario**
  Relatable story: someone hearing "AI" everywhere and feeling lost. Set the tone for the whole book — warm, zero jargon.

- [ ] **Step 2: Write core content**
  Explain AI as pattern recognition, not sentient robots. Use everyday analogies (Netflix recommendations, phone autocomplete, spam filters). Cover: narrow AI vs. general AI, machine learning basics without the math, why it suddenly seems like AI is everywhere (what changed in 2022-2023).

- [ ] **Step 3: Write "Myth vs. Reality" sidebar**
  Myth: "AI thinks like a human brain." Reality: explain what it actually does.

- [ ] **Step 4: Write "Try This Now" exercise**
  Simple hands-on task the reader can do immediately (e.g., ask ChatGPT or Claude a question and observe what happens).

- [ ] **Step 5: Write key takeaway summary**
  3-4 bullet points. The "if you remember nothing else" version.

- [ ] **Step 6: Commit**
  ```bash
  git add book/manuscript/01-what-even-is-ai.md
  git commit -m "content: write Chapter 1 — What Even Is AI?"
  ```

---

### Task 3: Chapter 2 — The Big Names & What They Do

**Files:**
- Create: `book/manuscript/02-the-big-names.md`

- [ ] **Step 1: Write opening scenario**
  Someone overwhelmed by all the names — ChatGPT, Claude, Gemini, Copilot, Siri, Alexa — "aren't these all the same thing?"

- [ ] **Step 2: Write core content**
  Who makes what (OpenAI, Anthropic, Google, Microsoft, Apple, Amazon). What each is best at. Why there are so many — the competitive landscape in plain terms. Brief mention of open-source models. Organized as a "meet the players" guide, not a feature comparison chart.

- [ ] **Step 3: Write "Myth vs. Reality" sidebar**
  Myth: "One AI is clearly the best." Reality: they have different strengths.

- [ ] **Step 4: Write "Try This Now" exercise**
  Try asking the same question to two different free AI tools and compare the answers.

- [ ] **Step 5: Write key takeaway summary**

- [ ] **Step 6: Commit**
  ```bash
  git add book/manuscript/02-the-big-names.md
  git commit -m "content: write Chapter 2 — The Big Names & What They Do"
  ```

---

### Task 4: Chapter 3 — How to Actually Talk to AI

**Files:**
- Create: `book/manuscript/03-how-to-talk-to-ai.md`

- [ ] **Step 1: Write opening scenario**
  Someone types "help me" into ChatGPT and gets a useless answer. Then rephrases and gets something great.

- [ ] **Step 2: Write core content**
  Prompting basics: be specific, give context, tell it what you want. The "garbage in, garbage out" principle. Show 3-5 before/after prompt examples. Cover: asking follow-up questions, telling AI to try again, giving it a role ("explain like I'm 10").

- [ ] **Step 3: Write "Myth vs. Reality" sidebar**
  Myth: "You need special technical skills to use AI." Reality: you just need to be clear about what you want.

- [ ] **Step 4: Write "Try This Now" exercise**
  Take a vague prompt, rewrite it using the principles from this chapter, and compare results.

- [ ] **Step 5: Write key takeaway summary**

- [ ] **Step 6: Commit**
  ```bash
  git add book/manuscript/03-how-to-talk-to-ai.md
  git commit -m "content: write Chapter 3 — How to Actually Talk to AI"
  ```

---

### Task 5: Chapter 4 — What AI Is Good At (And Terrible At)

**Files:**
- Create: `book/manuscript/04-good-at-and-terrible-at.md`

- [ ] **Step 1: Write opening scenario**
  Someone uses AI to draft a perfect email, then asks it a math question and gets confidently wrong answer.

- [ ] **Step 2: Write core content**
  Good at: writing, summarizing, brainstorming, translation, coding assistance, pattern recognition. Terrible at: math (sometimes), recent events, being factually reliable without checking, understanding context like a human, emotional intelligence. Introduce "hallucination" in plain language. The golden rule: AI is a draft machine, not a fact machine.

- [ ] **Step 3: Write "Myth vs. Reality" sidebar**
  Myth: "If AI says it confidently, it must be true."

- [ ] **Step 4: Write "Try This Now" exercise**
  Ask AI a factual question you know the answer to. See if it gets it right. Then ask something obscure and try to verify.

- [ ] **Step 5: Write key takeaway summary**

- [ ] **Step 6: Commit**
  ```bash
  git add book/manuscript/04-good-at-and-terrible-at.md
  git commit -m "content: write Chapter 4 — What AI Is Good At (And Terrible At)"
  ```

---

### Task 6: Chapter 5 — Automation ≠ AI (But They're Best Friends)

**Files:**
- Create: `book/manuscript/05-automation-vs-ai.md`

- [ ] **Step 1: Write opening scenario**
  Someone's email auto-reply vs. AI writing a personalized response — same "automatic," completely different technology.

- [ ] **Step 2: Write core content**
  Define automation (if-this-then-that, rules-based, predictable). Define AI (pattern recognition, learning, probabilistic). How they work together: automation handles the plumbing, AI handles the thinking. Everyday examples: smart thermostat (automation) vs. AI recommending your schedule. Mention tools like Zapier, IFTTT, Make as the bridge between them.

- [ ] **Step 3: Write "Myth vs. Reality" sidebar**
  Myth: "AI and automation are the same thing."

- [ ] **Step 4: Write "Try This Now" exercise**
  Identify 3 things in your daily life that are automation (not AI) and 3 that are actually AI.

- [ ] **Step 5: Write key takeaway summary**

- [ ] **Step 6: Commit**
  ```bash
  git add book/manuscript/05-automation-vs-ai.md
  git commit -m "content: write Chapter 5 — Automation vs AI"
  ```

---

### Task 7: Chapter 6 — AI Tools You Can Use Today for Free

**Files:**
- Create: `book/manuscript/06-free-tools-today.md`

- [ ] **Step 1: Write opening scenario**
  "You don't need to spend a dime to start using AI right now."

- [ ] **Step 2: Write core content**
  Curated walkthrough of free tools (as of 2026): ChatGPT free tier, Claude free tier, Google Gemini, Microsoft Copilot, Perplexity, NotebookLM, Canva AI features, Grammarly. For each: what it does, how to access it, one specific thing to try first. Organized by use case (writing, research, images, productivity) not just a list.

- [ ] **Step 3: Write "Myth vs. Reality" sidebar**
  Myth: "The good AI tools all cost money."

- [ ] **Step 4: Write "Try This Now" exercise**
  Pick one tool from the list you've never tried. Spend 10 minutes exploring it with a real task you have.

- [ ] **Step 5: Write key takeaway summary**

- [ ] **Step 6: Commit**
  ```bash
  git add book/manuscript/06-free-tools-today.md
  git commit -m "content: write Chapter 6 — AI Tools You Can Use Today for Free"
  ```

---

### Task 8: Chapter 7 — "Will AI Take My Job?"

**Files:**
- Create: `book/manuscript/07-will-ai-take-my-job.md`

- [ ] **Step 1: Write opening scenario**
  The anxiety: headlines screaming about millions of jobs disappearing. A real person wondering if their career is over.

- [ ] **Step 2: Write core content**
  Honest framing: AI changes jobs more than it eliminates them. Which tasks get automated vs. which jobs disappear entirely. The "AI won't take your job, but someone using AI might" framework. Industries most and least affected. How to future-proof yourself: learn to work WITH AI, not compete against it. Skills that become more valuable, not less.

- [ ] **Step 3: Write "Myth vs. Reality" sidebar**
  Myth: "AI will replace most jobs within 5 years."

- [ ] **Step 4: Write "Try This Now" exercise**
  List your top 5 daily work tasks. For each one, ask: could AI help me do this faster? Could AI do this without me? What part still needs a human?

- [ ] **Step 5: Write key takeaway summary**

- [ ] **Step 6: Commit**
  ```bash
  git add book/manuscript/07-will-ai-take-my-job.md
  git commit -m "content: write Chapter 7 — Will AI Take My Job?"
  ```

---

### Task 9: Chapter 8 — AI at Home: Practical Everyday Uses

**Files:**
- Create: `book/manuscript/08-ai-at-home.md`

- [ ] **Step 1: Write opening scenario**
  A busy parent using AI to plan meals for the week, help a kid with homework, and plan a vacation — all in 20 minutes.

- [ ] **Step 2: Write core content**
  Practical, specific use cases organized by life area: Cooking & meal planning, Travel planning, Health questions (with caveats), Budgeting & personal finance, Home organization, Helping kids with homework, Gift ideas, Writing personal emails/letters, Smart home devices. For each: what to ask, what tool to use, what to watch out for.

- [ ] **Step 3: Write "Myth vs. Reality" sidebar**
  Myth: "AI is only useful for work stuff."

- [ ] **Step 4: Write "Try This Now" exercise**
  Use AI to plan your meals for the next 3 days based on what's already in your fridge.

- [ ] **Step 5: Write key takeaway summary**

- [ ] **Step 6: Commit**
  ```bash
  git add book/manuscript/08-ai-at-home.md
  git commit -m "content: write Chapter 8 — AI at Home"
  ```

---

### Task 10: Chapter 9 — AI at Work: Even If You're Not "Techy"

**Files:**
- Create: `book/manuscript/09-ai-at-work.md`

- [ ] **Step 1: Write opening scenario**
  Someone who "isn't a tech person" discovers they can cut their email writing time in half.

- [ ] **Step 2: Write core content**
  Office-ready use cases anyone can do: Email drafting and replies, Meeting note summaries, Spreadsheet formulas and data cleanup, Presentation outline creation, Research and report writing, Proofreading and editing, Brainstorming and ideation. For each: step-by-step how to do it, example prompts, which free tool to use. Address the "is it cheating?" question directly.

- [ ] **Step 3: Write "Myth vs. Reality" sidebar**
  Myth: "Using AI at work is cheating."

- [ ] **Step 4: Write "Try This Now" exercise**
  Take your most recent work email draft. Paste it into an AI tool and ask it to improve the tone and clarity. Compare.

- [ ] **Step 5: Write key takeaway summary**

- [ ] **Step 6: Commit**
  ```bash
  git add book/manuscript/09-ai-at-work.md
  git commit -m "content: write Chapter 9 — AI at Work"
  ```

---

### Task 11: Chapter 10 — What Is "Agentic AI" and Why Is Everyone Talking About It?

**Files:**
- Create: `book/manuscript/10-agentic-ai.md`

- [ ] **Step 1: Write opening scenario**
  The difference between asking AI "what should I cook?" vs. having AI check your fridge, find recipes, order missing ingredients, and set a timer.

- [ ] **Step 2: Write core content**
  What "agentic" means: AI that plans and executes multi-step tasks on its own. How it's different from the chatbot-style AI in earlier chapters. Real examples in 2026: AI agents booking travel, managing calendars, writing and sending emails, doing research across multiple sources. Why this is the big next wave. What's working, what's still clunky, and where it's headed. Keep it grounded — this is the newest/most hyped chapter, so extra care to separate reality from marketing.

- [ ] **Step 3: Write "Myth vs. Reality" sidebar**
  Myth: "AI agents can fully replace a human assistant right now."

- [ ] **Step 4: Write "Try This Now" exercise**
  Try giving an AI a multi-step task (e.g., "Research the 3 best-rated budget laptops, compare their specs, and write me a recommendation"). See how it handles the complexity.

- [ ] **Step 5: Write key takeaway summary**

- [ ] **Step 6: Commit**
  ```bash
  git add book/manuscript/10-agentic-ai.md
  git commit -m "content: write Chapter 10 — Agentic AI"
  ```

---

### Task 12: Chapter 11 — Privacy, Safety & the Stuff Worth Worrying About

**Files:**
- Create: `book/manuscript/11-privacy-and-safety.md`

- [ ] **Step 1: Write opening scenario**
  Someone pastes their tax return into ChatGPT to ask a question, then wonders: "Wait, who just saw that?"

- [ ] **Step 2: Write core content**
  What happens to your data when you use AI tools. What companies do (and don't) promise about privacy. Practical privacy tips: what NOT to put into AI tools, how to use private/incognito modes, opting out of training data. Deepfakes and misinformation — how to spot AI-generated content. AI bias — what it is, why it happens, how it affects you. The "stuff worth actually worrying about" vs. sci-fi fears. Keep it empowering, not scary.

- [ ] **Step 3: Write "Myth vs. Reality" sidebar**
  Myth: "AI companies keep everything you type forever and sell it."

- [ ] **Step 4: Write "Try This Now" exercise**
  Check the privacy settings on one AI tool you use. Find the opt-out for training data. Takes 2 minutes.

- [ ] **Step 5: Write key takeaway summary**

- [ ] **Step 6: Commit**
  ```bash
  git add book/manuscript/11-privacy-and-safety.md
  git commit -m "content: write Chapter 11 — Privacy, Safety & the Stuff Worth Worrying About"
  ```

---

### Task 13: Chapter 12 — Your 30-Day AI Starter Plan

**Files:**
- Create: `book/manuscript/12-thirty-day-starter-plan.md`

- [ ] **Step 1: Write opening scenario**
  "You've read the book. You get it. Now what? Here's your 30-day plan to go from understanding AI to actually using it every day."

- [ ] **Step 2: Write core content**
  Week 1 (Days 1-7): Getting started — sign up for free tools, try basic prompts, explore one tool per day. Week 2 (Days 8-14): Building habits — use AI for one real task per day (home or work). Week 3 (Days 15-21): Going deeper — try multi-step tasks, experiment with different tools for the same job, start customizing your prompts. Week 4 (Days 22-30): Making it yours — identify your top 3 use cases, build a personal prompt library, teach someone else one thing you learned. Each day: specific action item, which tool to use, estimated time (5-15 min).

- [ ] **Step 3: Write "Myth vs. Reality" sidebar**
  Myth: "You need to be an expert to get real value from AI."

- [ ] **Step 4: Write "Try This Now" exercise**
  Start Day 1 right now. Don't wait until tomorrow.

- [ ] **Step 5: Write key takeaway summary**

- [ ] **Step 6: Commit**
  ```bash
  git add book/manuscript/12-thirty-day-starter-plan.md
  git commit -m "content: write Chapter 12 — Your 30-Day AI Starter Plan"
  ```

---

### Task 14: Back Matter

**Files:**
- Create: `book/manuscript/13-back-matter.md`

- [ ] **Step 1: Write About the Author section**
  Placeholder template with `[Your Name]` and `[Your Bio]` — short version (2-3 sentences) and long version (1 paragraph).

- [ ] **Step 2: Write Resources & Links page**
  Compile resources specifically from the "Try This Now" exercises across all 12 chapters. Organize by chapter reference. Include URLs. Keep it actionable — only the tools/links readers need for the hands-on exercises, not every mention in the book.

- [ ] **Step 3: Write "Also By / What's Next" page**
  Placeholder for future works. Include a call-to-action to join the email list / follow on social media.

- [ ] **Step 4: Commit**
  ```bash
  git add book/manuscript/13-back-matter.md
  git commit -m "content: add back matter — author bio, resources, what's next"
  ```

---

### Task 15: Assemble Full Manuscript

**Files:**
- Create: `book/assembled-manuscript.md`

- [ ] **Step 1: Concatenate all chapter files in order**
  Combine `00-front-matter.md` through `13-back-matter.md` into a single `assembled-manuscript.md` with proper section breaks.

- [ ] **Step 2: Add page break markers**
  Insert `---` (horizontal rule) between each chapter to indicate page breaks for conversion.

- [ ] **Step 3: Verify internal hyperlinks**
  Ensure TOC links point to correct heading anchors. Verify all cross-chapter references work.

- [ ] **Step 4: Commit**
  ```bash
  git add book/assembled-manuscript.md
  git commit -m "content: assemble full manuscript from all chapters"
  ```

---

## Phase 2: Marketing Assets

### Task 16: Amazon KDP Listing Copy

**Files:**
- Create: `book/marketing/amazon-description.md`

- [ ] **Step 1: Write book title + subtitle**
  Optimized for Kindle search. Primary title + benefit-driven subtitle.

- [ ] **Step 2: Write 4,000-character book description**
  With HTML formatting (bold, line breaks) per KDP standards. Hook → promise → chapter highlights → call to action.

- [ ] **Step 3: Write 7 backend keywords**
  Research-informed search terms for Amazon's hidden keyword fields.

- [ ] **Step 4: Write category recommendations**
  2 KDP categories to maximize visibility and reduce competition.

- [ ] **Step 5: Commit**
  ```bash
  git add book/marketing/amazon-description.md
  git commit -m "marketing: write Amazon KDP listing copy, keywords, categories"
  ```

---

### Task 17: Gumroad Sales Page Copy

**Files:**
- Create: `book/marketing/gumroad-sales-page.md`

- [ ] **Step 1: Write headline + subheadline**
  Benefit-driven. Speaks directly to the target audience's pain point.

- [ ] **Step 2: Write benefit bullet list**
  What the reader walks away with — outcomes, not features.

- [ ] **Step 3: Write "Who this is for" section**
  Clear description of ideal reader. Also mention who it's NOT for (sets expectations).

- [ ] **Step 4: Write FAQ section**
  3-4 common objections: "Do I need to be technical?", "Is this just about ChatGPT?", "How is this different from free blog posts?", "What format is it?"

- [ ] **Step 5: Write social proof placeholder**
  Template for where reviews will go once available.

- [ ] **Step 6: Commit**
  ```bash
  git add book/marketing/gumroad-sales-page.md
  git commit -m "marketing: write Gumroad sales page copy"
  ```

---

### Task 18: Email Sequence

**Files:**
- Create: `book/marketing/email-sequence.md`

- [ ] **Step 1: Write Email 1 — Welcome (Day 0)**
  Thank them, set expectations for the series, link to Chapter 6's free tools for an instant win. Warm, excited tone.

- [ ] **Step 2: Write Email 2 — Quick Win (Day 3)**
  Walk through one specific AI exercise from the book. Make it copy-paste actionable. Prove the book's value.

- [ ] **Step 3: Write Email 3 — What's Next (Day 7)**
  Ask what they found most useful (engagement), tease future content, invite them to share the book / leave a review.

- [ ] **Step 4: Write subject lines**
  A/B options for each email (2 subject lines per email).

- [ ] **Step 5: Commit**
  ```bash
  git add book/marketing/email-sequence.md
  git commit -m "marketing: write 3-email post-purchase drip sequence"
  ```

---

### Task 19: Author Bio, Cover Brief, Launch Assets

**Files:**
- Create: `book/marketing/author-bio.md`
- Create: `book/marketing/canva-cover-brief.md`
- Create: `book/marketing/launch-announcement.md`
- Create: `book/marketing/review-request-template.md`

- [ ] **Step 1: Write author bio**
  Short (2-3 sentences for Amazon) and long (1 paragraph for Gumroad/back matter) versions. `[Your Name]` placeholders.

- [ ] **Step 2: Write Canva cover brief**
  Recommended colors, fonts, layout. Reference 3-5 comp titles (successful e-books in similar space). Specify text hierarchy (title large, subtitle medium, author small). Note KDP cover dimension requirements (1600x2560px recommended).

- [ ] **Step 3: Write launch announcement**
  Short social media post (Twitter/LinkedIn length) and longer version (for email to personal network).

- [ ] **Step 4: Write review request template**
  Friendly message to send early readers. Make it easy — include direct link placeholders for Amazon review page.

- [ ] **Step 5: Commit**
  ```bash
  git add book/marketing/author-bio.md book/marketing/canva-cover-brief.md book/marketing/launch-announcement.md book/marketing/review-request-template.md
  git commit -m "marketing: add author bio, cover brief, launch announcement, review request"
  ```

---

## Phase 3: Platform Setup Guides

### Task 20: Manuscript Conversion Guide

**Files:**
- Create: `book/guides/manuscript-conversion.md`

- [ ] **Step 1: Write Pandoc conversion instructions**
  How to install Pandoc. Command to convert Markdown → DOCX (`pandoc assembled-manuscript.md -o manuscript.docx`). How to add styles in Word after conversion.

- [ ] **Step 2: Write PDF generation instructions**
  Option A: Print to PDF from Word/Google Docs. Option B: Pandoc with a PDF engine. Recommend the simpler option.

- [ ] **Step 3: Write EPUB conversion instructions**
  Option A (recommended): Upload DOCX directly to KDP — KDP's built-in converter handles EPUB/Kindle format automatically. Option B: Use Calibre (free, open-source) to convert DOCX → EPUB locally before uploading. Include Calibre download link and the specific conversion steps.

- [ ] **Step 4: Write KDP-specific formatting tips**
  Heading styles that convert cleanly to Kindle. Hyperlinked TOC requirements. Image handling (if any). Page break markers.

- [ ] **Step 5: Commit**
  ```bash
  git add book/guides/manuscript-conversion.md
  git commit -m "guides: write manuscript conversion guide (Markdown → DOCX → EPUB → PDF)"
  ```

---

### Task 21: KDP Setup Guide

**Files:**
- Create: `book/guides/kdp-setup-guide.md`

- [ ] **Step 1: Write account creation walkthrough**
  Step-by-step with expected screens. Tax information section. Bank account for royalties.

- [ ] **Step 2: Write book upload walkthrough**
  Where to enter title, subtitle, description, keywords, categories. How to upload DOCX and cover. How to handle the ISBN prompt (skip it — KDP assigns free ASIN). Preview tool usage.

- [ ] **Step 3: Write pricing and publishing steps**
  How to set $4.99 price. Select 70% royalty. Territory selection. DO NOT enroll in KDP Select (exclusivity conflict with Gumroad). Click publish — what happens next (24-72hr review).

- [ ] **Step 4: Commit**
  ```bash
  git add book/guides/kdp-setup-guide.md
  git commit -m "guides: write KDP setup guide"
  ```

---

### Task 22: Gumroad Setup Guide

**Files:**
- Create: `book/guides/gumroad-setup-guide.md`

- [ ] **Step 1: Write account creation walkthrough**
  Step-by-step. Payment setup (Stripe connect).

- [ ] **Step 2: Write product creation walkthrough**
  How to create a digital product. Upload PDF. Set $9.99 price. Paste in sales page copy from `gumroad-sales-page.md`. Cover image upload.

- [ ] **Step 3: Write launch checklist**
  Test purchase flow. Verify PDF download works. Check email receipt. Set up discount codes with explicit warning: **Do not use public discount codes that reduce the effective price below $4.99 (your KDP list price).** Gumroad's public coupon pages are indexable by search engines, and Amazon's price-matching policy can automatically lower your KDP price to match. Private/direct-link codes carry less risk but caution is still advised. Explain the mechanism clearly so the user understands *why*.

- [ ] **Step 4: Commit**
  ```bash
  git add book/guides/gumroad-setup-guide.md
  git commit -m "guides: write Gumroad setup guide"
  ```

---

### Task 23: Mailchimp Drip Setup Guide

**Files:**
- Create: `book/guides/mailchimp-drip-guide.md`

- [ ] **Step 1: Write account setup and audience creation**
  Create free Mailchimp account. Create an audience. Set up signup form or Gumroad → Mailchimp integration (via Zapier free tier or manual export).

- [ ] **Step 2: Write automation sequence setup**
  How to create an automated email sequence (Customer Journey). Set triggers: Day 0, Day 3, Day 7. Paste email content from `email-sequence.md`. Set subject lines.

- [ ] **Step 3: Write testing instructions**
  How to send test emails. How to verify timing. How to preview on mobile.

- [ ] **Step 4: Write ConvertKit alternative note**
  Add a brief section noting that ConvertKit is an alternative email platform but automated sequences (drip campaigns) require their paid Creator plan at $29/mo. The free tier only supports broadcast (one-time) emails. Include this so the user has a documented fallback if Mailchimp doesn't work for them.

- [ ] **Step 5: Commit**
  ```bash
  git add book/guides/mailchimp-drip-guide.md
  git commit -m "guides: write Mailchimp drip sequence setup guide"
  ```

---

## Phase 4: Post-Launch

### Task 24: Post-Launch Actions

- [ ] **Step 1: Send review request to early readers**
  Using the template from `book/marketing/review-request-template.md`, send to friends, family, early buyers. Include direct link to the Amazon review page (found in KDP dashboard under your book's detail page).

- [ ] **Step 2: Monitor first-week performance**
  Check KDP dashboard for sales, page reads, and ranking. Check Gumroad dashboard for sales and email signups. Note any patterns (which platform is performing better, what time of day sales come in).

- [ ] **Step 3: Adjust if needed**
  Based on first-week data: consider adjusting Amazon keywords/categories if discoverability is low, tweaking the Gumroad sales page copy if conversion is low, or adjusting pricing. Claude can help rewrite any of these assets.

- [ ] **Step 4: Commit any updates**
  ```bash
  git add -A
  git commit -m "post-launch: update marketing assets based on performance data"
  ```

---

## Final Assembly

### Task 25: Final Review and Polish

- [ ] **Step 1: Read through assembled manuscript for consistency**
  Verify tone is consistent across all chapters. Check that cross-references between chapters are accurate. Verify all "Try This Now" exercises reference tools that were covered.

- [ ] **Step 2: Verify all deliverables are complete**
  Check every item in the spec's Deliverables table against actual files produced. Confirm nothing is missing.

- [ ] **Step 3: Final commit**
  ```bash
  git add -A
  git commit -m "final: complete manuscript review and polish"
  ```
