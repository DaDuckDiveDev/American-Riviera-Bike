# American-Riviera-Bike

Local static rebuild of the **American Riviera Bike Tours and Rentals** website,
originally hosted on Rezgo at <https://riviera.rezgo.com>.

This is a near 1:1 static reconstruction of the Rezgo booking site, rebuilt as
self-contained local files (no CDN or platform dependencies) for migration and
further development.

## Pages

- `index.html` — homepage with the full tour & rental catalog (10 items)
- `terms.html` — Booking Terms page

## Structure

```
index.html
terms.html
assets/
  css/   bootstrap.min.css, fontawesome.min.css, fonts.css, rezgo.css
  js/    jquery.min.js, bootstrap.bundle.min.js
  img/   rezgo-logo.svg, tours/*.jpg (10 tour/rental photos, 1280×720)
  fonts/ Kumbh Sans + Lato (woff2, weights 300/400/700)
  webfonts/ Font Awesome Free
```

## How it was built

- The original site renders its catalog inside a Rezgo `<iframe>`; that content
  has been inlined into a single standalone page.
- All third-party libraries are vendored locally: **Bootstrap 5.2.1**,
  **Font Awesome Free 6.4**, **jQuery 3.5.1**, and the **Kumbh Sans** + **Lato**
  web fonts. The Google Fonts `@import`s were removed from `rezgo.css` and are
  now served from `assets/fonts/`.
- Font Awesome **duotone** (`fad`) icons — a Pro-only feature on the original —
  were mapped to the Free **solid** equivalents so they render.
- The Rezgo theme stylesheet (`rezgo.css`) is vendored verbatim for fidelity.

## Notes / next steps

- Booking is server-side, so **Book Now**, **More details**, and **Gift Card**
  links point to the live Rezgo booking engine (`https://riviera.rezgo.com/...`).
  Re-point these when a replacement booking flow is in place.
- The "Load more items" button is inert (there is only one page of items).

## Run locally

Open `index.html` directly, or serve the folder:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```
