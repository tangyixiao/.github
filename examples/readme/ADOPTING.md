# Adopt this README

The [Chinese example](README.md) and [English example](README.en.md) implement the approved product-first README direction using GitHub's native headings, links, tables and small SVG images. They use OJ NEXUS as factual sample content; copying this directory does not turn another repository into that application.

## Replace before publishing

- Replace the name, logo, description and all repository, release, download, issue, roadmap, documentation and license URLs in both languages.
- Keep the receiving project's existing license and attribution. The example's product license badge and links describe OJ NEXUS, not every project adopting the template.
- Replace the illustrated hero with useful real screenshots when available. Until then, preserve the visible illustration label and alternative text. Document supported functionality and platform maturity rather than implying feature parity.
- Update the release table from actual published assets and notes. Version numbers here are a dated snapshot, not a promise that the current release is always this version.
- The four development cards show publication stages. Edit their SVG text and colors when a stage changes; no completion percentage or milestone count is inferred.
- Change the Shields repository and Star History `repos` query together. Neither embed contains a token. The public external services and GitHub's image proxy may cache results or fail; linked release, star and documentation pages remain ordinary usable links.
- If external chart services are unsuitable, replace the chart with a data-generated snapshot and state its observation/update date. Do not use the concept-art chart as statistics.
- Do not publish a full screenshot of this README as its only content. Keep text selectable and links useful.

## GitHub rendering

The logo is a separate image. Feature and stage cards are individual small SVGs in inline `picture` elements, so GitHub can wrap them at narrower widths. Dark sources follow the viewer's preferred color scheme. This is not a custom web layout; GitHub controls article width, table overflow, image proxying and typography.

Verify both README files in GitHub at desktop and phone widths. Check source selection, Chinese fonts, image loading, native download tables, keyboard links, external badges and Star History. A sanitized Markdown API response is useful but does not prove the browser loaded remote images.

## Rights and provenance

The OJ NEXUS hub-and-three-nodes logo follows [its Android vector source](https://github.com/tangyixiao/OJ-NEXUS/blob/main/app/src/main/res/drawable/ic_launcher_foreground.xml). Retain applicable Apache-2.0 and NOTICE obligations when copying that project asset. Original hero/card illustrations in this example are supplied under this repository's license; they contain platform names, not bundled official platform logo files.

[Star History](https://github.com/star-history/star-history) supplies the external chart using its documented public embed. [Shields](https://shields.io/) supplies the external badges. Their displayed images remain service-generated resources, not included source assets or a claim of affiliation.

## Check locally

Run `python -B scripts/check.py` from the repository root. It checks local references, generated website consistency and source budgets without an install. Validate external services and the actual GitHub presentation separately. Copying these Markdown files does not configure workflows, repository labels, Packages, releases or platform settings.
