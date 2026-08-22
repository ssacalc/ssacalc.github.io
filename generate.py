"""
Generates all pages for the Social Security Calculator site:
  - index.html                              hub: live JS claiming-age + breakeven calculator
  - {year}-full-retirement-age.html         per-birth-year FRA detail page (1943-1959)
  - 1960-and-later-full-retirement-age.html combined page (FRA is flat at 67 from here on)

All percentages come from SSA's own reduction/credit formulas (see ssa_data.py) - never a
guessed or asserted dollar figure. The live calculator takes the visitor's own estimated
FRA benefit as input and computes the rest client-side; nothing is sent to a server.

Deliberately NOT included in this v1: a COLA page. The 2027 COLA isn't announced until
2026-10-14 (SSA press release), so a page today would be almost entirely "estimates, check
back in October" - thin compared to the FRA content, which is fixed law. Add it once the
real number is out (see usstatewages-minimum-wage-site memory for the same phasing choice
made on that site).
"""
import os

from ssa_data import (
    DETAIL_YEARS, fra_months_for_year, fra_label, year_label, pct_of_pia, fmt_pct,
    SOURCE_FRA, SOURCE_REDUCTION, SOURCE_DELAYED,
)
from static_pages import about_html, privacy_html, contact_html, SITE_NAME, page_shell

OUTPUT_DIR = "docs"
BASE_URL = "https://ssacalc.github.io"

DISPLAY_AGES = [62, 63, 64, 65, 66, 67, 68, 69, 70]
DROPDOWN_YEARS = list(range(1943, 2009))

DISCLAIMER = """
  <div class="disclaimer">
    * This site provides general information for planning purposes only, based on Social
    Security Administration formulas that apply to most retired-worker benefits. It is not
    personalized financial, legal, or tax advice, and doesn't account for spousal/survivor
    benefits, continued work while claiming, taxation of benefits, or other individual
    circumstances. Confirm your actual benefit estimate at
    <a href="https://www.ssa.gov/myaccount" target="_blank" rel="noopener">ssa.gov/myaccount</a>
    and consider talking to a licensed financial advisor before deciding when to claim.
  </div>
"""


def detail_slug(year):
    if year == "1960plus":
        return "1960-and-later-full-retirement-age.html"
    return f"{year}-full-retirement-age.html"


def pct_table_html(fra_months):
    rows = []
    for age in DISPLAY_AGES:
        months = age * 12
        pct = pct_of_pia(months, fra_months)
        is_fra = months == fra_months
        cls = ' class="fra-row"' if is_fra else ""
        badge = ' <span class="badge fra">FRA</span>' if is_fra else ""
        rows.append(f'<tr{cls}><td>{age}{badge}</td><td class="num">{fmt_pct(pct)}% of full benefit</td></tr>')
    return f"""<table>
    <tr><th>Claiming age</th><th>Benefit</th></tr>
    {"".join(rows)}
  </table>"""


