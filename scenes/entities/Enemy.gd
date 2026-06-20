extends CharacterBody2D

# Enemy properties configuration
@export var monster_id: String = "slime" # slime, goblin, skeleton, boss

# Combat state
var monster_name: String = ""
var level: int = 1
var max_hp: float = 10.0
var hp: float = 10.0
var atk: int = 2
var defense: int = 1
var speed: float = 40.0
var xp_reward: int = 10
var gold_reward: int = 5
var loot_item: String = ""
var loot_chance: float = 0.0

var is_dead: bool = false
var respawn_time: float = 10.0
var respawn_timer: float = 0.0

# AI State Machine
enum State { ROAM, CHASE, ATTACK, STAGGER }
var current_state: State = State.ROAM
var spawn_position: Vector2
var roam_target: Vector2
var roam_timer: float = 0.0

# Agro
var agro_range: float = 130.0
var attack_range: float = 28.0
var attack_cooldown: float = 1.5
var attack_timer: float = 0.0

# Knockback & Stagger
var knockback_velocity: Vector2 = Vector2.ZERO
var knockback_friction: float = 8.0
var stagger_duration: float = 0.2
var stagger_timer: float = 0.0

# Reference to player
var player_node: Node = null

# Animation spritesheet coordinates
var char_x_offset: int = 0
var char_y_offset: int = 0
var anim_frame: int = 0
var anim_timer: float = 0.0
var current_dir: int = 0 # 0: Down, 1: Up, 2: Left, 3: Right

# UI components
@onready var sprite: Sprite2D = $Sprite2D
@onready var hp_bar: ProgressBar = $HPBar
@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var name_label: Label = $NameLabel

func _ready():
	add_to_group("enemy")
	spawn_position = global_position
	
	# Connect mouse interaction for click targeting
	input_pickable = true
	mouse_entered.connect(_on_mouse_entered)
	
	setup_monster_stats()
	_pick_new_roam_target()

func setup_monster_stats():
	if monster_id == "slime":
		monster_name = "Slime Pegajoso"
		level = 1
		max_hp = 15.0
		hp = max_hp
		atk = 4
		defense = 1
		speed = 35.0
		xp_reward = 15
		gold_reward = 5
		loot_item = "slime_core"
		loot_chance = 0.50
		# Sheet mapping: Row 5, Col 2 (x=192, y=128)
		char_x_offset = 192
		char_y_offset = 128
		attack_range = 28.0
		agro_range = 100.0
	elif monster_id == "goblin":
		monster_name = "Goblin Asaltante"
		level = 2
		max_hp = 35.0
		hp = max_hp
		atk = 8
		defense = 2
		speed = 60.0
		xp_reward = 35
		gold_reward = 12
		loot_item = "wolf_claw"
		loot_chance = 0.40
		# Sheet mapping: Row 6, Col 0 (x=0, y=256)
		char_x_offset = 0
		char_y_offset = 256
		attack_range = 30.0
		agro_range = 130.0
	elif monster_id == "skeleton":
		monster_name = "Guerrero Esqueleto"
		level = 3
		max_hp = 60.0
		hp = max_hp
		atk = 14
		defense = 4
		speed = 50.0
		xp_reward = 75
		gold_reward = 25
		loot_item = "steel_shield"
		loot_chance = 0.15
		# Sheet mapping: Row 7, Col 1 (x=96, y=256)
		char_x_offset = 96
		char_y_offset = 256
		attack_range = 30.0
		agro_range = 140.0
	elif monster_id == "boss":
		monster_name = "Señor Oscuro (BOSS)"
		level = 5
		max_hp = 300.0
		hp = max_hp
		atk = 24
		defense = 7
		speed = 55.0
		xp_reward = 500
		gold_reward = 250
		loot_item = "demon_heart"
		loot_chance = 1.0 # 100% Drop
		# Sheet mapping: Row 8, Col 2 (x=192, y=256)
		char_x_offset = 192
		char_y_offset = 256
		attack_range = 45.0
		agro_range = 180.0
	elif monster_id == "dummy":
		monster_name = "Muñeco de Práctica"
		level = 1
		max_hp = 10000.0
		hp = max_hp
		atk = 0
		defense = 2
		speed = 0.0
		xp_reward = 0
		gold_reward = 0
		loot_chance = 0.0
		attack_range = 0.0
		agro_range = 0.0
		# Show training dummy as signpost
		sprite.texture = load("res://assets/tileset.png")
		sprite.region_rect = Rect2(0, 16, 16, 16) # Signpost tile
		
	# Scale boss size
	if monster_id == "boss":
		sprite.scale = Vector2(1.8, 1.8)
		collision_shape.scale = Vector2(1.5, 1.5)
	elif monster_id == "dummy":
		sprite.scale = Vector2(1.5, 1.5)
		
	name_label.text = "Lvl " + str(level) + " " + monster_name
	if monster_id == "boss":
		name_label.label_settings = LabelSettings.new()
		name_label.label_settings.font_color = Color(1.0, 0.2, 0.2)
		name_label.label_settings.outline_size = 3
		name_label.label_settings.outline_color = Color.BLACK
		
	hp_bar.max_value = max_hp
	hp_bar.value = hp
	
	if monster_id != "dummy":
		update_sprite_rect()

