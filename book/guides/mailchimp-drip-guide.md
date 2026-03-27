# Mailchimp Drip Sequence Setup Guide

**Goal:** Automatically send 3 emails to every Gumroad buyer of *AI for the Rest of Us* on Day 0, Day 3, and Day 7 after purchase.

**Email content lives in:** `book/marketing/email-sequence.md`

---

## 1. Account Setup and Audience Creation

1. Go to [mailchimp.com](https://mailchimp.com) and click **Sign Up Free**.
2. Create your account with a valid email address and verify it.
3. Free tier includes up to **500 contacts** and access to **automated customer journeys** (the feature we need for drip sequences).
4. Once logged in, go to **Audience > Audience dashboard**.
5. Click **Manage Audience > Settings** to configure your list:
   - **Audience name:** "AI for the Rest of Us Readers"
   - **Default From name:** Your first name (matches the friendly tone of the emails)
   - **Default From email:** The email address you want readers to reply to
6. Under **Audience fields and \*|MERGE|\* tags**, confirm that `FNAME` (First Name) is enabled — the emails use `[First Name]` personalization.

---

## 2. Getting Gumroad Buyers Into Mailchimp

You need a way to move each new Gumroad customer into your Mailchimp audience automatically (or semi-automatically). Two options:

### Option A: Zapier Free Tier (Recommended)

This is the hands-off approach. Once set up, every new sale flows into Mailchimp automatically.

1. Go to [zapier.com](https://zapier.com) and create a free account.
2. Click **Create Zap**.
3. **Trigger step:**
   - Search for **Gumroad** as the trigger app.
   - Select the trigger event: **New Sale**.
   - Connect your Gumroad account (you will need your Gumroad API key — find it under Gumroad > Settings > Advanced).
   - Test the trigger to confirm Zapier can see your sales.
4. **Action step:**
   - Search for **Mailchimp** as the action app.
   - Select the action: **Add/Update Subscriber**.
   - Connect your Mailchimp account.
   - Map the fields:
     - **Audience:** select "AI for the Rest of Us Readers"
     - **Email:** map to the buyer's email from the Gumroad trigger
     - **First Name (FNAME):** map to the buyer's name from the Gumroad trigger
     - **Tag:** type `new-buyer` (this tag is what triggers the email journey — see Section 3)
   - Test the action to confirm a test subscriber appears in Mailchimp.
5. **Turn on the Zap.**

**Free tier limit:** Zapier's free plan allows **100 tasks/month**. Each sale uses 1 task, so this covers up to 100 sales/month. If you exceed that, upgrade to a paid Zapier plan or switch to Option B.

### Option B: Manual CSV Export

Simpler to set up but requires periodic manual work.

1. In Gumroad, go to **Audience** and click **Export**.
2. Download the CSV of all customers.
3. In Mailchimp, go to **Audience > Import contacts**.
4. Upload the CSV and map the email and name columns.
5. During import, apply the tag `new-buyer` to all imported contacts.
6. Repeat this process weekly (or however often you want new buyers to receive the sequence).

**Recommendation:** Use Option A if you want a fully automated, set-it-and-forget-it workflow. Use Option B only if you prefer simplicity and are comfortable with a manual step every few days.

---

## 3. Setting Up the Automated Email Sequence

Mailchimp calls its automation builder **Customer Journeys**. Here is how to build the 3-email drip sequence.

### Create the Journey

1. In Mailchimp, go to **Automations > Customer Journeys**.
2. Click **Create Journey**.
3. Name it something clear, like "Post-Purchase Drip — AI for the Rest of Us."
4. Select your audience ("AI for the Rest of Us Readers").

### Set the Starting Point

5. Click **Choose a starting point**.
6. Select **"Tag is added"**.
7. Choose the tag: `new-buyer`.
   - This means: any time a contact gets the `new-buyer` tag (either via Zapier or manual import), they enter this journey.

### Email 1 — Welcome (Day 0)

8. Click the **+** button to add a journey point.
9. Select **Send email**.
10. Configure the email:
    - **Subject line:** Use one of the A/B options from `email-sequence.md` Email 1:
      - A: "You're in! Here's where to start with your new book"
      - B: "The one chapter to read first (hint: it's not Chapter 1)"
      - Or use Mailchimp's subject line A/B test feature to test both.
    - **Preview text:** "Skip straight to the free tools — you'll be using AI in 10 minutes."
    - **From name and email:** Should auto-populate from your audience settings.
    - **Body:** Open the email designer, choose a simple single-column layout, and paste the body content from Email 1 in `email-sequence.md`. Replace `[First Name]` with the Mailchimp merge tag `*|FNAME|*`.
11. Click **Save**.

### Wait Step (3 Days)

12. Click the **+** button below Email 1.
13. Select **Time delay**.
14. Set the delay to **3 days**.

### Email 2 — Quick Win (Day 3)

15. Click the **+** button below the time delay.
16. Select **Send email**.
17. Configure the email:
    - **Subject line:** Pick from Email 2 options:
      - A: "Try this 30-second AI trick (copy-paste ready)"
      - B: "I dare you to try this before dinner tonight"
    - **Preview text:** "Paste this prompt into ChatGPT and watch what happens."
    - **Body:** Paste the body content from Email 2 in `email-sequence.md`. Replace `[First Name]` with `*|FNAME|*`. Make sure the blockquote prompt is formatted clearly (use a colored background or indent in the email designer).
18. Click **Save**.

### Wait Step (4 More Days)

19. Click the **+** button below Email 2.
20. Select **Time delay**.
21. Set the delay to **4 days** (3 + 4 = Day 7 from purchase).

### Email 3 — What's Next (Day 7)

22. Click the **+** button below the time delay.
23. Select **Send email**.
24. Configure the email:
    - **Subject line:** Pick from Email 3 options:
      - A: "One quick question (and a peek at what's coming)"
      - B: "What's been the most useful thing so far?"
    - **Preview text:** "I'd love to hear what clicked for you — plus a sneak peek at new stuff."
    - **Body:** Paste the body content from Email 3 in `email-sequence.md`. Replace `[First Name]` with `*|FNAME|*`. Update `[Gumroad link]` and `[Review link placeholder]` with your actual links before going live.
25. Click **Save**.

### Activate

26. Review the full journey map — you should see: **Tag added > Email 1 > Wait 3 days > Email 2 > Wait 4 days > Email 3**.
27. Click **Turn On** (top right) to activate the journey.

---

## 4. Testing

Before real buyers start flowing through, verify everything works:

1. **Send test emails:** In each email step of the journey, click **Send a test email** and send to your own address. Do this for all 3 emails.
2. **Check formatting:**
   - Open each test email on desktop and on your phone.
   - Verify text is readable, links are clickable, and the layout looks clean.
   - Confirm that `*|FNAME|*` merge tags render properly (in test emails they may show as a fallback or your own name).
3. **Verify links work:**
   - Click every link in every email — the Gumroad product link, the review link, and any chapter references.
   - Make sure nothing is broken or pointing to a placeholder.
4. **Check timing and delays:**
   - In the journey builder, confirm the delays read "3 days" and "4 days" respectively.
5. **Run a full test subscriber (optional but recommended):**
   - Add yourself as a new subscriber with the `new-buyer` tag.
   - You will receive Email 1 immediately, Email 2 in 3 days, and Email 3 in 7 days.
   - This confirms the entire flow end-to-end.
   - After testing, remove yourself or mark the test contact so it does not skew your analytics.

---

## 5. ConvertKit (Kit) as an Alternative

If Mailchimp does not work for you, [Kit](https://kit.com) (formerly ConvertKit) is a popular email platform built specifically for creators.

**Key differences to be aware of:**

- Kit's **free tier** supports up to 10,000 subscribers but only allows **broadcast (one-time) emails**. It does **not** include automated drip sequences on the free plan.
- Automated email sequences require Kit's **Creator plan**, which starts at **$29/month**.
- Kit's automation builder is arguably more intuitive than Mailchimp's for simple drip sequences.
- Kit also integrates directly with Gumroad (no Zapier needed on paid plans).

**Bottom line:** Mailchimp's free tier is the better starting point because it includes automated journeys at no cost. If you outgrow Mailchimp or want a more creator-focused platform, Kit is a solid upgrade — just budget for the monthly cost.
