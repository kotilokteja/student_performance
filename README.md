# Academic Guard

I have an already-working Streamlit ML project called:

"EdTech Academic Risk Early-Warning System"

I am uploading my CURRENT working project files.

I want you to act as a SENIOR PRODUCT DESIGNER + SENIOR FRONTEND ENGINEER.

Your job is to transform the EXISTING UI into a polished, premium, professional web application while preserving the entire existing ML/application logic.

============================================================
🚨 ABSOLUTE RULE — DO NOT BREAK MY EXISTING PROJECT
============================================================

This is an EXISTING WORKING PROJECT.

DO NOT rebuild it from scratch.

DO NOT replace the ML implementation.

DO NOT change the dataset.

DO NOT change the trained model.

DO NOT change the target definition.

DO NOT change preprocessing.

DO NOT change feature encoding.

DO NOT change prediction logic.

DO NOT change probability calculation.

DO NOT change evaluation calculations.

DO NOT remove existing functionality.

DO NOT remove existing pages.

DO NOT change the project's purpose.

DO NOT invent a new ML model.

DO NOT replace working Python logic with fake/demo data.

DO NOT hardcode values that are currently calculated dynamically.

The existing functionality is the source of truth.

Your job is:

EXISTING WORKING APPLICATION
            ↓
PROFESSIONAL UI/UX UPGRADE
            ↓
KEEP ALL EXISTING LOGIC EXACTLY THE SAME

If something works, preserve it.

If you need to restructure code to create a better UI, move existing logic into functions without changing what the logic does.

============================================================
PROJECT PURPOSE
============================================================

The application is an:

"EdTech Academic Risk Early-Warning System"

It analyzes student academic information and predicts whether a student is:

0 = Not At Risk
1 = At Risk

The application already contains functionality such as:

- Dashboard
- Risk Assessment
- Model Performance
- Dataset Insights
- About
- ML prediction
- probability
- charts
- model evaluation
- dataset analysis
- existing navigation
- existing student input fields
- existing preset/demo functionality if present
- existing export functionality if present

KEEP ALL OF THEM.

============================================================
FIRST: INSPECT THE PROJECT
============================================================

Before changing anything:

1. Read the COMPLETE current app.py.
2. Read all existing frontend/CSS files.
3. Identify the existing:
   - model loading
   - dataset loading
   - preprocessing
   - target creation
   - feature list
   - prediction function
   - probability calculation
   - model evaluation
   - charts
   - navigation
   - session state
   - sidebar
   - Back buttons
   - input forms
4. Understand how everything currently works.

DO NOT start generating a new application before understanding the existing one.

============================================================
DESIGN GOAL
============================================================

I want the UI to look like a REAL modern software product.

Not:

- a college project
- a default Streamlit dashboard
- a generic AI-generated dashboard
- a page full of random cards

Take design inspiration from the QUALITY and PRINCIPLES of:

- Apple
- Linear
- Vercel
- Stripe
- Notion
- modern SaaS dashboards
- premium analytics platforms
- modern education technology products

DO NOT COPY any of them.

Do not reproduce their exact layouts or branding.

Instead use:

- excellent typography
- whitespace
- consistent spacing
- strong hierarchy
- restrained color usage
- precise alignment
- consistent component sizing
- subtle borders
- subtle shadows
- meaningful interaction
- excellent charts
- clean navigation
- professional micro-interactions

The result should look like a product a real software company could ship.

============================================================
VERY IMPORTANT — KEEP THE LEFT SIDEBAR
============================================================

The application MUST have a persistent left navigation/sidebar.

It must contain:

OVERVIEW
• Dashboard
• Risk Assessment

ANALYTICS
• Model Performance
• Dataset Insights

PROJECT
• About

The sidebar MUST remain visible while navigating between pages.

If the user clicks a Back button:

THE SIDEBAR MUST NOT DISAPPEAR.

If Back returns to Dashboard:

- Dashboard opens
- sidebar remains visible
- Dashboard is highlighted

Do NOT create duplicate sidebars.

Do NOT conditionally hide the sidebar because of page state.

Navigation should be controlled from a single consistent application layout.

============================================================
LAYOUT SYSTEM
============================================================

Create a proper design system.

Use a consistent spacing scale.

Use consistent:

- margins
- padding
- card radius
- borders
- shadows
- typography
- component heights
- gaps

Cards in the same row MUST have equal height.

Example:

┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│ KPI        │ │ KPI        │ │ KPI        │ │ KPI        │
│            │ │            │ │            │ │            │
└────────────┘ └────────────┘ └────────────┘ └────────────┘

NOT:

┌──────────┐ ┌─────────────────┐ ┌───────┐
│          │ │                 │ │       │
│          │ │                 │ │       │
└──────────┘ │                 │ └───────┘
             └─────────────────┘

All cards within a component group should align perfectly.

============================================================
SHAPE SYSTEM
============================================================

Use a consistent shape language.

Small cards:
12px radius

Main cards:
16px radius

Hero/large panels:
20px radius

Buttons:
10px radius

Badges:
pill-shaped

Do not randomly mix many different radii.

============================================================
COLOR THEORY
============================================================

