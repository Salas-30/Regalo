import os
import random
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, ListProperty
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image

# --- FECHA DE ANIVERSARIO ---
FECHA_INICIO = datetime(2025, 11, 30, 0, 0) 

# --- RUTAS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
AUDIO_DIR = os.path.join(ASSETS_DIR, 'audio')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
GALLERY_DIR = os.path.join(ASSETS_DIR, 'gallery')

if not os.path.exists(GALLERY_DIR): os.makedirs(GALLERY_DIR)

# --- COLORES ---
COLORES_SUAVES = [
    (0.8, 0.6, 0.7, 1), (0.4, 0.5, 0.6, 1), (0.6, 0.5, 0.7, 1),
    (0.3, 0.3, 0.35, 1), (0.4, 0.6, 0.6, 1), (0.7, 0.5, 0.5, 1),
    (0.5, 0.5, 0.6, 1), (0.25, 0.25, 0.3, 1), (0.6, 0.4, 0.5, 1),
    (0.45, 0.45, 0.45, 1)
]

# --- RAZONES ---
MIS_RAZONES = [
    "Amo cómo se iluminan tus ojos cuando sonríes.",
    "Me das paz incluso a kilómetros de distancia.",
    "Eres mi primer pensamiento al despertar.",
    "Admiro tu fuerza y cómo luchas por lo que quieres.",
    "Tu voz es mi sonido favorito en el mundo.",
    "Porque contigo, incluso el silencio es cómodo.",
    "Haces que quiera ser una mejor persona.",
    "Amo que tengamos nuestro propio lenguaje y chistes.",
    "Porque aguantas mis locuras (y esta app es prueba de ello).",
    "Por cómo me apoyas en mis días malos.",
    "Porque eres la mujer más hermosa, por dentro y por fuera.",
    "Amo imaginar nuestro futuro juntos.",
    "Porque cada mensaje tuyo me alegra el día.",
    "Por la paciencia que tienes con la distancia.",
    "Porque eres mi mejor amiga y mi novia a la vez.",
    "Amo tu risa, es contagiosa.",
    "Porque me haces sentir amado como nadie más.",
    "Por esos detalles pequeños que tienes conmigo.",
    "Porque confío en ti ciegamente.",
    "Porque eres inteligente y brillante.",
    "Amo cómo nos complementamos.",
    "Porque a pesar de la distancia, te siento cerca.",
    "Por todas las veces que nos hemos reído hasta llorar.",
    "Porque eres mi hogar.",
    "Amo que seas tan cariñosa.",
    "Porque eres única, no hay nadie como tú.",
    "Por cómo me miras (incluso por videollamada).",
    "Porque vale la pena cada segundo de espera por ti.",
    "Simplemente, porque eres tú.",
    "Porque te amo más de lo que las palabras pueden decir."
]

