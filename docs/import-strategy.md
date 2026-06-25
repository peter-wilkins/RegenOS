# Farm data import strategy

Many farms already have useful data in farm management systems, machinery platforms, spreadsheets, PDFs, and adviser reports.

RegenOS should not require farmers to recreate everything from scratch.

But it should also not depend on perfect integrations with every proprietary platform.

## Likely systems farmers may already use

Common UK and international farm software/platforms include:

- Gatekeeper
- Omnia
- John Deere Operations Center
- Trimble Ag Software
- AgriWebb
- Fieldmargin
- Muddy Boots / Greenlight Grower Management
- machinery display exports
- agronomist/adviser systems
- spreadsheets
- PDF soil reports

The exact mix varies heavily by farm type, adviser, country, and machinery brand.

## Import principle

Support messy, partial imports.

The user should be able to upload whatever they have and RegenOS should extract what it can, show a review screen, and let the user correct it.

Do not require a perfect export format before the product is useful.

## Import priority order

### 1. Manual draw/edit

Always support drawing boundaries and features manually.

This is the fallback that keeps the product usable for everyone.

### 2. Common spatial formats

Support these early:

- GeoJSON
- Shapefile ZIP
- KML/KMZ
- GPX where useful
- CSV with coordinates

These are the most realistic generic formats for boundaries, tracks, points, and field features.

### 3. Spreadsheet imports

Support CSV/XLSX imports for:

- field names
- crop history
- soil test results
- field areas
- notes
- sample locations if coordinates exist

### 4. PDF/report extraction

Many soil reports and adviser reports arrive as PDFs.

The MVP should not promise perfect extraction, but should support assisted import:

- upload PDF
- extract tables/text where possible
- show review screen
- map fields/samples manually if needed

### 5. Platform-specific importers

Add importers for common systems only after seeing real export files.

Potential first targets:

- Gatekeeper
- John Deere Operations Center
- Omnia
- Fieldmargin

Avoid guessing proprietary formats without samples.

### 6. API integrations

APIs are useful later, but should not block the MVP.

Most proprietary agricultural systems will vary by permissions, region, subscription, and data access terms.

## Canonical internal model

Every importer should convert into the same internal model.

Do not let proprietary source formats leak into the core domain.

Minimum imported objects:

- holding/farm
- field/parcel
- boundary geometry
- field name/reference
- crop history
- soil sample
- soil test result
- operation/application record
- yield/production layer if available
- note/observation
- uploaded source file

## Import review workflow

Every import should be treated as provisional until reviewed.

Suggested flow:

1. User uploads file or connects source.
2. RegenOS identifies possible data types.
3. RegenOS previews extracted fields/parcels/samples.
4. User maps columns and resolves duplicates.
5. User confirms coordinate system if needed.
6. User accepts import.
7. Imported data is stored with source/provenance.

## Provenance

Every imported object should remember where it came from.

Fields:

- source type
- source filename or platform
- import timestamp
- imported by
- original identifier
- confidence score
- transformation notes

This matters because farm data will be messy and sometimes wrong.

## Coordinate systems

Expect pain here.

Imports may use:

- WGS84 latitude/longitude
- British National Grid
- local machinery coordinate systems
- shapefile projection files
- missing/incorrect CRS metadata

The import wizard must make coordinate system issues visible and correctable.

## RPA / government field data

In the UK, official land parcel and rural payments data may be very useful where the farmer can access/export it.

RegenOS should eventually support importing official parcel boundaries where legally and practically possible.

But the MVP should not depend on direct government integration.

## AI-assisted import

A strong future feature:

> Upload everything you have.

RegenOS then attempts to recognise:

- field boundaries
- field names
- soil tests
- crop history
- yield maps
- wet areas
- constraints
- possible restoration opportunities

The user reviews and approves rather than entering everything manually.

## Importer architecture

```text
Uploaded source file / connected platform
        |
        v
Source-specific parser
        |
        v
Staging objects
        |
        v
Review and mapping UI
        |
        v
Canonical RegenOS model
        |
        v
Project planning and suitability engine
```

## Suggested first import implementation

Build these first:

1. GeoJSON field boundary import.
2. Shapefile ZIP field boundary import.
3. KML/KMZ boundary import.
4. CSV field list import.
5. Soil test CSV import.
6. Manual draw/edit fallback.

Then gather real Gatekeeper, Omnia, Fieldmargin, and John Deere exports from friendly farms before writing specific importers.
