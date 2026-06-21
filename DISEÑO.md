# MeaCore Quest — Documento de Diseño

## 1. Pilares de Diseño y Propuesta de Valor

**Prioridad**: Progresión > Personalización > Cooperación > Inmersión > Comunidad > Competencia

- **Progresión**: Pilar central. Stats con fórmula Solo Leveling (STR→ATK, CON→HP, INT→MATK/MP, DEX→crit/evasión, VIT→MDEF). 3 puntos de stat + 1 skill point por nivel. Diminishing returns en crítico y evasión.
- **Personalización**: 8 slots de equipo (arma, armadura, escudo, casco, guantes, botas, anillo, capa) + capa cosmética superpuesta + mascota con stats propias.
- **Cooperación (asíncrona)**: Mazmorras y raids con oleadas, chat global simulado con 15 frases de "jugadores" (lazos débiles), sistema de misiones compartidas.
- **Inmersión**: Efectos reactivos (hit-stop 4 frames, screen shake, zoom punch, hit flash, knockback direccional, death tween, partículas por tipo de daño, trail visual de armas).
- **Comunidad (lazos débiles)**: Chat persistente con 15 NPCs "jugadores" que rotan frases de economía (venta de ítems, búsqueda de grupo). Sin interdependencia económica real en MVP — es single-player con ambientación MMO.

---

## 2. Arquitectura Matemática del Combate

### Fórmula de Daño: Modelo de División (Ratio Asintótico)

```
damage = raw * 100 / (100 + target_def)
```

- `raw = atk_stat * skill_multiplier * combo_multiplier`
- 50 ATK vs 0 DEF → 50 daño
- 50 ATK vs 100 DEF → 25 daño
- 50 ATK vs 200 DEF → 16.6 daño
- **Ventaja**: Nunca llega a 0 (floor a 1). Escala infinitamente sin muros de daño. Cada punto de DEF vale menos cuanto más tienes.

### Críticos: Rendimientos Decrecientes (Michaelis-Menten)

```gdscript
crit_chance = 0.03 + cap * dex / (half_point + dex)
# cap = 0.37, half_point = 80
```

- 30 DEX → 14.1% | 80 DEX → 21.5% | 200 DEX → 29.4%
- **Nunca supera 40%** (base 3% + cap 37%)
- Evasión: misma función con cap=0.22, half_point=140

### Pipeline de Ejecución (Orden estricto)

1. `raw = attack_stat * skill.multiplier * combo_multiplier`
2. `post_mitigation = raw * 100 / (100 + target_def)`
3. `post_mitigation = max(1, post_mitigation)` (floor)
4. `if crit: damage = int(post_mitigation * 1.5)`
5. `target.take_damage(damage, is_crit)`

---

## 3. Sistema de Atributos y Estadísticas

### Relación Atributos → Derivados

| Atributo | HP | MP | ATK | MATK | DEF | MDEF | Crit | Evasión |
|----------|:--:|:--:|:---:|:----:|:---:|:----:|:----:|:-------:|
| **STR** | | | +2 | | | | | |
| **DEX** | | | | | | | DR | DR |
| **INT** | | +5 | | +2 | | | | |
| **CON** | +10 | | | | +0.5 | | | |
| **VIT** | | | | | | +0.5 | | |

### Rendimientos Decrecientes (DR)

```gdscript
func _diminishing_return(value: float, cap: float, half_point: float) -> float:
    return cap * value / (half_point + value)
```

- Modelo Michaelis-Menten (no tangente hiperbólica ni logística)
- **half_point**: valor donde se alcanza la mitad del cap. DEX half_point=80 para crit significa que con 80 DEX tienes 18.5% de crit (la mitad del cap 37%).
- No hay exponente `n` — es lineal en el numerador, no sigmoide.

### Salud Efectiva (EH)

```gdscript
var dr = float(def) / (def + 100.0)
eh = max_hp / (1.0 - dr)
```

