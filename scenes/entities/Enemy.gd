extends CharacterBody2D

@export var monster_id: String = "slime" 

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

enum State { ROAM, CHASE, ATTACK, STAGGER }
var current_state: State = State.ROAM
var spawn_position: Vector2
var roam_target: Vector2
var roam_timer: float = 0.0

var agro_range: float = 130.0
var attack_range: float = 28.0
var attack_cooldown: float = 1.5
var attack_timer: float = 0.0

var knockback_velocity: Vector2 = Vector2.ZERO
var knockback_friction: float = 8.0
var stagger_duration: float = 0.2
var stagger_timer: float = 0.0

var player_node: Node = null

var anim_frame: int = 0
var anim_timer: float = 0.0
var current_dir: int = 0 

@onready var sprite: Sprite2D = $Sprite2D
@onready var hp_bar: ProgressBar = $HPBar
@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var name_label: Label = $NameLabel

func _ready():
	add_to_group("enemy")
	spawn_position = global_position
	input_pickable = true
	mouse_entered.connect(_on_mouse_entered)
	setup_monster_stats()
	_pick_new_roam_target()

func setup_monster_stats():
	sprite.region_enabled = true
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
		sprite.texture = load("res://assets/slime_v3.png")
		attack_range = 28.0
		agro_range = 100.0
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
		sprite.texture = load("res://assets/skeleton_v3.png")
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
		loot_chance = 1.0
		sprite.texture = load("res://assets/demon_boss.png") # Usamos el original o uno nuevo si hubiera
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
		sprite.texture = load("res://assets/tileset.png")
		sprite.region_rect = Rect2(0, 16, 16, 16)
		
	if monster_id == "boss":
		sprite.scale = Vector2(1.8, 1.8)
		collision_shape.scale = Vector2(1.5, 1.5)
	elif monster_id == "dummy":
		sprite.scale = Vector2(1.5, 1.5)
		
	name_label.text = "Lvl " + str(level) + " " + monster_name
	hp_bar.max_value = max_hp
	hp_bar.value = hp
	
	if monster_id != "dummy":
		update_sprite_rect()

func _physics_process(delta):
	if is_dead:
		_process_respawn(delta)
		return
	queue_redraw()
	if monster_id == "dummy":
		if hp < max_hp:
			hp = min(max_hp, hp + 50.0 * delta)
			hp_bar.value = hp
		return
	if attack_timer > 0.0:
		attack_timer -= delta
	if player_node == null:
		var players = get_tree().get_nodes_in_group("player")
		if players.size() > 0: player_node = players[0]
	if knockback_velocity.length() > 0.0:
		knockback_velocity = knockback_velocity.move_toward(Vector2.ZERO, knockback_friction * delta)
	if current_state == State.STAGGER:
		stagger_timer -= delta
		if stagger_timer <= 0.0: current_state = State.CHASE
		else:
			velocity = knockback_velocity
			move_and_slide()
			return
	match current_state:
		State.ROAM: _process_roam(delta)
		State.CHASE: _process_chase(delta)
		State.ATTACK: _process_attack(delta)
	_animate_movement(delta)

func _process_roam(delta):
	if player_node != null and not player_node.is_dead:
		var dist = global_position.distance_to(player_node.global_position)
		if dist <= agro_range and not _is_in_safe_zone(player_node.global_position):
			current_state = State.CHASE
			return
	roam_timer -= delta
	if roam_timer <= 0.0: _pick_new_roam_target()
	var dir = (roam_target - global_position)
	if dir.length() > 5.0:
		velocity = dir.normalized() * (speed * 0.6)
		move_and_slide()
	else: velocity = Vector2.ZERO

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
	if attack_timer <= 0.0:
		attack_timer = attack_cooldown
		var attack_dir = (player_node.global_position - global_position).normalized()
		var tween = create_tween()
		tween.tween_property(sprite, "offset", attack_dir * 6.0, 0.08)
		tween.tween_property(sprite, "offset", Vector2.ZERO, 0.08)
		player_node.take_damage(atk)

