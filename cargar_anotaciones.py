"""
Carga las 7 anotaciones cifradas en Supabase.
Requiere ANN_ENCRYPT_KEY y SUPABASE_SERVICE_ROLE_KEY en .env
"""
import subprocess, sys

anotaciones = [
    (
        "RV1960", 40, 18, 6,
        """La piedra que no se colgó nadie

Jesús no usa aquí lenguaje pastoral. Usa lenguaje de condena sin apelación. No dice «corrígete». Dice: mejor que estuvieras muerto antes de haberlo hecho.

En España, entre 1950 y 2020, al menos 440.000 personas fueron víctimas de abuso sexual en el ámbito de la Iglesia Católica, según el informe del Defensor del Pueblo de 2023. No son datos de una campaña anticlerical. Son datos del Estado.

Durante décadas, la respuesta institucional no fue la piedra de molino. Fue el traslado silencioso del agresor a otra parroquia. Fue el archivo sellado. Fue el comunicado pidiendo «proporcionalidad» en la cobertura mediática.

La Cadena COPE —propiedad de la Conferencia Episcopal— tituló durante años con el «0,2%»: la proporción de sacerdotes denunciados respecto al total del clero. El argumento que ningún jurado del mundo aceptaría como defensa, convertido en titular de portada.

Quien haga tropezar a uno de estos pequeños, decía Jesús.
La institución que gestiona su legado lleva setenta años administrando ese tropiezo."""
    ),
    (
        "RV1960", 41, 9, 42,
        """Escándalo con cobertura mediática propia

El término griego original es skandalizo: hacer caer, tender una trampa, destruir la fe de alguien. Marcos no habla de mal ejemplo. Habla de un acto que rompe a una persona desde adentro.

Los datos del informe Sauvé en Francia (2021) establecieron 330.000 víctimas. El informe alemán de 2022: más de 27.000 en ese país. Australia, Irlanda, Bélgica: el patrón se repite en cada país donde se ha investigado con independencia real. España fue de los últimos en hacerlo, y solo tras presión parlamentaria sostenida.

Durante todo ese tiempo, los medios de la propia Iglesia española construyeron un relato de persecución: que las cifras estaban infladas, que había «agenda ideológica», que el anticlericalismo distorsionaba la realidad.

Escándalo con departamento de comunicación propio.
Eso es lo que Marcos no imaginó."""
    ),
    (
        "RV1960", 42, 17, 2,
        """El mar más cercano siempre fue el silencio

Lucas escribe para una comunidad gentil, sin las referencias internas del judaísmo de Mateo. Lo que le importa transmitir es universal: hay una jerarquía en los crímenes, y atacar a quien no puede defenderse ocupa el lugar más alto.

El sistema de encubrimiento documentado en la Iglesia española —y en cada Iglesia nacional donde se ha investigado— no fue espontáneo. Fue estructural. Requirió decisiones activas: no llamar a la policía, no informar a las familias, reubicar al agresor, presionar a las víctimas para que guardasen silencio en nombre de la fe o de la institución.

No es negligencia. Es política.

La piedra de molino de Lucas pesa lo mismo en 2024 que en el siglo I.
La diferencia es que ahora sabemos los nombres de quienes decidieron no usarla."""
    ),
    (
        "RV1960", 23, 1, 17,
        """Lo que se aprende y lo que se enseña

Isaías habla a una nación religiosa. Templos llenos, liturgias perfectas, ofrendas abundantes. Y Dios diciéndoles: me cansan sus rituales. Lo que quiero es esto: justicia. Específicamente, justicia para quienes no tienen poder.

La Iglesia Católica española gestiona miles de colegios donde se educa a millones de niños. Es el mayor sistema educativo privado del país, financiado en gran parte con fondos públicos. En ese sistema, durante décadas, operaron agresores con protección institucional.

«Socorred al oprimido.» En los documentos internos que han salido a la luz —en España como en Irlanda, en Alemania como en Chile— la instrucción era otra: proteger a la institución primero. Las víctimas, después. O nunca.

Isaías no hablaba de una institución hostil a la religión.
Hablaba exactamente de esta."""
    ),
    (
        "RV1960", 24, 5, 28,
        """El lustre y los límites

Jeremías escribe sobre una clase dirigente religiosa que ha prosperado mientras pervierte la justicia. No sobre paganos. Sobre los guardianes de la ley sagrada que la doblan en beneficio propio.

La Iglesia española recibe anualmente más de 11.000 millones de euros en financiación pública directa e indirecta: asignación tributaria, exenciones fiscales, subvenciones, conciertos educativos. Es, por cualquier métrica, una institución que ha prosperado.

Y sin embargo, cuando las víctimas de abuso fueron a los tribunales eclesiásticos, el «pleito de los pobres» no prosperó. Cuando fueron a los tribunales civiles, los plazos de prescripción —que la propia Iglesia nunca impulsó reformar— habían vencido en la mayoría de los casos.

Engordados y lustrosos.
Jeremías lleva veintiséis siglos esperando que alguien le contradiga."""
    ),
    (
        "RV1960", 40, 23, 27,
        """La arquitectura de la apariencia

El sepulcro blanqueado es una imagen de higiene pública: en la ley judía, una tumba marcada de blanco avisa al viajero para que no la toque y no quede impuro. La hipocresía religiosa funciona igual: limpia por fuera para que nadie mire adentro.

La Iglesia Católica española construyó durante el siglo XX una imagen pública de garante moral de la nación. Custodio de la familia, de la infancia, de los valores. Esa imagen fue usada para acceder a los cuerpos de miles de menores, y después para silenciar lo que había ocurrido.

El informe del Defensor del Pueblo señala que la mayoría de los abusos se produjeron en contextos de confianza institucional: colegios religiosos, parroquias, movimientos juveniles. La arquitectura del sepulcro estaba perfectamente diseñada.

Blanca por fuera.
Los datos, adentro."""
    ),
    (
        "RV1960", 42, 18, 16,
        """De los tales

Esta frase es quizás la más usada en la iconografía cristiana de la infancia: el Cristo acogedor, los niños corriendo hacia él, la ternura como centro del mensaje.

Es también la más profanada.

«Dejad a los niños venir a mí.» En centenares de casos documentados en España, ese mandato fue invertido: los niños venían —enviados por sus familias, en la confianza de la fe— y lo que encontraron no fue protección sino depredación. Y sobre esa depredación, silencio. Y sobre ese silencio, estadística.

El 0,2% del que hablan ciertos medios son personas. Tenían nombres antes de que la institución los convirtiera en porcentaje. Tenían fe antes de que alguien en una posición de autoridad sagrada decidiera que su cuerpo era disponible.

De los tales es el reino de Dios.
De los tales también debería ser la justicia."""
    ),
]

if __name__ == "__main__":
    print(f"Cargando {len(anotaciones)} anotaciones cifradas...\n")
    for t, b, c, v, texto in anotaciones:
        r = subprocess.run(
            [sys.executable, "admin_annotations.py", "add", t, str(b), str(c), str(v), texto],
            capture_output=True, text=True, encoding="utf-8"
        )
        print(r.stdout.strip() or r.stderr.strip())
    print("\n--- Verificación ---")
    subprocess.run([sys.executable, "admin_annotations.py", "list"])