# Open questions

## Product

- Is RegenOS mainly for farmers, advisers, contractors, or funders first?
- Is the first commercial wedge grant evidence, water restoration planning, or JobDone integration?
- Should the first project be UK-focused or deliberately country-neutral?
- Is the first user a farmer doing work, or an adviser designing work for farmers?

## JobDone

- Does JobDone own tasks, or does RegenOS own restoration-domain tasks?
- What is the minimum task schema needed for evidence capture?
- Does JobDone already support GPS, photos, attachments, and completion criteria?
- How should offline field use work?

## Grants and funding

- Should funding rules be hand-curated first?
- Can guidance documents be transformed into structured rules safely?
- How do we represent uncertainty in eligibility?
- How do we prevent users assuming approval is guaranteed?
- How do we track version changes in scheme rules?

## GIS and suitability

- What layers are available freely in the UK?
- What layers are available globally?
- Should the first suitability engine use raster scoring, vector rules, or both?
- How much should be automated before a human adviser must approve?

## Evidence

- Should evidence files be immutable once used in a claim?
- Should every photo have location/time metadata?
- How do we handle missing or poor-quality evidence?
- How do we produce claim packs in formats funders actually accept?

## Technical stack

- Is the core system Clojure, Python, or both?
- Is PostGIS required from day one?
- Should templates live as YAML in git before moving into a database?
- Should RegenOS be API-first?
- Should work packages become an open interchange format?

## Business model

- Free/open-source core plus paid hosting?
- Consultancy/service business first?
- Contractor marketplace later?
- White-label tool for advisers?
- Paid evidence-pack generation?