CALCULATOR_JS = """
<script>
function fraMonthsJS(year) {
  const table = {1943:792,1944:792,1945:792,1946:792,1947:792,1948:792,1949:792,1950:792,
    1951:792,1952:792,1953:792,1954:792,1955:794,1956:796,1957:798,1958:800,1959:802};
  return year >= 1960 ? 804 : (table[year] || 792);
}
function fraLabelJS(year) {
  const m = fraMonthsJS(year), y = Math.floor(m/12), mm = m%12;
  return mm === 0 ? String(y) : `${y} and ${mm} months`;
}
function pctOfPiaJS(claimMonths, fraM) {
  if (claimMonths < fraM) {
    const early = fraM - claimMonths, first = Math.min(early, 36), rest = early - first;
    return 100 - (first*(5/9) + rest*(5/12));
  } else if (claimMonths > fraM) {
    const late = Math.min(claimMonths, 840) - fraM;
    return 100 + late*(2/3);
  }
  return 100;
}
function fmtPctJS(p) {
  return p.toFixed(1).replace(/\\.0$/, '');
}
function onBenefitInput() {
  const el = document.getElementById('fraBenefit');
  const cursorFromEnd = el.value.length - el.selectionStart;
  const digits = el.value.replace(/[^0-9]/g, '');
  el.value = digits === '' ? '' : parseInt(digits, 10).toLocaleString('en-US');
  const pos = Math.max(el.value.length - cursorFromEnd, 0);
  el.setSelectionRange(pos, pos);
}
function breakevenAge(a, b) {
  for (let m = b.months; m <= 100*12; m++) {
    if (b.monthly*(m - b.months) >= a.monthly*(m - a.months)) return Math.round(m/12);
  }
  return null;
}
function calculate() {
  const yearEl = document.getElementById('birthYear');
  const benefitEl = document.getElementById('fraBenefit');
  const year = parseInt(yearEl.value, 10);
  const benefit = parseFloat((benefitEl.value || '').replace(/,/g, ''));
  if (!year || !benefit || benefit <= 0) {
    alert('Enter your birth year and your estimated benefit at full retirement age.');
    return;
  }
  const fraM = fraMonthsJS(year);
  let rows = '';
  [62,63,64,65,66,67,68,69,70].forEach(age => {
    const months = age*12;
    const pct = pctOfPiaJS(months, fraM);
    const amount = benefit * pct / 100;
    const isFra = months === fraM;
    rows += `<tr${isFra ? ' class="fra-row"' : ''}><td>${age}${isFra ? ' <span class="badge fra">FRA</span>' : ''}</td>` +
      `<td class="num">$${amount.toLocaleString('en-US',{maximumFractionDigits:0})}/mo</td>` +
      `<td class="num">${fmtPctJS(pct)}%</td></tr>`;
  });
  document.getElementById('resultTable').innerHTML = rows;

  const claims = [
    {label: 'Claim at 62', months: 62*12},
    {label: `Claim at FRA (${fraLabelJS(year)})`, months: fraM},
    {label: 'Claim at 70', months: 70*12},
  ];
  claims.forEach(c => c.monthly = benefit * pctOfPiaJS(c.months, fraM) / 100);

  let lines = '';
  [[claims[0],claims[1]], [claims[1],claims[2]], [claims[0],claims[2]]].forEach(([a,b]) => {
    if (a.months === b.months) return;
    const be = breakevenAge(a, b);
    lines += `<div class="breakeven-line"><b>${b.label}</b> passes <b>${a.label}</b> in lifetime total ` +
      (be ? `around age <b>${be}</b>.` : `only after age 100 (essentially never, at these amounts).`) +
      `</div>`;
  });
  document.getElementById('breakevenResult').innerHTML = lines;
  document.getElementById('calcResult').style.display = 'block';
}
window.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  const y = params.get('year');
  if (y) document.getElementById('birthYear').value = y;
});
</script>
"""


GROWTH_SVG = """
<svg viewBox="0 0 320 130" width="100%" height="110" role="img"
     aria-label="Three plants of increasing size, illustrating how your benefit grows the longer you wait to claim"
     style="display:block;margin:18px auto;max-width:320px">
  <line x1="20" y1="120" x2="300" y2="120" stroke="var(--border)" stroke-width="2"/>
  <path d="M50,120 L54,98 L76,98 L80,120 Z" fill="#c98a56"/>
  <line x1="65" y1="98" x2="65" y2="85" stroke="#8a5f3a" stroke-width="2"/>
  <circle cx="65" cy="80" r="11" fill="var(--primary)"/>
  <circle cx="57" cy="86" r="7" fill="#8b7ff0"/>
  <circle cx="73" cy="86" r="7" fill="#8b7ff0"/>
  <path d="M140,120 L145,98 L175,98 L180,120 Z" fill="#c98a56"/>
  <line x1="160" y1="98" x2="160" y2="68" stroke="#8a5f3a" stroke-width="2"/>
  <circle cx="160" cy="61" r="15" fill="var(--primary)"/>
  <circle cx="147" cy="70" r="9" fill="#8b7ff0"/>
  <circle cx="173" cy="70" r="9" fill="#8b7ff0"/>
  <circle cx="160" cy="48" r="8" fill="#8b7ff0"/>
  <path d="M230,120 L236,98 L274,98 L280,120 Z" fill="#c98a56"/>
  <line x1="255" y1="98" x2="255" y2="50" stroke="#8a5f3a" stroke-width="2"/>
  <circle cx="255" cy="42" r="18" fill="var(--primary)"/>
  <circle cx="238" cy="53" r="11" fill="#8b7ff0"/>
  <circle cx="272" cy="53" r="11" fill="#8b7ff0"/>
  <circle cx="255" cy="25" r="9" fill="#8b7ff0"/>
  <circle cx="255" cy="18" r="7" fill="#f5b942"/>
</svg>
"""


