import asyncio
import random

from src.db.crud import (
    create_document,
    delete_document,
    get_all_documents,
    get_document,
    update_document,
)

simple_dict = {"text": 1, "text2": 2, "_id": 13}

# note = asyncio.run(create_document(simple_dict))
#
# print(note)


# async def main():
#     all_notes = await get_all_documents()
#     for note in all_notes:
#         print(await update_document(note["_id"], update_data={"text": random.randint(10, 100_000)}))
#
#
# asyncio.run(main())


print(asyncio.run(delete_document(13)))


#
# update_note = update_document(note)
#
# delete_document(note)
