# Health Calculator

Run `health.py` for an interactive and user-friendly health calculator. Includes computation for:

- Body Mass Index
- Body Adiposity Index
- Basal Metabolic Rate
- Fat Percent (Tape Measure)
- Fat Percent (Calipers)

User information is saved in `user.json`, which may be directly modified. Measurement units are:

- Weight: kg
- Height: cm
- Gender: boolean (m/f)
- Age: years
- Circumference: cm
- Skinfold calipers: mm

The contents of `user.json` must conform to the JSON schema specified in `schema.json`.
