def is_valid_article(article: dict) -> bool:
    required_fields = ["title", "description", "url", "urlToImage"]

    for field in required_fields:
        if not article.get(field):
            return False

    return True