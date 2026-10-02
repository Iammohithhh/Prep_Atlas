/* Prep Atlas: static, browser-local practice. No accounts or execution server. */
'use strict';
const $ = s => document.querySelector(s);
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const STORAGE = 'prep-atlas-progress-v1';
const sections = {
  dsa:{name:'DSA',icon:'⌘',symbol:'{ }',desc:'Arrays to graphs. Learn the patterns behind company coding rounds.'},
  ml:{name:'AI & ML',icon:'✧',symbol:'✧',desc:'Theory, ML coding, GenAI, system design and research interviews.'},
  aptitude:{name:'Aptitude',icon:'◈',symbol:'∑',desc:'Quantitative, logical, verbal and data interpretation practice.'},
  cs:{name:'CS fundamentals',icon:'▤',symbol:'▤',desc:'OS, databases, networks, programming and core concepts.'}
};
const statuses = {new:'Not started',attempted:'Attempted',solved:'Solved',revisit:'Revisit'};
let bank, progress = {}, storageOkay = true, filters = {search:'',company:'',topic:'',difficulty:'',status:'',origin:'',role:''}, page = 0;
let editor = null, activeQuestion = null, worker = null, workerReady = null, job = null, runTimeout = null, loadTimeout = null, initReject = null, route = '', toastTimer;
try { const stored = JSON.parse(localStorage.getItem(STORAGE) || '{}'); if(stored && typeof stored === 'object' && !Array.isArray(stored)) progress = stored; } catch { storageOkay = false; }
const getProgress = id => progress[id] || {};
const statusOf = id => statuses[getProgress(id).status] ? getProgress(id).status : 'new';
const LABELS = {'ml-coding':'ML coding','ml-theory':'ML theory','ml-system-design':'ML system design','llm-genai':'LLM & GenAI','stats-probability':'Statistics & probability','deep-learning':'Deep learning','data-analysis':'Data analysis',dp:'Dynamic programming',bst:'BST','stack-queue':'Stack & queue','two-pointers':'Two pointers','sliding-window':'Sliding window','binary-search':'Binary search','bit-manipulation':'Bit manipulation','linked-list':'Linked list',os:'Operating systems',dbms:'DBMS',sql:'SQL',oop:'OOP','c-cpp-output':'C / C++ output','java-output':'Java output','python-output':'Python output','data-interpretation':'Data interpretation','general-cs':'General CS','digital-electronics':'Digital electronics','computer-architecture':'Computer architecture','software-engineering':'Software engineering'};
const human = str => LABELS[str] || String(str||'').replace(/-/g,' ').replace(/^\w/,c=>c.toUpperCase());
const qCompanies = q => [q.company,...(q.also_asked_by||[])].filter(Boolean);
const cleanUrl = url => { try { let u = new URL(url); return ['http:','https:'].includes(u.protocol) ? u.href : ''; } catch { return ''; } };
function markdown(text) {
  if (!window.marked || !window.DOMPurify) return `<p>${esc(text).replace(/\n/g,'<br>')}</p>`;
  const math=[];
  // Protect TeX from Markdown's underscore and backslash interpretation.
  const readable=String(text||'').replace(/\$\$([\s\S]+?)\$\$|\$([^$\n]+)\$/g,(_,block,inline)=>{const i=math.length;math.push({formula:block??inline,display:block!==undefined});return `ATLASMATHTOKEN${i}END`;});
  let result=DOMPurify.sanitize(marked.parse(readable), {FORBID_TAGS:['img','style','iframe','form','input'],FORBID_ATTR:['style']});
  return result.replace(/ATLASMATHTOKEN(\d+)END/g,(_,i)=>math[i]?`<span data-formula="${esc(math[i].formula)}" data-display="${math[i].display}">${esc(math[i].formula)}</span>`:'');
}
function renderMath(){
  if(window.katex)document.querySelectorAll('[data-formula]').forEach(el=>{if(!el.dataset.rendered){katex.render(el.dataset.formula,el,{throwOnError:false,displayMode:el.dataset.display==='true',trust:false});el.dataset.rendered='true';}});
  // Syntax colours and a copy button for every rendered code block.
  document.querySelectorAll('.prose pre > code').forEach(code=>{
    if(code.dataset.enhanced)return;code.dataset.enhanced='true';
    if(window.hljs){try{hljs.highlightElement(code)}catch{}}
    const btn=document.createElement('button');btn.type='button';btn.className='copy-code';btn.textContent='Copy';
    btn.onclick=async()=>{try{await navigator.clipboard.writeText(code.textContent);btn.textContent='Copied'}catch{const r=document.createRange();r.selectNodeContents(code);getSelection().removeAllRanges();getSelection().addRange(r);btn.textContent='Selected'}setTimeout(()=>btn.textContent='Copy',1500)};
    code.parentElement.appendChild(btn);
  });
}
function toast(message) { $('#toast').textContent = message; $('#toast').classList.add('visible'); clearTimeout(toastTimer); toastTimer = setTimeout(()=>$('#toast').classList.remove('visible'),3500); }
function save(id, changes) {
  progress[id] = {...getProgress(id), ...changes, updated:Date.now()};
  try { localStorage.setItem(STORAGE,JSON.stringify(progress)); storageOkay = true; } catch { storageOkay = false; toast('Browser storage is unavailable or full. Export your progress to keep it.'); }
  renderSidebarProgress();
}
function statusSelect(q) { return `<select class="status-select" data-status="${esc(q.id)}" aria-label="Progress for ${esc(q.title)}">${Object.entries(statuses).map(([k,v])=>`<option value="${k}" ${statusOf(q.id)===k?'selected':''}>${v}</option>`).join('')}</select>`; }
function renderSidebarProgress() {
  if (!bank) return;
  const solved = bank.questions.filter(q=>statusOf(q.id)==='solved').length;
  $('#sidebar-progress').innerHTML = `<div class="sidebar-summary"><span>Your progress</span><strong>${solved} / ${bank.questions.length}</strong></div><div class="progress-track"><span style="width:${100*solved/Math.max(1,bank.questions.length)}%"></span></div>`;
}
function renderNav(active) {
  const links = [['overview','◫','Overview'], ...Object.keys(sections).map(id=>[id,`<span class="dot ${id}"></span>`,sections[id].name]),['patterns','↗','Most asked'],['progress','✓','My progress'],['trends','◷','Research'],['coverage','◎','Sources & coverage']];
  $('#nav').innerHTML = links.map(([id,icon,label],i)=>`${i===5?'<div class="nav-divider"></div>':''}<a href="#${id}" ${active===id?'class="active" aria-current="page"':''}><span class="nav-icon" aria-hidden="true">${icon}</span>${label}${sections[id]?`<span class="nav-count">${bank.questions.filter(q=>q.section===id).length}</span>`:''}</a>`).join('');
  renderSidebarProgress();
}
/* ---- Next / previous: the ordered list a question was opened from ---- */
const CONTEXT='prep-atlas-context';
function setContext(label,ids,href){try{sessionStorage.setItem(CONTEXT,JSON.stringify({label,ids,href}))}catch{}}
function contextFor(q){
  let ctx=null;try{ctx=JSON.parse(sessionStorage.getItem(CONTEXT)||'null')}catch{}
  if(!ctx||!Array.isArray(ctx.ids)||!ctx.ids.includes(q.id)){
    const ids=bank.questions.filter(x=>x.section===q.section&&x.subsection===q.subsection).map(x=>x.id);
    ctx={label:`${sections[q.section]?.name} · ${human(q.subsection)}`,ids,href:`#${q.section}?topic=${encodeURIComponent(q.subsection)}`};
  }
  const i=ctx.ids.indexOf(q.id);
  return {...ctx,index:i,prev:ctx.ids[i-1]||null,next:ctx.ids[i+1]||null};
}
function nextTopic(q){
  // The next topic in the same track that still has unsolved questions.
  const topics=[...new Set(bank.questions.filter(x=>x.section===q.section).map(x=>x.subsection))];
  const start=topics.indexOf(q.subsection);
  for(let k=1;k<=topics.length;k++){const t=topics[(start+k)%topics.length];if(t===q.subsection)continue;
    const list=bank.questions.filter(x=>x.section===q.section&&x.subsection===t);
    const first=list.find(x=>statusOf(x.id)!=='solved');if(first)return {topic:t,first,count:list.length};}
  return null;
}
function qnavBar(q){
  const c=contextFor(q),done=c.ids.filter(id=>statusOf(id)==='solved').length;
  const prev=c.prev?`<a href="#question/${encodeURIComponent(c.prev)}" id="prev-question">← Previous</a>`:`<a class="disabled" aria-hidden="true">← Previous</a>`;
  let next;
  if(c.next)next=`<a class="next" href="#question/${encodeURIComponent(c.next)}" id="next-question">Next question →</a>`;
  else{const t=nextTopic(q);next=t?`<a class="next" href="#question/${encodeURIComponent(t.first.id)}" id="next-question" data-topic-jump="${esc(t.topic)}">Next topic: ${esc(human(t.topic))} →</a>`:`<a class="next" href="${esc(c.href||'#'+q.section)}" id="next-question">Back to list →</a>`;}
  return `<nav class="qnav" aria-label="Question navigation">${prev}<div class="qnav-context"><strong>${c.index+1} of ${c.ids.length}</strong> · ${esc(c.label)}<div class="progress-track"><span style="width:${100*done/Math.max(1,c.ids.length)}%"></span></div></div>${next}</nav>`;
}
function nextCta(q){
  const c=contextFor(q);
  if(c.next){const n=bank.questions.find(x=>x.id===c.next);return `<div class="next-cta"><p>Up next: <strong>${esc(n?.title||'')}</strong></p><a class="primary" style="padding:8px 14px;border-radius:8px" href="#question/${encodeURIComponent(c.next)}">Next question →</a></div>`;}
  const t=nextTopic(q);
  return `<div class="next-cta"><p>You've reached the end of <strong>${esc(c.label)}</strong>.</p>${t?`<a class="primary" style="padding:8px 14px;border-radius:8px" href="#question/${encodeURIComponent(t.first.id)}">Start ${esc(human(t.topic))} →</a>`:`<a href="${esc(c.href||'#'+q.section)}">Back to list</a>`}</div>`;
}
function intro(title,subtitle,eyebrow='YOUR WORKSPACE',extra='') { return `<div class="intro"><div><div class="eyebrow">${eyebrow}</div><h1>${title}</h1><p>${subtitle}</p></div>${extra}</div>`; }
function table(questions,limit=null) {
  const rows = limit ? questions.slice(0,limit) : questions;
  if (!rows.length) return `<div class="table-wrap"><div class="empty"><h2>No questions found</h2><p>Try a different topic or clear your filters.</p></div></div>`;
  return `<div class="table-wrap"><table><thead><tr><th>Question</th><th class="company-column">Asked by</th><th>Difficulty</th><th>Progress</th></tr></thead><tbody>${rows.map(q=>`<tr class="question-list-row ${statusOf(q.id)==='solved'?'is-solved':''}"><td><a class="question-title" href="#question/${encodeURIComponent(q.id)}">${esc(q.title)}</a><span class="question-subtitle"><span class="dot ${q.section}" aria-hidden="true"></span>${esc(human(q.subsection))} <span aria-hidden="true">·</span> ${q.origin==='local'?'OA paper':q.origin==='practice'?'Practice':'Interview report'}${q.solution?' <span aria-hidden="true">·</span> Solution':''}${q.origin==='web'&&q.confidence!=='reported'?' · Limited evidence':''}</span></td><td class="company-cell">${esc(qCompanies(q).slice(0,2).join(', '))}${qCompanies(q).length>2?` <span class="pill">+${qCompanies(q).length-2}</span>`:''}</td><td><span class="pill ${q.difficulty}">${q.difficulty==='hard'?'Hard':'Easy / Medium'}</span></td><td>${statusSelect(q)}</td></tr>`).join('')}</tbody></table></div>`;
}
function mostAsked(section='') {
  const map = new Map();
  for (const q of bank.questions.filter(q=>!section||q.section===section)) {
    const key = `${q.section}:${q.subsection}`;
    if(!map.has(key)) map.set(key,{key,section:q.section,name:q.subsection,questions:[],companies:new Set(),reports:0});
    const row = map.get(key);row.questions.push(q);
    if(q.origin!=='practice') qCompanies(q).filter(c=>c!=='General').forEach(c=>row.companies.add(c));
    row.reports += (q.sources||[]).length;
  }
  return [...map.values()].sort((a,b)=>b.companies.size-a.companies.size||b.questions.length-a.questions.length);
}
function renderOverview() {
  const qs = bank.questions, solved = qs.filter(q=>statusOf(q.id)==='solved').length, touched = qs.filter(q=>statusOf(q.id)!=='new').length;
  const companies = new Set(qs.flatMap(q=>qCompanies(q)).filter(c=>c!=='General'));
  const popular = mostAsked().slice(0,4);
  const recent = qs.filter(q=>getProgress(q.id).updated).sort((a,b)=>getProgress(b.id).updated-getProgress(a.id).updated);
  const suggested = recent.length?recent:qs.filter(q=>q.checker).slice(0,4);
  $('#main').innerHTML = intro('Placement, one pattern at a time.','A focused question bank for coding rounds, AI & ML interviews, aptitude and core CS. Pick a track and keep moving.','PREPARE WITH A PLAN','<span class="round-label">Four tracks. One workspace.</span>')+
    `<div class="stats"><div class="stat"><div class="stat-label">Practice questions<span class="stat-icon">▤</span></div><strong>${qs.length}</strong><small>Distinct problems and interview prompts</small></div><div class="stat"><div class="stat-label">Companies covered<span class="stat-icon">▦</span></div><strong>${companies.size}</strong><small>Across local material and web reports</small></div><div class="stat"><div class="stat-label">Questions solved<span class="stat-icon">✓</span></div><strong>${solved}<span class="muted" style="font-size:15px"> / ${qs.length}</span></strong><small>${touched} started · ${Math.round(100*solved/Math.max(1,qs.length))}% complete</small></div><div class="stat"><div class="stat-label">Ready for review<span class="stat-icon">↻</span></div><strong>${qs.filter(q=>statusOf(q.id)==='revisit').length}</strong><small>Your saved revisit list</small></div></div>`+
    `<div class="dashboard-grid"><div><div class="section-heading"><h2>Choose your track</h2><span class="muted" style="font-size:10px">Build understanding. Then build speed.</span></div><div class="track-grid">${Object.entries(sections).map(([id,s])=>{const list=qs.filter(q=>q.section===id),done=list.filter(q=>statusOf(q.id)==='solved').length;return `<a class="track-card ${id}" href="#${id}"><div class="track-card-top"><span class="track-symbol">${s.symbol}</span><h3>${s.name}</h3><span class="arrow">→</span></div><p>${s.desc}</p><div class="progress-track"><span style="width:${100*done/Math.max(1,list.length)}%"></span></div><div class="track-card-bottom"><span>${list.length} questions</span><span>${done} solved</span></div></a>`}).join('')}</div><div class="recent"><div class="section-heading"><h2>${recent.length?'Continue where you left off':'Start with a coding pattern'}</h2><a href="#${recent.length?'progress':'dsa'}">View all →</a></div>${table(suggested,4)}</div></div><aside class="dashboard-side"><div class="focus-panel"><div class="eyebrow">TODAY’S FOCUS</div><h2>Understand the pattern.<br>Skip the repetition.</h2><p>Similar questions are grouped with their company tags. Spend your time on the variations that teach you something new.</p><a href="#patterns">Explore patterns →</a></div><div class="panel"><h3>Frequently represented topics</h3><p class="subheading">Ranked by companies in this collection, not hiring-wide frequency.</p>${popular.map(t=>`<div class="topic-row"><div><a href="#${t.section}?topic=${encodeURIComponent(t.name)}">${esc(human(t.name))}</a><span class="muted">${t.companies.size} companies</span></div><div class="progress-track"><span style="width:${100*t.companies.size/Math.max(1,popular[0]?.companies.size)}%"></span></div></div>`).join('')}<a class="source-link" href="#coverage">See collection coverage ↗</a></div></aside></div>`;
  if(!storageOkay) $('#main').insertAdjacentHTML('afterbegin','<div class="callout warning">Progress storage is unavailable. Use Export progress to keep a backup.</div>');
}
function filterSelect(key,label,values) {return `<select id="filter-${key}" aria-label="${label}"><option value="">${label}</option>${values.map(v=>{const val=Array.isArray(v)?v[0]:v,txt=Array.isArray(v)?v[1]:v;return `<option value="${esc(val)}" ${filters[key]===val?'selected':''}>${esc(txt)}</option>`}).join('')}</select>`;}
function filtered(list) {
  const words=filters.search.toLowerCase().trim().split(/\s+/).filter(Boolean);
  return list.filter(q=>(!filters.company||qCompanies(q).includes(filters.company))&&(!filters.topic||q.subsection===filters.topic||(q.topics||[]).includes(filters.topic))&&(!filters.difficulty||q.difficulty===filters.difficulty)&&(!filters.status||statusOf(q.id)===filters.status)&&(!filters.origin||q.origin===filters.origin)&&(!filters.role||(q.role||'').toLowerCase().includes(filters.role.toLowerCase()))&&words.every(w=>[q.title,q.statement,q.pattern,q.subsection,...qCompanies(q),...(q.topics||[])].join(' ').toLowerCase().includes(w)));
}
function renderBank(section) {
  const list=bank.questions.filter(q=>['progress','all'].includes(section)||q.section===section), s=sections[section];
  const companies=[...new Set(list.flatMap(q=>qCompanies(q)))].sort();
  const topics=[...new Set(list.map(q=>q.subsection))].sort();
  $('#main').innerHTML = section==='progress'?intro('Your practice, saved.','Review attempts, revisit problems and keep your notes close. Progress is personal to this browser.'):section==='all'?intro(filters.company||'All questions','Company questions across DSA, AI & ML, aptitude and core CS.','COMPANY QUESTION BANK'):intro(s.name,s.desc,'QUESTION BANK',`<span class="round-label">${list.length} questions · ${topics.length} topics</span>`);
  // Topic chips: work through a track one topic at a time.
  const chipTopics=topics.map(t=>{const qs=list.filter(q=>q.subsection===t);return {t,n:qs.length,done:qs.filter(q=>statusOf(q.id)==='solved').length}}).sort((a,b)=>b.n-a.n);
  if(sections[section])$('#main').insertAdjacentHTML('beforeend',`<div class="topic-strip" role="toolbar" aria-label="Topics"><button class="topic-chip ${!filters.topic?'active':''}" data-chip="">All <span class="count">${list.length}</span></button>${chipTopics.map(c=>`<button class="topic-chip ${filters.topic===c.t?'active':''}" data-chip="${esc(c.t)}">${esc(human(c.t))} <span class="count">${c.done}/${c.n}</span><span class="mini" aria-hidden="true"><span style="width:${100*c.done/c.n}%"></span></span></button>`).join('')}</div>`);
  $('#main').insertAdjacentHTML('beforeend',`<div class="filters"><div class="search-wrap"><span aria-hidden="true">⌕</span><input id="search" aria-label="Search questions" placeholder="Search questions, patterns or keywords…" value="${esc(filters.search)}"></div><div class="filter-row">${filterSelect('company','All companies',companies)}${filterSelect('topic','All topics',topics.map(t=>[t,human(t)]))}${filterSelect('difficulty','All difficulties',[['easy-medium','Easy / Medium'],['hard','Hard']])}${filterSelect('status','All progress',Object.entries(statuses))}${filterSelect('origin','All sources',[['local','Local OA'],['web','Web report'],['practice','Practice adaptation']])}${section==='ml'?filterSelect('role','All roles',[['MLE','ML engineer'],['AS','Applied scientist'],['DS','Data scientist'],['Research','Research']]):''}<button id="clear-filters">Clear</button><span id="results-count" class="results-count"></span></div></div><div id="question-results"></div>`);
  function renderResults(){
    let visible=filtered(list); if(section==='progress'&&!filters.status) visible=visible.filter(q=>statusOf(q.id)!=='new'||getProgress(q.id).notes);
    const size=20,pages=Math.ceil(visible.length/size);page=Math.max(0,Math.min(page,pages-1));
    $('#results-count').textContent=`${visible.length} result${visible.length===1?'':'s'}`;
    const ctxLabel=section==='progress'?'My progress':section==='all'?(filters.company||'All questions'):`${s.name}${filters.topic?' · '+human(filters.topic):''}${filters.company?' · '+filters.company:''}`;
    const qs=new URLSearchParams(Object.entries(filters).filter(([,v])=>v));setContext(ctxLabel,visible.map(q=>q.id),`#${section}${qs.toString()?'?'+qs:''}`);
    document.querySelectorAll('[data-chip]').forEach(b=>b.classList.toggle('active',b.dataset.chip===filters.topic));
    $('#question-results').innerHTML=table(visible.slice(page*size,(page+1)*size));
    if(visible.length) $('#question-results .table-wrap').insertAdjacentHTML('beforeend',`<div class="pagination"><span>Showing ${page*size+1}–${Math.min((page+1)*size,visible.length)} of ${visible.length}</span><div><button id="prev-page" ${page===0?'disabled':''}>← Previous</button><button id="next-page" ${page+1>=pages?'disabled':''}>Next →</button></div></div>`);
    if($('#prev-page')) $('#prev-page').onclick=()=>{page--;renderResults()};if($('#next-page')) $('#next-page').onclick=()=>{page++;renderResults()};
  }
  $('#search').oninput=e=>{filters.search=e.target.value;page=0;renderResults()};
  for(const key of ['company','topic','difficulty','status','origin','role']){const el=$(`#filter-${key}`);if(el)el.onchange=e=>{filters[key]=e.target.value;page=0;renderResults()};}
  $('#clear-filters').onclick=()=>{for(const k in filters) filters[k]='';page=0;renderBank(section)};
  document.querySelectorAll('[data-chip]').forEach(b=>b.onclick=()=>{filters.topic=b.dataset.chip;page=0;const sel=$('#filter-topic');if(sel)sel.value=filters.topic;renderResults()});
  renderResults();
}
function sourceCard(q) {
  return `<div class="panel source-card"><h3>Question provenance</h3><div class="badge-row"><span class="pill">${q.origin==='local'?'Local OA archive':q.origin==='practice'?'Practice adaptation':'Web interview report'}</span></div><p style="margin-top:12px">${q.origin==='local'?'Transcribed from the local archive. Personal details and source images are excluded.':q.origin==='practice'?'An original exercise based on a pattern in the collection. Added constraints and tests are for practice; this wording is not claimed to be an actual OA.':'Paraphrased from the saved research. Company associations are reports, not independently confirmed interview questions.'}</p>${q.confidence&&q.confidence!=='reported'?`<div class="callout warning">${esc(q.evidence_note||'Limited evidence. The report may rely on a snippet, an older account or a compilation.')}</div>`:''}${q.role?`<p><strong>Role:</strong> ${esc(q.role)}<br><strong>Round:</strong> ${esc(q.round||'Not recorded')}</p>`:''}${(q.sources||[]).map(src=>cleanUrl(src.url)?`<a class="source-link" href="${esc(cleanUrl(src.url))}" target="_blank" rel="noopener noreferrer">${esc(src.label||'Source')} ↗${src.date?`<span class="muted"> · ${esc(src.date)}</span>`:''}</a>`:'').join('')}${q.leetcode&&cleanUrl(q.leetcode.url)?`<a class="source-link" href="${esc(cleanUrl(q.leetcode.url))}" target="_blank" rel="noopener noreferrer">${esc(q.leetcode.name)} ↗<small class="muted"> (${esc(q.leetcode.similarity||'related')})</small></a>`:''}</div>`;
}
function questionBody(q) {
  let out=markdown(q.statement);
  if(q.practice_spec)out+=`<div class="callout neutral"><strong>Conventions for the practice checks</strong>${markdown(q.practice_spec)}${markdown('```python\n'+q.practice_signature+'\n```')}The source statement above is preserved. The runner checks this explicitly specified function interface.</div>`;
  for(const [key,title] of [['input_format','Input'],['output_format','Output'],['function_signature','Function signature'],['constraints','Constraints']]) if(q[key]) out+=`<h3 class="detail-heading">${title}</h3>${markdown(key==='function_signature'?`\`\`\`python\n${q[key]}\n\`\`\``:q[key])}`;
  for(const [i,e] of (q.examples||[]).entries()) out+=`<div class="example"><h3 class="detail-heading">Example ${i+1}</h3><div class="example-label">Input</div><pre>${esc(e.input)}</pre><div class="example-label">Output</div><pre>${esc(e.output)}</pre>${e.explanation?markdown(e.explanation):''}</div>`;
  if(q.notes) out+=`<div class="callout warning">${esc(q.notes)}</div>`;
  if(q.options?.length) out+=`<fieldset style="border:0;padding:0;margin:24px 0 0"><legend class="detail-heading">Choose an answer</legend>${q.options.map((v,i)=>`<label class="mcq-option" data-option="${i}"><input type="radio" name="answer" value="${i}"><span class="bubble" aria-hidden="true">${String.fromCharCode(65+i)}</span><span>${markdown(v).replace(/^<p>|<\/p>\s*$/g,'')}</span></label>`).join('')}</fieldset><button id="check-answer" class="primary" style="margin-top:13px">Check answer</button><div id="answer-result" aria-live="polite"></div>`;
  else if(q.type==='numeric'&&q.answer)out+=`<div class="section-space"><label for="numeric-answer">Your answer</label><input id="numeric-answer" class="numeric-answer" placeholder="A number or fraction, e.g. 1/4" autocomplete="off"><button id="check-answer" class="primary">Check answer</button><div id="answer-result" aria-live="polite"></div></div>`;
  return out;
}
function renderQuestion(id) {
  const q=bank.questions.find(q=>q.id===id); if(!q){$('#main').innerHTML=intro('Question not found.','This link may belong to a different question bank.')+'<a href="#overview">Back to overview →</a>';return;}
  activeQuestion=q;
  const coding=q.type==='coding'||q.subsection==='ml-coding';
  $('#main').innerHTML=`<a class="back-link" href="#${q.section}">← Back to ${esc(sections[q.section]?.name||'questions')}</a><div class="eyebrow">${esc(sections[q.section]?.name)} / ${esc(human(q.subsection))}</div><h1 class="detail-title">${esc(q.title)}</h1><div class="detail-meta"><span class="pill ${q.difficulty}">${q.difficulty==='hard'?'Hard':'Easy / Medium'}</span>${qCompanies(q).map(c=>`<span class="pill">${esc(c)}</span>`).join('')}${statusSelect(q)}</div><div class="detail-grid ${coding?'':'reading'}"><div class="detail-panel"><div class="tabs" role="tablist" aria-label="Question details"><button role="tab" aria-selected="true" id="tab-problem" aria-controls="detail-content" class="active" data-tab="problem">Problem</button><button role="tab" aria-selected="false" id="tab-approach" aria-controls="detail-content" data-tab="approach">Approach</button><button role="tab" aria-selected="false" id="tab-solution" aria-controls="detail-content" data-tab="solution">Solution${q.solution?'':' <span class="muted">(soon)</span>'}</button><button role="tab" aria-selected="false" id="tab-notes" aria-controls="detail-content" data-tab="notes">My notes</button></div><div id="detail-content" class="detail-content prose" role="tabpanel" aria-labelledby="tab-problem">${questionBody(q)}</div></div><div class="detail-side">${coding?`<div class="detail-panel"><div class="editor-head"><strong>Python 3.12</strong><span class="muted">NumPy included · browser execution</span></div><div id="code-editor" class="editor" aria-label="Python code editor"></div><div class="runner-controls"><button id="run-code" class="primary">▶ Run</button>${q.checker?'<button id="check-code">✓ Check solution</button>':''}<button id="stop-code" hidden>■ Stop</button><button id="reset-code" title="Restore starter code">↺ Reset</button><span id="runtime-status" class="runtime-label">Ready when you are</span></div><div class="console"><label for="stdin">Standard input</label><textarea id="stdin" spellcheck="false" placeholder="Input for input() or sys.stdin">${esc(getProgress(q.id).stdin??q.default_stdin??'')}</textarea><div class="output-title"><span>Output</span><span id="execution-time"></span></div><pre id="output" aria-live="polite">Run your code to see output here.</pre></div><div class="runner-note">${q.checker?'Checks use additional practice cases. Passing them is useful feedback, not a guarantee of correctness for every input.':'No verified test suite is attached. Run code with your own input; use Approach to review the intended idea.'} Ctrl / ⌘ + Enter to run. Code and input save automatically.</div></div><div style="margin-top:16px">${sourceCard(q)}</div>`:sourceCard(q)+`<div class="panel"><h3>Make this pattern stick</h3><p class="subheading">Explain the approach without looking. Write down the step you missed, then mark the question for a revisit.</p><div class="badge-row">${(q.topics||[]).map(t=>`<a class="pill" href="#${q.section}?topic=${encodeURIComponent(t)}">${esc(human(t))}</a>`).join('')}</div></div>`}</div></div>${qnavBar(q)}`;
  const attachAnswer=()=>{if(!$('#check-answer'))return;$('#check-answer').onclick=()=>{
    const selected=$('input[name=answer]:checked'),numeric=$('#numeric-answer'); if(!selected&&!numeric?.value.trim()){toast(q.options?'Choose an option first.':'Enter an answer first.');return;}
    const chosen=numeric?numeric.value.trim():q.options[Number(selected.value)];
    const number=v=>{let s=String(v).trim();if(/^[+-]?\d+(\.\d+)?\s*\/\s*[+-]?\d+(\.\d+)?$/.test(s)){const [a,b]=s.split('/').map(Number);return b?a/b:NaN;}return /^[+-]?(\d+(\.\d*)?|\.\d+)$/.test(s)?Number(s):NaN;};
    const correct=chosen===q.answer||(numeric&&Number.isFinite(number(chosen))&&Number.isFinite(number(q.answer))&&Math.abs(number(chosen)-number(q.answer))<=1e-8*Math.max(1,Math.abs(number(q.answer))));
    save(q.id,{status:correct&&q.answer_confidence==='high'?'solved':statusOf(q.id)==='new'?'attempted':statusOf(q.id),choice:numeric?chosen:Number(selected.value)});
    document.querySelectorAll(`[data-status="${CSS.escape(q.id)}"]`).forEach(s=>s.value=statusOf(q.id));
    if(q.options){const ci=q.options.indexOf(q.answer);document.querySelectorAll('.mcq-option').forEach(el=>{const i=Number(el.dataset.option);el.classList.toggle('is-correct',i===ci);el.classList.toggle('is-wrong',!correct&&i===Number(selected.value))});}
    $('#answer-result').innerHTML=`<div class="answer-result ${correct?'':'wrong'}"><span class="verdict">${q.answer_confidence==='low'?'The saved answer is uncertain.':correct?'Correct.':'Not quite.'}</span>${q.answer?` Answer: <strong>${esc(q.answer)}</strong>`:' No confirmed answer is recorded.'}${q.explanation?markdown(q.explanation):''}${q.solution?'<button class="quiet" id="open-solution" style="padding-left:0;color:var(--accent);font-weight:600">Read the full solution →</button>':''}</div>${nextCta(q)}`;
    if($('#open-solution'))$('#open-solution').onclick=()=>{revealSolution=true;$('#tab-solution').click()};
  }};
  attachAnswer();
  document.querySelectorAll('[data-tab]').forEach(btn=>btn.onclick=()=>{
    const tab=btn.dataset.tab;
    document.querySelectorAll('[data-tab]').forEach(el=>{el.classList.toggle('active',el===btn);el.setAttribute('aria-selected',String(el===btn))});
    $('#detail-content').setAttribute('aria-labelledby',btn.id);
    if(tab==='problem'){$('#detail-content').innerHTML=questionBody(q);attachAnswer()}
    else if(tab==='solution'){renderSolution(q)}
    else if(tab==='approach'){$('#detail-content').innerHTML=`<h3>${q.type==='subjective'?'Discussion outline':'Approach & explanation'}</h3>${markdown(q.explanation||'No worked explanation is recorded yet. Use the linked source as a starting point; treat this prompt as open-ended practice.')}${q.answer?`<h3>Recorded answer</h3>${markdown(q.answer)}<p class="muted">Confidence: ${esc(q.answer_confidence||'not recorded')}</p>`:''}`}
    else{$('#detail-content').innerHTML='<h3>Your notes</h3><p class="muted">Capture the idea, a mistake, or a reason to revisit.</p><textarea id="notes" class="notes-input" aria-label="Your notes" placeholder="What did you learn? What would you do differently?"></textarea><p class="subheading" style="margin-top:10px">Saved automatically in this browser.</p>';$('#notes').value=getProgress(q.id).notes||'';$('#notes').oninput=e=>save(q.id,{notes:e.target.value});}
  });
  if(coding) setupEditor(q);
}
let revealSolution=false;
function renderSolution(q){
  const box=$('#detail-content');
  if(!q.solution){box.innerHTML=`<div class="solution-gate"><h3>The detailed solution is on its way</h3><p>A full worked solution for this question is still being written. Until then, the Approach tab explains the core idea.</p><button id="go-approach">Read the approach</button></div>`;$('#go-approach').onclick=()=>$('#tab-approach').click();return;}
  if(!revealSolution&&!getProgress(q.id).revealed){
    box.innerHTML=`<div class="solution-gate"><h3>Try it first</h3><p>Give the problem an honest attempt. The full solution covers the idea, the reasoning, ${q.type==='coding'?'tested Python code, a dry run ':'every step '}and the usual traps.</p><button class="primary" id="reveal-solution">Show the full solution</button></div>`;
    $('#reveal-solution').onclick=()=>{revealSolution=true;save(q.id,{revealed:true});renderSolution(q)};return;
  }
  // Prefer the code block that defines the function the practice checks call.
  const blocks=[...q.solution.matchAll(/```(?:python|py)\n([\s\S]*?)```/g)].map(m=>m[1]);
  const fn=q.checker?.function;
  const code=(fn&&blocks.find(b=>new RegExp(`^def ${fn}\\s*\\(`,'m').test(b)))||blocks[0];
  box.innerHTML=`${code&&editor?'<div class="solution-actions"><button id="load-solution">Load this solution into the editor</button></div>':''}${markdown(q.solution)}${nextCta(q)}`;
  if($('#load-solution'))$('#load-solution').onclick=e=>{
    const b=e.currentTarget;if(b.dataset.confirm!=='1'){b.dataset.confirm='1';b.textContent='Replace your code? Click again to confirm';return;}
    save(q.id,{prevCode:editor.getValue()});editor.setValue(code,-1);save(q.id,{code});b.textContent='Loaded. Your previous code is kept in this browser';b.disabled=true;
  };
}
function setupEditor(q) {
  const starter=q.starter||'# Write your solution here.\n# Use input() / sys.stdin for input, or implement the given signature.\n\n';
  const code=getProgress(q.id).code??starter;
  if(window.ace){
    ace.config.set('basePath','vendor');editor=ace.edit('code-editor');editor.session.setMode('ace/mode/python');editor.session.setUseWorker(false);editor.setOptions({fontSize:'12px',showPrintMargin:false,tabSize:4,useSoftTabs:true,wrap:true});editor.setValue(code,-1);setEditorTheme();
    editor.on('change',()=>save(q.id,{code:editor.getValue()}));editor.commands.addCommand({name:'run',bindKey:{win:'Ctrl-Enter',mac:'Command-Enter'},exec:()=>runCode(false)});
  }else{const ta=document.createElement('textarea');ta.className='editor';ta.setAttribute('aria-label','Python code');ta.value=code;$('#code-editor').replaceWith(ta);ta.id='code-editor';editor={getValue:()=>ta.value,setValue:v=>{ta.value=v},destroy:()=>{}};ta.oninput=()=>save(q.id,{code:ta.value});}
  $('#stdin').oninput=e=>save(q.id,{stdin:e.target.value});
  $('#run-code').onclick=()=>runCode(false);if($('#check-code'))$('#check-code').onclick=()=>runCode(true);
  $('#stop-code').onclick=()=>stopWorker('Execution stopped.');
  $('#reset-code').onclick=()=>{editor.setValue(starter,-1);save(q.id,{code:starter});toast('Starter code restored.');};
}
function setEditorTheme(){if(editor?.setTheme)editor.setTheme(`ace/theme/${isDark()?'tomorrow_night':'tomorrow'}`)}
function isDark(){const t=document.documentElement.dataset.theme;return t==='dark'||(t==='system'&&matchMedia('(prefers-color-scheme: dark)').matches)}
function runtime(message){if($('#runtime-status'))$('#runtime-status').textContent=message;}
function busy(on){for(const s of ['#run-code','#check-code','#reset-code'])if($(s))$(s).disabled=on;if($('#stop-code'))$('#stop-code').hidden=!on;}
function prepareWorker() {
  if(workerReady)return workerReady;
  worker=new Worker('python-worker.js');const thisWorker=worker;
  workerReady=new Promise((resolve,reject)=>{
    initReject=reject;loadTimeout=setTimeout(()=>{if(worker===thisWorker)stopWorker('Python took too long to load. Try Run again.');},90000);
    worker.onmessage=e=>{if(worker!==thisWorker)return;const data=e.data;if(data.type==='status'){runtime(data.message);return;}if(data.type==='ready'){clearTimeout(loadTimeout);initReject=null;resolve();}if(data.type==='init-error'){clearTimeout(loadTimeout);initReject=null;reject(new Error(data.error));}if(data.type==='result'&&job&&data.id===job.id){clearTimeout(runTimeout);const j=job;job=null;j.resolve(data);}};
    worker.onerror=e=>{clearTimeout(loadTimeout);clearTimeout(runTimeout);initReject=null;reject(new Error(e.message||'Python worker failed.'));if(job){job.reject(new Error(e.message||'Python worker failed.'));job=null;}};
  });
  return workerReady;
}
async function runCode(check) {
  if(job||!activeQuestion||!editor)return;
  const q=activeQuestion,code=editor.getValue(),stdin=$('#stdin').value;
  const token={};window.currentRun=token;busy(true);runtime('Loading Python…');$('#output').textContent='Starting Python. The first run loads the local runtime…';
  save(q.id,{code,stdin,status:statusOf(q.id)==='new'?'attempted':statusOf(q.id)});
  try{
    try{await prepareWorker()}catch(e){throw new Error(`Python couldn't start (${e.message}).\n\nReload the page with Ctrl + Shift + R (Cmd + Shift + R on Mac), then press Run again. If it keeps failing, try another browser.`)}
    if(window.currentRun!==token||activeQuestion?.id!==q.id)return;
    runtime('Running…');$('#output').textContent=check?'Checking practice cases…':'Running…';
    const result=await new Promise((resolve,reject)=>{
      const id=Date.now()+Math.random();job={id,resolve,reject};runTimeout=setTimeout(()=>stopWorker('Time limit exceeded (10 seconds).'),10000);
      worker.postMessage({id,code,stdin,checker:check?q.checker:null});
    });
    if(window.currentRun!==token||activeQuestion?.id!==q.id)return;
    $('#output').textContent=result.error?result.error:result.output||'(No output)';$('#execution-time').textContent=`${result.elapsed.toFixed(0)} ms`;
    if(result.passed!==undefined){if(result.passed){save(q.id,{status:'solved'});document.querySelectorAll(`[data-status="${CSS.escape(q.id)}"]`).forEach(s=>s.value='solved');runtime('Practice checks passed');toast('Practice checks passed. Marked solved.');if(!$('.console .next-cta'))$('#output').insertAdjacentHTML('afterend',nextCta(q));}else runtime('Review failing cases');}else runtime(result.error?'Execution error':'Run complete');
  }catch(e){if(window.currentRun===token){if(activeQuestion?.id===q.id&&$('#output')){$('#output').textContent=e.message;runtime('Ready to retry');}if(worker){worker.terminate();worker=null;}workerReady=null;}
  }finally{if(window.currentRun===token){busy(false);window.currentRun=null;}}
}
function stopWorker(message='') {
  if(worker)worker.terminate();worker=null;workerReady=null;clearTimeout(runTimeout);clearTimeout(loadTimeout);
  if(initReject){const reject=initReject;initReject=null;reject(new Error(message||'Execution stopped.'));}
  if(job){const j=job;job=null;j.reject(new Error(message||'Execution stopped.'));}
  window.currentRun=null;busy(false);if(message&&$('#output'))$('#output').textContent=message;runtime('Stopped');
}
function renderPatterns() {
  const topics=mostAsked();
  $('#main').innerHTML=intro('Patterns worth your time.','Explore topics across companies, then practise the distinct variations. Counts describe this collection; they are not a prediction of your next OA.','MOST ASKED IN THIS COLLECTION')+`<div class="topic-grid">${topics.map(t=>{const solved=t.questions.filter(q=>statusOf(q.id)==='solved').length;return `<div class="panel topic-card"><div class="badge-row"><span class="pill">${sections[t.section]?.name}</span><span class="pill">${t.companies.size} companies</span></div><h3 style="margin-top:15px">${esc(human(t.name))}</h3><p>${esc([...t.companies].slice(0,4).join(', '))}${t.companies.size>4?'…':''}</p><div class="progress-track"><span style="width:${100*solved/Math.max(1,t.questions.length)}%"></span></div><p>${t.questions.length} distinct prompts · ${solved} solved</p><a href="#${t.section}?topic=${encodeURIComponent(t.name)}">Practise this topic →</a></div>`}).join('')}</div>`;
}
function renderTrends() {
  $('#main').innerHTML=intro('The research behind your prep.','Saved reports cover recent interview prompts and company OA formats. Dates, round details and verification limits remain attached to the sources.','WEB RESEARCH')+`<div class="report-list">${bank.reports.map(r=>`<div class="report-card"><div class="eyebrow">SAVED ${esc(bank.collected)}</div><h3>${esc(r.title)}</h3><p>${esc(r.description)}</p><button data-report="${esc(r.file)}">Read report →</button></div>`).join('')}</div><div class="callout warning">Research is partial. Some entries come from snippets or community compilations, and listing dates may differ from interview dates. Older formats are kept with their dates; they are not asserted to be current.</div><div id="report-body" class="panel prose section-space"><h2>Pick a report to read.</h2><p>Company formats, resource links and the original source caveats are preserved.</p></div>`;
  document.querySelectorAll('[data-report]').forEach(btn=>btn.onclick=async()=>{try{const res=await fetch(`data/${btn.dataset.report}`);if(!res.ok)throw Error('Report could not be loaded.');$('#report-body').innerHTML=markdown(await res.text());$('#report-body').scrollIntoView({behavior:'smooth',block:'start'});}catch(e){toast(e.message)}});
}
function renderCoverage() {
  const qs=bank.questions;
  $('#main').innerHTML=intro('Know what you’re practising.','Local OA transcriptions, paraphrased web reports and original practice adaptations have separate provenance. This page makes the gaps visible.','SOURCES & COVERAGE')+`<div class="stats"><div class="stat"><div class="stat-label">Local OA questions</div><strong>${qs.filter(q=>q.origin==='local').length}</strong><small>Transcribed entries retained after deduplication</small></div><div class="stat"><div class="stat-label">Web prompts</div><strong>${qs.filter(q=>q.origin==='web').length}</strong><small>Paraphrases with reported company tags</small></div><div class="stat"><div class="stat-label">Practice adaptations</div><strong>${qs.filter(q=>q.origin==='practice').length}</strong><small>Original exercises with added specifications</small></div><div class="stat"><div class="stat-label">Tested coding exercises</div><strong>${qs.filter(q=>q.checker).length}</strong><small>Verified reference solutions and practice checks</small></div></div><div class="outline-grid"><div class="panel"><h3>How duplicate patterns are handled</h3><p class="subheading">Cosmetic repeats are merged. A variation stays separate when it changes the constraints, strategy or learning objective. Company associations and source references are combined rather than discarded.</p></div><div class="panel"><h3>Your data & source privacy</h3><p class="subheading">Progress, notes and code live in browser storage. There are no accounts or cross-device sync. Export a backup before changing browsers. Source screenshots and the private OCR index are excluded from this website.</p></div></div><div class="callout warning">The archive contains ${bank.coverage.total_files} deduplicated source files. ${bank.coverage.reviewed_files} have contributed to saved question transcriptions or explicit skips. Remaining files are still awaiting content review; OCR extraction alone does not count as a reviewed question.</div><div class="section-heading section-space"><h2>Company coverage</h2><span class="muted" style="font-size:10px">Last built ${esc(bank.collected)}</span></div><div class="table-wrap"><table class="coverage-table"><thead><tr><th>Company</th><th>Archive files</th><th>Reviewed files</th><th>Local questions</th><th>Web prompts</th></tr></thead><tbody>${bank.coverage.companies.map(c=>`<tr><td><a href="#all?company=${encodeURIComponent(c.name)}">${esc(c.name)}</a></td><td>${c.files}</td><td>${c.reviewed}</td><td>${qs.filter(q=>q.origin==='local'&&qCompanies(q).includes(c.name)).length}</td><td>${qs.filter(q=>q.origin==='web'&&qCompanies(q).includes(c.name)).length}</td></tr>`).join('')}</tbody></table></div>`;
}
function navigate() {
  const hash=location.hash.slice(1)||'overview', [path,query='']=hash.split('?'), [view,...args]=path.split('/');
  if(editor){editor.destroy();editor=null;}if(job||window.currentRun)stopWorker();activeQuestion=null;revealSolution=false;
  if(route!==view){filters={search:'',company:'',topic:'',difficulty:'',status:'',origin:'',role:''};page=0;}route=view;
  const params=new URLSearchParams(query); for(const [key,value]of params)if(key in filters)filters[key]=value;
  document.body.classList.remove('menu-open');$('#menu').setAttribute('aria-expanded','false');
  const label=sections[view]?.name||({overview:'Overview',all:'All questions',patterns:'Most asked patterns',progress:'My progress',trends:'Web research',coverage:'Sources & coverage',question:'Question'}[view]||'Overview');
  const qv=view==='question'?bank.questions.find(q=>q.id===decodeURIComponent(args.join('/'))):null;
  $('#breadcrumb').innerHTML=qv?`<a href="#${qv.section}">${esc(sections[qv.section]?.name)}</a><span>/</span><a href="#${qv.section}?topic=${encodeURIComponent(qv.subsection)}">${esc(human(qv.subsection))}</a>`:esc(label);document.title=`${label} · Prep Atlas`;renderNav(view==='question'?bank.questions.find(q=>q.id===decodeURIComponent(args.join('/')))?.section:view);
  if(view==='question')renderQuestion(decodeURIComponent(args.join('/')));
  else if(sections[view]||['progress','all'].includes(view))renderBank(view);
  else if(view==='patterns')renderPatterns();else if(view==='trends')renderTrends();else if(view==='coverage')renderCoverage();else renderOverview();
  renderMath();window.scrollTo(0,0);
}
new MutationObserver(()=>renderMath()).observe($('#main'),{childList:true,subtree:true});
document.addEventListener('change',e=>{if(e.target.matches('[data-status]')){save(e.target.dataset.status,{status:e.target.value});if(route==='overview'||route==='patterns')navigate();}});
$('#theme').value=document.documentElement.dataset.theme||'system';
$('#theme').onchange=e=>{document.documentElement.dataset.theme=e.target.value;try{localStorage.setItem('prep-atlas-theme',e.target.value)}catch{}setEditorTheme()};
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',setEditorTheme);
$('#menu').onclick=()=>{const open=document.body.classList.toggle('menu-open');$('#menu').setAttribute('aria-expanded',String(open))};
$('#backup').onclick=()=>{const blob=new Blob([JSON.stringify({format:'prep-atlas',version:1,exported:new Date().toISOString(),progress},null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='prep-atlas-progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);toast('Progress backup exported.')};
$('#restore').onclick=()=>$('#import-file').click();
$('#import-file').onchange=async e=>{const file=e.target.files[0];if(!file)return;try{
  if(file.size>10*1024*1024)throw Error('Backup is too large (maximum 10 MB).');
  const data=JSON.parse(await file.text());if(data.format!=='prep-atlas'||data.version!==1||!data.progress||typeof data.progress!=='object'||Array.isArray(data.progress))throw Error('This is not a valid Prep Atlas backup.');
  const known=new Set(bank.questions.map(q=>q.id));let count=0;
  for(const [id,entry]of Object.entries(data.progress)){if(!known.has(id)||!entry||typeof entry!=='object'||Array.isArray(entry))continue;const p={};if(statuses[entry.status])p.status=entry.status;for(const k of ['notes','code','stdin'])if(typeof entry[k]==='string')p[k]=entry[k].slice(0,500000);if(typeof entry.updated==='number'&&Number.isFinite(entry.updated))p.updated=entry.updated;
    if((getProgress(id).updated||0)>(p.updated||0))continue;progress[id]={...getProgress(id),...p};count++;}
  localStorage.setItem(STORAGE,JSON.stringify(progress));navigate();toast(`${count} question records imported. Newer local records were kept.`);
}catch(err){toast(err.message)}finally{e.target.value=''}};
document.addEventListener('keydown',e=>{
  const typing=/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)||document.activeElement.closest?.('.ace_editor');
  if(!typing&&!e.ctrlKey&&!e.metaKey&&!e.altKey&&route==='question'){if(e.key==='n'&&$('#next-question')){e.preventDefault();$('#next-question').click()}if(e.key==='p'&&$('#prev-question')){e.preventDefault();$('#prev-question').click()}}
  if(e.key==='/'&&!typing&&$('#search')){e.preventDefault();$('#search').focus()}if(e.key==='Escape'){document.body.classList.remove('menu-open');$('#menu').setAttribute('aria-expanded','false')}});
window.addEventListener('hashchange',()=>{if(bank)navigate()});
fetch('data/questions.json').then(r=>{if(!r.ok)throw Error('Question bank could not be loaded.');return r.json()}).then(data=>{bank=data;navigate()}).catch(e=>{$('#main').innerHTML=intro('Couldn’t load the question bank.',esc(e.message))+'<p class="muted">Start the local server using START_PREP.cmd, then refresh this page.</p>'});
