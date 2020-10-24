from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import hashlib
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import random
#Declaracias de variables y estructuras que utilizaremos
listaEliminar = []
dniMozo = 0

app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import db
from models import Pedidos, Productos, ItemsPedidos, Usuarios

@app.route('/')
def Inicio():
    return render_template('inicioAcceso.html')
#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************
@app.route('/control', methods =['POST' , 'GET'])
def Control():
    if request.method == 'POST':
        if request.form['dni'] and request.form['password']:  #si dni y contraseña no vienen vacío
            usuario = Usuarios.query.filter_by( DNI = request.form['dni']).first() #busqueda en la bd un dni igual al que se ingreso
            if usuario is None:   #no encontro el dni
                return render_template('error.html', mensaje = "ERROR: DNI incorrecto", url='Inicio' )
            else:
                global dniMozo
                dniMozo = request.form['dni']
                passEncriptada = hashlib.md5(bytes(request.form['password'], encoding='utf-8'))  #encripta clave
                clave = passEncriptada.hexdigest()  #transforma a hexadecimal
                if clave == usuario.Clave:   #claves coincidentes
                    if usuario.Tipo == 'Mozo' :  #evalua tipo de usuario
                        return render_template('funcionesMozo.html')
                    else:
                        return render_template('funcionCocinero.html')
                else:
                    return render_template('error.html', mensaje = "ERROR: Contraseña incorrecta",url='Inicio')
        else:
            return render_template('error.html', mensaje = "ERROR: Los campos son obligatorios",url='Inicio')
    else:
        return render_template('funcionesMozo.html')
#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************
@app.route('/numeroMesa')
def numeroMesa():
    crearPedido.precioTotal = 0
    return render_template('numeroMesa.html')
#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************
@app.route('/crearPedido',methods =['POST' , 'GET'])
@app.route('/crearPedido/<float:precio>/<int:numProducto>',methods =['POST' , 'GET'])
def crearPedido(precio=0,numProducto=0):
    if precio==0:   #si precio es vacio, es la primera vez que lo llama
        if request.method == 'POST':
            if request.form['mesa']:   #si mesa tiene algo, nos lleva a crearPedido
                mesa = request.form['mesa']
                ult_pedido=db.session.query(Pedidos).order_by(Pedidos.NumPedido.desc()).first() #ordena la lista de pedidos y nos trae el primero(que sería el ultimo)
                #dniMozo=session['DNI']
                unPedido = Pedidos(NumPedido=ult_pedido.NumPedido+1,Fecha=datetime.date.today(),Total=0,Cobrado='False', Observacion='', DNIMozo=dniMozo,Mesa=mesa)
                db.session.add(unPedido)
                db.session.commit()
                return render_template('crearPedido.html',productos=Productos.query.all(), pedido='', band=0, Total=0)
            else:
                return render_template('error.html', mensaje = "ERROR: Ingrese número de mesa",url='numeroMesa')
    else:
        ult_item=db.session.query(ItemsPedidos).order_by(ItemsPedidos.NumItem.desc()).first() #nos traemos el ultimo items
        ult_pedido=db.session.query(Pedidos).order_by(Pedidos.NumPedido.desc()).first()       #nos traemos el ultimo pedido
        Items = ItemsPedidos(NumItem=ult_item.NumItem+1, NumPedido=ult_pedido.NumPedido, NumProducto=numProducto, Precio=precio, Estado='Pendiente')
        db.session.add(Items)
        db.session.commit()
        if not hasattr (crearPedido, "precioTotal"):   #
            crearPedido.precioTotal = 0                #
            crearPedido.precioTotal += precio          #  variable estatica
        else:                                          #
            crearPedido.precioTotal += precio          #
        Pedido = db.session.query(Pedidos).order_by(Pedidos.NumPedido.desc()).first()
        return  render_template('crearPedido.html', productos = Productos.query.all(), pedido=Pedido, band=1, Total= crearPedido.precioTotal)

