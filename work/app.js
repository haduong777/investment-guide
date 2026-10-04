(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const money = n => new Intl.NumberFormat('en-US', {style:'currency',currency:'USD',maximumFractionDigits:0}).format(n);
  const menu = $('menu'), sidebar = $('sidebar');
  function closeMenu(){sidebar.classList.remove('open');menu.setAttribute('aria-expanded','false');}
  menu.addEventListener('click',()=>{const open=sidebar.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});
  sidebar.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
  document.addEventListener('keydown',e=>{if(e.key==='Escape' && sidebar.classList.contains('open')){closeMenu();menu.focus();}});
  document.querySelector('main').addEventListener('click',closeMenu);
  const sections=[...document.querySelectorAll('.chapter')], nav=[...document.querySelectorAll('nav a')];
  let scheduled=false;
  function reading(){
    const max=document.documentElement.scrollHeight-innerHeight;
    $('progress').style.width=(max>0?scrollY/max*100:0)+'%';
    let current='';sections.forEach(s=>{if(s.getBoundingClientRect().top<170)current=s.id;});
    nav.forEach(a=>{const active=a.hash==='#'+current;a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});
    scheduled=false;
  }
  addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(reading);}},{passive:true});
  addEventListener('resize',reading);reading();
  document.querySelectorAll('.filter').forEach(button=>button.addEventListener('click',()=>{
    document.querySelectorAll('.filter').forEach(b=>{const on=b===button;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on));});
    let count=0;document.querySelectorAll('.fund-card').forEach(card=>{card.hidden=button.dataset.filter!=='all'&&card.dataset.kind!==button.dataset.filter;if(!card.hidden)count++;});
    $('filter-status').textContent=`Showing ${count} funds.`;
  }));
  function validNumber(id){const el=$(id),value=el.valueAsNumber;const good=Number.isFinite(value)&&value>=Number(el.min)&&value<=Number(el.max);el.setAttribute('aria-invalid',String(!good));return good?value:null;}
  function stress(){
    const pct=Number($('stock-weight').value),amount=validNumber('stress-amount');
    $('stock-label').textContent=pct+'%';
    $('stress-mix').textContent=`${pct}% stocks · ${100-pct}% bonds`;
    if(amount===null){$('stress-after').textContent='—';$('stress-loss').textContent='Enter an amount from $0 to $100,000,000.';return;}
    const loss=.4*pct/100+.1*(1-pct/100),after=amount*(1-loss);
    $('stress-after').textContent=money(after);$('stress-loss').textContent=`−${money(amount*loss)} / −${(loss*100).toFixed(0)}%`;
    $('stress-fill').style.width=(1-loss)*100+'%';
  }
  ['stock-weight','stress-amount'].forEach(id=>$(id).addEventListener('input',stress));stress();
  function growth(){
    $('years-label').textContent=$('years').value;
    const ids=['initial','monthly','years','return','fee-a','fee-b'],values=ids.map(validNumber);
    if(values.some(v=>v===null)){$('growth-error').textContent='Enter values within the displayed limits: starting amount $0–$10 million, monthly $0–$100,000, return −10% to 15%, fees 0%–5%.';['balance-a','balance-b','fee-difference','contributed'].forEach(id=>$(id).textContent='—');$('growth-lines').innerHTML='';$('growth-desc').textContent='Enter valid inputs to calculate this illustration.';return;}
    $('growth-error').textContent='';
    const [initial,monthly,years,ret,feeA,feeB]=values;
    const monthlyA=Math.pow(1+(ret-feeA)/100,1/12)-1,monthlyB=Math.pow(1+(ret-feeB)/100,1/12)-1;
    let a=initial,b=initial;const pointsA=[a],pointsB=[b],pointsC=[initial];
    for(let month=1;month<=years*12;month++){a=a*(1+monthlyA)+monthly;b=b*(1+monthlyB)+monthly;if(month%12===0){pointsA.push(a);pointsB.push(b);pointsC.push(initial+monthly*month);}}
    $('balance-a').textContent=money(a);$('balance-b').textContent=money(b);$('fee-difference').textContent=money(a-b);$('contributed').textContent=money(initial+monthly*years*12);
    const chartWidth=Math.max(240,Math.min(780,$('growth-chart').clientWidth));
    $('growth-chart').setAttribute('viewBox',`0 0 ${chartWidth} 290`);
    const max=Math.max(...pointsA,...pointsB,...pointsC,1)*1.08,left=chartWidth<500?46:65,right=chartWidth-25,top=18,bottom=250;
    const y=v=>bottom-(v/max)*(bottom-top),x=i=>left+(right-left)*i/years;
    const path=arr=>arr.map((v,i)=>(i?'L':'M')+x(i).toFixed(2)+','+y(v).toFixed(2)).join(' ');
    let lines='';for(let i=0;i<=4;i++){const val=max*i/4,yy=y(val);const label=val>=1000000?'$'+(val/1000000).toFixed(1)+'m':val>=1000?'$'+Math.round(val/1000)+'k':'$'+Math.round(val);lines+=`<line x1="${left}" y1="${yy}" x2="${right}" y2="${yy}" stroke="#d8dccf"/><text x="${left-12}" y="${yy+4}" text-anchor="end" fill="#5f6a60" font-size="11">${label}</text>`;}
    [0,Math.round(years/2),years].filter((n,i,a)=>a.indexOf(n)===i).forEach(v=>{lines+=`<text x="${x(v)}" y="278" text-anchor="middle" fill="#5f6a60" font-size="11">Year ${v}</text>`;});
    lines+=`<path d="${path(pointsC)}" fill="none" stroke="#727c69" stroke-width="2" stroke-dasharray="2 5"/><path d="${path(pointsB)}" fill="none" stroke="#96542e" stroke-width="3" stroke-dasharray="7 5"/><path d="${path(pointsA)}" fill="none" stroke="#294e3b" stroke-width="3.5"/>`;
    $('growth-lines').innerHTML=lines;
    $('growth-desc').textContent=`Over ${years} years, contributions total ${money(initial+monthly*years*12)}. With assumed gross return ${ret}% and fee A ${feeA}%, the ending value is ${money(a)}. With fee B ${feeB}%, it is ${money(b)}. This is a constant-return illustration, not a forecast.`;
  }
  ['initial','monthly','years','return','fee-a','fee-b'].forEach(id=>$(id).addEventListener('input',growth));growth();
  addEventListener('resize',growth);
  const checks=[...document.querySelectorAll('[data-check]')],key='first-dollar-checklist-v1';
  let canStore=true;
  try {const saved=JSON.parse(localStorage.getItem(key)||'{}');checks.forEach(c=>c.checked=saved[c.dataset.check]===true);} catch(_){canStore=false;$('storage-note').textContent='Checks work for this session. This browser is not saving them; download the worksheet to keep a copy.';}
  function checklist(save=true){
    const count=checks.filter(c=>c.checked).length;$('check-count').textContent=`${count} of ${checks.length} decisions checked`;
    $('check-status').textContent=count===checks.length?'All decisions reviewed. Recheck the current fund and order details before making a purchase; this checklist does not assess suitability.':`${checks.length-count} decisions left to review. Use the unchecked items to decide what to resolve next.`;
    if(save&&canStore){try{localStorage.setItem(key,JSON.stringify(Object.fromEntries(checks.map(c=>[c.dataset.check,c.checked]))));}catch(_){canStore=false;$('storage-note').textContent='Your browser could not save these checks. Download the worksheet to keep a copy.';}}
  }
  checks.forEach(c=>c.addEventListener('change',()=>checklist()));checklist(false);
  $('reset-checks').addEventListener('click',()=>{checks.forEach(c=>c.checked=false);checklist();});
  $('download-plan').addEventListener('click',()=>{
    const text=`FIRST DOLLAR — PERSONAL PLANNING WORKSHEET\nGuide research date: 4 October 2026\n\nContext: California resident; Vietnamese citizen; STEM OPT; stated US tax resident; approximately nine months remaining in US.\n\nMY PLAN\nGoal: ____________________\nSpending date / investment horizon: ____________________\nEmergency reserve: ____________________\nNine-month and moving-cost budget: ____________________\nDebt balances / rates: ____________________\nEmployer match and vesting: ____________________\nIncome / filing status / IRA eligibility: ____________________\nBroker and account type: ____________________\nLong-term stock / bond allocation: ____________________\nFunds and their jobs: ____________________\nMonthly contribution: ____________________\nReview date and rebalancing rule: ____________________\nBroker and cross-border tax review before departure: ____________________\n\nCHECKLIST\n${checks.map(c=>(c.checked?'[x] ':'[ ] ')+c.parentElement.innerText.replace(/\s+/g,' ').trim()).join('\n\n')}\n\nSCENARIOS\nThe page calculators are hypothetical illustrations, not forecasts. A completed checklist is not a suitability assessment.\n\nNEXT UNRESOLVED QUESTION\n____________________\n`;
    const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download='first-dollar-planning-worksheet.txt';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  let printDetails=[];
  addEventListener('beforeprint',()=>{printDetails=[...document.querySelectorAll('details')].map(d=>[d,d.open]);printDetails.forEach(([d])=>d.open=true);});
  addEventListener('afterprint',()=>printDetails.forEach(([d,open])=>d.open=open));
  $('print').addEventListener('click',()=>window.print());
})();
