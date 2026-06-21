# Propuesta de Plan de Sprints y Mapa del Proyecto para MeaCoreQuest (Versión Mejorada)

## 1. Cadencia y Duración de Sprints

Se mantiene una cadencia de **sprints de 2 semanas** para facilitar una gestión ágil del proyecto, permitiendo entregas incrementales y una retroalimentación constante. Cada sprint estará enfocado en un objetivo específico y contendrá un conjunto de tareas claramente definidas y priorizadas.

## 2. Epics y Módulos Principales

Basado en el análisis del `README.md` y la estructura actual del código, se han identificado y categorizado los siguientes epics o módulos fundamentales para el desarrollo de MeaCoreQuest:

| Epic | Nombre | Descripción Detallada |
| :--- | :--- | :--- |
| **Epic 1** | **Combate y Core Gameplay** | Este epic abarca todas las mecánicas fundamentales de interacción y combate del juego, incluyendo el movimiento del personaje, los sistemas de ataque y defensa, y la implementación de efectos visuales y de sonido que mejoran la experiencia de combate. |
| **Epic 2** | **Sistema de Personajes y Progresión** | Se centra en la gestión del personaje del jugador, su progresión a través de niveles, la asignación de atributos, la implementación de un sistema de clases distintivo y la gestión de equipamiento que influye en las estadísticas y habilidades. |
| **Epic 3** | **Mundo y Contenido** | Incluye la creación del entorno de juego, la generación procedural de mapas, la implementación de la inteligencia artificial de los enemigos, el diseño y la integración de un sistema de misiones, y la configuración de encuentros con jefes finales. |
| **Epic 4** | **Interfaz de Usuario y Sonido** | Este epic se dedica al desarrollo de la interfaz gráfica del usuario (GUI), incluyendo el HUD, los menús de inventario y personaje, y la integración de efectos de sonido y música que contribuyen a la atmósfera del juego. |
| **Epic 5** | **Calidad y Optimización** | Un epic transversal que asegura la estabilidad, el rendimiento y la mantenibilidad del código. Incluye refactorización, implementación de pruebas, optimización de recursos y la creación de documentación técnica exhaustiva. |

## 3. Propuesta de Sprints Detallados

A continuación, se presenta una propuesta mejorada de los primeros sprints, con un enfoque en la calidad y el detalle de cada tarea.

### Sprint 1: Fundamentos del Combate y Movimiento

**Objetivo:** Establecer una base sólida para el movimiento del jugador y las mecánicas de combate esenciales, garantizando una experiencia de juego fluida y reactiva.

**Tareas Clave:**
*   **Implementación de Movimiento Básico del Jugador (W/A/S/D o Flechas):** Desarrollar el sistema de entrada para el movimiento direccional del jugador, asegurando una respuesta precisa y la correcta interacción con el entorno de juego. Incluir detección de colisiones básicas.
*   **Desarrollo del Sistema de Ataque Básico (Click Izquierdo/Espacio):** Crear la lógica para el ataque principal del jugador, incluyendo animaciones de ataque, la definición de hitboxes y la detección de impactos contra entidades enemigas.
*   **Implementación del Dash Evasivo con I-frames (Click Derecho):** Diseñar y codificar la habilidad de dash, que permitirá al jugador moverse rápidamente y otorgará un breve período de invulnerabilidad (i-frames) para esquivar ataques. Asegurar la fluidez de la animación y la correcta duración de los i-frames.
*   **Integración de Hit-stop en los Impactos:** Añadir un efecto de 
congelamiento de frames (hit-stop) al momento de un impacto exitoso, tanto al atacar como al ser atacado, para mejorar la sensación de impacto y la retroalimentación visual del combate.

### Sprint 2: Progresión Básica y Primer Enemigo

**Objetivo:** Habilitar la progresión inicial del personaje y la introducción de un enemigo básico, sentando las bases para el sistema de RPG.

**Tareas Clave:**
*   **Implementación de Status Window y Atributos:** Desarrollar la interfaz y la lógica para la ventana de estado del personaje, mostrando atributos como STR, DEX, INT, CON, VIT. Asegurar que estos atributos influyan correctamente en las estadísticas de combate y otras habilidades del personaje.
*   **Desarrollo del Sistema de Subida de Nivel y Asignación de Puntos:** Crear el sistema de experiencia, la lógica para subir de nivel y la funcionalidad para que el jugador asigne puntos a sus atributos al alcanzar un nuevo nivel.
*   **Creación de Enemigo Básico (Slime) con IA Simple:** Diseñar e implementar un enemigo tipo Slime con un comportamiento básico de patrulla, detección del jugador y un patrón de ataque simple. Incluir su propia barra de vida y detección de daño.
*   **Implementación de HUD Básico (HP/MP):** Desarrollar la Interfaz de Usuario (HUD) en pantalla para mostrar de manera clara y legible las barras de salud (HP) y maná (MP) del jugador, actualizándose en tiempo real.

