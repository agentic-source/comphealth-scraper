# Amazon KDP Setup and Publishing Guide

> For first-time publishers. This guide walks through every screen you'll encounter when publishing "AI for the Rest of Us" on Kindle Direct Publishing.

---

## 1. Account Creation

1. Go to [kdp.amazon.com](https://kdp.amazon.com)
2. Sign in with your existing Amazon account, or create a new one — any standard Amazon account works
3. Complete the **Tax Information** section:
   - US authors: you'll fill out a W-9
   - International authors: you'll fill out a W-8BEN
   - KDP walks you through the entire process with a step-by-step interview — no need to download forms yourself
4. Add a **bank account** for royalty payments:
   - You'll need your routing number and account number
   - KDP also supports wire transfer for international authors
5. **Timeline:** Your account is usually ready immediately after submitting tax info. No waiting period.

---

## 2. Book Upload Walkthrough

From the KDP dashboard, click **Create New Title**, then select **Kindle eBook** (not paperback).

### Book Details (Screen 1)

| Field | What to Enter |
|-------|--------------|
| **Language** | English |
| **Book Title** | AI for the Rest of Us |
| **Subtitle** | 12 Things You Need to Know Before Everyone Else Figures It Out |
| **Author** | [Your Name] |
| **Description** | Paste the HTML-formatted version from `book/marketing/amazon-description.md` |
| **Keywords** | Enter all 7 backend keywords from `amazon-description.md` (one per field) |
| **Categories** | Select the 2 recommended categories from `amazon-description.md` |

### ISBN Prompt

- Select **"Get a free KDP ISBN"** or simply skip this step
- KDP assigns a free ASIN (Amazon Standard Identification Number) automatically
- You do **NOT** need to purchase an ISBN for Kindle-only publishing

### Manuscript Upload (Screen 2)

1. **Upload manuscript:** Upload your DOCX file. KDP converts it automatically to Kindle format.
2. **Upload cover:** Upload your cover image at **1600x2560px** resolution, in JPG or TIFF format.
3. **Preview your book:** Click **Launch Previewer** — this is critical.
   - Check every chapter
   - Verify all Table of Contents links work
   - Test formatting across device types: phone, tablet, and Kindle e-reader
   - Look for broken images, weird spacing, or orphaned headings

> Do not skip the previewer. Formatting issues that look fine in Word can break badly on Kindle.

---

## 3. Pricing and Publishing (Screen 3)

### KDP Select Enrollment

- **DO NOT ENROLL in KDP Select.**
- KDP Select requires Amazon exclusivity — enrolling means you cannot sell on Gumroad or any other platform.
- Select the **standard listing** option instead.

### Territories

- Select **All territories (worldwide rights)**

### Pricing

| Setting | Value |
|---------|-------|
| **List Price (USD)** | $4.99 |
| **Royalty Plan** | 70% (available for books priced $2.99–$9.99) |

- KDP will auto-suggest prices for other marketplaces (UK, EU, CA, AU, etc.)
- Accept the defaults or adjust — the defaults are reasonable currency conversions

### Publish

- Click **Publish Your Kindle eBook**
- Your book enters Amazon's review queue
- Review typically takes **24–72 hours**
- You'll receive an email when the book is live

---

## 4. After Publishing

- Your book receives an **ASIN** — Amazon's unique product identifier
- It appears in Kindle Store search results within 24–72 hours of approval
- Track sales and royalties in the **KDP Reports** dashboard
- You can **update the manuscript** or **edit the description** at any time from the KDP bookshelf — updates go through a brief re-review

---

## Quick Reference: What You Need Before Starting

- [ ] Amazon account
- [ ] Bank routing and account numbers
- [ ] Tax ID (SSN for US, or equivalent for W-8BEN)
- [ ] Final DOCX manuscript file
- [ ] Cover image (1600x2560px, JPG or TIFF)
- [ ] Book description (HTML-formatted) from `book/marketing/amazon-description.md`
- [ ] 7 backend keywords from `book/marketing/amazon-description.md`
- [ ] 2 category selections from `book/marketing/amazon-description.md`
