import rg

BIG_DIST = 100000000

class Robot:

	def act(self, game):
		x,y = self.location
		bot = None
		active_team = {}
		active_enemy = {}
		enemy_distance  = {}
		for loc, bot in game.get('robots').items():
			if bot.get('player_id') != self.player_id:
				active_enemy[loc] = bot
				enemy_distance[loc] = 0
			else:
				active_team[loc] = bot
		for loc in active_enemy:
			for myloc in active_team:
				enemy_distance[loc] = enemy_distance[loc] + rg.dist(loc, myloc)
		priority_loc, attack_loc = self.findPriority(active_team, active_enemy,enemy_distance)
		if rg.dist(self.location, priority_loc) <= 1 and attack_loc:
			return ['attack', attack_loc]
		else: 
			return ['move', rg.toward(self.location, priority_loc)]
		return ['move', rg.toward(self.location, rg.CENTER_POINT)]
		
	def findPriority(self,active_team, active_enemy,enemy_distance):
		direction = {"up":(0,-1), "down":(0,1),"left":(-1,0),"right":(1,0)}
		dist = BIG_DIST
		shortest_loc = self.get_closest_in_dict(enemy_distance)
		nearest_weak = self.get_weakest_ally(active_team)
		adjacent_enemies = self.check_adjacent(active_enemy, nearest_weak)

		return shortest_loc, shortest_loc

	def get_weakest_ally(self, active_team):
		temp_loc = (0,0)
		weak_team_near = BIG_DIST
		lowest_hp = 50
		for loc in active_team:
			distance = rg.dist(self.location, loc)
			if distance < weak_team_near and active_team[loc].hp < lowest_hp:
				weak_team_near = distance
				temp_loc = loc
		return temp_loc

	def check_adjacent(self, active_enemy, loc, direction):
		x, y = loc
		list_of_locs = []
		for d in direction:
			dx, dy = d
			if (x+dx,y+dy) in active_enemy:
				list_of_locs.append((x+dx, y+dy))
		return list_of_locs

	def get_closest_in_dict(self, dictio):
		dist = BIG_DIST
		temp_loc = (0,0)
		for loc in dictio:
			distance = dictio[loc]
			if dist>=distance:
				dist = distance
				temp_loc = loc
		return temp_loc

	def get_closest_in_list(self, list):
