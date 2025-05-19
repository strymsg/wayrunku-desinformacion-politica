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
            'value': "./../../..//span[contains(@class, 'xkrqix3 x1sur9pj')][contains(text(), 'compartido')]"
        },
        'share-btn-rel-to-comment': { # relative to comment count
            'stype': 'xpath',
            'value': './../../../../../..//span[@data-ad-rendering-role="share_button"]'
        },
        'copy-url': {
            # This works by first clicking `share-btn-rel-to-comment'
            'stype': 'xpath',
            'value': '//div[@class="x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x1iyjqo2 x2lwn1j"]//span[text()="Copiar enlace"]'
        },
        'react-like-count': {
            # me gusta
            'stype': 'xpath',
            'value': "//div[@class='x1ey2m1c x9f619 xds687c x17qophe x10l6tqk x13vifvy']//div[contains(@aria-label,'Me gusta')]"
        },
        'react-love-count': {
            # me encanta
            'stype': 'xpath',
            'value': "//div[@class='x1ey2m1c x9f619 xds687c x17qophe x10l6tqk x13vifvy']//div[contains(@aria-label,'Me encanta')]"
        },
        'react-icare-count': {
            # me importa
            'stype': 'xpath',
            'value': "//div[@class='x1ey2m1c x9f619 xds687c x17qophe x10l6tqk x13vifvy']//div[contains(@aria-label, 'Me importa')]"
        },
        'react-sad-count': {
            # me entristece
            'stype': 'xpath',
            'value': "//div[@class='x1ey2m1c x9f619 xds687c x17qophe x10l6tqk x13vifvy']//div[contains(@aria-label,'Me entristece')]"
        },
        'react-wow-count': {
            # me asombra
            'stype': 'xpath',
            'value': "//div[@class='x1ey2m1c x9f619 xds687c x17qophe x10l6tqk x13vifvy']//div[contains(@aria-label,'Me asombra')]"
        },
        'react-angry-count': {
            # me enoja
            'stype': 'xpath',
            'value': "//div[@class='x1ey2m1c x9f619 xds687c x17qophe x10l6tqk x13vifvy']//div[contains(@aria-label,'Me enoja')]"
        },
        'react-haha-count': {
            # me divierte
            'stype': 'xpath',
            'value': '//div[@class="x1ey2m1c x9f619 xds687c x17qophe x10l6tqk x13vifvy"]//div[contains(@aria-label,"Me divierte")]'
        },
        'react-modal-close': {
            'stype': 'css',
            'value': 'div.x1d52u69.xktsk01 > div[aria-label="Cerrar"]'
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
            'value': './/div[@class="xu06os2 x1ok221b"]//span[@class="x1rg5ohu x6ikm8r x10wlt62 x16dsc37 xt0b8zv"]'
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
            
            
            }
    }
}