#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************
@app.route('/pedidoCargado',methods =['POST' , 'GET'])
def pedidoCargado():
    if request.method == 'POST':
        observacion = request.form['observacion']
        ult_pedido = db.session.query(Pedidos).order_by(Pedidos.NumPedido.desc()).first()
        ult_pedido.Observacion = observacion           #
        ult_pedido.Total = crearPedido.precioTotal     # Modificacion del pedido
        ult_pedido.DNIMozo = dniMozo                   #
        db.session.add(ult_pedido)
        db.session.commit()
    return render_template('pedidoCargado.html')
#*********************************************************************************************************************************************************
#*********************************************************************************************************************************************************
@app.route('/marcarPedido')
@app.route('/marcarPedido/<int:item>/<int:num_pedido>')
def marcarPedido(item=0, num_pedido=0):
    if item==0:
        pedidos=Pedidos.query.all()  #traemos la lista de pedidos
        for pedido in pedidos:
            cont_1 = 0         # estos contadores sirven para evaluar los prouctos que hay que eliminar
            rango = 0          #
            for item in pedido.items_pedido:
                rango += 1
                if(item.Estado=='Listo'):    #evalua si todos los itemsPedidos estan en listo
                    cont_1+=1
            if cont_1==rango:                  #si son iguales es porque estan todos listos
                listaEliminar.append(pedido)   #agrega a la lista los pedidos a eliminar
        long = int(len(listaEliminar))
        for i in range(long):
            pedidos.remove(listaEliminar[i-i])    #elimina la lista de pedidos
            listaEliminar.pop(i-i)                #cerea la lista a eliminar
        return render_template('listadoPendiente.html',li_pedidos=pedidos, xlong = len(pedidos))
    else:
        pedidos = Pedidos.query.all()
        x = pedidos[num_pedido-2].items_pedido[0].NumItem       #x tiene el valor del primer items que se cargo en el pedido
        un_item = pedidos[num_pedido-2].items_pedido[item-x]    #Nos trae el items a modificar su estado(sirve para el resguardo)
        db.session.delete(un_item)     #lo elimina
        Nitem = ItemsPedidos(NumItem=un_item.NumItem, NumPedido=un_item.NumPedido, NumProducto=un_item.NumProducto, Precio=un_item.Precio, Estado='Listo')
        db.session.add(Nitem)  #lo carga de vuelta
        db.session.commit()
        pedidos[num_pedido-2].items_pedido[item-x].Estado='Listo'   #y aqui modifica en la lista que trajimos su estado
        #pedidos = Pedidos.query.all()
        for pedido in pedidos:
            cont_1 = 0         # estos contadores sirven para evaluar los prouctos que hay que eliminar
            rango = 0          #
            for item in pedido.items_pedido:
                rango += 1
                if(item.Estado=='Listo'):    #evalua si todos los itemsPedidos estan en listo
                    cont_1+=1
            if cont_1==rango:                 #si son iguales es porque estan todos listos
                listaEliminar.append(pedido)  #agrega a la lista los pedidos a eliminar
        long = int(len(listaEliminar))
        for i in range(long):
            pedidos.remove(listaEliminar[i-i])  #elimina la lista de pedidos
            listaEliminar.pop(i-i)            #cerea la lista a eliminar
        return render_template('listadoPendiente.html',li_pedidos=pedidos, xlong = len(pedidos))

#**************************************************************************************************************************
#**************************************************************************************************************************
@app.route('/consultarPedidos')
def consultarPedidos():
    listaPedidos = Pedidos.query.filter_by(Cobrado='False')
    fecha = datetime.date.today()
    hoy = fecha.day
    return render_template('pedidosNoCobrados.html', li_pedidos = listaPedidos, hoy=hoy, fecha=fecha)
#**************************************************************************************************************************
#**************************************************************************************************************************

if __name__ == '__main__':
    print("Hoka munod")
    db.create_all()
    app.run(debug = True)
