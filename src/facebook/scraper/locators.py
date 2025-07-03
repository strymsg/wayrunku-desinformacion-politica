"""
This is part of wayrunku-desinformacion-politica
Copyright Rodrigo Garcia 2025
"""

locators = {
    'profiles': {
        'title': {
            'stype': 'css',
            'value': 'div.x1e56ztr h1.html-h1.x11i5rnm'
        },
        'friends-count': {
            'stype': 'xpath',
            'value': "//span[@dir='auto']/a[contains(@href, '/friends/')]"
        },
        'about-tab-by-name': {
            'stype': 'xpath',
            # Por ejemplo: Publicaciones, Información, Amigos, etc.
            'value': lambda label: f"//a[contains(@class,'x3nfvp2 xrbpyxo x1itg65n x16dsc37')]//span[text()='{label}']"
        },
        'friends': {
            
        },
        'restricted-profile': {
            'stype': 'xpath',
            'value': '//div[@class="xzsf02u x1rrkw1b x1lkfr7t"][@aria-level="1"][contains(text(), "restringió su perfil")]'
        }
    },
    'figure-profiles': {
        'followers-count': {
            'stype': 'xpath',
            'value': "//a[contains(@href,'followers')][contains(.,'seguidores')]"
            # ejemplo 233 mil seguidores
        },
        'following-count': {
            'stype': 'xpath',
            'value': "//a[contains(@href,'following')][contains(.,'seguidos')]"
        },
        'profile-transparency-btn': {
            'stype': 'xpath',
            'value': "//a[contains(@href,'transparency')]/span[contains(.,'Transparencia')]"
        },
        'creation-date': {
            'stype': 'xpath',
            'value': "//span[@class='xi81zsa x1nxh6w3 x1sibtaa'][text()='Fecha de creación']/../../../..//span[@dir='auto']"
        }
    },
    'posts': {
        'container-by-number': {
            'stype': 'xpath',
            'value': lambda number: f'//div[@aria-posinset="{number}"][@class="x1a2a7pz"]'
        },
        'container': { # parece ser
            'stype': 'xpath',
            #'value': '//div[@class="x1a2a7pz"]'
            'value': '//div[@data-virtualized="false"]'

            #'value': '//span[@class="html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs xkrqix3 x1sur9pj"]'
            # tambien quiza parece ser mejor usar el boton me gusta (pulgar arriba)
            # //span[@class="x3nfvp2"]/i

            # pruebas
            # //div[@class="xabvvm4 xeyy32k x1ia1hqs x1a2w583 x6ikm8r x10wlt62"][@data-visualcompletion="ignore-dynamic"]/../div/../..
        },
        'container-main': {
            'stype': 'xpath',
            'value': '//div[@data-virtualized="false"]/../../div'
        },
        'interact-container': {
            # O todo el contenedor de botones (me gusta, comentar, compartir)
            # 
            'stype':'xpath',
            #'value': '//span[@class="x3nfvp2"]/i/../../../../../../../../..'
            'value': '//div[@class="xabvvm4 xeyy32k x1ia1hqs x1a2w583 x6ikm8r x10wlt62"][@data-visualcompletion="ignore-dynamic"]'
        },
        'react-count': {
            # Tambien al hacer click se abre el modal con el conteo de reacciones
            'stype': 'xpath',
            'value': '//div[@class="x1a2a7pz"]//span[@class="x1e558r4"]'
        },
        'react-count-c': { # child element of post
            # Tambien al hacer click se abre el modal con el conteo de reacciones
            'stype': 'xpath',
            'value': './/span[@class="x1e558r4"]'
        },
        'comment-count': {
            'stype': 'xpath',
            'value': "//div[@class='x1a2a7pz']//span[contains(@class, 'xkrqix3 x1sur9pj')][contains(text(), 'comentarios')]",
        },
        'comment-count-c': { # child element of post
            'stype': 'xpath',
            'value': ".//span[contains(@class, 'xkrqix3 x1sur9pj')][contains(text(), 'comentarios')]",
        },
        'share-count': {
            'stype': 'xpath',
            'value': "//div[@class='x1a2a7pz']//span[contains(@class, 'xkrqix3 x1sur9pj')][contains(text(), 'compartido')]"
        },
        'share-count-c': { # child element of post
            'stype': 'xpath',
            'value': ".//span[contains(@class, 'xkrqix3 x1sur9pj')][contains(text(), 'compartido')]"
        },
        'share-count-rel-to-comment': { # relative to comment count
            'stype': 'xpath',
            'value': lambda root_locator: f"{root_locator}/../../..//span[contains(@class, 'xkrqix3 x1sur9pj')][contains(text(), 'compartido')]"
        },
        'share-btn-rel-to-comment': { # relative to comment count
            'stype': 'xpath',
            'value': lambda root_locator: f'{root_locator}/../../../../../..//span[@data-ad-rendering-role="share_button"]'
        },
        'share-btn-rel-to-like-btn': { # relative to like button
            'stype': 'xpath',
            'value': lambda root_locator: f'{root_locator}//span[@data-ad-rendering-role="me gusta_button"]/../../../../../..//span[@data-ad-rendering-role="share_button"]' 
        },
        'copy-url': {
            # This works by first clicking `share-btn-rel-to-comment'
            'stype': 'xpath',
            'value': '//div[@class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x1iyjqo2 x2lwn1j"]//span[text()="Copiar enlace"]'
        },
        'react-total-reactions': {
            'stype': 'xpath',
            #'value': lambda root_locator: f'{root_locator}//span[@class="x1e558r4"]'
            #'value': lambda root_locator: f'{root_locator}//span[@class="x1e558r4"]/../../../../../../div',
            'value': lambda root_locator: f'{root_locator}//span[@class="xt0b8zv x1jx94hy xrbpyxo x1lbueug"]'
        },
        'react-like-count': {
            # me gusta
            'stype': 'xpath',
            'value': "//div[@role='tab'][contains(@aria-label, 'con Me gusta')]"
        },
        'react-love-count': {
            # me encanta
            'stype': 'xpath',
            'value': "//div[@role='tab'][contains(@aria-label, 'con Me encanta')]"
        },
        'react-icare-count': {
            # me importa
            'stype': 'xpath',
            'value': "//div[@role='tab'][contains(@aria-label, 'con Me importa')]"
        },
        'react-sad-count': {
            # me entristece
            'stype': 'xpath',
            'value': "//div[@role='tab'][contains(@aria-label, 'con Me entristece')]"
        },
        'react-wow-count': {
            # me asombra
            'stype': 'xpath',
            'value': "//div[@role='tab'][contains(@aria-label, 'con Me asombra')]"
        },
        'react-angry-count': {
            # me enoja
            'stype': 'xpath',
            'value': "//div[@role='tab'][contains(@aria-label, 'con Me enoja')]"
        },
        'react-haha-count': {
            # me divierte
            'stype': 'xpath',
            'value': "//div[@role='tab'][contains(@aria-label, 'con Me divierte')]"
        },
        'react-modal-close': {
            'stype': 'css',
            #'value': 'div.x1d52u69.xktsk01 > div[aria-label="Cerrar"]'
            'value': 'div.xyqm7xq.x1ys307a > div[aria-label="Cerrar"]'
        },
        'posted-by': {
            # Nombre del perfil que hizo el post original
            # La estrategia seria, primero hacer scroll al 'container' de post y luego ejecutar este locator, solo seleccionar al primero
            'stype': 'xpath',
            'value': '//div[@class="x1a2a7pz"]//div[@data-ad-rendering-role="profile_name"]//a/strong/span'
        },
        'posted-date': {
            'stype': 'xpath',
            'value': '//div[@class="x1a2a7pz"]//div[@class="xu06os2 x1ok221b"]//span[@class="x1rg5ohu x6ikm8r x10wlt62 x16dsc37 xt0b8zv"]'
        },
        # child element of post
        'posted-date-c': {
            'stype': 'xpath',
            'value': lambda root_locator: f'{root_locator}//div[@class="xu06os2 x1ok221b"]//span[@class="x1rg5ohu x6ikm8r x10wlt62 x16dsc37 xt0b8zv"]'
        },
        'posted-date-text': {
            # Para obtener el texto de la fecha de publicacion, primero hay que hacer hover en
            # el elemento 'posted-date', luego se revela un tooltip con el siguiente locator
            'stype': 'xpath',
            'value': "//div[@class='__fb-dark-mode']//div[@role='tooltip']/span"
        },
        

        'post-content': {
            # tomar en cuenta #«r1c1» (funciona para el post 1

            # misc
            # div arriba del container del post
            # aria-describedby="«r1ea» «r1eb» «r1ec» «r1ee» «r1ed»"
            # aria-labelledyby="«r1e9»"

            # De aqui salen locators
            # fecha: #«r1ea»
            # text del post: #«r1eb»
            # Contenido (video o imagen): #«r1ec»
            # Contador de reacciones (boton): #«r1ee»
            # Contador de comentarios: #«r1ed»


            ## Otro ejemplo
            # «r1gt» «r1gu» «r1gv» «r1h1» «r1h0»
            # «r1gt»: Fecha (parece cuando es un repost tiene el nombre de otra persona aparte de solo el texto de la fecha)
            # «r1gu»: Contenido (texto)
            # «r1gv»: Contenido (video o imagen)
            # «r1h1»: Contador de reacciones (boton)
            # «r1h0»: Contador de comentarios (texto)

            # En general
            # Locator: //div[@data-virtualized="false"]/../../div
            # Retorna
            # <div aria-posinset="2" aria-describedby="«r1c0» «r1c1» «r1c2» «r1c4» «r1c3»" aria-labelledby="«r1bv»" class="x1a2a7pz">...</div>
            # De este elemento, la prop `aria-describedby' tiene los ids de:

            # aria-describedby="<Fecha> <Contenido textual> <Contenido multimedia> <contador de reacciones (boton)> <Contador de comentarios>

            # aria-labelledyby=<Nombre del perfil>
            
            
        },

        ## Para reels ##
        'post-reel-url-rel-to-content-locator': {
            # Para obtener la url de un reel, la estrategia es:
            # Usar el locator de contenido dinamico, por ejemplo «r1ea» y combinarlo con este
            # asi queda: //*[@id='«r1ea»']//a[@aria-label="Abrir reel en el visor de Reels"]
            # De este elemento la url se encuentra en la prop. href
            'stype': 'xpath',
            'value': lambda post_locator: f'{post_locator}//a[@aria-label="Abrir reel en el visor de Reels"]'
        },
        'post-reel-content-rel-to-content-locator': {
            'stype': 'xpath',
            #'value': lambda post_locator: f'{post_locator}//a[@aria-label="Abrir reel en el visor de Reels"]//div[@class="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a"]'
            'value': lambda post_locator: f'{post_locator}//div[@class="xdj266r x14z9mp xat24cr x1lziwak x1vvkbs x126k92a"]'
        },
        'post-reel-date-rel-to-content-locator': {
            # Esto devuelve un array, solo se debe seleccionar el primer elemento o
            # construir:
            # (//*[@id='«r1ea»']//a[@aria-label="Abrir reel en el visor de Reels"]//span[@class="html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j"])[1]
            'stype': 'xpath',
            # Revisar lo anterior ^^^ por alguna razon el locator no funciona usando desde playwright, pero en los navegadores directamente si.

            'value': lambda post_locator: f'({post_locator}//a[@aria-label="Abrir reel en el visor de Reels"]//span[@class="html-span xdj266r x14z9mp xat24cr x1lziwak xexx8yu xyri2b x18d9i69 x1c1uobl x1hl2dhg x16tdsg8 x1vvkbs x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j x1mshkth"])[1]'
        },
        'post-reel-reactions-to-content-locator': {
            # Construir obteniendo el quinto elemento, ejemplo:
            # (//*[@id='«re»']//a[@aria-label="Abrir reel en el visor de Reels"]//span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"])[5]
            'stype': 'xpath',
            #'value': lambda post_locator: f'({post_locator}//a[@aria-label="Abrir reel en el visor de Reels"]//span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"])[5]'
            #'value': lambda post_locator: f'{post_locator}//a[@aria-label="Abrir reel en el visor de Reels"]//div[@aria-label="Me gusta"]/../..//span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"]',
            'value': lambda post_locator: f'{post_locator}//a[@aria-label="Abrir reel en el visor de Reels"]//div[@aria-label="Me gusta"]/../..//span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"]'
        },
        'post-reel-comments-to-content-locator': {
            # Construir obteniendo el quinto elemento, ejemplo:
            # (//*[@id='«re»']//a[@aria-label="Abrir reel en el visor de Reels"]//span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"])[6]
            'stype': 'xpath',
            'value': lambda post_locator: f'{post_locator}//div[@aria-label="Comentar"]/../..//span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"]'
            #'value': lambda post_locator: f'({post_locator}//a[@aria-label="Abrir reel en el visor de Reels"]//span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"])[6]'
        },
        'post-reel-shares-to-content-locator': {
            # Construir obteniendo el quinto elemento, ejemplo:
            # (//*[@id='«re»']//a[@aria-label="Abrir reel en el visor de Reels"]//span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"])[7]
            'stype': 'xpath',
            #'value': lambda post_locator: f'({post_locator}//a[@aria-label="Abrir reel en el visor de Reels"]//span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"])[7]'
            'value': lambda post_locator: f'{post_locator}//div[@aria-label="Compartir"]/../..//span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"]'
        },
    }
}
