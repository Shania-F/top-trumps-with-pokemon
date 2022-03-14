#TOP TRUMPS using PokeAPI
#Compare stats; have the highest number to WIN!

import random
import requests

#generate a random pokemon
def gen_pokemon(): 
  n = random.randint(1, 151)
  url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(n)
  response = requests.get(url)
  pokemon = response.json()
  stats = pokemon['stats']
  return {
    'id': pokemon['id'],    
    'name': pokemon['name'],
    'hp': stats[0]['base_stat'],
    'attack': stats[1]['base_stat'],
    'defense': stats[2]['base_stat']
  }

#display pokemon dictionary in a readable way
def disp_pokemon(dict):
  print('#{}- {}'.format(dict['id'],dict['name'].capitalize()))
  print('HP:{} Attack:{} Defense:{}'.format(dict['hp'],dict['attack'],dict['defense']))
#for hard mode (stats not visible beforehand)
def disp_pokemon_h(dict):
  print('#{}- {}'.format(dict['id'],dict['name'].capitalize()))

#open file in eXclusive mode; catch error if it exists
try:
  with open('highscore.txt', 'x') as f:
      f.write('0')
except FileExistsError:
  pass # nothing is done

#team selection
def poke_choose():
  p = int(input())
  while p<1 or p>6:
    p = int(input("Please choose a number from 1 to 6:"))
  return p

all_choices = []
my_team = []
flag = 0

print("Welcome to TOP TRUMPS with Pokémon!")

difficulty = input("\nPlease select a difficulty: [easy/hard]")
while flag == 0:
  if difficulty == "easy" or difficulty == "hard":
    flag = 1
  else:
    difficulty = input("Please choose between 'easy' or 'hard' mode:")   

print("\nSelect 3 different Pokémon for your team. Your choices are:")
for i in range(6):
  all_choices.append(gen_pokemon())
if difficulty == 'easy':  
  for i in range(6):
    print('{}--->'.format(i+1))
    disp_pokemon(all_choices[i])
if difficulty == 'hard':  
  for i in range(6):
    print('{}--->'.format(i+1))
    disp_pokemon_h(all_choices[i])  

print('\nChoose a Pokémon: [1-6]')
p1 = poke_choose()

print('\nChoose a second Pokémon: [1-6]') 
p2 = poke_choose()
while p2 == p1: 
  print("You've already chosen that Pokémon. Please enter a different number: [1-6]")
  p2 = poke_choose()

print('\nChoose a third Pokémon: [1-6]')  
p3 = poke_choose()
while p3 == p1 or p3 == p2:
  print("You've already chosen that Pokémon. Please enter a different number: [1-6]")
  p3 = poke_choose()

my_team.append(all_choices[p1-1])
my_team.append(all_choices[p2-1])
my_team.append(all_choices[p3-1])

#best of 3 battles
count = 0
score = 0

for i in range(3):
  if difficulty == 'easy':
    print("Your Pokémon:") 
    disp_pokemon(my_team[i]) 
  print("\nBattle #{}: Which stat will you choose? [hp/attack/defense]".format(i+1))
  flag = 0
  choice = input()
  while flag == 0:
    if choice == "hp" or choice == "attack" or choice == "defense":
      flag = 1
    else:
      choice = input("Please enter a valid stat: [hp/attack/defense]")     
  opp_pokemon = gen_pokemon()
  if difficulty == 'hard':
    print("\nYour Pokémon:") 
    disp_pokemon(my_team[i])
  print("\nOpponent's Pokémon:")
  disp_pokemon(opp_pokemon)
  if my_team[i][choice] > opp_pokemon[choice]:
    print("\nYou win!\n")
    count += 1
    score += (my_team[i][choice] - opp_pokemon[choice])*100 # difference of winning stat
  elif my_team[i][choice] == opp_pokemon[choice]:
    print("\nDraw.\n")
  else:  
    print("\nYou lose...\n")

print("You won {}/3 battle(s)".format(count))
if count >=2:
    print("Victory! Great job.")
else:  
    print("You lose... Better luck next time.")

print("\nScore: {}".format(score))
with open('highscore.txt', 'r') as f:
  old_score = int(f.read())
if score > old_score:
  print("NEW HIGH SCORE!") 
  with open('highscore.txt', 'w') as f:
    f.write(str(score))
