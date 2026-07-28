# ADR-005 — Ausencia de evidencia no es evidencia negativa: separar madurez de calidad

**Fecha:** 2026-07-28
**Estado:** Aceptado
**Decisionario:** Jose Acevedo

---

## Contexto

Distribución real de arquetipos de empleado en producción (2026-07-28), sobre 44 perfiles:

| Perfil | Personas | promotionScore (min–max) | skillLevel | efficiencyIndex | Experiencia media |
|---|---:|---|---:|---:|---:|
| `at-risk` | 17 | 0,193 – 0,324 | 0,24 | 0,071 | 0,21 años |
| `ghost` | 18 | 0,133 – 0,236 | 0,24 | 0,020 | 0,05 años |
| `neutral` | 9 | 0,206 – 0,370 | 0,29 | 0,076 | 0,26 años |

**Cero `anchor`, cero `high-potential`, cero `specialist`, cero `maverick`.** Todos los scores
comprimidos en la banda baja: `promotionScore` nunca supera 0,37 sobre 1; `efficiencyIndex` no
llega a 0,08.

La causa es `totalExperienceYears`: entre 0,05 y 0,26 años — semanas. `reliability` se compone de
`dataMaturity × dataQuality`, y `dataMaturity` crece con la masa de datos observada. Con pocas
semanas de observación, la madurez es baja para todos, y arrastra consigo todos los índices
derivados.

**El sistema está midiendo antigüedad en la plataforma, no calidad del trabajador.** Un encargado
con veinte años de oficio aparece como `ghost` porque CheckBiz lleva tres meses observándolo.

---

## Problema

El modelo actual **confunde dos cosas que nunca deben compartir etiqueta**:

- *No tengo suficiente evidencia sobre esta persona*
- *Esta persona rinde mal*

Publicar los arquetipos tal cual le diría a un cliente que 35 de sus 44 personas están "en riesgo"
o son "fantasmas". Además de ser falso, en un producto de control horario tiene **implicaciones
laborales serias**: nadie debe poder justificar una decisión sobre un trabajador con una etiqueta
que en realidad significa "el sistema es nuevo".

---

## Decisión

1. **Ninguna etiqueta de arquetipo se publica mientras la madurez de esa persona esté por debajo
   del mínimo.** En su lugar se devuelve un estado explícito de observación insuficiente
   (`warming`, ADR-004), nunca `at-risk` ni `ghost`.

2. **La fiabilidad se normaliza por madurez** antes de compararse: se separa `dataQuality` (cómo
   de bien lo hace con lo observado) de `dataMaturity` (cuánto se ha observado), y solo la primera
   entra en comparaciones entre personas. Algoritmo en **TDR-003**.

3. **Las comparaciones son siempre relativas** — contra la propia historia, contra la cohorte de
   mismo puesto y responsabilidad, o contra los demás centros. Nunca contra una escala universal
   fija, que con el estado actual deja a todo el mundo suspenso.

4. `at-risk` y `ghost` pasan a ser **conclusiones derivadas de una caída observada** contra la
   propia línea base, no del valor absoluto de un score.

---

## Justificación

**Es un requisito ético y legal, no solo estadístico.** Una etiqueta sobre una persona debe poder
sostenerse en una conversación con esa persona.

**Restaura la capacidad discriminante.** Si todos los perfiles son `at-risk`, el arquetipo no
informa. Separando madurez de calidad, las diferencias reales vuelven a emerger.

**Protege el diferencial.** El efecto centro (ADR-003) compara a cada persona consigo misma y por
eso es inmune a este sesgo. Coherencia: si esa es la razón de que funcione, debe ser la regla
general.

---

## Consecuencias

**Positivas**
- El panel deja de acusar en falso
- Los arquetipos recuperan valor informativo conforme madura la observación
- Se elimina un riesgo laboral y reputacional real

**Negativas / compromisos**
- Durante los primeros meses de cada cliente, gran parte de la capa de perfiles estará en
  `warming`. Es correcto: refleja la realidad
- Hay que fijar el umbral mínimo de observación por métrica
- Requiere revisar el cálculo de arquetipos aguas arriba; mientras tanto, el panel filtra en
  lectura para no publicar etiquetas no sostenibles
