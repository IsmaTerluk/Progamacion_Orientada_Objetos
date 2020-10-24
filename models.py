from __main__ import app
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy(app)

class Productos(db.Model):
    NumProducto = db.Column(db.Integer,primary_key=True)
    Nombre = db.Column(db.String(120),nullable=False)
    PrecioUnitario = db.Column(db.Float,nullable=False)
    items_producto = db.relationship('ItemsPedidos',backref='productos',lazy='dynamic')

class ItemsPedidos(db.Model):
    __tablename__ = 'ItemsPedidos'
    NumItem = db.Column(db.Integer,primary_key=True)
    NumPedido = db.Column(db.Integer,db.ForeignKey('pedidos.NumPedido'))
    NumProducto = db.Column(db.Integer,db.ForeignKey('productos.NumProducto'))
    Precio = db.Column(db.Float,nullable=False)
    Estado = db.Column(db.String(50),nullable=False)
    Producto=db.relationship('Productos')
    Pedido=db.relationship('Pedidos')
    
class Pedidos(db.Model):
    NumPedido = db.Column(db.Integer,primary_key=True)
    Fecha = db.Column(db.DateTime)
    Total = db.Column(db.Float,nullable=False)
    Cobrado = db.Column(db.String(2),nullable=False)
    Observacion = db.Column(db.Text)
    DNIMozo = db.Column(db.Integer,db.ForeignKey('usuarios.DNI'))
    Mesa = db.Column(db.Integer,nullable=False,unique=True)
    items_pedido = db.relationship('ItemsPedidos',backref='pedidos',lazy='dynamic')

class Usuarios(db.Model):
    DNI = db.Column(db.Integer,primary_key=True)
    Clave = db.Column(db.String(16),nullable=False,unique=True)
    Tipo = db.Column(db.String(16),nullable=False,unique=True)
    pedido_cargado = db.relationship('Pedidos',backref='usuarios',lazy='dynamic')
