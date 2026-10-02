import json,sys,urllib.request,time
def gql(query,variables={}):
    for i in range(3):
        try:
            req=urllib.request.Request("https://leetcode.com/graphql",data=json.dumps({"query":query,"variables":variables}).encode(),headers={"Content-Type":"application/json","Referer":"https://leetcode.com","User-Agent":"Mozilla/5.0"})
            return json.load(urllib.request.urlopen(req,timeout=30))
        except Exception as e:
            time.sleep(2)
    return {}
Q="""query discussPostItems($orderBy: ArticleOrderByEnum, $keywords: [String]!, $tagSlugs: [String!], $skip: Int, $first: Int) {
  ugcArticleDiscussionArticles(orderBy: $orderBy, keywords: $keywords, tagSlugs: $tagSlugs, skip: $skip, first: $first) {
    totalNum
    edges { node { title topicId createdAt } }
  }
}"""
def search(kw,order="MOST_RELEVANT",n=50):
    r=gql(Q,{"orderBy":order,"keywords":[kw],"tagSlugs":[],"skip":0,"first":n})
    if 'errors' in r or 'data' not in r: return r.get('errors','ERR')
    return [e['node'] for e in r['data']['ugcArticleDiscussionArticles']['edges']]
def fetch(tid):
    r=gql("query($t:Int!){ ugcArticleDiscussionArticle(topicId:$t){ title content createdAt } }",{"t":int(tid)})
    return (r.get('data') or {}).get('ugcArticleDiscussionArticle')
