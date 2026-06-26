# Offline Field Notebook MVP

## Job

Peter walks the farm and ground-truths candidate water places.

The app must let him capture:

- current location
- field name, if known
- note
- photo
- simple observation type
- timestamp

It must keep working with poor or no mobile signal.

## Product shape

This is an offline-first web app, not a full native app at first.

The first app should:

1. load the farm field dataset while online
2. cache the app shell and field geometry
3. show the water-walk candidates
4. capture observations locally
5. keep a local outbox of unsynced observations
6. export a JSON bundle for RegenOS or JobDone

## Important constraint

Browser access to location, camera, and service workers needs a secure context.

For the first test we should use one of:

- HTTPS private workbench / Tailscale HTTPS route
- a small native shell that hosts the web app in a WebView and provides device
  capabilities
- localhost during laptop testing

Do not rely on plain HTTP on a phone for the real field test.

## Offline map decision

Do not make online map tiles critical for the first field test.

The app should work even if the background map is unavailable:

- field boundaries from KML are cached locally
- candidate fields are listed and tappable
- GPS coordinates are captured
- observations can be saved without a tile layer

Cached tiles or OS map overlays are useful later, but they are not the first
proof.

## Observation record

Start with a small durable record:

```json
{
  "schemaVersion": "regenos.fieldObservation.v1",
  "id": "local-generated-id",
  "projectId": "dewlish-water-walk",
  "createdAt": "2026-06-26T12:00:00Z",
  "location": {
    "latitude": 50.0,
    "longitude": -2.0,
    "accuracyMetres": 12
  },
  "fieldName": "River",
  "observationType": "wet_ground",
  "note": "Standing water near lower corner after rain.",
  "photoIds": ["local-photo-id"],
  "syncStatus": "local_only"
}
```

Photos should live in IndexedDB as blobs, with metadata in the observation
record. Avoid base64 inside JSON except for manual export/debug.

## First UI

Keep the first UI boring:

- top: current field / GPS status
- main: cached field map or candidate list
- one primary button: `Add observation`
- capture flow: photo, note, save
- export button hidden in a simple menu

This is a field tool, not a dashboard.

## Later sync

Later, observations can sync to:

- a local RegenOS folder
- JobDone as evidence
- a RegenOS backend
- a share pack for an adviser or funder

The first version only needs reliable local capture and export.
