"""
Written guides for the Social Security calculator site.

The calculator answers one question - how much your benefit changes with claiming age. These cover
the decisions that sit around that number and that no percentage table can answer: what happens if
you keep working, what a spouse or survivor is entitled to, how much of the benefit is taxed, and
what you can undo after the fact.

Editorial rule: the dollar thresholds quoted here are the ones fixed in statute and NOT indexed to
inflation (the provisional-income thresholds, unchanged since 1983 and 1993). Anything the SSA
re-sets annually - the earnings test limits, the taxable maximum, the COLA - is described rather
than quoted, with a link to the SSA page that carries the current figure.

Each guide is a dict: slug, title, description (meta), body (HTML fragment).
"""

SSA_EARNINGS_TEST = "https://www.ssa.gov/benefits/retirement/planner/whileworking.html"
SSA_SPOUSE = "https://www.ssa.gov/benefits/retirement/planner/applying7.html"
SSA_SURVIVORS = "https://www.ssa.gov/benefits/survivors/"
SSA_TAXES = "https://www.ssa.gov/benefits/retirement/planner/taxes.html"
SSA_WITHDRAW = "https://www.ssa.gov/benefits/retirement/planner/withdrawal.html"
SSA_SUSPEND = "https://www.ssa.gov/benefits/retirement/planner/suspend.html"
SSA_MYACCOUNT = "https://www.ssa.gov/myaccount"
SSA_COLA = "https://www.ssa.gov/cola/"
IRS_PUB915 = "https://www.irs.gov/publications/p915"
MEDICARE_SIGNUP = "https://www.medicare.gov/basics/get-started-with-medicare/sign-up"