func _physics_process(delta):
	if is_dead:
		_process_respawn(delta)
		return

	# Redraw target circle if selected
	queue_redraw()

	if monster_id == "dummy":
		# Auto heal dummy if damaged
		if hp < max_hp:
			hp = min(max_hp, hp + 50.0 * delta)
			hp_bar.value = hp
		return

	# Tick timers
	if attack_timer > 0.0:
		attack_timer -= delta


	# Search player if not found
	if player_node == null:
		var players = get_tree().get_nodes_in_group("player")
		if players.size() > 0:
			player_node = players[0]

	# Knockback decay
	if knockback_velocity.length() > 0.0:
		knockback_velocity = knockback_velocity.move_toward(Vector2.ZERO, knockback_friction * delta)
		if knockback_velocity.length() < 5.0:
			knockback_velocity = Vector2.ZERO

	# Stagger timer
	if current_state == State.STAGGER:
		stagger_timer -= delta
		if stagger_timer <= 0.0:
			current_state = State.CHASE
		else:
			velocity = knockback_velocity
			move_and_slide()
			return

	# State Machine Logic
	match current_state:
		State.ROAM:
			_process_roam(delta)
		State.CHASE:
			_process_chase(delta)
		State.ATTACK:
			_process_attack(delta)

	# Face direction animation
	_animate_movement(delta)

func _process_roam(delta):
	# Check if player is near
	if player_node != null and not player_node.is_dead:
		var dist = global_position.distance_to(player_node.global_position)
		if dist <= agro_range and not _is_in_safe_zone(player_node.global_position):
			current_state = State.CHASE
			return

	roam_timer -= delta
	if roam_timer <= 0.0:
		_pick_new_roam_target()
		
	var dir = (roam_target - global_position)
	if dir.length() > 5.0:
		velocity = dir.normalized() * (speed * 0.6)
		move_and_slide()
	else:
		velocity = Vector2.ZERO

func _pick_new_roam_target():
	roam_timer = randf_range(3.0, 6.0)
	var angle = randf() * 2.0 * PI
	var radius = randf_range(20.0, 60.0)
	roam_target = spawn_position + Vector2(cos(angle), sin(angle)) * radius

func _process_chase(delta):
	if player_node == null or player_node.is_dead or _is_in_safe_zone(player_node.global_position):
		current_state = State.ROAM
		velocity = Vector2.ZERO
		return

	var dist = global_position.distance_to(player_node.global_position)
	
	if dist > agro_range * 1.5:
		current_state = State.ROAM
		velocity = Vector2.ZERO
		return
		
	if dist <= attack_range:
		current_state = State.ATTACK
		velocity = Vector2.ZERO
		return

	# Move towards player
	var dir = (player_node.global_position - global_position).normalized()
	velocity = dir * speed
	move_and_slide()

func _process_attack(delta):
	if player_node == null or player_node.is_dead:
		current_state = State.ROAM
		return

	var dist = global_position.distance_to(player_node.global_position)
	if dist > attack_range * 1.2:
		current_state = State.CHASE
		return

	# Attack check
	if attack_timer <= 0.0:
		attack_timer = attack_cooldown
		# Lunge towards player
		var attack_dir = (player_node.global_position - global_position).normalized()
		var tween = create_tween()
		tween.tween_property(sprite, "offset", attack_dir * 6.0, 0.08)
		tween.tween_property(sprite, "offset", Vector2.ZERO, 0.08)
		
		# Deal damage
		player_node.take_damage(atk)

func _is_in_safe_zone(pos: Vector2) -> bool:
	# Safe zone around coordinates (0 to 600, 0 to 600) (Town boundaries)
	return pos.x > -50 and pos.x < 650 and pos.y > -50 and pos.y < 650

func _animate_movement(delta):
	if velocity.length() > 2.0:
		# Determine current_dir
		if abs(velocity.x) > abs(velocity.y):
			current_dir = 3 if velocity.x > 0 else 2
		else:
			current_dir = 0 if velocity.y > 0 else 1
			
		anim_timer += delta
		if anim_timer >= ANIM_SPEED():
			anim_timer = 0.0
			anim_frame = 1 if anim_frame == 2 else 2
	else:
		anim_frame = 0
		anim_timer = 0.0
		
	update_sprite_rect()

