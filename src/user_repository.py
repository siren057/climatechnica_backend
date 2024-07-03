from user_translator import *


class UserRepository:
    def __init__(self, db, translator: UserMongoTranslator):
        self.collection = db["users"]
        self.translator = translator

    async def get_all(self):
        return [self.translator.from_document(document) for document in await self.collection.find().to_list(None)]

    async def get_by_id(self, user_id):
        document = await self.collection.find_one({"_id": ObjectId(user_id)})
        return self.translator.from_document(document) if document else None

    async def update(self, user_id, user: User):
        await self.collection.update_one({"_id": ObjectId(user_id)},
                                         {'$set': self.translator.to_document(user)})

    async def create(self, user: User):
        result = await self.collection.insert_one(self.translator.to_document(user))
        return str(result.inserted_id)

    async def delete(self, user_id: str):
        await self.collection.delete_one({"_id": ObjectId(user_id)})
