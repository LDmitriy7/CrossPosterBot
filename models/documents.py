import mongoengine as me


class Replace(me.EmbeddedDocument):
    old_text: str = me.StringField()
    new_text: str = me.StringField()


class Route(me.Document):
    source_id: int = me.IntField()
    target_id: int = me.IntField()
    replaces: list[Replace] = me.EmbeddedDocumentListField(Replace)
