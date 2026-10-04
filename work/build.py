from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
SOURCES={
'residency':('IRS · Tax residency','https://www.irs.gov/individuals/international-taxpayers/determining-an-individuals-tax-residency-status'),
'519':('IRS · Tax guide for aliens','https://www.irs.gov/publications/p519'),
'w9':('IRS · Form W-9 instructions','https://www.irs.gov/instructions/iw9'),
'stem':('DHS · STEM OPT training requirements','https://studyinthestates.dhs.gov/form-i-983-overview'),
'limits':('IRS · 2026 retirement limits','https://www.irs.gov/newsroom/401k-limit-increases-to-24500-for-2026-ira-limit-increases-to-7500'),
'roth':('IRS · Roth IRAs','https://www.irs.gov/retirement-plans/roth-iras'),
'withdraw':('IRS · IRA distributions','https://www.irs.gov/publications/p590b'),
'hsa':('IRS · HSA rules','https://www.irs.gov/publications/p969'),
'hsa26':('IRS · 2026 HSA limits','https://www.irs.gov/irb/2026-02_IRB'),
'fidelity':('Fidelity · Pricing','https://www.fidelity.com/trading/commissions-margin-rates'),
'recurring':('Fidelity · Recurring investments','https://www.fidelity.com/trading/recurring-investments'),
'schwab':('Schwab · Pricing','https://www.schwab.com/pricing'),
'slices':('Schwab · Fractional stocks and ETFs','https://www.schwab.com/fractional-shares-stock-slices'),
'ibkr':('Interactive Brokers · Pricing','https://www.interactivebrokers.com/en/pricing/commissions-home.php?menu=A'),
'vbroker':('Vanguard · Brokerage fees','https://investor.vanguard.com/client-benefits/investment-fees'),
'fdic':('FDIC · Deposit insurance','https://www.fdic.gov/resources/deposit-insurance/understanding-deposit-insurance'),
'sipc':('SIPC · What is protected','https://www.sipc.org/for-investors/what-sipc-protects'),
'etf':('SEC · ETF basics','https://www.investor.gov/introduction-investing/investing-basics/investment-products/mutual-funds-and-exchange-traded-2'),
'wrappers':('SEC · ETFs and mutual funds compared','https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/characteristics-mutual-funds-exchange-traded-funds'),
'mf':('FINRA · Mutual funds','https://www.finra.org/investors/investing/investment-products/mutual-funds'),
'fees':('SEC · How investment fees compound','https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/updated'),
'vti':('Vanguard · VTI','https://advisors.vanguard.com/investments/products/vti/vanguard-total-stock-market-etf?source=autosugg'),
'voo':('Vanguard · VOO','https://advisors.vanguard.com/investments/products/voo/vanguard-sp-500-etf?fromSearch=true&source=autosuggest'),
'vxus':('Vanguard · VXUS','https://advisors.vanguard.com/investments/products/vxus/vanguard-total-international-stock-etf?compositionTabBox=1'),
'vt':('Vanguard · VT','https://advisors.vanguard.com/investments/products/new/vt/vanguard-total-world-stock-etf'),
'bnd':('Vanguard · BND','https://investor.vanguard.com/investment-products/etfs/profile/bnd'),
'bndfee':('Vanguard · Fund expense ratios, April 2026','https://personal1.vanguard.com/pdf/total_return_chart.pdf?2210125343='),
'sgov':('iShares · SGOV','https://www.ishares.com/us/products/314116/ishares-0-3-month-treasury-bond-etf'),
'bills':('TreasuryDirect · Treasury bills','https://www.treasurydirect.gov/marketable-securities/treasury-bills/'),
'ibonds':('TreasuryDirect · Series I savings bonds','https://www.treasurydirect.gov/savings-bonds/i-bonds/'),
'gains':('IRS · Capital gains and losses','https://www.irs.gov/taxtopics/tc409'),
'550':('IRS · Investment income and wash sales','https://www.irs.gov/publications/p550'),
'pfic':('IRS · PFIC reporting','https://www.irs.gov/instructions/i8621'),
'foreign':('IRS · FBAR and Form 8938','https://www.irs.gov/businesses/comparison-of-form-8938-and-fbar-requirements'),
'pe':('SEC · Private equity funds','https://www.investor.gov/introduction-investing/investing-basics/investment-products/private-investment-funds/private-equity'),
'accredited':('SEC · Accredited investors','https://www.sec.gov/resources-small-businesses/capital-raising-building-blocks/accredited-investors'),
'interval':('FINRA · Interval funds','https://www.finra.org/investors/insights/interval-funds'),
'retailpe':('SEC · Registered funds of private funds','https://www.sec.gov/about/divisions-offices/division-investment-management/fund-disclosure-glance/accounting-disclosure-information/adi-2025-16-registered-closed-end-funds-private-funds'),
'leverage':('SEC · Leveraged and inverse ETFs','https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-alerts/sec'),
'etn':('SEC · Exchange-traded notes','https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/investor-bulletins-50'),
'settlement':('SEC · T+1 settlement','https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins/new-t1-settlement-cycle-what-investors-need-know-investor-bulletin'),
'abroad':('Fidelity · Accounts and overseas restrictions','https://www.fidelity.com/trading/faqs-about-account'),
'estate':('IRS · Estate tax for noncitizens','https://www.irs.gov/businesses/small-businesses-self-employed/frequently-asked-questions-on-estate-taxes-for-nonresidents-not-citizens-of-the-united-states'),
'estatesitus':('IRS · US-situated estate assets','https://www.irs.gov/individuals/international-taxpayers/some-nonresidents-with-us-assets-must-file-estate-tax-returns'),
'caadjust':('California FTB · Resident adjustments','https://www.ftb.ca.gov/forms/2025/2025-540-ca-instructions.html'),
'ca1001':('California FTB · Income adjustments','https://www.ftb.ca.gov/forms/2025/2025-1001-publication.pdf'),
'capenalty':('California FTB · Retirement distribution taxes','https://www.ftb.ca.gov/forms/2025/2025-3805p-instructions.html'),
'cagains':('California FTB · Capital gains','https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html'),
'treaties':('IRS · In-force income-tax treaties','https://www.irs.gov/businesses/international-businesses/united-states-income-tax-treaties-a-to-z'),
'findex':('Fidelity · Index mutual funds','https://www.fidelity.com/mutual-funds/investing-ideas/index-funds'),
'dividend':('IRS · Dividends and distributions','https://www.irs.gov/taxtopics/tc404'),
'wash':('Fidelity · Wash-sale rules','https://www.fidelity.com/learning-center/personal-finance/wash-sales-rules-tax'),
'bonds':('FINRA · Bonds','https://www.finra.org/investors/investing/investment-products/bonds'),
'tips':('TreasuryDirect · TIPS','https://www.treasurydirect.gov/marketable-securities/tips/'),
'duration':('FINRA · Duration and rate sensitivity','https://syndication.finra.org/content/duration-what-interest-rate-hike-could-do-your-bond-portfolio'),
'niit':('IRS · Net investment income tax','https://www.irs.gov/taxtopics/tc559'),
'peeconomics':('CFA Institute · Economics of private equity','https://rpc.cfainstitute.org/-/media/documents/article/rf-brief/economics-of-private-equity.pdf'),
'pej':('CFA Institute · Private equity and the J-curve','https://rpc.cfainstitute.org/sites/default/files/-/media/documents/book/rf-publication/2018/rf-v2018-n1-1.pdf'),
'buybill':('TreasuryDirect · Buying at auction','https://www.treasurydirect.gov/marketable-securities/buying-a-marketable-security/'),
'sellbill':('TreasuryDirect · Selling before maturity','https://treasurydirect.gov/marketable-securities/selling-marketable-securities/'),
}
SOURCES['etn']=('SEC · Exchange-traded notes','https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-50')
def cite(match):
    keys=match.group(1).split(',')
    return '<span class="sources">'+' · '.join('<a href="'+SOURCES[k][1]+'" target="_blank" rel="noopener noreferrer">'+SOURCES[k][0]+' ↗</a>' for k in keys)+'</span>'