- 50 DEF → 33.3% reducción → EH = HP × 1.5
- 100 DEF → 50% reducción → EH = HP × 2.0
- 200 DEF → 66.7% reducción → EH = HP × 3.0
- EH escala linealmente con DEF (cada punto de DEF suma ~1% de EH), no cuadráticamente.

---

## 4. Persistencia y Simulación del Entorno

**Persistencia**: Solo **persistencia de personaje** (stats, inventario, equipo, mascota, cosméticos, misiones completadas). No hay mundo persistente.

**No implementado** (fuera de alcance del MVP):
- Sin construcción de casas ni modificación de terreno
- Sin propagación de fuego
- Sin clima dinámico
- Sin degradación de estructuras
- Sin economía persistente entre sesiones

El mundo es proceduralmente generado con TileMap (hierba, agua, paredes, árboles, portales) pero no mutable por el jugador. La simulación se limita a respawn de enemigos (10s), chat simulado (12s entre mensajes) y misiones diarias (reset por fecha).

---

## 5. Interfaz y Experiencia de Usuario (UI/UX)

### Divulgación Progresiva

1. **Pantalla de creación**: Solo nombre + 3 clases con stats base visibles. Sin fórmulas.
2. **Asignación de stats**: 5 puntos para distribuir con previsualización en vivo de derivados (HP, MP, ATK, MATK, DEF, MDEF, Crit%, EH). Ocultas las fórmulas, muestras los resultados.
3. **HUD de juego**: Frame de jugador (HP/MP/XP/nivel), target frame, hotbar de skills, chat, quest tracker. Sin números de stats.
4. **Panel de personaje**: Stats completos (STR/DEX/INT/CON/VIT) + derivados + equipo. Solo visible al abrirlo explícitamente.
5. **Tooltips**: Al hacer hover sobre items, muestran stats con formato `+X STAT` sin explicar la fórmula de daño.

### Organización del Panel de Personaje

```
┌─────────────────────────────────────────────┐
│         [Identificación: Clase, Nivel]       │
│ ┌─────────────────┐  ┌────────────────────┐ │
│ │ STATS           │  │ EQUIPO             │ │
│ │ STR: 12         │  │ [Arma] [Casco]     │ │
│ │ DEX: 8          │  │ [Armadura] [Botas] │ │
│ │ INT: 14         │  │ [Escudo] [Guantes] │ │
│ │ CON: 7          │  │ [Anillo] [Capa]    │ │
│ │ VIT: 9          │  │                    │ │
│ │                 │  │ DERIVADOS          │ │
│ │ Pts: 3 [Asignar]│  │ ATK MATK DEF       │ │
│ │                 │  │ MDEF Crit Eva EH   │ │
│ └─────────────────┘  └────────────────────┘ │
└─────────────────────────────────────────────┘
```

---

## 6. Modelo de Progresión y Grupo

### Zonas Estáticas (sin level scaling)

| Zona | Enemigos | Nivel |
|------|----------|:-----:|
| Pradera (Sur) | Slimes | 1 |
| Bosque (Este) | Goblins | 2 |
| Cementerio (Noroeste) | Esqueletos | 3 |
| Arena (Norte) | Boss Demonio | 5 |
| Mazmorra: Cueva de Slimes | Slime Rey | 2+ |
| Mazmorra: Cripta | Esqueleto Lord | 3+ |
| Raid: Campamento Goblin | Jefe Goblin (5 oleadas) | 3+ |

**Side-kicking**: No implementado. Es single-player; no hay sistema de grupo ni de nivelación automática. La progresión es individual.

### Curva de XP

```
xp_needed *= 1.5 (por nivel)
```

- Nvl 1→2: 100 XP | Nvl 2→3: 150 XP | Nvl 3→4: 225 XP | Nvl 4→5: 337 XP | Nvl 5→6: 506 XP

### Recompensas por Nivel

- +3 stat points
- +1 skill point
- Nivel 3: desbloqueo de tercera habilidad (Torbellino / Furia de Hielo / Flechas Lluvia)
- Mazmorras: desbloquean mascotas
- Raids: desbloquean cosméticos
