"""
Static pages required for AdSense review (privacy policy / about / contact), plus shared
theme parts (style/header/footer/GA+AdSense snippet), mirroring the us-state-minimum-wage /
us-paycheck-calculator / krcalctools project structure (see site-deployment-handoff.md).

GA4 property "ssacalc" created under the same account as the other sites ("마자용"),
measurement ID G-75N1M00YPR. ADSENSE_CLIENT reuses the existing publisher account
(ca-pub- IDs are per-publisher, not per-site) - just add this as a new site in the
AdSense dashboard once it's live, no new registration needed.
"""

SITE_NAME = "Social Security Calculator"
CONTACT_EMAIL = "contact@yourdomain.com"

GA4_MEASUREMENT_ID = "G-75N1M00YPR"
ADSENSE_CLIENT = "ca-pub-5607384951754093"

GA_SNIPPET = f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA4_MEASUREMENT_ID}');
</script>
<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}"
     crossorigin="anonymous"></script>"""

FOOTER_NAV = """
  <div class="footer-nav">
    <a href="index.html">Home</a>
    <a href="about.html">About</a>
    <a href="privacy.html">Privacy Policy</a>
    <a href="contact.html">Contact</a>
  </div>
"""

FAVICON = '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 100 100%27%3E%3Ctext y=%27.9em%27 font-size=%2790%27%3E%F0%9F%A7%AE%3C/text%3E%3C/svg%3E">'

SITE_HEADER = """
  <header class="site-header">
    <a href="index.html" class="brand">\U0001F9EE Social Security Calculator</a>
    <nav class="site-nav">
      <a href="index.html">Calculator</a>
      <a href="about.html">About</a>
    </nav>
  </header>
