from reportlab.platypus import (

    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer

)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import io

from flask import (
    Blueprint,
    render_template,
    session,
    request,
    redirect,
    url_for,
    flash, send_file
)

from app.services.venta_service import (
    buscar_producto_codigo, guardar_venta, 
    obtener_tipos_pago, obtener_nombre_pago,
    obtener_ticket,
    obtener_historial_ventas
)

ventas_bp = Blueprint(
    'ventas',
    __name__,
    url_prefix='/ventas'
)


@ventas_bp.route('/')
def pos():

    carrito = session.get(
        'carrito',
        []
    )

    total = sum(

        item['subtotal']

        for item in carrito

    )

    tipos_pago = obtener_tipos_pago()

    return render_template(

        'ventas/pos.html',

        carrito=carrito,
        total=total,
        tipos_pago=tipos_pago
    )

@ventas_bp.route('/agregar', methods=['POST'])
def agregar_producto():

    codigo_barras = request.form['codigo_barras']

    producto = buscar_producto_codigo(
        codigo_barras
    )

    if not producto:

        flash(
            'Producto no encontrado',
            'warning'
        )

        return redirect(
            url_for('ventas.pos')
        )

    carrito = session.get(
        'carrito',
        []
    )

    encontrado = False

    for item in carrito:

        if item['id_producto'] == producto['id_producto']:

            nueva_cantidad = (
                item['cantidad'] + 1
            )

            if nueva_cantidad > producto['stock_actual']:

                flash(

                    f"Stock insuficiente | Disponible: {producto['stock_actual']}",

                    'warning'

                )

                return redirect(
                    url_for('ventas.pos')
                )

            item['cantidad'] = nueva_cantidad

            item['subtotal'] = (

                item['cantidad']
                *
                item['precio']

            )

            encontrado = True

            break

    if not encontrado:

        if producto['stock_actual'] <= 0:

            flash(

                'Producto sin stock',

                'warning'

            )

            return redirect(
                url_for('ventas.pos')
            )

        carrito.append({

            'id_producto':
                producto['id_producto'],

            'nombre':
                producto['nombre'],

            'precio':
                float(producto['precio']),

            'cantidad':
                1,

            'subtotal':
                float(producto['precio'])

        })

    session['carrito'] = carrito

    flash(
        f"{producto['nombre']} agregado",
        'success'
    )

    return redirect(
        url_for('ventas.pos')
    )


@ventas_bp.route('/limpiar')
def limpiar_carrito():

    session.pop(
        'carrito',
        None
    )

    flash(
        'Carrito cancelado',
        'info'
    )

    return redirect(
        url_for('ventas.pos')
    )

@ventas_bp.route('/eliminar/<int:id_producto>')
def eliminar_item(id_producto):

    carrito = session.get(
        'carrito',
        []
    )

    carrito = [

        item

        for item in carrito

        if item['id_producto']
        != id_producto

    ]

    session['carrito'] = carrito

    flash(
        'Producto eliminado',
        'info'
    )

    return redirect(
        url_for('ventas.pos')
    )

@ventas_bp.route(
    '/cobrar',
    methods=['POST']
)
def cobrar():

    carrito = session.get(
        'carrito',
        []
    )

    if not carrito:

        flash(
            'Carrito vacío',
            'warning'
        )

        return redirect(
            url_for('ventas.pos')
        )

    id_tipo_pago = request.form.get(
        'id_tipo_pago'
    )

    resultado = guardar_venta(

        carrito,

        id_tipo_pago

    )

    if resultado['ok']:

        session.pop(
            'carrito',
            None
        )

        nombre_pago = obtener_nombre_pago(

            resultado['id_tipo_pago']

        )

        ticket_url = url_for(

            'ventas.ticket',

            id_venta=resultado['id_venta']

        )

        flash(

            f"""
            ✓ Venta registrada<br>
            Folio: {resultado['folio']}<br>
            Pago: {nombre_pago}<br>
            Total: ${resultado['total']:.2f}<br><br>

            <a href="{ticket_url}"

            class="btn btn-ticket-flash">

            <i class="bi bi-receipt"></i>

            Ver Ticket

            </a>
            """,

            'success'
        )

    else:

        flash(

            f"Error venta: {resultado['error']}",

            'danger'

        )

    return redirect(
        url_for('ventas.pos')
    )