def index_html():
    year_options = "\n".join(f'<option value="{y}">{y}</option>' for y in DROPDOWN_YEARS)
    year_grid_items = "\n".join(
        f'<li><a href="{detail_slug(y)}">{year_label(y)}</a></li>' for y in DETAIL_YEARS
    )

    body = f"""
  <h1>Social Security Claiming Age Calculator</h1>
  <p>See how your monthly Social Security benefit changes depending on the age you claim it,
  and how long it takes for waiting to pay off in total dollars received. Uses the same
  reduction and delayed-credit formulas as SSA's own calculators.</p>
  {GROWTH_SVG}
  <div class="calc-card">
    <div class="calc-row">
      <div class="calc-field">
        <label for="birthYear">Your birth year</label>
        <select id="birthYear">
          <option value="">Select year</option>
          {year_options}
        </select>
      </div>
      <div class="calc-field">
        <label for="fraBenefit">Estimated benefit at full retirement age ($/month)</label>
        <input type="text" inputmode="numeric" id="fraBenefit" placeholder="e.g. 2,200" oninput="onBenefitInput()">
      </div>
    </div>
    <button class="calc-btn" onclick="calculate()">Calculate</button>

    <div class="calc-result" id="calcResult">
      <table>
        <tr><th>Claiming age</th><th>Monthly benefit</th><th>% of full benefit</th></tr>
        <tbody id="resultTable"></tbody>
      </table>
      <h2>When does waiting pay off?</h2>
      <div id="breakevenResult"></div>
    </div>
  </div>
  <p class="source">Don't know your estimated benefit? Look it up for free at
  <a href="https://www.ssa.gov/myaccount" target="_blank" rel="noopener">ssa.gov/myaccount</a>.
  Nothing you enter here is sent anywhere - the calculator runs entirely in your browser.</p>

  <div class="explain">
    <h2>How the age you claim changes your benefit</h2>
    <p>Every Social Security retirement benefit is built around one number: your benefit at
    <b>full retirement age (FRA)</b>, which is 66-67 depending on your birth year. Claim earlier
    (as early as 62) and your monthly benefit is permanently reduced; claim later (up to 70) and
    it's permanently increased.</p>
    <ul class="steps">
      <li><b>Claiming early:</b> reduced by 5/9 of 1% for each of the first 36 months before FRA,
      then 5/12 of 1% for each additional month - up to 30% less at 62 if your FRA is 67.</li>
      <li><b>Claiming late:</b> increased by 2/3 of 1% (8%/year) for each month you delay past
      FRA, up to age 70 - up to 24-32% more, depending on your FRA.</li>
    </ul>
  </div>

  <h2>Full retirement age by birth year</h2>
  <ul class="year-grid">
    {year_grid_items}
  </ul>

  <div class="faq">
    <h2>Frequently asked questions</h2>
    <details>
      <summary>What is full retirement age (FRA)?</summary>
      <p>The age at which you receive 100% of your calculated Social Security benefit - no
      reduction for claiming early, no bonus for delaying. It's 66 for anyone born 1943-1954,
      rises in two-month steps for people born 1955-1959, and is 67 for anyone born 1960 or
      later. If you were born on January 1, SSA has you use the previous year's FRA.</p>
    </details>
    <details>
      <summary>Is there any reason to claim before FRA?</summary>
      <p>Yes - health, immediate income need, or simply valuing money now over a larger amount
      later are all legitimate reasons people claim at 62. The reduction is permanent, but
      "permanent smaller check" isn't automatically the wrong choice for everyone.</p>
    </details>
    <details>
      <summary>What is a "breakeven age" and does it mean I should wait?</summary>
      <p>It's the age at which the larger checks from delaying have added up to more total
      dollars than claiming earlier would have paid by that same age. It's useful context, not
      a recommendation - it assumes you live past that age, ignores taxes and investment returns
      on the money you'd have received earlier, and says nothing about your own health or plans.</p>
    </details>
    <details>
      <summary>Does this affect spousal or survivor benefits?</summary>
      <p>This calculator covers your own retired-worker benefit only. Spousal and survivor
      benefits use related but different rules - see SSA's
      <a href="https://www.ssa.gov/benefits/retirement/planner/applying7.html" target="_blank" rel="noopener">benefits planner</a>
      for those.</p>
    </details>
  </div>
{DISCLAIMER}
"""
    return page_shell(
        f"{SITE_NAME} - When Should You Claim Social Security?",
        "Calculate your Social Security monthly benefit at every claiming age from 62 to 70, and see the breakeven age where delaying pays off, using SSA's own official formulas.",
        body,
        extra_head=CALCULATOR_JS,
    )