# --- KV STRING ---
kv_string = '''
#:import dp kivy.metrics.dp

<IntroScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Image:
            id: logo_img
            source: app.get_resource('logo.png')
            size_hint: (0.7, 0.7)
            allow_stretch: True
            keep_ratio: True
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            opacity: 1
            mipmap: True

<SongListItem>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(100)
    padding: dp(10)
    spacing: dp(15)
    canvas.before:
        Color:
            rgba: 0, 0, 0, 0.5 
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 1, 1, 1, 0.1
        Line:
            points: [self.x + dp(10), self.y, self.right - dp(10), self.y]
            width: 1

    Image:
        source: root.image_source
        size_hint_x: None
        width: dp(80)
        allow_stretch: True
        keep_ratio: True
        mipmap: True 

    Label:
        text: root.song_title
        text_size: self.size      
        halign: 'left'            
        valign: 'center'          
        padding_x: dp(10)             
        font_size: '19sp'
        color: 1, 1, 1, 1         

<LibraryScreen>:
    FloatLayout:
        Image:
            source: app.get_resource('fondo_lista.jpg')
            allow_stretch: True
            keep_ratio: False
            size_hint: (1, 1)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

        BoxLayout:
            orientation: 'vertical'
            
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(120)
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 0.6
                    Rectangle:
                        pos: self.pos
                        size: self.size
                
                Label:
                    text: "♥ Nuestras canciones ♥"
                    font_size: '26sp'
                    color: 1, 0.41, 0.71, 1
                    bold: True
                    size_hint_y: 0.4
                
                Label:
                    id: time_counter
                    text: "Calculando..."
                    font_size: '15sp'
                    color: 1, 1, 1, 0.9
                    bold: True
                    size_hint_y: 0.6
                    halign: 'center'
                    valign: 'middle'

            ScrollView:
                BoxLayout:
                    id: song_list_container
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    padding: dp(5)
                    spacing: dp(5)

            BoxLayout:
                size_hint_y: None
                height: dp(60) 
                padding: dp(5)
                spacing: dp(5)
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 0.8
                    Rectangle:
                        pos: self.pos
                        size: self.size

                Button:
                    text: "♥ Carta"
                    background_color: 1, 0.41, 0.71, 0.8
                    font_size: '14sp'
                    bold: True
                    on_release: root.show_love_message()

                Button:
                    text: "¿Por qué te amo?"
                    background_color: 1, 0.8, 0, 0.8 
                    font_size: '14sp'
                    bold: True
                    on_release: root.show_random_reason()

                Button:
                    text: "★ Galería"
                    background_color: 0.2, 0.6, 1, 0.8
                    font_size: '14sp'
                    bold: True
                    on_release: root.go_to_gallery()

<PlayerScreen>:
    canvas.before:
        Color:
            rgba: root.background_color 
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)

        Button:
            text: "◄ Volver atrás"
            size_hint_y: 0.08
            background_color: 0, 0, 0, 0
            color: 1, 1, 1, 0.7
            on_release: root.go_back()

        Label:
            text: "♥ Nuestra biblioteca ♥"
            font_size: '20sp'
            color: 1, 1, 1, 0.9 
            bold: True
            size_hint_y: 0.1
            outline_width: 1
            outline_color: (0, 0, 0, 0.5)

        Image:
            id: album_art
            source: ''
            size_hint_y: 0.45
            allow_stretch: True
            keep_ratio: True
            mipmap: True 

        Label:
            id: song_label
            text: "Cargando..."
            font_size: '20sp'
            size_hint_y: 0.1
            color: 1, 1, 1, 1
            halign: 'center'
            bold: True
            outline_width: 1
            outline_color: (0, 0, 0, 0.5)

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.15 # Un poco mas alto para que el circulo quepa bien
            spacing: dp(10)
            
            Label:
                id: current_time_lbl
                text: "00:00"
                font_size: '14sp'
                size_hint_x: 0.15
                color: 1, 1, 1, 1
                bold: True
                outline_width: 1
                outline_color: (0,0,0,0.5)

            # SLIDER CON BOTON CIRCULAR
            Slider:
                id: progress_bar
                min: 0
                max: 100
                value: 0
                size_hint_x: 0.7
                cursor_size: (dp(30), dp(30)) # Circulo grande
                background_width: dp(30)
                on_touch_up: root.seek_audio(*args)
            
            Label:
                id: total_time_lbl
                text: "00:00"
                font_size: '14sp'
                size_hint_x: 0.15
                color: 1, 1, 1, 1
                bold: True
                outline_width: 1
                outline_color: (0,0,0,0.5)

        BoxLayout:
            size_hint_y: 0.15
            spacing: dp(20)
            padding: [dp(20), 0, dp(20), 0]
            
            Button:
                text: "<<"
                background_color: 1, 1, 1, 0.2 
                color: 1, 1, 1, 1
                on_release: root.play_prev()
            
            Button:
                id: btn_play_pause
                text: "PAUSA"
                background_color: 1, 0.41, 0.71, 1
                font_size: '18sp'
                bold: True
                on_release: root.toggle_play()

            Button:
                text: ">>"
                background_color: 1, 1, 1, 0.2
                color: 1, 1, 1, 1
                on_release: root.play_next()

<GalleryScreen>:
    FloatLayout:
        Image:
            source: app.get_resource('fondo_lista.jpg')
            allow_stretch: True
            keep_ratio: False
            size_hint: (1, 1)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

        BoxLayout:
            orientation: 'vertical'
            
            BoxLayout:
                size_hint_y: 0.12 
                padding: dp(10)
                spacing: dp(10)
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 0.6
                    Rectangle:
                        pos: self.pos
                        size: self.size
                
                Button:
                    text: "◄"
                    font_size: '24sp'
                    size_hint_x: None
                    width: dp(50)
                    background_color: 0,0,0,0
                    color: 1, 1, 1, 1
                    on_release: root.go_back()
                
                Label:
                    text: "Nuestros Recuerdos"
                    font_size: '22sp'
                    bold: True
                    color: 1, 1, 1, 1
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size 
            
            ScrollView:
                GridLayout:
                    id: gallery_grid
                    cols: 2
                    spacing: dp(5)
                    padding: dp(5)
                    size_hint_y: None
                    height: self.minimum_height
'''

