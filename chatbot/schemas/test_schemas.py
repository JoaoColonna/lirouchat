from ninja import Schema

class TesteSchema(Schema):
    id: int
    titulo: str
    texto: str
    criado_em: str
    usuario_id: int
    conversa_id: int

class TesteCreateSchema(Schema):
    tipo: str

class TesteMensagem(Schema):
    conversa_id: int
    resposta: str