"""Compile explicitly curated content. OCR output is NEVER auto-published."""
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path
from practice import make_practice
from outlines import outline

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'site/data'
COLLECTED='2026-10-01'

def canonical(company):
    company=company.replace('**','').strip()
    for prefix in ['Google','Microsoft','Adobe','Amazon','OpenAI','Apple','Uber','LinkedIn','Meta','Samsung']:
        if company.startswith(prefix):return 'Samsung SRIB' if prefix=='Samsung' else prefix
    return {'MSR India':'Microsoft','D. E. Shaw':'DE Shaw'}.get(company,company)

def source_keys(report):
    keys={}
    for line in report.splitlines():
        match=re.match(r'\|\s*([A-Z][A-Z0-9-]+)\s*\|\s*(.*?)\s*\|',line)
        if match:
            url=re.search(r'https?://[^\s|)]+',match[2])
            if url:keys[match[1]]={'url':url[0], 'label':match[1], 'limited':'snippet' in match[2] or 'unverified' in match[2]}
    return keys

def parse_ml():
    text=(ROOT/'research/ai_ml_questions.md').read_text(encoding='utf-8')
    sources=source_keys(text);topic='ml-theory';questions=[]
    topic_map={'1':'ml-theory','2':'stats-probability','3':'deep-learning','4':'llm-genai','5':'ml-coding','6':'ml-system-design','7':'research'}
    # Only equivalent prompts are merged, not whole topics.
    merge_groups=[[25,26,36],[54,160],[94,97],[96,102,106]]
    aliases={n:g[0] for g in merge_groups for n in g}
    merged={}
    for line in text.splitlines():
        match=re.match(r'### (\d+)\.',line)
        if match:
            if match[1]=='8':break  # broad multi-problem lists remain in the original research report
            topic=topic_map.get(match[1],topic)
        if not re.match(r'\|\s*\d+\s*\|',line):continue
        cols=[c.strip() for c in line.strip().strip('|').split('|')]
        if len(cols)!=8:raise ValueError(f'Unexpected research table row: {line}')
        number=int(cols[0]);_,title,company,role,round_,difficulty,src,date=cols
        company=canonical(company)
        refs=[]
        # Handle the report's abbreviated PH-AMZ/AMZ2 notation.
        src=src.replace('PH-AMZ/AMZ2','PH-AMZ / PH-AMZ2')
        for key in sources:
            if re.search(r'(?<![A-Z0-9-])'+re.escape(key)+r'(?![A-Z0-9-])',src):
                refs.append({**sources[key],'date':date})
        for url in re.findall(r'https?://[^\s)]+',src):refs.append({'url':url,'label':'Source','date':date,'limited':True})
        limited=any(s.get('limited') for s in refs) or 'unverified' in src or any(y in date for y in ['2021','2022','2023'])
        q=dict(id=f'web-ml-{aliases.get(number,number):03}',company=company,also_asked_by=[],section='ml',subsection=topic,topics=[topic],
            pattern=title.lower(),difficulty='hard' if difficulty=='H' or '/ H' in difficulty else 'easy-medium',
            type='coding' if topic=='ml-coding' else 'subjective',title=title,statement=title+'.\n\n'+
            ('The saved report contains a short coding prompt, not a complete input/output specification. Clarify shapes and edge cases before implementation. Use the linked source for the reported format.' if topic=='ml-coding' else 'Discuss the question and explain your assumptions, reasoning and trade-offs.'),
            role=role,round=round_,origin='web',sources=refs,confidence='limited' if limited or not refs else 'reported',
            evidence_note='Snippet, compilation or older report. The company association has not been independently confirmed.' if limited else 'The saved report did not retain a direct source link for this entry.',
            explanation=outline(title,topic))
        key=q['id']
        if key in merged:
            old=merged[key]
            if company!=old['company'] and company not in old['also_asked_by']:old['also_asked_by'].append(company)
            for ref in refs:
                if ref not in old['sources']:old['sources'].append(ref)
            continue
        merged[key]=q;questions.append(q)
    return questions

