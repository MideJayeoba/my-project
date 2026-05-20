# Phase 2 Offline PWA Conversion Plan

## 1) Frontend packaging and installability
- Add a production build pipeline for `interface/frontend/web` using Vite + `vite-plugin-pwa` (Workbox under the hood).
- Set `manifest.json` fields for Android installability: `name`, `short_name`, `display=standalone`, `theme_color`, `background_color`, icon set (`192`, `512`, maskable variants).
- Ensure all icons and splash assets are bundled in the static output so first-run install prompts work on low-end Android devices.

## 2) Service worker strategy (Workbox)
- Configure Workbox precache for immutable static assets (`index.html`, JS bundles, CSS, icons, fonts).
- Use runtime caching routes:
  - `NetworkFirst` for `/api/config`-style lightweight metadata endpoints.
  - `StaleWhileRevalidate` for non-critical shell assets.
  - `CacheFirst` for local audio cues/short UI effects.
- Add navigation fallback to app shell for client-side routing resilience.
- Version caches with explicit names (`voice-medai-shell-v1`, `voice-medai-runtime-v1`) and enforce cleanup of outdated caches during activate.

## 3) Offline data persistence (IndexedDB)
- Add IndexedDB store(s) for:
  - session metadata (`timestamp`, `duration`, `status`)
  - transcripts and guidance text logs for clinician audit (with explicit retention policy)
  - optional queued uploads for deferred sync workflows
- Use a thin data layer (Dexie or idb) to avoid ad-hoc IndexedDB calls.
- Encrypt sensitive local records at rest where feasible and provide periodic purge tooling for PHC admins.

## 4) Voice pipeline behavior offline
- Detect backend reachability from the client and switch UI state to offline mode icon when unavailable.
- Queue voice requests locally only if policy allows; otherwise provide immediate local audio prompt that clinician support is required.
- Keep the UI text-free while using icon/sound state transitions for accessibility.

## 5) FastAPI backend changes for fully offline-first first load
- Serve built frontend assets directly from FastAPI (`StaticFiles`) so one local service delivers both API and app shell.
- Add endpoint for service worker scope and cache-busting metadata (`/app-version`) to coordinate safe updates.
- Package ASR, quantized LLM GGUF, FAISS index, and TTS resources in local storage paths defined by `.env`.
- Add startup checks that verify model/index availability and emit a machine-readable readiness endpoint before accepting requests.
- Introduce optional local-only auth/session guard for multi-device PHC LAN usage without internet identity providers.

## 6) Validation checklist before field deployment
- Cold-start test with internet fully disabled.
- Confirm app install works on target Android versions used in Akure clinics.
- Measure first response latency and sustained throughput on clinic hardware.
- Verify retained session logs can be reviewed and purged by authorized staff.
- Run clinician walkthrough to validate that icon/audio-only UX remains understandable offline.