def year_detail_html(year):
    fra_m = fra_months_for_year(year)
    label = year_label(year)
    fra = fra_label(year)
    who = f"born in {year}" if year != "1960plus" else "born in 1960 or later"

    headline = f"""
  <div class="headline">
    <div>Full retirement age for someone {who}</div>
    <div class="amount">{fra}</div>
  </div>"""

    faq = f"""
  <div class="faq">
    <h2>Frequently asked questions</h2>
    <details>
      <summary>What is the full retirement age for someone {who}?</summary>
      <p>{fra}. At that age, you receive 100% of your calculated benefit - no early-claiming
      reduction, no delayed-retirement credit.</p>
    </details>
    <details>
      <summary>What happens if I claim at 62?</summary>
      <p>Your benefit is permanently reduced to {fmt_pct(pct_of_pia(62*12, fra_m))}% of your full
      amount, since 62 is the earliest age Social Security retirement benefits can start.</p>
    </details>
    <details>
      <summary>What happens if I delay past my full retirement age?</summary>
      <p>Your benefit increases by 2/3 of 1% (8%/year) for every month you wait past
      {fra}, up to age 70 - reaching {fmt_pct(pct_of_pia(70*12, fra_m))}% of your full amount if
      you wait all the way to 70. There's no benefit to delaying past 70.</p>
    </details>
    <details>
      <summary>Where do I find my actual benefit amount?</summary>
      <p>This page shows percentages of your full benefit, not a dollar figure - your actual
      full-retirement-age benefit depends on your own earnings history. Look it up for free at
      <a href="https://www.ssa.gov/myaccount" target="_blank" rel="noopener">ssa.gov/myaccount</a>,
      then use the <a href="index.html?year={1960 if year == '1960plus' else year}">calculator</a> to
      see your actual dollar amounts at every claiming age.</p>
    </details>
  </div>"""

    body = f"""
  <h1>Full Retirement Age for {label}</h1>
  {headline}

  <div class="explain">
    <h2>Your benefit at every claiming age</h2>
    <p>Shown as a percentage of your full (FRA) benefit - enter your own estimated dollar amount
    in the <a href="index.html?year={1960 if year == '1960plus' else year}">calculator</a> to see
    real dollar figures.</p>
  </div>
  {pct_table_html(fra_m)}

  <p class="source">Sources:
    <a href="{SOURCE_FRA[1]}" target="_blank" rel="noopener">{SOURCE_FRA[0]} - full retirement age</a>,
    <a href="{SOURCE_REDUCTION[1]}" target="_blank" rel="noopener">early claiming reduction</a>,
    <a href="{SOURCE_DELAYED[1]}" target="_blank" rel="noopener">delayed retirement credits</a>.
  </p>
  {faq}

  <div class="nav"><a href="index.html">&larr; Back to calculator</a></div>
{DISCLAIMER}
"""
    title = f"Full Retirement Age for {label}: {fra} | {SITE_NAME}"
    desc = f"Full Social Security retirement age for someone {who} is {fra}. See your benefit percentage at every claiming age from 62 to 70."
    return page_shell(title, desc, body)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    valid_filenames = {"index.html", "about.html", "privacy.html", "contact.html", "sitemap.xml", "ads.txt"}
    for year in DETAIL_YEARS:
        valid_filenames.add(detail_slug(year))
    for fname in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, fname)
        if os.path.isfile(path) and fname.endswith(".html") and fname not in valid_filenames:
            os.remove(path)

    urls = []

    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html())
    urls.append(f"{BASE_URL}/index.html")

    for year in DETAIL_YEARS:
        with open(os.path.join(OUTPUT_DIR, detail_slug(year)), "w", encoding="utf-8") as f:
            f.write(year_detail_html(year))
        urls.append(f"{BASE_URL}/{detail_slug(year)}")

    static_files = {"about.html": about_html(), "privacy.html": privacy_html(), "contact.html": contact_html()}
    for filename, html in static_files.items():
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(html)
        urls.append(f"{BASE_URL}/{filename}")

    print(f"Generated {len(urls)} pages -> {OUTPUT_DIR}/")
    return urls


if __name__ == "__main__":
    main()