func _is_in_safe_zone(pos: Vector2) -> bool:
	return pos.x > -50 and pos.x < 650 and pos.y > -50 and pos.y < 650

func _animate_movement(delta):
	if velocity.length() > 2.0:
		if abs(velocity.x) > abs(velocity.y): current_dir = 3 if velocity.x > 0 else 2
		else: current_dir = 0 if velocity.y > 0 else 1
		anim_timer += delta
		if anim_timer >= 0.15:
			anim_timer = 0.0
			anim_frame = (anim_frame + 1) % 4
	else:
		anim_frame = 0
		anim_timer = 0.0
	update_sprite_rect()

func update_sprite_rect():
	if monster_id == "dummy": return
	var frame_size = 240
	if sprite.texture:
		var tex_w = sprite.texture.get_width()
		# Si la textura es pequeña (ya procesada a 32x32), usamos 32
		if tex_w <= 256: frame_size = 32
		else: frame_size = tex_w / 8
	
	var frame_x = anim_frame * frame_size
	var frame_y = current_dir * frame_size
	sprite.region_rect = Rect2(frame_x, frame_y, frame_size, frame_size)
	sprite.scale = Vector2(32.0 / frame_size, 32.0 / frame_size)
	if monster_id == "boss": sprite.scale *= 1.8

func take_damage(amount: int, is_crit: bool = false):
	if is_dead: return
	hp = max(0.0, hp - amount)
	hp_bar.value = hp
	var num_color = Color(1.0, 0.9, 0.2) if is_crit else Color(1.0, 1.0, 1.0)
	GameManager.show_damage_number.emit(global_position + Vector2(0, -16), str(amount), num_color)
	if current_state == State.ROAM: current_state = State.CHASE
	var tween = create_tween()
	tween.tween_property(sprite, "self_modulate", Color(1, 0.2, 0.2), 0.08)
	tween.tween_property(sprite, "self_modulate", Color.WHITE, 0.08)
	SoundManager.play_sfx("hit")
	if hp <= 0: die()

func die():
	is_dead = true
	velocity = Vector2.ZERO
	GameManager.gold += gold_reward
	GameManager.add_xp(xp_reward)
	GameManager.track_kill(monster_id)
	if loot_item != "" and randf() <= loot_chance:
		GameManager.add_item_to_inventory(loot_item)
	var tween = create_tween()
	tween.tween_property(sprite, "scale", Vector2.ZERO, 0.2)
	hp_bar.visible = false
	name_label.visible = false
	collision_shape.set_deferred("disabled", true)
	if GameManager.target == self: GameManager.target = null
	respawn_timer = respawn_time

func _process_respawn(delta):
	respawn_timer -= delta
	if respawn_timer <= 0.0:
		is_dead = false
		hp = max_hp
		hp_bar.value = hp
		hp_bar.visible = true
		name_label.visible = true
		global_position = spawn_position
		current_state = State.ROAM
		update_sprite_rect()
		collision_shape.set_deferred("disabled", false)

func _input_event(viewport, event, shape_idx):
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		GameManager.target = self
		get_viewport().set_input_as_handled()

func _on_mouse_entered(): pass

func apply_knockback(kb_vel: Vector2):
	knockback_velocity = kb_vel
	if current_state != State.ATTACK and current_state != State.STAGGER:
		current_state = State.STAGGER
		stagger_timer = stagger_duration
	var tween = create_tween()
	tween.tween_property(sprite, "self_modulate", Color(1, 0.2, 0.2), 0.05)
	tween.tween_property(sprite, "self_modulate", Color.WHITE, 0.05)

func _draw():
	if not is_dead and GameManager and GameManager.target == self:
		var r = 16.0
		if monster_id == "boss": r = 26.0
		draw_arc(Vector2(0, 4), r, 0, PI * 2, 16, Color(1.0, 0.2, 0.2), 1.5)
