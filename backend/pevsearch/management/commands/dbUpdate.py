import requests
from ...models import Post, Tag, Like
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from datetime import datetime
from django.db import transaction
import time
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):

    help = "devsearchのデータベースをアップデートするコマンド"

    def handle(self, *args, **options):
        print(f'データベースアップデート開始{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        qiita_post = self.get_qiita_posts()
        print("qiita終了")
        zenn_post = self.get_zenn_posts()
        print("zenn終了")
        all_posts = qiita_post + zenn_post
        start_time = time.time() 
        self.save_posts(all_posts)
        end_time = time.time()  # 終了時刻を記録
        elapsed_time = end_time - start_time  # 経過時間を計算
        print(f"保存実行時間: {elapsed_time} seconds")
        print(f'データベースアップデート終了{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')


    def get_zenn_posts(self):
        """
        zennの個人開発タグが付いている最新記事をスクレイピングするコード
        
        return:
        - {タイトル, 作成日, タグ, url, zennでのいいね数}オブジェクトのリスト

        1ページ48記事×10ページ: 480記事

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
        
        return article_list

    def get_qiita_posts(self):

        """
        qiitaの個人開発、ポートフォリオタグが付いている最新記事をスクレイピングするコード
        
        return:
        - {タイトル, 作成日, タグ, url, qiitaでのいいね数}オブジェクトのリスト

        1ページ50記事×10ページ: 500記事

        """

        qiita_api_url = "https://qiita.com/api/v2/items"
        access_token = "5f1ba6d39373a1de489a781b85ade8468a64e71f"

        page = 1
        article_list = []
        while page <= 10:  #10
            # クエリパラメーターを設定
            params = {
                'query': "tag:個人開発,ポートフォリオ", 
                'page': page, 
                'per_page': 50, 
            }

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

        return article_list


    def save_posts(self, fetched_posts):
        """
            投稿レコード一括取得 1回
            タグレコード一括取得 1回
            新規タグの作成 m回
            投稿の更新、追加 2回
            新規投稿の取得
            タグの設定 l回
            クエリ数O(n+m)
        """
        existing_posts = Post.objects.in_bulk(field_name='url') # title
        existing_tags = Tag.objects.in_bulk(field_name='tagname') 

        # データベースの初期化の際は、こちら
        if not existing_posts and not existing_tags:
            self.first_save_posts(fetched_posts)
            return 
        
        pending_updates = []
        pending_adds = []
        new_post_tags = {}

        for fetched_post in fetched_posts:
            url = fetched_post['url'] # url
            tags = fetched_post.pop('tags', [])
            
            tag_objects = []
            for tag in tags:
                tag_name = tag['name']
                if tag_name in existing_tags:
                    tag_objects.append(existing_tags[tag_name])
                else:
                    # 新しくきたタグに２回目以降アクセスした場合、通常のcreateメソッドでintegrity errorくる
                    new_tag, created = Tag.objects.get_or_create(tagname=tag_name)
                    existing_tags[new_tag.tagname] = new_tag
                    tag_objects.append(new_tag)
                

            post_data = existing_posts.get(url)

            # 取得してきた投稿がすでにデータベースにあるものだったら
            if post_data:
                if post_data.site_Like != fetched_post['likes_count']:
                    post_data.site_Like = fetched_post['likes_count']
                    pending_updates.append(post_data)

            # 新しい投稿だったら
            else:
                new_post = Post(
                    title=fetched_post["title"],
                    createdAt=fetched_post["created_at"],
                    url=fetched_post["url"],
                    image=fetched_post["ogp_img_url"],
                    site_Like=fetched_post["likes_count"]
                )
                pending_adds.append(new_post)
                new_post_tags[new_post.url] = tag_objects # title
                


        if pending_updates:
            Post.objects.bulk_update(pending_updates, ['site_Like'])
        if pending_adds:
            Post.objects.bulk_create(pending_adds)

       
        now = timezone.now()
        time = now - timedelta(minutes=1)
        # 上の一括挿入で、idを受け取れないので、ここで取得
        new_posts = Post.objects.filter(createdAt__gte=time)

        for new_post in new_posts:
            new_post.tags.set(new_post_tags[new_post.url]) # title


    def first_save_posts(self, fetched_posts):
        # 一意制約を回避するには、致し方内
        tag_names = []
        for fetched_post in fetched_posts:
            for tag in fetched_post['tags']:
                new_tag, created = Tag.objects.get_or_create(tagname=tag['name'])
                tag_names.append(new_tag.tagname)

        post_instances = []
        for fetched_post in fetched_posts:
            post = Post(
                title=fetched_post["title"],
                createdAt=fetched_post["created_at"],
                url=fetched_post["url"],
                image=fetched_post["ogp_img_url"],
                site_Like=fetched_post["likes_count"]
            )
            post_instances.append(post)

        with transaction.atomic():
            Post.objects.bulk_create(post_instances)

        tags = Tag.objects.in_bulk(field_name='tagname')
        posts = Post.objects.in_bulk(field_name='url') # title

        for fetched_post in fetched_posts:
            post_instance = posts[fetched_post['url']]
            tag_instances = [tags[tag_name] for tag_name in tag_names]
            post_instance.tags.set(tag_instances)