Builder.load_string(kv_string)

# --- CALCULO TIEMPO ---
def calcular_tiempo_juntos(inicio):
    ahora = datetime.now()
    
    meses_totales = (ahora.year - inicio.year) * 12 + (ahora.month - inicio.month)
    if ahora.day < inicio.day:
        meses_totales -= 1
    
    years = meses_totales // 12
    months = meses_totales % 12
    
    mes_anterior = ahora.month - 1 if ahora.day < inicio.day else ahora.month
    ano_referencia = ahora.year
    if mes_anterior == 0: 
        mes_anterior = 12
        ano_referencia -= 1
        
    try:
        ultimo_mes_cumplido = datetime(ano_referencia, mes_anterior, inicio.day)
    except ValueError:
        ultimo_mes_cumplido = datetime(ano_referencia, mes_anterior, 28)
        
    diff = ahora - ultimo_mes_cumplido
    days = diff.days
    
    seconds_total = diff.seconds
    hours = seconds_total // 3600
    minutes = (seconds_total % 3600) // 60
    seconds = seconds_total % 60

    tiempo_str = f"{months} Meses, {days} Días"
    if years > 0:
        tiempo_str = f"{years} Año, " + tiempo_str
    
    reloj_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"Tiempo juntos:\n{tiempo_str}\n{reloj_str}"

# --- CLASES ---

class SongListItem(ButtonBehavior, BoxLayout):
    song_title = StringProperty("")
    image_source = StringProperty("")

class IntroScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.start_fade_out, 5)

    def start_fade_out(self, dt):
        anim = Animation(opacity=0, duration=1)
        anim.bind(on_complete=self.change_screen)
        anim.start(self.ids.logo_img)

    def change_screen(self, *args):
        self.manager.current = 'library'