"""

SITE_STYLE = """
  :root {
    --primary: #2563eb; --primary-dark: #1d4ed8; --bg: #f8f9fc; --card-bg: #ffffff;
    --text: #111827; --muted: #6b7280; --border: #e5e7eb;
    --warn-bg: #fff7ed; --warn-text: #9a3412;
    --good-bg: #dcfce7; --good-text: #166534;
  }
  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    max-width: 680px; margin: 0 auto; padding: 0 20px 60px; color: var(--text);
    line-height: 1.7; background: var(--bg);
  }
  a { color: var(--primary); }
  .site-header {
    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;
    gap: 10px; padding: 18px 0; border-bottom: 1px solid var(--border); margin-bottom: 28px;
  }
  .site-header .brand { font-weight: 800; font-size: 17px; color: var(--text); text-decoration: none; }
  .site-nav { display: flex; gap: 2px; flex-wrap: wrap; }
  .site-nav a { font-size: 13px; color: var(--muted); text-decoration: none; padding: 6px 10px; border-radius: 999px; }
  .site-nav a:hover { background: #eef2ff; color: var(--primary); }

  h1 { font-size: 23px; margin-bottom: 8px; }
  h2 { font-size: 16px; margin-top: 28px; }

  .headline {
    background: linear-gradient(135deg,#eef2ff,#f5f3ff); border-radius: 16px;
    padding: 26px; text-align: center; margin: 20px 0;
  }
  .headline .amount { font-size: 34px; font-weight: 800; color: var(--primary); }

  .badge { display: inline-block; font-size: 12px; font-weight: 700; padding: 3px 10px; border-radius: 999px; }
  .badge.fra { background: #eef2ff; color: var(--primary-dark); }
  .badge.best { background: var(--good-bg); color: var(--good-text); }

  table.rule, table { width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 13px; }
  table.rule th, table.rule td, table th, table td { border: 1px solid var(--border); padding: 9px 10px; text-align: left; }
  table.rule td.num, table td.num { text-align: right; }
  th { color: var(--muted); font-weight: 600; background: #fafafa; }
  tr.fra-row td { background: #eef2ff; font-weight: 700; }

  .source { font-size: 12px; color: var(--muted); }
  .source a { color: var(--muted); }
  .disclaimer {
    margin-top: 32px; padding: 14px 16px; background: #fafafa; border-radius: 10px;
    font-size: 12px; color: var(--muted); line-height: 1.6;
  }

  .explain { margin-top: 26px; font-size: 14px; color: #374151; }
  .explain h2 { font-size: 15px; }
  .steps { margin: 12px 0 0; padding-left: 20px; }
  .steps li { margin-bottom: 8px; }

  .calc-card {
    background: var(--card-bg); border: 1px solid var(--border); border-radius: 14px;
    padding: 20px; margin: 20px 0;
  }
  .calc-row { display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 12px; }
  .calc-field { flex: 1; min-width: 160px; }
  .calc-field label { display: block; font-size: 12px; color: var(--muted); margin-bottom: 4px; font-weight: 600; }
  .calc-field select, .calc-field input {
    width: 100%; padding: 9px 10px; border: 1px solid var(--border); border-radius: 8px;
    font-size: 14px; background: #fff; color: var(--text);
  }
  .calc-btn {
    background: var(--primary); color: #fff; border: none; border-radius: 8px;
    padding: 10px 18px; font-size: 14px; font-weight: 700; cursor: pointer; width: 100%;
  }
  .calc-btn:hover { background: var(--primary-dark); }
  .calc-result { margin-top: 18px; display: none; }
  .breakeven-line { padding: 10px 12px; background: #f5f3ff; border-radius: 8px; font-size: 13px; margin-bottom: 8px; }

  .faq { margin-top: 26px; }
  .faq h2 { font-size: 15px; margin-bottom: 10px; }
  .faq details {
    border: 1px solid var(--border); border-radius: 10px; padding: 12px 16px;
    margin-bottom: 8px; background: var(--card-bg);
  }
  .faq summary { cursor: pointer; font-weight: 600; font-size: 14px; }
  .faq details p { margin: 10px 0 0; font-size: 13px; color: #374151; line-height: 1.6; }

  .nav { margin-top: 24px; font-size: 14px; }
  .nav a { text-decoration: none; }

  .year-grid { list-style: none; padding: 0; margin: 18px 0; display: grid; gap: 8px; grid-template-columns: repeat(auto-fill, minmax(90px, 1fr)); }
  .year-grid li a {
    display: block; padding: 10px 8px; background: var(--card-bg); border: 1px solid var(--border);
    border-radius: 10px; text-decoration: none; color: var(--text); font-size: 13px; text-align: center;
  }
  .year-grid li a:hover { border-color: var(--primary); color: var(--primary); }

  .footer-nav {
    margin-top: 40px; padding-top: 18px; border-top: 1px solid var(--border);
    font-size: 13px; color: var(--muted); display: flex; flex-wrap: wrap; gap: 4px 14px;
  }
  .footer-nav a { color: var(--muted); text-decoration: none; }
  .footer-nav a:hover { color: var(--primary); }
"""


def page_shell(title, description, body, extra_head=""):
    return f"""<!doctype html>
<html lang="en">
<head>
{GA_SNIPPET}
<meta charset="utf-8">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="viewport" content="width=device-width, initial-scale=1">
{FAVICON}
{extra_head}
<style>{SITE_STYLE}</style>
</head>
<body>
{SITE_HEADER}
{body}
{FOOTER_NAV}
</body>
</html>"""


def about_html():
    return page_shell(
        f"About - {SITE_NAME}",
        f"{SITE_NAME} helps you see how your Social Security retirement benefit changes depending on the age you claim it.",
        f"""
  <h1>About This Site</h1>
  <p>{SITE_NAME} shows how much your Social Security retirement benefit changes depending on
  when you claim it, using the Social Security Administration's own reduction and delayed-credit
  formulas - and how long it takes for delaying to "catch up" in total dollars received.</p>

  <h2>Where the numbers come from</h2>
  <p>Full retirement age (FRA) and the benefit percentages shown here come directly from
  SSA's published formulas: a 5/9 of 1% monthly reduction for the first 36 months you claim
  before FRA, 5/12 of 1% per month beyond that, and a 2/3 of 1% monthly credit (8%/year) for
  delaying past FRA up to age 70. These are fixed federal rules, not estimates - see each
  page's source link.</p>

  <h2>What this site doesn't do</h2>
  <p>This site never guesses your actual benefit amount. The calculator asks for your own
  estimated benefit at full retirement age, which you can look up for free at
  <a href="https://www.ssa.gov/myaccount" target="_blank" rel="noopener">ssa.gov/myaccount</a>,
  and computes everything else from that. It also doesn't tell you the "right" age to claim -
  that depends on your health, other income, and family situation. It shows you the math so
  you can make that call yourself, ideally alongside a licensed financial advisor.</p>
""",
    )


def privacy_html():
    return page_shell(
        f"Privacy Policy - {SITE_NAME}",
        f"Privacy policy for {SITE_NAME}.",
        f"""
  <h1>Privacy Policy</h1>
  <p>{SITE_NAME} ("the site") respects your privacy. This policy explains what information is
  collected when you visit.</p>

  <h2>1. Information We Collect</h2>
  <p>This site has no account system or login. The retirement calculator runs entirely in your
  browser - the birth year and benefit amount you enter are never sent to or stored on any
  server. Third-party services such as Google AdSense and Google Analytics may automatically
  collect cookie-based data (pages visited, device type, approximate location) for advertising
  and analytics purposes.</p>

  <h2>2. Cookies</h2>
  <p>This site uses cookies served by Google and its partners to serve ads. You can opt out of
  personalized advertising via <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google Ads Settings</a>,
  or block cookies entirely in your browser settings.</p>

  <h2>3. Third-Party Advertising</h2>
  <p>This site displays ads served by Google AdSense. Google may use cookies to serve ads based on
  your prior visits to this or other websites. See Google's advertising policies for details.</p>

  <h2>4. Contact</h2>
  <p>Questions about this privacy policy can be sent to <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>

  <h2>5. Effective Date</h2>
  <p>This policy is effective as of August 23, 2026.</p>
""",
    )


def contact_html():
    return page_shell(
        f"Contact - {SITE_NAME}",
        f"Contact page for {SITE_NAME}.",
        f"""
  <h1>Contact</h1>
  <p>Questions, corrections, or advertising/partnership inquiries can be sent to the email below.</p>
  <p><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
""",
    )