def parse_dsa():
    text=(ROOT/'research/dsa_oa_questions.md').read_text(encoding='utf-8')
    company=None;questions=[];context_source=None;counter=0
    for line in text.splitlines():
        if line.startswith('### '):
            company=canonical(line[4:].split('[')[0].strip());context_source=None
        if line.startswith('Source:'):
            urls=re.findall(r'\]\((https?://[^)]+)\)',line)
            if urls:context_source=urls[0]
        if company not in ['DE Shaw','Samsung SRIB','Navi','Qualcomm','HiLabs']:continue
        if not re.match(r'\|\s*\d+\s*\|',line):continue
        cols=[c.strip() for c in line.strip().strip('|').split('|')]
        if len(cols)<6:continue
        title=cols[1]
        if '[T]' in title or any(w in title.lower() for w in ['questions (linked','2d-array problem','bit-masking problems','ds track','merge intervals, top k']):continue
        if '[u, generic]' in title.lower():continue
        urls=re.findall(r'\]\((https?://[^)]+)\)',line)
        if urls:context_source=urls[0]
        if not context_source:continue
        counter+=1
        difficulty=cols[4];tags=[x.strip() for x in cols[3].split(',')]
        topic={'graph':'graphs','BFS/DFS':'graphs','DP':'dp','trees':'trees','linked list':'linked-list','two pointers':'two-pointers'}.get(tags[0],tags[0].lower().replace(' ','-'))
        title=title.replace('[U]','').strip()
        questions.append(dict(id=f'web-dsa-{counter:03}',company=company,also_asked_by=[],section='dsa',subsection=topic,topics=tags,
           pattern=title.lower(),difficulty='hard' if 'Hard' in difficulty else 'easy-medium',type='coding',title=title,
           statement=title+'\n\nThis is a paraphrased interview prompt. The saved report does not contain a complete problem specification or constraints. Use the linked source and agree on input/output conventions before coding.',
           origin='web',confidence='limited',evidence_note='An interview report or compilation, sometimes older than 2024. It is not confirmed as a current campus OA.',sources=[{'label':'Reported source','url':context_source,'date':cols[-1] if len(cols)>=8 else 'Date uncertain'}],
           explanation='Start by clarifying the precise problem and constraints from the source. Identify the required invariant or state, work through a small example, and test edge cases. The saved report names the pattern but does not include a verified editorial.'))
    return questions

# Addresses that are part of a problem's own sample data (verified), exempt from the leak check for that id only.
SAMPLE_EMAILS={'curated-local-ibm-email-regex':{'a7_1@baddomain.com','abcdef1234@hackerrank.com','julia0_@hackerrank.com','julia@gmail.com','julia@hackerrank.com','julia_0@hackerrank.com','julia_@hackerrank.com','user@hackerrank.com'}}

