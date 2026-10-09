"""
Social Security claiming-age data: full retirement age (FRA) by birth year, and the
official reduction/credit formulas used to compute benefit percentage at any claiming age.

Sourced 2026-08-23 from SSA's own planner pages:
  - FRA table: ssa.gov/benefits/retirement/planner/ageincrease.html
  - Early claiming reduction: ssa.gov/benefits/retirement/planner/agereduction.html
    (5/9 of 1% per month for the first 36 months before FRA, 5/12 of 1% per month for
    any additional months beyond that)
  - Delayed retirement credit: ssa.gov/benefits/retirement/planner/delayret.html
    (2/3 of 1% per month, i.e. 8%/year, from FRA up to age 70; applies to anyone born
    1943 or later)

These are fixed federal formulas (Social Security Amendments of 1983 + later law), not
figures that vary by news cycle - there is exactly one authoritative source and it hasn't
changed in decades, unlike krcalctools' bonus-calculator situation (see
feedback-programmatic-seo-data-quality memory). The one SSA figure that DOES change every
year (COLA) is deliberately NOT included here - the 2027 COLA isn't announced until
2026-10-14, and this site launches without a COLA page rather than publish projections as
if they were official (see note in generate.py).

Never hardcode a person's actual dollar benefit - the calculator always takes the user's
own estimated FRA benefit as input (they look it up at ssa.gov/myaccount) and computes
everything else from these percentages.
"""

# Full retirement age by birth year, in total months (e.g. 66 years 8 months = 800).
# Anyone born in a given year uses that year's FRA regardless of birth month, EXCEPT
# SSA's own rule that people born on January 1 use the PRIOR year's FRA (noted in the FAQ).
FRA_MONTHS = {
    1943: 66 * 12, 1944: 66 * 12, 1945: 66 * 12, 1946: 66 * 12, 1947: 66 * 12,
    1948: 66 * 12, 1949: 66 * 12, 1950: 66 * 12, 1951: 66 * 12, 1952: 66 * 12,
    1953: 66 * 12, 1954: 66 * 12,
    1955: 66 * 12 + 2,
    1956: 66 * 12 + 4,
    1957: 66 * 12 + 6,
    1958: 66 * 12 + 8,
    1959: 66 * 12 + 10,
}
FRA_MONTHS_1960_PLUS = 67 * 12

# One page per DISTINCT full retirement age, not per birth year.
#
# The 1960-and-later page was already combined on this reasoning. The same logic applies at the
# other end and was missed: 1943 through 1954 all share an FRA of exactly 66, so those twelve pages
# were identical apart from the year in the heading - same percentage table, same FAQ answers, same
# everything. That is the pattern AdSense rejected uspaycheckcalc for, so they are now one page.
#
# 1955-1959 stay individual because each really does have its own FRA (66 and 2 months through
# 66 and 10 months).
YEARS_FRA_66 = list(range(1943, 1955))
DETAIL_YEARS = ["1943-1954", 1955, 1956, 1957, 1958, 1959, "1960plus"]

EARLY_RATE_FIRST_36 = 5 / 9    # % per month, first 36 months before FRA
EARLY_RATE_BEYOND_36 = 5 / 12  # % per month, beyond 36 months before FRA
DELAYED_RATE = 2 / 3           # % per month, FRA to age 70
MAX_CLAIM_MONTHS = 70 * 12
MIN_CLAIM_MONTHS = 62 * 12

SOURCE_FRA = ("Social Security Administration", "https://www.ssa.gov/benefits/retirement/planner/ageincrease.html")
SOURCE_REDUCTION = ("Social Security Administration", "https://www.ssa.gov/benefits/retirement/planner/agereduction.html")
SOURCE_DELAYED = ("Social Security Administration", "https://www.ssa.gov/benefits/retirement/planner/delayret.html")


def fra_months_for_year(year):
    if year == "1960plus":
        return FRA_MONTHS_1960_PLUS
    if year == "1943-1954":
        return FRA_MONTHS[1943]
    return FRA_MONTHS.get(year, FRA_MONTHS_1960_PLUS)


def fra_label(year):
    months = fra_months_for_year(year)
    y, m = divmod(months, 12)
    return f"{y}" if m == 0 else f"{y} and {m} months"


def year_label(year):
    if year == "1960plus":
        return "1960 or later"
    if year == "1943-1954":
        return "1943-1954"
    return str(year)


def year_phrase(year):
    """How to refer to the cohort in a sentence ('someone born ...')."""
    if year == "1960plus":
        return "born in 1960 or later"
    if year == "1943-1954":
        return "born between 1943 and 1954"
    return f"born in {year}"


def pct_of_pia(claim_months, fra_months):
    """Benefit as a percentage of the full (FRA) benefit, for a given claiming age in months."""
    if claim_months < fra_months:
        early = fra_months - claim_months
        first = min(early, 36)
        rest = early - first
        reduction = first * EARLY_RATE_FIRST_36 + rest * EARLY_RATE_BEYOND_36
        return 100 - reduction
    if claim_months > fra_months:
        late = min(claim_months, MAX_CLAIM_MONTHS) - fra_months
        return 100 + late * DELAYED_RATE
    return 100.0


def fmt_pct(pct):
    s = f"{pct:.1f}"
    return s[:-2] if s.endswith(".0") else s