class LibraryScreen(Screen):
    is_loaded = False 

    def on_enter(self):
        if not self.is_loaded:
            self.load_songs_from_assets()
            self.is_loaded = True
            
        self.update_timer = Clock.schedule_interval(self.update_love_counter, 1)
        self.update_love_counter(0)

    def on_leave(self):
        if hasattr(self, 'update_timer'):
            self.update_timer.cancel()

    def update_love_counter(self, dt):
        texto = calcular_tiempo_juntos(FECHA_INICIO)
        self.ids.time_counter.text = texto

    def load_songs_from_assets(self):
        container = self.ids.song_list_container
        container.clear_widgets()
        
        if not os.path.exists(AUDIO_DIR):
            lbl = Label(text="Falta carpeta assets/audio", size_hint_y=None, height=50)
            container.add_widget(lbl)
            return

        files = [f for f in os.listdir(AUDIO_DIR) if f.endswith('.mp3')]
        files.sort()

        if not files:
            lbl = Label(text="No hay canciones .mp3", size_hint_y=None, height=50)
            container.add_widget(lbl)
            return

        for index, song_name in enumerate(files):
            base_name = song_name.rsplit('.', 1)[0]
            jpg_path = os.path.join(IMAGES_DIR, base_name + ".jpg")
            png_path = os.path.join(IMAGES_DIR, base_name + ".png")
            default_path = os.path.join(IMAGES_DIR, 'default.jpg')
            
            img_path = default_path
            if os.path.exists(jpg_path): img_path = jpg_path
            elif os.path.exists(png_path): img_path = png_path
            
            clean_name = song_name.replace('.mp3', '').replace('_', ' ')
            
            item = SongListItem(song_title=clean_name, image_source=img_path)
            item.bind(on_release=lambda x, idx=index: self.manager.get_screen('player').start_playlist(files, idx))
            container.add_widget(item)

    def show_love_message(self):
        mensaje = (
            "Hola mi amorcitoooooo, como tau? bien? me alegro mucho mucho mi princesa, "
            "felices dos meses mi amor, se que un app de repente puede parecer algo muy simple "
            "y mas un reproductor, pero es nuestro reproductor, una prueba de lo que sentimos "
            "a pesar de esta inmensa distancia, y yo estoy muy feliz y espero que tu también, "
            "y aunque estemos lejos físicamente, quiero que cuando entres a escuchar música aquí "
            "sientas que estoy a tu lado, sosteniendo tu mano, gracias por ser mi inspiración "
            "y por aguantarme tanto, te amo inmensamente, mas de lo que las palabras pueden expresar, "
            "que la disfrutes...\n\nMi increíble y maravillosa novia."
        )
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        scroll = ScrollView(size_hint=(1, 1))
        label = Label(text=mensaje, font_size='19sp', color=(1, 1, 1, 1), halign='center', valign='middle', size_hint_y=None, text_size=(dp(270), None))
        label.bind(texture_size=label.setter('size'))
        scroll.add_widget(label)
        close_btn = Button(text="Cerrar", size_hint_y=None, height=dp(50), background_color=(1, 0.41, 0.71, 1), bold=True)
        content.add_widget(scroll)
        content.add_widget(close_btn)
        popup = Popup(title="♥ Para mi princesa ♥", title_color=(1, 0.41, 0.71, 1), title_size='22sp', content=content, size_hint=(0.9, 0.7), separator_color=(1, 0.41, 0.71, 1), background_color=(0.1, 0.1, 0.1, 0.95), auto_dismiss=False)
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

    def show_random_reason(self):
        razon = random.choice(MIS_RAZONES)
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        label = Label(text=f'"{razon}"', font_size='22sp', color=(1, 1, 1, 1), halign='center', valign='middle', text_size=(dp(250), None), bold=True, italic=True)
        close_btn = Button(text="♥", size_hint_y=None, height=dp(50), background_color=(1, 0.8, 0, 1), bold=True)
        content.add_widget(label)
        content.add_widget(close_btn)
        popup = Popup(title="Te amo porque...", title_color=(1, 0.8, 0, 1), content=content, size_hint=(0.8, 0.5), separator_color=(1, 0.8, 0, 1), background_color=(0.1, 0.1, 0.1, 0.95))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

    def go_to_gallery(self):
        self.manager.transition.direction = 'up'
        self.manager.current = 'gallery'

class GalleryScreen(Screen):
    is_loaded = False

    def on_enter(self):
        if not self.is_loaded:
            self.load_images()
            self.is_loaded = True

    def load_images(self):
        grid = self.ids.gallery_grid
        grid.clear_widgets()

        if not os.path.exists(GALLERY_DIR):
            grid.add_widget(Label(text="No existe assets/gallery", size_hint_y=None, height=50))
            return

        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
        
        images = []
        for root, dirs, files in os.walk(GALLERY_DIR):
            for f in files:
                if f.lower().endswith(valid_extensions):
                    full_path = os.path.join(root, f)
                    images.append(full_path)
        
        images.sort()

        if not images:
            grid.add_widget(Label(text="Agrega fotos en assets/gallery", size_hint_y=None, height=50))
            return

        for img_path in images:
            img_widget = Image(
                source=img_path,
                size_hint_y=None,
                height=dp(200),
                allow_stretch=True,
                keep_ratio=True,
                mipmap=True
            )
            grid.add_widget(img_widget)

    def go_back(self):
        self.manager.transition.direction = 'down'
        self.manager.current = 'library'

