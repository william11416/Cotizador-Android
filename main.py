import flet as ft

precios_cpu = {
    "AMD Ryzen 5 5600": 330999,
    "AMD Ryzen 7 5700X": 383554,
    "INTEL Core i5-12400F": 319989,
    "INTEL Core i7-12700K": 654332,
}

precios_ram = {8: 161180, 16: 219999, 32: 473629, 64: 1149999}
opciones_ram = [8, 16, 32, 64]

precio_gpu = 830781
precio_ssd = 295000
precio_armado = 40000
precio_envio = 25000

potencia_cpu = {
    "AMD Ryzen 5 5600": 65,
    "AMD Ryzen 7 5700X": 65,
    "INTEL Core i5-12400F": 65,
    "INTEL Core i7-12700K": 125,
}

potencia_gpu = 200
potencia_base = 100

def main(page: ft.Page):
    page.title = "Cotizador de Precios"
    page.scroll = ft.ScrollMode.AUTO

    
#------------ DECLARACION DE COMPONENTES --------------

    campo_nombre = ft.TextField(label="Ingresa tu nombre", width=300)
    campo_presupuesto = ft.TextField(label="Ingresa tu presupuesto tope disponible en pesos", width=300)

    dropdown_procesador = ft.Dropdown(
        label="Selecciona un Procesador",
        options=[
            ft.dropdown.Option("AMD Ryzen 5 5600"),
            ft.dropdown.Option("AMD Ryzen 7 5700X"),
            ft.dropdown.Option("INTEL Core i5-12400F"),
            ft.dropdown.Option("INTEL Core i7-12700K"),
        ],
        width=300,
    )

    texto_ram = ft.Text("Memoria RAM: 8 GB")
    slider_ram = ft.Slider(min=0, max=3, divisions=3, value=0, width=300)

    mensaje_opciones = ft.Text("Adicionales optativos")
    placa_video = ft.Checkbox(label="Placa de video Dedicada", value=False)
    ssd_extra = ft.Checkbox(label="Unidad SSD extra", value=False)
    serv_armado = ft.Checkbox(label="Servicio de Armado", value=False)

    mensaje_entrega = ft.Text("Active para envío a domicilio o desactive para retiro en tienda")
    modalidad_de_entrega = ft.Switch(value=False)

    mensaje_met_pago = ft.Text("Selecciona el medio de pago")
    radio_pago = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="efectivo", label="Efectivo o Transferencia bancaria (10% de descuento)"),
            ft.Radio(value="debito", label="Tarjeta de Débito (precio de lista)"),
            ft.Radio(value="credito", label="Tarjeta de Crédito en 3 cuotas (15% de recargo)"),
        ])
    )

    boton_calcular = ft.Button("Calcular")

    texto_alerta = ft.Text("", color="red")
    texto_resultado = ft.Text("")

# -------------- FUNCIONES CONTROLADORAS DE EVENTOS -------------------

    def actualizar_ram(e):
        gb = opciones_ram[int(slider_ram.value)]
        texto_ram.value = f"Memoria RAM: {gb} GB"
        page.update()

    def calcular(e):
        texto_alerta.value = ""
        texto_resultado.value = ""

        # Validar que haya procesador y medio de pago
        if not dropdown_procesador.value:
            texto_alerta.value = "Selecciona un procesador."
            page.update()
            return
        if not radio_pago.value:
            texto_alerta.value = "Selecciona un medio de pago."
            page.update()
            return

        # Leer el presupuesto protegido con try/except
        try:
            presupuesto = float(campo_presupuesto.value)
        except ValueError:
            texto_alerta.value = "El presupuesto debe ser un número válido."
            page.update()
            return

        # Subtotal
        subtotal = precios_cpu[dropdown_procesador.value]
        gb_ram = opciones_ram[int(slider_ram.value)]
        subtotal += precios_ram[gb_ram]

        if placa_video.value:
            subtotal += precio_gpu
        if ssd_extra.value:
            subtotal += precio_ssd
        if serv_armado.value:
            subtotal += precio_armado
        if modalidad_de_entrega.value:
            subtotal += precio_envio

        # Medio de pago
        cuota = 0
        if radio_pago.value == "efectivo":
            total = subtotal * 0.90
        elif radio_pago.value == "debito":
            total = subtotal
        else:
            total = subtotal * 1.15
            cuota = total / 3

        # Consumo eléctrico estimado
        consumo = potencia_cpu[dropdown_procesador.value] + potencia_base
        if placa_video.value:
            consumo += potencia_gpu
        consumo = consumo * 1.25

        if consumo > 450:
            fuente = "Se recomienda una fuente de 650W o superior."
        else:
            fuente = "Se recomienda una fuente convencional de 500W."

        # Comparación con el presupuesto
        if total <= presupuesto:
            saldo = presupuesto - total
            comparacion = f"Cotización aprobada. Saldo a favor: ${saldo:,.2f}"
        else:
            faltante = total - presupuesto
            comparacion = f"Presupuesto insuficiente. Faltan ${faltante:,.2f}"

        # Armado del texto de resultados
        nombre = campo_nombre.value.strip() or "cliente"
        texto_resultado.value = (
            f"Cotización para {nombre}\n\n"
            f"Subtotal: ${subtotal:,.2f}\n"
            f"Total a pagar: ${total:,.2f}"
        )

        if radio_pago.value == "credito":
            texto_resultado.value += f"\nCada cuota: ${cuota:,.2f}"

        texto_resultado.value += f"\nConsumo estimado: {consumo:.0f} W\n{fuente}"
        texto_resultado.value += f"\n\n{comparacion}"
        page.update()

    # Asignación de eventos
    slider_ram.on_change = actualizar_ram
    boton_calcular.on_click = calcular
    
#----------- ENSAMBLADO FINAL --------------
    
    page.add(
        campo_nombre,
        campo_presupuesto,
        dropdown_procesador,
        texto_ram,
        slider_ram,
        mensaje_opciones,
        placa_video,
        ssd_extra,
        serv_armado,
        mensaje_entrega,
        modalidad_de_entrega,
        mensaje_met_pago,
        radio_pago,
        boton_calcular,
        texto_alerta,
        texto_resultado,
    )
ft.run(main)