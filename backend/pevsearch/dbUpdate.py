from datetime import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Post, Tag, Like
from pprint import pprint
from bs4 import BeautifulSoup


def get_zenn_posts():
    """
    zennの個人開発タグが付いている最新記事をスクレイピングするコード
    
    return:
    - {タイトル, 作成日, タグ, url, zennでのいいね数}オブジェクトのリスト

    """

    url = "https://zenn.dev/topics/個人開発"

    # 記事のクラス
    article_class = "ArticleList_container__V4svj"
    tag_class = "View_topicName____nYp"
    title_class = "ArticleList_title__mmSkv"
    like_class = "ArticleList_like__7aNZE"

    page = 1
    article_list = []

    while page <= 10:
        params = {
            "order": "latest", #最新記事で
            "page": page,
        }
        print("zenn実行中")
        response = requests.get(url, params=params)

        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article', class_=article_class)


            for article in articles:
                tag_list = []
                # 個別ページにいって記事に紐づくタグを取得しにいく
                article_url = "https://zenn.dev" + article.find("a")["href"]
                response = requests.get(article_url)
                soup = BeautifulSoup(response.text, "html.parser")
                tags_html = soup.find_all("div", class_=tag_class)
                for tag_html in tags_html:
                    tag_list.append({"name": tag_html.text})

                # いいねが0の時は表示されないから、分岐
                try:
                    likes_count = article.find(class_=like_class).text

                except AttributeError:
                    likes_count = "0"

                ogp_img_url = soup.find('meta', {'property': 'og:image'}).get("content") if soup.find('meta', {'property': 'og:image'}) else None

                
                article_info = {
                    "title": article.find(class_=title_class).text,
                    "created_at": article.find("time")["datetime"],
                    "tags": tag_list,
                    "url": article_url,
                    "ogp_img_url": ogp_img_url,
                    "likes_count": likes_count
                }
                
                article_list.append(article_info)
            
            page += 1
        else:
            print(f"ページの取得中にエラーが発生しました: {response.status_code}")
    
    print("zenn実行終了")
    return article_list

def get_qiita_posts():

    """
    qiitaの個人開発、ポートフォリオタグが付いている最新記事をスクレイピングするコード
    
    return:
    - {タイトル, 作成日, タグ, url, qiitaでのいいね数}オブジェクトのリスト

    """

    qiita_api_url = "https://qiita.com/api/v2/items"
    access_token = "5f1ba6d39373a1de489a781b85ade8468a64e71f"

    page = 1
    article_list = []
    while page <= 10:
        # クエリパラメーターを設定
        params = {
            'query': "tag:個人開発,ポートフォリオ", 
            'page': page, 
            'per_page': 50, 
        }

        print("qiita実行中")
        response = requests.get(qiita_api_url, params=params, headers={'Authorization': f'Bearer {access_token}'})
        articles = response.json()

        for article in articles:
            article_indiv_page = requests.get(article["url"], headers={'Authorization': f'Bearer {access_token}'})
            soup = BeautifulSoup(article_indiv_page.text, "html.parser")
            ogp_img_url = soup.find('meta', {'property': 'og:image'}).get("content") if soup.find('meta', {'property': 'og:image'}) else None

            article_info = {
                "title": article["title"],
                "created_at": article["created_at"],
                "tags": article["tags"],
                "url": article["url"],
                "ogp_img_url": ogp_img_url,
                "likes_count": article["likes_count"]
            }

            article_list.append(article_info)
        page += 1


    print("qiita実行終了")
    return article_list

def save_posts(posts):
    """
    投稿を受け取ってデータベースで格納する

    input: 
    - {タイトル, 作成日, タグ, url, 各サイトでのいいね数}オブジェクトのリスト
    """
    print(len(posts))

    for post in posts:
        post_result, isPostCreated = Post.objects.get_or_create(
            title=post['title'],
        )
        #一意制約を回避するために設定を分ける
        post_result.createdAt = post["created_at"]
        post_result.url = post["url"]
        post_result.site_Like = post["likes_count"]
        post_result.image = post["ogp_img_url"]
        post_result.save()

        for tag in post["tags"]:
            tag_result, isTagCreated = Tag.objects.get_or_create(
                tagname=tag["name"]
            )

            post_result.tags.add(tag_result)
            

def update():
    qiita_post = get_qiita_posts()
    zenn_post = get_zenn_posts()
    all_posts = qiita_post + zenn_post
    save_posts(all_posts)

def delete():
    posts = Post.objects.all()
    posts.delete()
    tags = Tag.objects.all()
    tags.delete()
    likes = Like.objects.all()
    likes.delete()

# new=>
def start():
   """
   Scheduling data update
   Run update function once every 12 seconds
   """
   scheduler = BackgroundScheduler()

   # 最初の実行をスケジューラに追加
   scheduler.add_job(update, 'date')  # 'date'トリガーは一度だけ実行
   
   scheduler.add_job(update, 'interval', hours=1) # schedule
#    scheduler.add_job(delete, 'interval', seconds=5) # schedule
   scheduler.start()