content='\n'.join(p.read_text() for p in sorted((ROOT/'work').glob('chapter-*.html')))
content=re.sub(r'\[\[([a-z0-9,]+)\]\]',cite,content)
content=content.replace('{{SOURCE_DIRECTORY}}',''.join(f'<a href="{url}" target="_blank" rel="noopener noreferrer">{name} ↗</a>' for name,url in SOURCES.values()))
chapters=[('start','The starting point'),('foundations','How investing works'),('accounts','Choose your account'),('brokers','Choose your broker'),('funds','Understand the funds'),('portfolio','Build a portfolio'),('costs','Returns & real costs'),('alternatives','Beyond ETFs'),('private','Private equity, unpacked'),('taxes','Taxes & paperwork'),('buy','Your first purchase'),('checklist','Ready for dollar one'),('glossary','Plain-English glossary'),('references','Sources & assumptions'),('leaving','If you leave the US')]
nav=''.join(f'<a href="#{id}"><span>{i:02}</span>{label}</a>' for i,(id,label) in enumerate(chapters,1))
css=(ROOT/'work/style.css').read_text()
js=(ROOT/'work/app.js').read_text()
page='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f5f3ea"><meta name="description" content="A practical illustrated guide to US investing, ETFs, brokerage accounts, private equity and taxes for a STEM OPT student who is a US tax resident."><title>First Dollar — A practical guide to investing in the US</title><style>'''+css+'''</style></head>
<body><a class="skip" href="#main">Skip to guide</a><div class="read-progress" aria-hidden="true"><div id="progress"></div></div>
<aside class="sidebar" id="sidebar"><a class="brand" href="#top"><span class="brand-mark" aria-hidden="true">f<span> / </span>d</span>first dollar<span class="edition">AN INVESTOR’S FIELD GUIDE</span></a><div class="nav-label">YOUR ROUTE</div><nav aria-label="Guide chapters">'''+nav+'''</nav><div class="sidebar-note">US-domiciled investments.<br>Built for a thoughtful first step.<span>2026 EDITION · 04 OCT</span></div></aside>
<div class="page"><header class="topbar"><a href="#top" class="mobile-brand">first dollar /</a><span class="top-context">THE PRACTICAL GUIDE / UNITED STATES</span><div class="top-actions"><button id="menu" aria-expanded="false" aria-controls="sidebar">Contents</button><button id="print" title="Print or save as PDF">Print guide <span aria-hidden="true">↗</span></button></div></header>
<main id="main"><section class="hero" id="top"><div class="hero-copy"><div class="eyebrow"><span class="dot"></span> FOR YOUR FIRST INVESTMENT & THE YEARS AFTER</div><h1>Your first dollar.<br><em>A clearer direction.</em></h1><p class="dek">A practical guide to investing in the US.<br>Understand the accounts. Know what you own.<br>Build a plan you can stay with.</p><div class="hero-buttons"><a class="button" href="#start">Start the guide <span aria-hidden="true">↘</span></a><a class="text-link" href="#funds">Explore the funds <span aria-hidden="true">→</span></a></div><div class="hero-meta">FOR A STEM OPT STUDENT · US TAX RESIDENT<br><span>ETFs, retirement accounts, bonds, private markets & the details that matter.</span></div></div>
<figure class="hero-art"><svg viewBox="0 0 440 445" role="img" aria-labelledby="hero-title hero-desc"><title id="hero-title">Many investments. One deliberate starting point.</title><desc id="hero-desc">An illustrated investment tree branches from your first dollar into cash, bonds and stocks. A broad fund holds many businesses rather than one company.</desc><defs><pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".75" fill="#98aa92" opacity=".5"/></pattern></defs><rect x="1" y="1" width="438" height="443" rx="3" fill="#e6eadc"/><rect x="1" y="1" width="438" height="443" fill="url(#grid)"/><circle cx="223" cy="201" r="134" fill="none" stroke="#8b9d85" stroke-dasharray="3 7"/><path d="M220 342V238M220 273L103 189M220 273L335 176M220 236V129" stroke="#284c3b" stroke-width="2" fill="none"/><path d="M90 174h27M322 161h26M207 115h26" stroke="#284c3b" stroke-width="2"/><g transform="translate(159 60)"><rect x="5" y="5" width="125" height="78" fill="#bbc7ad"/><rect width="125" height="78" rx="2" fill="#f8f6ed" stroke="#284c3b"/><path d="M17 27h20v31H17zM45 17h20v41H45zM74 34h20v24H74z" fill="#839c73"/><text x="103" y="61" fill="#284c3b" font-size="13">↗</text></g><g transform="translate(37 151)"><rect x="5" y="5" width="123" height="78" fill="#bbc7ad"/><rect width="123" height="78" rx="2" fill="#f8f6ed" stroke="#284c3b"/><rect x="17" y="18" width="34" height="43" rx="2" fill="#cfdfad" stroke="#284c3b"/><circle cx="34" cy="40" r="11" fill="none" stroke="#284c3b"/><text x="64" y="38" font-size="11" fill="#284c3b">CASH</text><text x="64" y="53" font-size="10" fill="#284c3b">Ready.</text></g><g transform="translate(280 150)"><rect x="5" y="5" width="123" height="78" fill="#bbc7ad"/><rect width="123" height="78" rx="2" fill="#f8f6ed" stroke="#284c3b"/><path d="M16 24h32v34H16zM21 19h32v34" fill="#e1b695" stroke="#284c3b"/><path d="M23 33h17M23 42h11" stroke="#284c3b"/><text x="65" y="38" font-size="11" fill="#284c3b">BONDS</text><text x="65" y="53" font-size="10" fill="#284c3b">Steady.</text></g><text x="222" y="45" text-anchor="middle" font-size="11" letter-spacing="2" fill="#284c3b">STOCKS / GROWTH</text><g transform="translate(162 315)"><ellipse cx="58" cy="38" rx="55" ry="23" fill="#284c3b"/><path d="M3 19v18c0 31 110 31 110 0V19" fill="#b9d378" stroke="#284c3b"/><ellipse cx="58" cy="19" rx="55" ry="23" fill="#d4e69c" stroke="#284c3b"/><text x="58" y="26" text-anchor="middle" font-size="25" font-family="Georgia" fill="#284c3b">$1</text></g><text x="220" y="417" text-anchor="middle" font-size="10" letter-spacing="2" fill="#284c3b">A PLAN BEFORE A PURCHASE</text></svg><figcaption>01 / Start with a purpose. Give each dollar a job.</figcaption></figure></section>
<div class="intro-strip"><span><b>15</b> focused chapters</span><span><b>6</b> core fund examples</span><span><b>3</b> interactive tools</span><a href="#checklist">Your first-dollar checklist <span aria-hidden="true">↗</span></a></div>
'''+content+'''</main><footer><a href="#top">first dollar / <span>Back to the beginning ↑</span></a><p>Made for informed decisions, not market predictions.<br>Research checked 4 October 2026 · Educational guidance, not individualized financial, tax or legal advice.</p></footer></div><script>'''+js+'''</script></body></html>'''
output_dir = ROOT / 'outputs'
output_dir.mkdir(exist_ok=True)
(output_dir / 'index.html').write_text(page)
(output_dir / 'first-dollar.html').write_text(page)
print(f'Built GitHub Pages site: {len(page):,} characters; {len(SOURCES)} linked references.')
