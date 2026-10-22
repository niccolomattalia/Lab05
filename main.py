import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    f1 = ft.TextField(label="tipo:", height=60)
    f2 = ft.TextField(label="marca:", height=60)
    f3 = ft.TextField(label="anno di acquisto:", height=60)
    txtOut = ft.TextField(width=100, disabled=True, value="0", text_align=ft.TextAlign.CENTER)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"


    def piu(e):
        valoreCorrente = txtOut.value
        txtOut.value = str(int(valoreCorrente) + 1)
        txtOut.update()

    def meno(e):
        valoreCorrente = txtOut.value
        txtOut.value = str(int(valoreCorrente) - 1)
        txtOut.update()

    def azzera(e):
        f1.value=""
        f2.value=""
        f3.value=""
        txtOut.value="0"
        page.update()

    def gestioneAggiunta(e):
        try:
            anno = int(f3.value)
            posti = int(txtOut.value)
            deposito.aggiungi_strumento(f1.value, f2.value, f3.value, txtOut.value)
            aggiorna_lista_strumenti()
        except ValueError:
            alert.show_alert("❌Errore, inserisci valori numerici validi per anno e posti")
        azzera(e)

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    btnMeno = ft.IconButton(icon=ft.Icons.REMOVE, icon_color="green", icon_size=24, on_click=meno)
    btnPiu = ft.IconButton(icon=ft.Icons.ADD, icon_color="green", icon_size=24, on_click=piu)



    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Text("Aggiungi nuovo strumento",size=15),
        ft.Row([f1, f2, f3, btnMeno,txtOut,btnPiu],alignment=ft.MainAxisAlignment.CENTER),
        ft.Button("Aggiungi strumento",on_click=gestioneAggiunta),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()
ft.run(main)
