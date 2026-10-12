# American-Riviera-Bike

Static site for **American Riviera Bike Tours and Rentals** (Santa Barbara, CA).

The marketing pages are a static rebuild of the WordPress site at
<https://biketoursofsb.com>; the booking list is a static rebuild of the Rezgo
catalog at <https://riviera.rezgo.com>. Everything is plain HTML, CSS and a
little JavaScript, with fonts, images and libraries served from `assets/`.

## Pages

| URL | File | What it is |
| --- | --- | --- |
| `/` | `index.html` | Home: hero, reviews, guide, tours, sights, rental pricing, fleet, FAQ, location |
| `/our-story/` | `our-story/index.html` | About Mike and the company |
| `/faq/` | `faq/index.html` | Frequently asked questions |
| `/contact-us/` | `contact-us/index.html` | Phone, address, hours and map |
| `/book.html` | `book.html` | Tour and rental catalog (10 items) linking to the Rezgo booking engine |
| `/terms.html` | `terms.html` | Booking terms |

The paths of the first four match the WordPress site, so existing links and
search results keep working when the domain is pointed here.

## Structure

```
index.html, book.html, terms.html
our-story/  faq/  contact-us/        one index.html each
assets/
  css/   chrome.css   header, footer, mobile bar, fonts and colour tokens (all pages)
         site.css     page styles for the marketing pages
         bootstrap.min.css, fontawesome.min.css, fonts.css, rezgo.css   booking pages only
  js/    site.js      mobile menu and compact header on scroll
         jquery.min.js, bootstrap.bundle.min.js                          booking pages only
  img/   site/        logo, favicons, hero, guide photos, sights/
         tours/       10 tour and rental photos
  fonts/ Montserrat, Poppins (marketing pages); Kumbh Sans, Lato (booking pages)
  webfonts/ Font Awesome Free
```

The header and footer markup is repeated in every page. When changing one,
change it in all six files.

## Things that still depend on other services

- **Booking**: **Book Now** and **Reserve** buttons for a specific tour or bike,
  and the Gift Card link, go to the live Rezgo booking engine
  (`https://riviera.rezgo.com/...`). General "Book Now" buttons go to `book.html`.
- **Reviews**: the home page embeds the Trustindex Google-reviews widget, which
  loads its stylesheet and script from `cdn.trustindex.io`.
- **Maps**: Google Maps embeds on the home and contact pages.
- **Not rebuilt yet**: the footer "Resources" links and the home page's
  "View Self-Guided Route" button still point to pages on the WordPress site
  (`/choosing-a-bike-...`, `/how-to-get-the-most-...`, `/ways-to-tour-...`).
  The WordPress `/available-bikes/` page is replaced by the fleet section of the
  home page. The WordPress contact form is not included.
- The "Load more items" button on `book.html` is inert (there is one page of items).

## Deploy

Every push to `main` uploads the site to SiteGround over SFTP
(`.github/workflows/deploy.yml`). It needs two repository **Actions** secrets:
`SFTP_KEY` and `SFTP_KEY_PASSPHRASE`.

## Run locally

Serve the folder (the pretty URLs need a server):

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```