class PlayerScreen(Screen):
    sound = None
    playlist = []
    current_index = 0
    paused_time = 0
    is_manual_stop = False
    background_color = ListProperty([0.1, 0.1, 0.1, 1])
    
    def start_playlist(self, song_list, index):
        self.playlist = song_list
        self.current_index = index
        self.paused_time = 0 
        self.load_track()
        self.manager.transition.direction = 'left'
        self.manager.current = 'player'

    def format_time(self, seconds):
        if seconds < 0: return "00:00"
        m = int(seconds / 60)
        s = int(seconds % 60)
        return f"{m:02d}:{s:02d}"

    def load_track(self):
        # DETENER RELOJES ANTES QUE NADA
        Clock.unschedule(self.update_progress)
        
        # SI HAY AUDIO SONANDO, PARARLO LIMPIAMENTE
        if self.sound:
            try:
                self.sound.unbind(on_stop=self.on_song_finish) # Romper conexión
                self.sound.stop()
            except:
                pass # Si falla al parar, ignorar
            self.sound = None
        
        self.ids.current_time_lbl.text = "00:00"
        self.ids.total_time_lbl.text = "00:00"
        self.ids.progress_bar.value = 0

        song_filename = self.playlist[self.current_index]
        full_audio_path = os.path.join(AUDIO_DIR, song_filename)
        
        self.sound = SoundLoader.load(full_audio_path)
        
        # Reconectar
        if self.sound:
            self.sound.bind(on_stop=self.on_song_finish)

        base_name = song_filename.rsplit('.', 1)[0]
        jpg_path = os.path.join(IMAGES_DIR, base_name + ".jpg")
        png_path = os.path.join(IMAGES_DIR, base_name + ".png")
        default_path = os.path.join(IMAGES_DIR, 'default.jpg')
        
        img_src = default_path
        if os.path.exists(jpg_path): img_src = jpg_path
        elif os.path.exists(png_path): img_src = png_path

        self.ids.album_art.source = img_src
        self.background_color = random.choice(COLORES_SUAVES)
        self.ids.song_label.text = song_filename.replace('.mp3', '').replace('_', ' ')
        self.ids.btn_play_pause.text = "PAUSA"
        
        if self.sound:
            self.is_manual_stop = False
            self.sound.play()
            # Actualizar barra cada 1 SEGUNDO (Menos carga al CPU = Mejor Audio)
            Clock.schedule_interval(self.update_progress, 1.0)
            # Leer duración despues de 1 seg para asegurar carga
            Clock.schedule_once(self.set_duration_label, 1.0)

    def set_duration_label(self, dt):
        if self.sound and self.sound.length > 0:
            self.ids.total_time_lbl.text = self.format_time(self.sound.length)
            self.ids.progress_bar.max = self.sound.length

    def on_song_finish(self, instance):
        # DETENER EL RELOJ DE LA BARRA INMEDIATAMENTE
        Clock.unschedule(self.update_progress)
        
        if not self.is_manual_stop:
            # Esperar 0.5s para cambio suave
            Clock.schedule_once(lambda dt: self.play_next(), 0.5)

    def update_progress(self, dt):
        if self.sound and self.sound.state == 'play':
            current = self.sound.get_pos()
            self.ids.progress_bar.value = current
            self.ids.current_time_lbl.text = self.format_time(current)

    def seek_audio(self, instance, touch):
        if self.sound and instance.collide_point(*touch.pos):
            self.sound.seek(instance.value)

    def toggle_play(self):
        if self.sound:
            if self.sound.state == 'play':
                self.is_manual_stop = True
                self.paused_time = self.sound.get_pos()
                self.sound.stop()
                self.ids.btn_play_pause.text = "PLAY"
            else:
                self.is_manual_stop = False
                self.sound.play()
                if self.paused_time > 0:
                    self.sound.seek(self.paused_time)
                self.ids.btn_play_pause.text = "PAUSA"

    def play_next(self):
        if not self.playlist: return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.paused_time = 0
        self.load_track()

    def play_prev(self):
        if not self.playlist: return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.paused_time = 0
        self.load_track()

    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'library'

class MusicApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(IntroScreen(name='intro'))
        sm.add_widget(LibraryScreen(name='library'))
        sm.add_widget(GalleryScreen(name='gallery'))
        sm.add_widget(PlayerScreen(name='player'))
        return sm
    
    def get_resource(self, filename):
        return os.path.join(IMAGES_DIR, filename)
    
    def on_pause(self):
        return True

if __name__ == '__main__':
    MusicApp().run()
