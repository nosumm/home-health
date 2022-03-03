from website import create_app, db
from website.models import User, Packet

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Packet': Packet}