### Sprint 3: Habilidades y Proyectiles

**Objetivo:** Introducir mecánicas de habilidades activas y un sistema de proyectiles funcional para diversificar el combate.

**Tareas Clave:**
*   **Implementación del Sistema de Habilidades (1/2/3):** Desarrollar la infraestructura para que el jugador pueda usar habilidades activas asignadas a teclas numéricas. Esto incluye la gestión de costos de maná (MP), tiempos de reutilización (cooldowns) y la activación de efectos asociados.
*   **Desarrollo del Sistema de Proyectiles:** Crear un sistema robusto para el lanzamiento de proyectiles, esencial para clases a distancia como el Mago y el Arquero. Incluir la capacidad de los proyectiles para perforar múltiples enemigos (piercing) y causar daño en un área (AoE).
*   **Integración de Efectos Visuales y Sonoros para Habilidades:** Añadir efectos visuales (partículas, animaciones) y sonoros distintivos para cada habilidad, proporcionando una retroalimentación clara y satisfactoria al jugador.
*   **Balanceo Inicial de Habilidades:** Realizar un balanceo preliminar de los valores de daño, costos de MP y cooldowns de todas las habilidades implementadas, buscando un equilibrio justo entre las diferentes clases y estilos de juego.

## 4. Mapa del Proyecto (Roadmap) Mejorado

Para una visualización más clara y profesional del roadmap, se utilizará un diagrama de flujo que represente las dependencias y el progreso entre los epics y sprints. Este diagrama será generado con D2 para mayor flexibilidad y detalle.

```d2
direction: right

CoreGameplay: {shape: rectangle, label: "Epic 1: Combate y Core Gameplay", style: {fill: "#add8e6", stroke: "#3182bd", stroke-width: 2}}
CharacterProgression: {shape: rectangle, label: "Epic 2: Sistema de Personajes y Progresión", style: {fill: "#add8e6", stroke: "#3182bd", stroke-width: 2}}
WorldQuests: {shape: rectangle, label: "Epic 3: Mundo y Misiones", style: {fill: "#add8e6", stroke: "#3182bd", stroke-width: 2}}
UI_Sound: {shape: rectangle, label: "Epic 4: Interfaz de Usuario y Sonido", style: {fill: "#add8e6", stroke: "#3182bd", stroke-width: 2}}
QualityOptimization: {shape: rectangle, label: "Epic 5: Calidad y Optimización", style: {fill: "#add8e6", stroke: "#3182bd", stroke-width: 2}}

Sprint1: {shape: circle, label: "Sprint 1: Fundamentos del Combate", style: {fill: "#aaffaa", stroke: "#228b22", stroke-width: 2}}
Sprint2: {shape: circle, label: "Sprint 2: Progresión Básica y Enemigo", style: {fill: "#aaffaa", stroke: "#228b22", stroke-width: 2}}
Sprint3: {shape: circle, label: "Sprint 3: Habilidades y Proyectiles", style: {fill: "#aaffaa", stroke: "#228b22", stroke-width: 2}}

CoreGameplay -> Sprint1
CharacterProgression -> Sprint2
CoreGameplay -> Sprint3

Sprint1 -> Sprint2: "Dependencia Crítica"
Sprint2 -> Sprint3: "Dependencia Crítica"

```

**Consideraciones para la Calidad (Mejoradas):**

*   **Revisiones de Código Rigurosas:** Implementar un proceso de revisión de código obligatorio para todas las nuevas características y correcciones de errores, asegurando la adherencia a los estándares de codificación, la identificación temprana de defectos y la mejora continua de la calidad del software.
*   **Estrategia de Pruebas Exhaustiva:** Fomentar una cultura de desarrollo impulsado por pruebas (TDD) donde sea aplicable. Desarrollar pruebas unitarias para componentes críticos, pruebas de integración para módulos interconectados y pruebas de aceptación para validar la funcionalidad desde la perspectiva del usuario.
*   **Documentación Viva:** Mantener la documentación técnica y de diseño actualizada en todo momento. Esto incluye comentarios claros y concisos en el código, un `README.md` completo, y la creación de una wiki o base de conocimientos para decisiones de diseño, guías de desarrollo y manuales de usuario.
*   **Refactorización Continua:** Asignar tiempo específico en cada sprint para la refactorización de código existente. Esto no solo mejora la legibilidad y mantenibilidad, sino que también reduce la deuda técnica y facilita la implementación de futuras características.
*   **Optimización de Rendimiento:** Monitorear y optimizar proactivamente el rendimiento del juego, identificando cuellos de botella y aplicando soluciones para garantizar una experiencia de juego fluida en diversas configuraciones de hardware.

Este plan de sprints y roadmap mejorado proporcionará una guía clara y detallada para el desarrollo de MeaCoreQuest, enfocándose en la calidad y la eficiencia en cada etapa.
