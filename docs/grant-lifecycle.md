# Grant lifecycle

RegenOS should model grants as a lifecycle, not as a single application form.

For Capital Grants-style schemes, the safe default is:

> plan and apply first, wait for an agreement, then do the work, then claim.

Do not start work or buy materials before the agreement start date unless the
specific scheme guidance says otherwise.

## Automation boundary

The official submission route is the Rural Payments service. RegenOS should not
assume a public API exists for applications or claims.

The useful automation is:

- prepare the right information
- create JobDone tasks
- collect evidence at the right time
- produce application and claim packs
- warn when the user is about to do work too early
- keep a durable audit trail

Actual submission should remain human-controlled unless an official API or
authorised agent route is available.

## Phases

### 1. Explore

Purpose:

- identify possible sites and interventions
- estimate rough value
- decide whether to investigate further

Typical tasks:

- water walk candidate site
- take exploratory photos
- record GPS point or boundary
- measure rough channel width, pond area, slope, or access constraints
- create rough budget
- record unknowns

Outputs:

- candidate intervention
- rough eligibility status
- rough budget
- evidence gaps

### 2. Pre-application

Purpose:

- decide whether the application can be made safely
- collect required support before submission

Typical tasks:

- check business and land are registered in Rural Payments
- check land parcels and maps
- check management control
- check existing agreements and double-funding risk
- check whether adviser support is required
- check consents, permits, SSSI, archaeology, drainage, access, public rights of way
- gather before-work photos where required
- prepare map/sketch
- prepare implementation plan or feasibility study where required
- confirm group funding limits and minimum claim issues

Outputs:

- application-ready checklist
- supporting evidence pack
- decision: apply, defer, or drop

### 3. Application

Purpose:

- submit a complete application through the official route

Typical tasks:

- fill Rural Payments application
- select capital items and quantities
- attach required supporting evidence
- submit application
- save submitted copy or confirmation

Outputs:

- submission record
- submitted evidence bundle
- application reference

### 4. Agreement

Purpose:

- accept or reject the offer and record the start rules

Typical tasks:

- review agreement offer
- accept within deadline if proceeding
- record agreement start date
- record claim-by date and agreement end date
- record durability period
- lock the "do not start before" gate

Outputs:

- accepted agreement
- agreement dates
- work can start only after start date

### 5. Delivery

Purpose:

- do the work to specification and collect evidence as it happens

Typical tasks:

- schedule work after agreement start date
- brief contractors or farm workers on agreement requirements
- capture during-work photos where needed
- keep invoices and receipts
- keep timesheets for own labour where relevant
- record measurements and completed specifications
- record unexpected changes

Outputs:

- completed work records
- invoices/receipts/timesheets
- during-work evidence
- updated budget actuals

### 6. Claim

Purpose:

- submit payment claim after work is complete and invoiced/charged

Typical tasks:

- capture after-work photos from same positions as before photos where required
- label photos correctly
- assemble invoices, receipts, permissions, maps, and measurements
- check minimum claim and part-claim rules
- submit claim through Rural Payments service
- record claim reference and date

Outputs:

- claim pack
- submitted claim record
- expected payment status

### 7. Payment and variance review

Purpose:

- compare estimate, claim, and actual payment
- improve future estimates

Typical tasks:

- record actual grant payment
- record actual cash costs
- record internal labour and machinery cost
- explain variance
- record what went better and worse than planned
- capture lesson for next time

Outputs:

- reviewed budget
- local cost knowledge

### 8. Durability and maintenance

Purpose:

- keep the funded item compliant after payment

Typical tasks:

- schedule inspections
- capture maintenance photos/notes
- record repairs
- keep records for the required period
- flag changes in circumstances

Outputs:

- maintenance trail
- audit-ready record

## Gate states

Every grant job should expose clear gates:

- `exploring`
- `application_ready`
- `submitted`
- `agreement_offered`
- `agreement_accepted`
- `work_allowed`
- `work_complete`
- `claim_ready`
- `claim_submitted`
- `paid`
- `reviewed`
- `maintenance`
- `dropped`

The most important safety gate is:

> `work_allowed` is false until an agreement has been accepted and the start date
> has arrived.

## Task phase names

Use these phase names in work packages:

- `explore`
- `pre_application`
- `application`
- `agreement`
- `delivery`
- `claim`
- `payment_review`
- `maintenance`

These are deliberately broader than any single scheme, so RegenOS can support
government grants, private funding, water company schemes, and nature markets.

## Evidence pack outputs

RegenOS should be able to generate:

- application pack
- agreement pack
- delivery evidence pack
- claim pack
- maintenance/audit pack
- variance review

Each pack should include source links, dates, assumptions, and missing items.