# Obtener nombre de tipo de pago para ticket`
@ventas_bp.route(
    '/ticket/<int:id_venta>'
)
def ticket(id_venta):

    venta, detalle = obtener_ticket(
        id_venta
    )

    return render_template(

        'ventas/ticket.html',

        venta=venta,
        detalle=detalle
    )

@ventas_bp.route(
    '/pdf/<int:id_venta>'
)
def ticket_pdf(id_venta):

    venta, detalle = obtener_ticket(
        id_venta
    )

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(

        buffer,

        pagesize=(230, 700),

        rightMargin=12,
        leftMargin=12,
        topMargin=18,
        bottomMargin=18

    )

    styles = getSampleStyleSheet()

    elementos = []

    # Header

    titulo = Paragraph(

        "<b>ABARROTES</b>",

        styles['Title']

    )

    elementos.append(titulo)

    elementos.append(

        Paragraph(

            "Ticket Venta",

            styles['Heading3']

        )

    )

    elementos.append(
        Spacer(1,12)
    )

    # Info

    elementos.append(

        Paragraph(

            f"<b>Folio:</b> {venta['folio']}",

            styles['BodyText']

        )

    )

    elementos.append(

        Paragraph(

            f"<b>Fecha:</b> {venta['fecha_venta']}",

            styles['BodyText']

        )

    )

    elementos.append(

        Paragraph(

            f"<b>Pago:</b> {venta['nombre_pago']}",

            styles['BodyText']

        )

    )

    elementos.append(
        Spacer(1,18)
    )

    # Tabla

    data = [

        [

            'Producto',
            'Cant',
            'Precio',
            'Sub'

        ]

    ]

    for item in detalle:

        data.append([

            item['nombre'],

            item['cantidad'],

            f"${item['precio_unitario']:.2f}",

            f"${item['subtotal']:.2f}"

        ])

    tabla = Table(

        data,

        colWidths=[90,35,40,45]

    )

    tabla.setStyle(

        TableStyle([

            (

                'BACKGROUND',

                (0,0),

                (-1,0),

                colors.HexColor('#edf2f7')

            ),

            (

                'TEXTCOLOR',

                (0,0),

                (-1,0),

                colors.HexColor('#343a40')

            ),

            (

                'FONTNAME',

                (0,0),

                (-1,0),

                'Helvetica-Bold'

            ),

            (

                'GRID',

                (0,0),

                (-1,-1),

                0.5,

                colors.HexColor('#dee2e6')

            ),

            (

                'ROWBACKGROUNDS',

                (0,1),

                (-1,-1),

                [

                    colors.white,

                    colors.HexColor('#fafafa')

                ]

            ),

            (

                'VALIGN',

                (0,0),

                (-1,-1),

                'MIDDLE'

            ),

            (

                'FONTSIZE',

                (0,0),

                (-1,-1),

                8

            )

        ])

    )

    elementos.append(tabla)

    elementos.append(
        Spacer(1,20)
    )

    # Total

    total = Paragraph(

        f"""

        <para align='right'>

        <font size=16>

        <b>TOTAL:

        ${venta['total']:.2f}</b>

        </font>

        </para>

        """,

        styles['BodyText']

    )

    elementos.append(total)

    elementos.append(
        Spacer(1,28)
    )

    # Footer

    footer = Paragraph(

        """

        <para align='center'>

        Gracias por su compra<br/>

        Sistema Inventario Abarrotes

        </para>

        """,

        styles['Italic']

    )

    elementos.append(footer)

    doc.build(elementos)

    buffer.seek(0)

    return send_file(

        buffer,

        as_attachment=True,

        download_name=f"{venta['folio']}.pdf",

        mimetype='application/pdf'

    )


@ventas_bp.route(
    '/historial'
)
def historial():

    ventas = obtener_historial_ventas()

    return render_template(

        'ventas/historial.html',

        ventas=ventas

    )