def main():
    OUT.mkdir(exist_ok=True)
    questions=[];reviewed=set();manifest=json.loads((ROOT/'build/manifest.json').read_text(encoding='utf-8'))
    for path in sorted((ROOT/'build/raw').glob('*.json')):
        batch=json.loads(path.read_text(encoding='utf-8'))
        for skip in batch.get('skipped_files',[]):reviewed.add(skip['file'])
        for q in batch['questions']:
            reviewed.update(q.get('source_files',[]))
            item={k:v for k,v in q.items() if k not in ['source_files','year']}
            # Source notes occasionally mention test identifiers; publish only content caveats.
            if item.get('notes') and re.search(r'candidate|test.*\b[A-Z0-9]{5,}\b',item['notes'],re.I):item.pop('notes')
            item['company']=canonical(item['company']);item['origin']='local';item['sources']=[]
            item['confidence']='limited' if item.get('answer_confidence')=='low' else 'reported'
            if item['confidence']=='limited':item['evidence_note']='The transcription records an ambiguous answer or missing information. Review the explanation and notes.'
            questions.append(item)
    questions+=parse_ml()+parse_dsa()
    practice,_=make_practice()
    # Add checks to the existing archive question instead of listing the same pattern twice.
    attach={'practice-histogram':'b08_devrev_trilogy_amzn_atl-001',
            'practice-distinct-window':'b08_devrev_trilogy_amzn_atl-002',
            'practice-prefix-kth':'b04_gameskraft_misc-001',
            'practice-rod-cutting':'b08_devrev_trilogy_amzn_atl-006'}
    by_id={q['id']:q for q in questions}
    # Repeat screenshots attached to existing questions (see curate_local.alias).
    for path in sorted((ROOT/'build/raw').glob('*.json')):
        for a in json.loads(path.read_text(encoding='utf-8')).get('aliases',[]):
            reviewed.update(a['source_files'])
            target=by_id.get(a['id'])
            if target is None:raise KeyError('alias to unknown id '+a['id'])
            company=canonical(a['company'])
            if company!=target['company'] and company not in target.setdefault('also_asked_by',[]):target['also_asked_by'].append(company)
    for p in practice:
        target=by_id.get(attach.get(p['id']))
        if target:
            target.update(checker=p['checker'],starter=p['starter'],practice_spec=p['statement'],practice_signature=p['function_signature'])
        else:questions.append(p)
    # Merge identical full statements only, or explicit ML aliases above. Never merge by topic alone.
    distinct=[];by_key={}
    for q in questions:
        key=(q['origin'],re.sub(r'\W+',' ',q['statement'].lower()).strip())
        if key in by_key:
            old=by_key[key]
            for company in [q['company']]+q.get('also_asked_by',[]):
                if company!=old['company'] and company not in old['also_asked_by']:old['also_asked_by'].append(company)
            old['sources'].extend(s for s in q.get('sources',[]) if s not in old['sources'])
        else:by_key[key]=q;distinct.append(q)
    # Detailed solutions written separately for questions that predate the solution field.
    final={q['id']:q for q in distinct}
    for path in sorted((ROOT/'build/solutions').glob('*.json')):
        for qid,text in json.loads(path.read_text(encoding='utf-8')).items():
            if qid in final and text.strip():final[qid]['solution']=text
    # LeetCode-style harness (build/make_harness.py): starter signature + verified test cases.
    harness_path=ROOT/'build/harness/harness.json'
    harness=json.loads(harness_path.read_text(encoding='utf-8')) if harness_path.exists() else {}
    for qid,h in harness.items():
        q=final.get(qid)
        if not q or q.get('checker'):continue
        q['starter']=h['starter']
        if h.get('cases'):q['checker']=dict(function=h['function'],params=h['params'],cases=h['cases'],samples=h['samples'],numpy=h.get('numpy',False),source='generated')
    for q in final.values():
        # Hand-written practice checks: name the parameters and treat the first cases as the visible examples.
        ch=q.get('checker')
        if ch and 'samples' not in ch:
            sig=re.match(r'\s*def\s+\w+\((.*)\)',q.get('practice_signature',''))
            ch['params']=[p.split('=')[0].split(':')[0].strip() for p in sig.group(1).split(',')] if sig else []
            ch['samples']=min(2,len(ch['cases']))
    # Short sections appended to an existing solution (e.g. the practice-check interface).
    addenda=ROOT/'build/solution_addenda.json'
    if addenda.exists():
        for qid,text in json.loads(addenda.read_text(encoding='utf-8')).items():
            if qid not in final:raise KeyError('addendum for unknown id '+qid)
            final[qid]['solution']=final[qid].get('solution','').rstrip()+'\n\n'+text
    all_companies=sorted(set(manifest)|{'Navi','Samsung SRIB','Turing'})
    coverage=dict(total_files=sum(map(len,manifest.values())),reviewed_files=len(reviewed),companies=[dict(name=c,files=len(manifest.get(c,[])),reviewed=sum(p in reviewed for p in manifest.get(c,[]))) for c in all_companies])
    reports=[dict(title='AI & ML interviews',file='ai_ml_questions.md',description='ML theory, statistics, GenAI, coding, system design and research-role prompts.'),dict(title='DSA & company OAs',file='dsa_oa_questions.md',description='Reported coding patterns, source links and gaps in company coverage.'),dict(title='Aptitude & core CS',file='aptitude_cs_fundamentals.md',description='Company formats, aptitude topics, technical sections and source caveats.')]
    data=dict(version=1,collected=COLLECTED,questions=distinct,coverage=coverage,reports=reports)
    # Validate the public payload: no source paths, email addresses or private raw blobs.
    ids=[q['id'] for q in distinct];assert len(ids)==len(set(ids))
    for q in distinct:
        assert q['section'] in ['dsa','ml','aptitude','cs']
        assert q['difficulty'] in ['easy-medium','hard']
        assert q['title'] and q['statement']
        emails=set(re.findall(r'\b[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}\b',json.dumps(q)))-SAMPLE_EMAILS.get(q['id'],set())
        assert not emails,(q['id'],emails)
    (OUT/'questions.json').write_text(json.dumps(data,ensure_ascii=False,indent=1),encoding='utf-8')
    for r in reports:shutil.copyfile(ROOT/'research'/r['file'],OUT/r['file'])
    print(f'Built {len(distinct)} questions; {len(reviewed)} source files accounted for.')

if __name__=='__main__':main()