GUIDES = [
    {
        "slug": "working-while-collecting-social-security",
        "title": "Working While Collecting: The Earnings Test Isn't a Tax",
        "description": "How the Social Security earnings test withholds benefits before full retirement age, why the money comes back, and when the test stops applying.",
        "body": f"""
  <h1>Working While Collecting Social Security</h1>
  <p class="lede">Claim before your full retirement age and keep working, and Social Security may
  withhold part of your benefit. Almost everyone who hears this concludes the money is gone. It
  isn't - it comes back, and understanding how changes whether claiming early while working is a
  mistake or merely a timing decision.</p>

  <h2>How the test works</h2>
  <p>The earnings test applies only to earned income - wages and self-employment. Pensions,
  investment income, annuities, capital gains and withdrawals from an IRA or 401(k) are all
  invisible to it. There are three stages:</p>
  <ul>
    <li><b>Before the year you reach FRA</b> - $1 of benefit is withheld for every $2 you earn above
    an annual limit.</li>
    <li><b>In the year you reach FRA</b> - the limit is substantially higher and the withholding
    rate drops to $1 for every $3, counting only the months before your birthday.</li>
    <li><b>From the month you reach FRA</b> - the test disappears entirely. You can earn any amount
    with no effect on your benefit, for the rest of your life.</li>
  </ul>
  <p>Both limits are reset each year, so check the
  <a href="{SSA_EARNINGS_TEST}" rel="noopener">SSA's current figures</a> rather than relying on a
  number you saw in an article.</p>

  <h2>The part everyone misses</h2>
  <p>Withheld benefits are not forfeited. When you reach full retirement age, Social Security
  recalculates your benefit upward to account for the months in which benefits were withheld. In
  effect you are treated as having claimed later than you did, and the higher payment continues for
  life.</p>
  <p>So the earnings test is not a penalty on working. It is a deferral. If you claim at 62, work,
  and have twelve months' worth of benefits withheld, your benefit at FRA is recomputed roughly as
  though you had claimed at 63 instead. You lost the use of that cash in the meantime, which is a
  real cost - but not the permanent loss it is usually described as.</p>
  <p>This also means the common advice "don't claim early if you're still working" overstates the
  case. The genuine argument against claiming early is the permanent reduction, which applies
  whether or not you work. The earnings test is a secondary consideration about cash flow.</p>

  <h2>Working also recalculates your benefit</h2>
  <p>Your benefit is based on your highest 35 years of indexed earnings. If you are still working
  and this year's earnings exceed one of those 35 years - which is common, since early-career
  earnings are low and some people have zero years in the count - the low year drops out and your
  benefit is recomputed upward automatically.</p>
  <p>You do not have to apply for this. It happens each year as earnings are reported, and the
  increase is retroactive to January of the following year.</p>

  <h2>What to check</h2>
  <ul>
    <li>Are you claiming before FRA and earning above the limit? If so, expect benefits to be
    withheld - and expect the recomputation at FRA.</li>
    <li>Do you have fewer than 35 years of earnings? Each additional working year replaces a zero and
    raises your benefit meaningfully.</li>
    <li>Is your income from work or from investments? Only work counts.</li>
  </ul>
  <p>Your own earnings record and benefit estimate are free at
  <a href="{SSA_MYACCOUNT}" rel="noopener">ssa.gov/myaccount</a>, and the
  <a href="index.html">calculator on this site</a> shows what each claiming age does to the
  percentage.</p>

  <div class="guide-nav"><a href="guides.html">&larr; All guides</a></div>
""",
    },
    {
        "slug": "spousal-benefits",
        "title": "Spousal Benefits: Up to Half, But Only on Someone Else's Terms",
        "description": "How Social Security spousal benefits are calculated, why delaying past full retirement age does nothing for them, and what deemed filing changed.",
        "body": f"""
  <h1>Spousal Benefits Explained</h1>
  <p class="lede">A spouse can receive up to half of the other spouse's full benefit. That sentence
  is where most explanations stop, and it leaves out the three things that actually determine what
  you get: whose retirement age governs, what the word "up to" is doing, and the fact that delaying
  does nothing at all.</p>

  <h2>Half of what, exactly</h2>
  <p>The spousal benefit is based on the worker's <em>primary insurance amount</em> - their benefit
  at their own full retirement age. It is not based on what they actually receive.</p>
  <p>This is the most common misunderstanding. If your spouse delays to 70 and collects 124% of
  their PIA, your spousal benefit is still calculated from 100% of their PIA, not from the enlarged
  figure. Their delay raises their own cheque and, eventually, a survivor benefit - but it does
  nothing for the spousal benefit while both of you are alive.</p>

  <h2>Delaying your own claim does nothing either</h2>
  <p>Retirement benefits grow by 8% a year for every year you delay past full retirement age, up to
  70. Spousal benefits do not. The spousal benefit maxes out at your full retirement age, and
  waiting beyond it adds exactly nothing.</p>
  <p>If a spousal benefit is all you will receive, claiming later than your FRA is simply forgoing
  money. Claiming <em>earlier</em> than FRA still reduces it permanently, so FRA is the target
  rather than 70.</p>

  <h2>You get the higher of the two, not both</h2>
  <p>If you qualify for a retirement benefit on your own record and a spousal benefit, you do not
  collect both. You receive an amount equal to the higher of the two. Social Security pays your own
  benefit first and then tops it up to the spousal amount if the spousal amount is larger.</p>
  <p>The practical consequence: if your own benefit already exceeds half your spouse's PIA, the
  spousal benefit is irrelevant to you.</p>

  <h2>Deemed filing closed the old strategy</h2>
  <p>There used to be a manoeuvre - file a restricted application for spousal benefits only, let
  your own benefit grow to 70, then switch. It no longer exists for most people. Under deemed
  filing, anyone born on or after 2 January 1954 who files for one benefit is treated as having
  filed for both, and simply receives the higher. Only those born before that date retain the
  restricted application option, and that cohort has now passed 70.</p>
  <p>Deemed filing does not apply to survivor benefits, which remain a genuinely separate claim -
  see the <a href="survivor-benefits.html">survivor benefits guide</a>.</p>

  <h2>Other conditions</h2>
  <ul>
    <li>The worker must have filed for their own benefit before a spousal benefit can be paid.</li>
    <li>You generally must be at least 62, or any age if caring for the worker's child who is under
    16 or disabled.</li>
    <li><b>Divorced spouses</b> can claim on an ex-spouse's record if the marriage lasted at least
    ten years and you have not remarried. After two years divorced, you can claim without the
    ex-spouse having filed - and it has no effect on what they or their current spouse receive. They
    are not notified.</li>
  </ul>

  <p class="source">The SSA's own page on
  <a href="{SSA_SPOUSE}" rel="noopener">benefits for a spouse</a> covers the filing mechanics.</p>

  <div class="guide-nav"><a href="guides.html">&larr; All guides</a></div>
""",
    },
    {
        "slug": "survivor-benefits",
        "title": "Survivor Benefits: The Reason Delaying Can Be Worth More Than It Looks",
        "description": "How Social Security survivor benefits work, why they can be claimed as early as 60, and why the higher earner's claiming age matters for two lifetimes.",
        "body": f"""
  <h1>Survivor Benefits</h1>
  <p class="lede">Survivor benefits are the part of Social Security most likely to be left on the
  table, because they follow different rules from everything else - different starting age,
  different percentage, and, crucially, no deemed filing. For a married couple, they are also the
  strongest argument for the higher earner delaying.</p>

  <h2>Up to 100%, not 50%</h2>
  <p>A surviving spouse can receive up to 100% of what the deceased was receiving, or would have
  been entitled to - not the 50% that applies to spousal benefits while both are alive. If the
  survivor's own benefit is larger, they keep their own. Either way the household goes from two
  cheques to one, which is why the size of the survivor benefit matters so much.</p>

  <h2>The claiming age that counts is the deceased's</h2>
  <p>This is the decision point couples most often get wrong. If the higher earner delays to 70,
  they lock in roughly 124% of their PIA - and that enlarged amount becomes the survivor benefit for
  whichever spouse outlives the other. If they claim at 62 instead, the survivor is capped near that
  reduced figure for the rest of their life.</p>
  <p>So the higher earner's delay buys benefit increases across two lifetimes rather than one, which
  substantially changes the breakeven arithmetic. The usual framing - "will I live long enough to
  come out ahead?" - is the wrong question for the higher earner in a couple. The right one is
  whether <em>either</em> of you will.</p>
  <p>The mirror image also holds: for the lower earner, delaying is worth much less, because their
  benefit likely disappears at the first death anyway.</p>

  <h2>Different ages apply</h2>
  <ul>
    <li>A surviving spouse can claim a survivor benefit from <b>age 60</b> - not 62 - or from 50 if
    disabled, with a permanent reduction for claiming before their full retirement age.</li>
    <li>At any age if caring for the deceased's child who is under 16 or disabled.</li>
    <li>A <b>surviving divorced spouse</b> qualifies if the marriage lasted at least ten years.</li>
    <li>Remarriage after 60 does not cost you a survivor benefit. Remarriage before 60 does, unless
    that marriage also ends.</li>
  </ul>

  <h2>You can take one and switch to the other</h2>
  <p>Deemed filing does not apply to survivor benefits. They and your own retirement benefit are
  separate claims, and you may take one first and switch to the other later.</p>
  <p>That flexibility is genuinely valuable and routinely missed. A widow with a modest survivor
  benefit and a larger earnings record of her own can claim the survivor benefit at 60, live on it
  while her own retirement benefit accrues delayed credits, and switch to her own at 70. The reverse
  works too. Nobody at the SSA will propose this; you have to ask.</p>
  <p>Note that survivor benefits cannot be applied for online - they require a phone call or an
  office visit.</p>

  <p class="source">See the SSA's <a href="{SSA_SURVIVORS}" rel="noopener">survivors benefits</a>
  pages for eligibility details and the one-time lump-sum death payment.</p>

  <div class="guide-nav"><a href="guides.html">&larr; All guides</a></div>
""",
    },
    {
        "slug": "social-security-taxes",
        "title": "How Much of Your Social Security Is Taxable",
        "description": "Provisional income, the 50% and 85% thresholds that have never been indexed for inflation, and why an IRA withdrawal can be taxed twice over.",
        "body": f"""
  <h1>How Much of Your Social Security Is Taxable</h1>
  <p class="lede">Up to 85% of your benefit can be subject to federal income tax. The thresholds
  that decide this were set in 1983 and 1993 and have never been adjusted for inflation - so a
  provision originally aimed at wealthy retirees now reaches a large share of ordinary ones, and
  reaches more of them every year.</p>

  <h2>Provisional income</h2>
  <p>Taxation is decided not by your benefit or your ordinary income but by a separate figure:</p>
  <p><b>Provisional income = adjusted gross income + tax-exempt interest + half of your Social
  Security benefit</b></p>
  <p>Note that tax-exempt municipal bond interest counts here even though it is not taxable itself.
  Municipal bonds do not keep you below the threshold.</p>
  <table>
    <tr><th>Provisional income</th><th>Single</th><th>Married filing jointly</th></tr>
    <tr><td>None of the benefit taxable</td><td>Under $25,000</td><td>Under $32,000</td></tr>
    <tr><td>Up to 50% taxable</td><td>$25,000 - $34,000</td><td>$32,000 - $44,000</td></tr>
    <tr><td>Up to 85% taxable</td><td>Over $34,000</td><td>Over $44,000</td></tr>
  </table>
  <p>These are the actual statutory figures, unchanged for decades. They are not typos and they are
  not indexed.</p>

  <h2>"85% taxable" is not an 85% tax</h2>
  <p>A frequent misreading. Crossing the upper threshold means up to 85% of your benefit is included
  in taxable income - it is then taxed at your ordinary rate. If you are in the 12% bracket, the tax
  on your benefit is roughly 12% of 85% of it, around 10%.</p>

  <h2>The trap: an extra dollar can cost more than a dollar</h2>
  <p>Because additional income raises provisional income, which can in turn drag more of your benefit
  into taxable income, a withdrawal from a traditional IRA can be taxed and simultaneously make more
  of your benefit taxable. Within the phase-in ranges this produces marginal rates noticeably higher
  than your nominal bracket - the effect sometimes called the tax torpedo.</p>
  <p>Two practical consequences. Roth withdrawals do not count toward provisional income at all, so
  they are unusually valuable in retirement for reasons beyond their own tax treatment. And the
  years between retiring and claiming Social Security are often the lowest-income years of a
  retirement - a natural window for Roth conversions, before benefits and required minimum
  distributions start.</p>

  <h2>State tax</h2>
  <p>Most states do not tax Social Security benefits at all, and the number that do has been falling
  as states repeal it. Those that still tax them generally apply their own exemptions and income
  thresholds, which are usually more generous than the federal ones. Check your own state rather
  than assuming either way.</p>

  <h2>Withholding</h2>
  <p>Social Security does not withhold federal tax unless you ask. You can request it with Form W-4V
  at a few fixed percentages, or pay quarterly estimated tax instead. Retirees who do neither are
  the ones who get an unwelcome surprise in their first April after claiming.</p>

  <p class="source">See the SSA's <a href="{SSA_TAXES}" rel="noopener">benefits planner on
  taxes</a> and <a href="{IRS_PUB915}" rel="noopener">IRS Publication 915</a> for the worksheets.</p>

  <div class="guide-nav"><a href="guides.html">&larr; All guides</a></div>
""",
    },
    {
        "slug": "breakeven-age",
        "title": "The Breakeven Age, and Why It's the Wrong Question",
        "description": "How Social Security breakeven analysis works, what it leaves out, and why longevity insurance is a better frame than a bet on your own lifespan.",
        "body": f"""
  <h1>The Breakeven Age, and Why It's the Wrong Question</h1>
  <p class="lede">Claim at 62 and the cheques start sooner but are smaller. Wait until 70 and they
  are far larger but you have skipped eight years of payments. The breakeven age is where the totals
  cross - and treating it as the deciding factor leads a lot of people to the wrong answer.</p>

  <h2>What the calculation does</h2>
  <p>Add up everything you would receive under each claiming age and find the age at which the later
  claim overtakes the earlier one. The <a href="index.html">calculator on this site</a> does exactly
  this with your own benefit figure.</p>
  <p>The crossings land in a fairly narrow range for most people: claiming early versus waiting to
  full retirement age tends to break even somewhere in the late seventies, and full retirement age
  versus 70 somewhere around the early eighties. The precise ages depend on your own full retirement
  age and are worth running rather than assuming.</p>

  <h2>Why it is the wrong frame</h2>
  <p>Breakeven analysis asks "which choice maximises my expected total?" and answers it by making
  you guess your date of death. But the risk that actually matters in retirement is not dying early
  - it is living a long time and running short of money.</p>
  <p>Seen that way, delaying Social Security is not a bet on longevity. It is insurance against it.
  Social Security is inflation-adjusted, lasts as long as you do, and carries no market risk. There
  is nothing else available to an ordinary retiree with those three properties, and increasing it by
  roughly 8% a year is a far cheaper way to buy more of it than any annuity on the market.</p>
  <p>If you claim early and die early, you "won" the breakeven calculation - and it did not matter,
  because you were not there to need the money. If you claim early and live to 95, you lost, and it
  mattered every month for thirty years. The two outcomes are not symmetric, which is precisely what
  a breakeven comparison ignores.</p>

  <h2>What the comparison also leaves out</h2>
  <ul>
    <li><b>Survivor benefits.</b> For the higher earner in a couple, delaying raises the payment for
    whichever spouse lives longer. The relevant lifespan is the longer of two, not your own - see the
    <a href="survivor-benefits.html">survivor benefits guide</a>.</li>
    <li><b>Taxes.</b> Benefits are taxed on different terms from IRA withdrawals, so the comparison
    of gross totals is not a comparison of spendable income - see
    <a href="social-security-taxes.html">how much of your benefit is taxable</a>.</li>
    <li><b>COLA compounding.</b> Cost-of-living adjustments apply to a larger base if you delayed, so
    the gap widens over time rather than staying fixed.</li>
    <li><b>The earnings test</b>, if you claim early and keep working - see
    <a href="working-while-collecting-social-security.html">working while collecting</a>.</li>
  </ul>

  <h2>When claiming early is genuinely right</h2>
  <p>None of this makes delaying universally correct. Claiming early is a reasonable decision if you
  have a health condition that materially shortens your life expectancy, if you have no spouse who
  would depend on a survivor benefit, if you need the income now and the alternative is high-interest
  debt, or if claiming lets you leave a job you cannot continue. Those are real reasons. "I want to
  get my money's worth" is not one.</p>

  <div class="guide-nav"><a href="guides.html">&larr; All guides</a></div>
""",
    },
    {
        "slug": "changing-your-mind",
        "title": "Changing Your Mind After You Claim: Withdrawal and Suspension",
        "description": "The two ways to undo or pause a Social Security claim - a 12-month withdrawal that requires repayment, and voluntary suspension at full retirement age.",
        "body": f"""
  <h1>Changing Your Mind After You Claim</h1>
  <p class="lede">Claiming Social Security feels irreversible, and it very nearly is. But there are
  two escape hatches, each with narrow conditions, and almost nobody knows about them until it is
  too late to use the first one.</p>

  <h2>Withdrawal: the 12-month do-over</h2>
  <p>Within <b>12 months</b> of your benefits starting, you can withdraw your application entirely
  using Form SSA-521. Social Security then treats you as never having claimed - your benefit resumes
  growing as though nothing happened, and you can claim again later at the higher percentage.</p>
  <p>The conditions are strict:</p>
  <ul>
    <li>You must <b>repay every dollar</b> paid out on your record - including anything paid to a
    spouse or children on it, and any Medicare premiums deducted.</li>
    <li>It is allowed <b>once in your lifetime</b>.</li>
    <li>The 12 months run from entitlement, not from when you made the decision.</li>
  </ul>
  <p>This is the right tool for a specific situation: you claimed at 62, then your circumstances
  changed - an inheritance, a new job, a reassessment of your health - and you can afford to give the
  money back. Having to repay the full amount is what makes it rare in practice.</p>

  <h2>Suspension: available from full retirement age</h2>
  <p>Once you reach full retirement age, you can voluntarily suspend your benefit without repaying
  anything. While suspended, you earn delayed retirement credits of 8% a year, up to age 70, and
  payments restart automatically at 70 if you do not request them sooner.</p>
  <p>Worked example of who this helps: someone who claimed at 62, regrets it, and is now 67. The
  12-month withdrawal window closed years ago. Suspending from 67 to 70 adds roughly 24% to their
  reduced benefit permanently - it does not undo the original reduction, but it recovers a
  meaningful part of it.</p>
  <p>The catch is that suspension stops benefits paid to anyone else on your record, except a
  divorced spouse. If a spouse is collecting on your record, suspending cuts their payment too, which
  often makes it a worse deal than it first appears.</p>

  <h2>Medicare keeps going</h2>
  <p>Suspending or withdrawing does not end Medicare coverage. What it ends is the automatic
  deduction of Part B premiums from your benefit - you will be billed directly instead, and you need
  to pay those bills to keep coverage.</p>
  <p>Worth separating the two in your head generally: Medicare eligibility at 65 and Social Security
  claiming are independent decisions. If you are not claiming at 65, you must still
  <a href="{MEDICARE_SIGNUP}" rel="noopener">enrol in Medicare</a> actively, and missing that window
  carries late-enrolment penalties that last for life.</p>

  <h2>What you cannot undo</h2>
  <p>Outside these two routes, a claiming decision is permanent. There is no partial withdrawal, no
  second lifetime do-over, and no mechanism for recalculating a reduction because you changed your
  mind at 75. That is the real argument for treating the original decision carefully - the
  <a href="breakeven-age.html">breakeven guide</a> covers how to think about it.</p>

  <p class="source">SSA references:
  <a href="{SSA_WITHDRAW}" rel="noopener">withdrawing your application</a> and
  <a href="{SSA_SUSPEND}" rel="noopener">suspending benefits</a>. Cost-of-living adjustments are
  published at <a href="{SSA_COLA}" rel="noopener">ssa.gov/cola</a>.</p>

  <div class="guide-nav"><a href="guides.html">&larr; All guides</a></div>
""",
    },
]

GUIDES_BY_SLUG = {g["slug"]: g for g in GUIDES}


def guide_slug(slug):
    return f"{slug}.html"
