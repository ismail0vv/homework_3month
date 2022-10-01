from aiogram import types, Dispatcher
import hashlib

async def inline_wiki_handler(query: types.InlineQuery):
    text = query.query or "echo"
    link = f"https://ru.wikipedia.org/wiki/{text}"
    articles = [types.InlineQueryResultArticle(
        id=hashlib.md5(text.encode()).hexdigest(),
        title="Wikipedia: ",
        url=link,
        input_message_content=types.InputMessageContent(
            message_text=link
        )
    )]
    await query.answer(articles, cache_time=60)


def register_inline_handler(dp: Dispatcher):
    dp.register_message_handler(inline_wiki_handler)