func ANIM_SPEED() -> float:
	# Slimes bouncy animation slower, skeletons clunky
	if monster_id == "slime": return 0.20
	return 0.15

func update_sprite_rect():
	var frame_x = char_x_offset + anim_frame * 32
	var frame_y = char_y_offset + current_dir * 32
	sprite.region_rect = Rect2(frame_x, frame_y, 32, 32)

func take_damage(amount: int, is_crit: bool = false):
	if is_dead: return
	
	hp = max(0.0, hp - amount)
	hp_bar.value = hp
	
	# Show damage number
	var num_color = Color(1.0, 0.9, 0.2) if is_crit else Color(1.0, 1.0, 1.0)
	var text = str(amount) + "!" if is_crit else str(amount)
	GameManager.show_damage_number.emit(global_position + Vector2(0, -16), text, num_color)
	
	# Force chase player if hit
	if current_state == State.ROAM:
		current_state = State.CHASE
		
	# Hurt flash
	var tween = create_tween()
	tween.tween_property(sprite, "self_modulate", Color(1, 0.2, 0.2), 0.08)
	tween.tween_property(sprite, "self_modulate", Color.WHITE, 0.08)
	
	SoundManager.play_sfx("hit")
	
	if hp <= 0:
		die()

func die():
	is_dead = true
	velocity = Vector2.ZERO
	
	# Award rewards
	GameManager.gold += gold_reward
	GameManager.add_xp(xp_reward)
	GameManager.add_chat_msg("[Botín]", "Derrotas a " + monster_name + ". ¡Obtienes +" + str(gold_reward) + " Oro!", Color(0.9, 0.8, 0.2))
	
	# Quest tracking
	GameManager.track_kill(monster_id)
	
	# Roll loot drops
	if loot_item != "" and randf() <= loot_chance:
		var ok = GameManager.add_item_to_inventory(loot_item)
		if ok:
			GameManager.add_chat_msg("[Botín]", "¡Has recogido [" + GameManager.items_db[loot_item]["name"] + "]!", Color(0.6, 0.8, 1.0))
			
	# Play death visual (scale down and disappear)
	var tween = create_tween()
	tween.tween_property(sprite, "scale", Vector2.ZERO, 0.2)
	tween.parallel().tween_property(sprite, "rotation", PI * 2, 0.2)
	
	# Hide overlay UI
	hp_bar.visible = false
	name_label.visible = false
	
	# Disable collisions
	collision_shape.set_deferred("disabled", true)
	
	# Reset target if player was targeting this
	if GameManager.target == self:
		GameManager.target = null
		
	respawn_timer = respawn_time

func _process_respawn(delta):
	respawn_timer -= delta
	if respawn_timer <= 0.0:
		# Respawn
		is_dead = false
		hp = max_hp
		hp_bar.value = hp
		hp_bar.visible = true
		name_label.visible = true
		global_position = spawn_position
		current_state = State.ROAM
		
		# Reset sprite
		sprite.scale = Vector2(1.8, 1.8) if monster_id == "boss" else Vector2.ONE
		sprite.rotation = 0.0
		
		# Re-enable collision
		collision_shape.set_deferred("disabled", false)
		
		# Play small spawn scale-up effect
		sprite.scale = Vector2.ZERO
		var target_scale = Vector2(1.8, 1.8) if monster_id == "boss" else Vector2.ONE
		var tween = create_tween()
		tween.tween_property(sprite, "scale", target_scale, 0.2)

# Input handling for targeting this enemy
func _input_event(viewport, event, shape_idx):
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		GameManager.target = self
		get_viewport().set_input_as_handled()

func _on_mouse_entered():
	pass

func apply_knockback(kb_vel: Vector2):
	knockback_velocity = kb_vel
	# Enter stagger state if not already in attack
	if current_state != State.ATTACK and current_state != State.STAGGER:
		current_state = State.STAGGER
		stagger_timer = stagger_duration
		velocity = Vector2.ZERO
	
	# Hurt flash for stagger
	if current_state == State.STAGGER:
		var tween = create_tween()
		tween.tween_property(sprite, "self_modulate", Color(1, 0.2, 0.2), 0.05)
		tween.tween_property(sprite, "self_modulate", Color.WHITE, 0.05)

# Custom drawing for MMO Selection Target Circle
func _draw():
	if not is_dead and GameManager and GameManager.target == self:
		# Draw selection ring below the enemy feet
		var r = 16.0
		if monster_id == "boss": r = 26.0
		draw_arc(Vector2(0, 4), r, 0, PI * 2, 16, Color(1.0, 0.2, 0.2), 1.5)