Use a restrained professional palette.

Background:
#F7F8FA

Card:
#FFFFFF

Primary text:
#111827

Secondary text:
#4B5563

Muted text:
#6B7280

Border:
#E5E7EB

Primary:
#2563EB

Safe:
#15803D

Safe background:
#F0FDF4

Risk:
#DC2626

Risk background:
#FEF2F2

Do NOT globally recolor the application if the current theme already works.

The main priority is:

READABILITY.

Some text in the current application is not visible or has poor contrast.

Audit EVERY page and fix ONLY the problematic text.

Check:

- headings
- subtitles
- card text
- sidebar text
- navigation
- buttons
- form labels
- help text
- KPI labels
- KPI values
- chart labels
- chart axes
- chart legends
- badges
- tables
- tooltips

Never use:

light gray text on white

or

white text on light backgrounds.

Do not make everything black.

Maintain a clear hierarchy.

============================================================
REMOVE UNNECESSARY UI
============================================================

IMPORTANT:

Do NOT simply add more cards.

Audit the current UI.

REMOVE ONLY genuinely unnecessary:

- duplicate headings
- duplicate descriptions
- repeated statistics
- empty boxes
- decorative boxes
- redundant text
- duplicate buttons
- unnecessary separators
- meaningless badges
- charts that duplicate information without adding value

But DO NOT remove any actual functionality.

The goal is:

FEWER BUT BETTER COMPONENTS.

Do not put every piece of text inside a card.

Do not create cards inside cards unless there is a clear reason.

============================================================
DASHBOARD
============================================================

Keep the existing dashboard functionality but make the presentation significantly better.

Create a clean hierarchy:

EYEBROW
Academic Intelligence

TITLE
Academic Risk
Early-Warning System

SHORT DESCRIPTION

Then a consistent KPI row.

Use the existing calculated values.

Examples:

Total Students
649

At Risk
301

Not At Risk
348

At-Risk Recall
98.3%

Do NOT hardcode these if the existing application calculates them.

Then:

RISK OVERVIEW

Use the existing risk data.

Create a polished interactive chart.

Then:

ACADEMIC SIGNALS

Show the existing calculated:

- Absences
- Study Time
- Failures
- G1
- G2

Then:

KEY INSIGHTS

Generate insights from the actual dataset.

Do not invent statistics.

============================================================
RISK ASSESSMENT
============================================================

This is one of the most important screens.

Organize existing inputs into logical sections.

Example:

01
ACADEMIC PERFORMANCE

02
SUPPORT & ENVIRONMENT

03
STUDENT ENGAGEMENT

Do not change which inputs the model receives.

Use the existing feature values.

Make the form visually clean.

============================================================
STUDY TIME UI
============================================================

IMPORTANT.

The existing dataset internally uses:

1 = Less than 2 hours/week
2 = 2–5 hours/week
3 = 5–10 hours/week
4 = More than 10 hours/week

DO NOT change these internal values.

The ML model must still receive:

1
2
3
4

But the USER INTERFACE must NOT show:

Study Time = 1
Study Time = 2
Study Time = 3
Study Time = 4

Instead display:

Weekly Study Time

○ Less than 2 hours
○ 2–5 hours
○ 5–10 hours
○ More than 10 hours

Then internally map:

Less than 2 hours → 1
2–5 hours → 2
5–10 hours → 3
More than 10 hours → 4

Do not change model behavior.

Apply the same UX principle to other coded fields if appropriate:
human-readable to user,
original encoded value to model.

============================================================
PREDICTION RESULT
============================================================

Keep the existing prediction logic EXACTLY THE SAME.

Improve only its presentation.

Make the result feel like a professional assessment.

Example:

ASSESSMENT RESULT

● AT RISK

78.4%

Probability of academic risk

RISK LEVEL
HIGH

Use the EXISTING probability.

Do not create another probability calculation.

Add a visual risk indicator/gauge if it does not interfere with the existing logic.

============================================================
HOVER INTERACTIONS
============================================================

Add subtle professional interactions.

KPI card hover:

- slight lift
- subtle shadow
- subtle border/accent change

Example:

Normal:

Total Students
649

Hover:

Total Students
649
View dataset →

Do NOT make every card behave this way.

Use hover only where useful.

Animation:
150–250ms.

No flashy animation.

============================================================
TOOLTIPS
============================================================

Add small information icons only where useful.

Example:

Accuracy ⓘ

Hover:

"Percentage of predictions that were correct on the test set."

Recall ⓘ

"Percentage of actual at-risk students correctly identified."

Risk Probability ⓘ

"Model-estimated probability that the student belongs to the At Risk class."

Do not add tooltips everywhere.

============================================================
CHART INTERACTIONS
============================================================

Improve existing charts rather than replacing useful ones unnecessarily.

Hovering over a chart element should show:

- exact value
- category
- percentage where useful

Example:

Grade: 12
Students: 72
Percentage: 11.1%

Calculate from the actual dataset.

============================================================
MODEL PERFORMANCE
============================================================

Keep existing model evaluation.

Improve presentation.

Show:

Accuracy
Precision
Recall
F1

Then:

CONFUSION MATRIX

Show the actual matrix.

Use an interactive heatmap if appropriate.

Hover should explain:

True Negative
False Positive
False Negative
True Positive

Then show model comparison using ACTUAL existing values.

Do not invent performance numbers.

============================================================
DATASET INSIGHTS
============================================================

Keep existing dataset analysis.

Improve visual hierarchy.

Show:

Students
Features
At-Risk Students
Not At-Risk Students

Then existing:

Risk Distribution

G3 Distribution

Academic Indicators

Use clean interactive charts.

============================================================
ABOUT
============================================================

Keep existing About content.

Improve typography and spacing.

Do not add unnecessary information.

============================================================
VISUAL ELEMENTS / IMAGES
============================================================

You MAY add a small number of tasteful visuals IF they genuinely improve the product.

Good examples:

- subtle academic/analytics illustration in Dashboard hero
- small illustration in About page
- minimal empty-state illustration
- lightweight SVG icons

Do NOT add:

- random stock photos
- giant student photos
- decorative images everywhere
- huge background images
- heavy assets that slow loading

If a visual doesn't improve usability, don't add it.

============================================================
ICONS
============================================================

Use one consistent icon style.

Examples:

Students → people icon
Risk → warning icon
Model → chart icon
Dataset → database icon
Assessment → clipboard/check icon

Do not use random emojis throughout the UI.

============================================================
PERFORMANCE
============================================================

The website must remain fast.

Keep or improve existing caching.

Use:

@st.cache_resource

for model loading.

Use:

@st.cache_data

for dataset loading and expensive static calculations.

Do not load the model repeatedly.

Do not reload the dataset unnecessarily.

Do not recalculate expensive evaluation on every UI interaction.

Avoid:

- huge images
- unnecessary JavaScript
- external resources that block loading
- excessive animations
- repeated CSS injection
- duplicate chart generation

============================================================
HTML / CSS / JAVASCRIPT
============================================================

You ARE allowed to create frontend files if they produce a better result.

Preferred structure:

project/
│
├── app.py
│
├── frontend/
│   ├── styles.css
│   ├── components.css
│   └── interactions.js
│
├── dataset/
│
├── model/
│
└── src/

Use CSS for:

- layout
- alignment
- cards
- hover effects
- transitions
- typography
- responsive behavior
- visual hierarchy

Use JavaScript ONLY where it genuinely improves interaction and is compatible with Streamlit.

Do not use JavaScript to replace the existing Python/ML logic.

If HTML/CSS/JS is not necessary for a specific feature, don't add it.

============================================================
RESPONSIVE DESIGN
============================================================

The UI should work properly on:

Desktop
Laptop
Tablet

No:

- overlapping
- clipped text
- horizontal scrolling
- broken charts
- uneven cards

============================================================
ACCESSIBILITY
============================================================

Every visible piece of text must be readable.

Check contrast.

Make interactive elements clearly identifiable.

Do not rely only on color to communicate risk.

Use labels/icons/text where useful.

============================================================
FINAL QUALITY STANDARD
============================================================

I want the result to feel like:

"An actual commercial EdTech analytics product."

NOT:

"An AI-generated Streamlit college project."

Before finishing, inspect every page and ask:

- Are the cards aligned?
- Are cards in the same row the same size?
- Is the sidebar always visible?
- Does Back preserve the sidebar?
- Is any text invisible?
- Is any information duplicated?
- Is anything unnecessarily boxed?
- Are charts useful?
- Are hover interactions subtle?
- Are tooltips useful?
- Are colors consistent?
- Is the page too crowded?
- Is there too much empty space?
- Does every component have a purpose?

============================================================
CRITICAL FINAL TEST
============================================================

Before giving me the final result:

1. Run a Python syntax check.
2. Start the application.
3. Test Dashboard.
4. Test Risk Assessment.
5. Test prediction.
6. Test probability.
7. Test Model Performance.
8. Test Dataset Insights.
9. Test About.
10. Test sidebar navigation.
11. Click Back from every applicable page.
12. Verify sidebar NEVER disappears.
13. Test all existing buttons.
14. Test all existing inputs.
15. Test charts.
16. Test hover interactions.
17. Test tooltips.
18. Check text contrast.
19. Check responsive layout.
20. Verify ML results are unchanged.

============================================================
FINAL OUTPUT
============================================================

Do NOT give me snippets.

Do NOT give me pseudocode.

Do NOT give me a generic replacement application.

Modify my ACTUAL uploaded project.

Return:

1. Complete modified files.
2. Clearly show which files were added/changed.
3. Exact folder structure.
4. Exact command to install any genuinely required dependency.
5. Exact command to run the application.
6. Briefly explain what UI changes were made.

MOST IMPORTANT:

I want the SAME PROJECT,
SAME ML LOGIC,
SAME DATA,
SAME MODEL,
SAME FEATURES,
SAME PROCEDURE,

with a MUCH BETTER PROFESSIONAL UI/UX.

Do not sacrifice functionality for appearance.

This project was built with [Lovable](https://lovable.dev).

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/f07b9aed-dacc-4e64-a75c-0eaa580cbe71).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
