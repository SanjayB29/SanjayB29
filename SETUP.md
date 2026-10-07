# SanjayB29 animated profile setup

## 1. Create the profile repository

The repository must be named exactly `SanjayB29` and be public.

```bash
gh repo create SanjayB29 --public --clone
cd SanjayB29
```

If the repository already exists, clone it instead.

## 2. Copy these files

Keep the structure:

```text
SanjayB29/
├── README.md
├── contrib-heatmap.svg
├── info-card.svg
├── sanjay-ascii.svg
├── data/
│   └── contributions.json
├── scripts/
│   ├── requirements.txt
│   ├── prep_photo.py
│   ├── make_ascii_svg.py
│   ├── make_info_card.py
│   ├── fetch_contributions.py
│   └── render_heatmap_svg.py
└── .github/workflows/
    └── update-profile-art.yml
```

## 3. Generate the portrait

Install the full local requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
```

Put your photo at the repository root, then:

```bash
python scripts/prep_photo.py source-photo.jpg
python scripts/make_ascii_svg.py
python scripts/make_info_card.py
```

## 4. Generate the live graph

```bash
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
```

## 5. Preview

Open `README.md` on GitHub after pushing. SVG SMIL animations are contained inside the images, so no JavaScript is needed in the README.

## 6. Push

```bash
git add .
git commit -m "feat: add animated terminal profile"
git push -u origin main
```

Then go to GitHub → Actions → **Update profile art** → **Run workflow** once.

The workflow will subsequently refresh the graph daily.

## Important

The portrait is intentionally left for your own photo. Add `source-photo.jpg` locally; it is ignored by git and is only used to generate `sanjay-ascii.svg`.
