```python
from graphics import Canvas
import math
    
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
PAUSE_TIME = 1/100
left_x = 600
top_y = 250
right_x = 700
bottom_y = 350
midpoint = (left_x + right_x)/2
ball_size = 40
velocity_conversion_factor = 3
left_rack = 300
right_rack = left_rack + 125
top_rung_offset = 145
bottom_rung_offset = top_rung_offset - 60
num_rounds = 5

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    draw_room(canvas)
    draw_backboard(canvas)
    ASCII_art() #done
#Game settings = [name, difficulty, shooter]
    game_settings = menu() #done
    name = game_settings[0]
    difficulty = game_settings[1]
    shooter = game_settings[2]
    if difficulty == str("easy"):
        hoop_size = 100
    if difficulty == str("medium"):
        hoop_size = 75
    if difficulty == str("hard"):
        hoop_size = 40
    net_count = hoop_size // 5 
#Objects for win/lose conditions
    draw_hoop(canvas, hoop_size) #done
    draw_net(canvas, hoop_size, net_count) #done
    draw_shooter(canvas, shooter) #done
    draw_post(canvas)
    balls = draw_rack(canvas, left_rack, right_rack, top_rung_offset, bottom_rung_offset)
    #Make ball object - done
    ball = 1
    overlapping_ball_and_hoop = []
    physics_state = {}
    count = 0
#Enter game loop
    while ball not in overlapping_ball_and_hoop and count < num_rounds:
        ball = canvas.create_oval(175, 400, 175 + ball_size, 400 + ball_size, "orange", "black")        
    #Get user input for launch angle
        angle = 91
        while type(angle) != float or angle < 0 or angle > 90:
            angle = (input("Enter your launch angle (0 to 90): "))
            try:
                angle = float(angle)
            except:
                print("Angle must be a numerical value")
            else:
                angle = float(angle)
                if angle < 0 or angle > 90:
                    print("Angle must be between 0 and 90")
    #Make launch velocity-determinator
    #Get user input for launch velocity
        velocity = 101
        while type(velocity) != float or velocity < 0 or velocity > 100:
            velocity = input("Enter your launch speed (1 to 100): ")
            try:
                velocity = float(velocity)
            except:
                print("Launch speed must be a numerical value")
            else:
                velocity = float(velocity)
                if velocity < 1 or velocity > 100:
                    print("Velocity must be between 1 and 100")
            if angle == 69 and velocity == 69:
                print("nice")
            print()            
#Define rules for projectile movement
#V_x = linear
        gravity = 1
        velocity = velocity / velocity_conversion_factor
        velocity_x = math.cos(3.1415 * angle/180) * velocity
        velocity_y = math.sin(3.1415 * angle/180) * velocity
#Ball motion program
#V_y affected follows gravity
#Ball stoping (velocity 0) ends each round loop
        while velocity != 0:
            velocity_y = velocity_y - gravity
            canvas.move(ball, velocity_x, -velocity_y )
            time.sleep(PAUSE_TIME)

#Set hit box for lose conditions
#Ball hits front rim/net
            overlapping_ball_and_net = (canvas.find_overlapping(
                midpoint - hoop_size/2 - 2,
                bottom_y - 4,
                midpoint - hoop_size/2 - 2,
                bottom_y + 5
            ))
            if ball in overlapping_ball_and_net:
                physics_state = freeze(velocity, velocity_x, velocity_y, gravity)
                velocity = physics_state[velocity]
                velocity_x = physics_state[velocity_x]
                velocity_y = physics_state[velocity_y]
                gravity = physics_state[gravity]
                print("Brick! Try again!\n")
#Ball overshoots the hoop
            overlapping_ball_and_strike_zone = (canvas.find_overlapping(
                midpoint + hoop_size / 2 + 3,
                bottom_y - 4,
                midpoint + hoop_size / 2 + 3,
                bottom_y
            ))
            if ball in overlapping_ball_and_strike_zone:
                physics_state = freeze(velocity, velocity_x, velocity_y, gravity)
                velocity = physics_state[velocity]
                velocity_x = physics_state[velocity_x]
                velocity_y = physics_state[velocity_y]
                gravity = physics_state[gravity]
                print("So close. Try again!\n")
#Ball hits floor
            overlapping_ball_and_floor = (canvas.find_overlapping(
                0, 
                CANVAS_HEIGHT,
                CANVAS_WIDTH,
                CANVAS_HEIGHT
            ))
            if ball in overlapping_ball_and_floor:
                physics_state = freeze(velocity, velocity_x, velocity_y, gravity)
                velocity = physics_state[velocity]
                velocity_x = physics_state[velocity_x]
                velocity_y = physics_state[velocity_y]
                gravity = physics_state[gravity]
                print("Basket's up there! Try again!\n")
#Ball hits ceiling
            overlapping_ball_and_ceiling = (canvas.find_overlapping(
                0, 
                0,
                CANVAS_WIDTH,
                0
            ))
            if ball in overlapping_ball_and_ceiling:
                physics_state = freeze(velocity, velocity_x, velocity_y, gravity)
                velocity = physics_state[velocity]
                velocity_x = physics_state[velocity_x]
                velocity_y = physics_state[velocity_y]
                gravity = physics_state[gravity]
                print("That shot might have worked outside. Try again!\n")
#Ball hits back wall
            overlapping_ball_and_back_wall = (canvas.find_overlapping(
                CANVAS_WIDTH, 
                0,
                CANVAS_WIDTH,
                CANVAS_HEIGHT
            ))
            if ball in overlapping_ball_and_back_wall:
                physics_state = freeze(velocity, velocity_x, velocity_y, gravity)
                velocity = physics_state[velocity]
                velocity_x = physics_state[velocity_x]
                velocity_y = physics_state[velocity_y]
                gravity = physics_state[gravity]
                print("Home Run! But wrong sport. Try again!\n")
                    
#Set hit box for win condition
            overlapping_ball_and_hoop = (canvas.find_overlapping(
                midpoint - hoop_size/2 + ball_size/2,
                bottom_y + 3,
                midpoint + hoop_size/2 - ball_size/2 ,
                bottom_y + 3
        ))
            if ball in overlapping_ball_and_hoop:
                physics_state = freeze(velocity, velocity_x, velocity_y, gravity)
                velocity = physics_state[velocity]
                velocity_x = physics_state[velocity_x]
                velocity_y = physics_state[velocity_y]
                gravity = physics_state[gravity]
                draw_net(canvas, hoop_size, net_count)
#Win statements                
                if count == 0:
                    print("Sweet Sassy Molassy, got it on the first try!")
                if difficulty == str("easy"):
                    print("You got it!\n""Try medium on for size next time!")
                if difficulty == str("medium"):
                    print("Booyah!\n""On to hard mode!")
                if difficulty == str("hard"):
                    print("Boomshackalacka! You're the ultimate Hoopsketball champion!")
                if shooter == str("Larry") or shooter == str("larry"):
                    color_text = "green"
                if shooter == str("Kareem") or shooter == str("kareem"):
                    color_text = "purple"
                if shooter == str("Diana") or shooter == str("diana"):
                    color_text = "purple"
                canvas.create_text(100, 100, f'Congratulations, {name}!', font = 'Arial', font_size = 50, color = color_text)
                canvas.create_text(100, 150, "You're the ultimate champion!", font = 'Arial', font_size = 50, color = color_text)
                play_again = input("Would you like to play again? (y/n): ")
                if play_again == str("y"):
                    main()
                else:
                    print("Thanks for playing!")
#remove balls from rack
        if count < len(balls):
            ball_remover(canvas, count, balls)
        count += 1
        if count == num_rounds - 1:
            print("Last ball, make this one count!")
#end game if exceeds number of rounds                       
    if count >= num_rounds:
        print("Keep practicing!")
        play_again = input("Would you like to play again? (y/n): ")
        if play_again == str("y"):
            main()
        else:
            print("Thanks for playing!")             
       
def freeze(velocity, velocity_x, velocity_y, gravity):
    physics_state = {velocity : 0, velocity_x : 0, velocity_y : 0, gravity : 0}
    return physics_state

def ASCII_art():
    print("""
Mike Billet's
        
 _   _   __    __   ___     _         __  ____  __          _   _
| | | | /  \  /  \ |   \   / \ || // | _||_  _||  \   /\   ||  ||
| | | || /\ || /\ || || | //\_|||//  ||    ||  ||\ | //\\\  ||  ||
| |_| |||  ||||  ||| || | \\\   | /   ||_   ||  ||// //__\\\ ||  ||
|  _  |||  ||||  |||  _/   \\\  | \   | _|  ||  | \  | __ | ||  ||
| | | |||  ||||  ||| |    _ \\\ || \  ||    ||  |/\| ||  || ||  ||
| | | || \/ || \/ || |   | \// ||\ \ ||_   ||  |\/| ||  || ||_ ||__
|_| |_| \__/  \__/ |_|    \_/  || \_\|__|  ||  |__/ ||  || |__||___|

Software Version 7.0
""")

def menu():
    name = input("Enter your name to continue: ")
    if name == str("Mike Billet"):
        print("The Creator has graced us with his presence. We are not worthy!")
    difficulty = str("blank")
    while difficulty != str("easy") and difficulty != str("medium") and difficulty != str("hard"):
        difficulty = input("Enter difficulty (easy/medium/hard): ")
        if difficulty != str("easy") and difficulty != str("medium") and difficulty != str("hard"):
            print('Difficulty must be "easy" "medium" or "hard"\n')
    shooter = str("blank")
    while shooter != str("kareem") and shooter != str("larry") and shooter != str("diana") and shooter != str("Kareem") and shooter != str("Larry") and shooter != str("Diana"):
        shooter = input("Pick your shooter style (Kareem, Larry, or Diana): ")
        if shooter != str("kareem") and shooter != str("larry") and shooter != str("diana") and shooter != str("Kareem") and shooter != str("Larry") and shooter != str("Diana"):
            print('Shooter must be "Kareem" "Larry" or "Diana"')
        print()
    print(f"Hello {name}, you find yourself in the ancient and noble game of Hoopsketball. \nDo you have what it takes to become the grand Hoopsketball champion?\n")
    game_settings = [name, difficulty, shooter]
    return game_settings

def ball_remover(canvas, count, balls):
    removed_ball = balls[count]
    canvas.delete(removed_ball)

#Draws rack with balls, returns balls as a set balls[] to be removed by ball_remover()
def draw_rack(canvas, left_rack, right_rack, top_rung_offset, bottom_rung_offset):
    canvas.create_rectangle(left_rack, CANVAS_HEIGHT - bottom_rung_offset, right_rack, CANVAS_HEIGHT - bottom_rung_offset + 5, "grey") #bottom rung
    canvas.create_rectangle(left_rack, CANVAS_HEIGHT - top_rung_offset, right_rack, CANVAS_HEIGHT - top_rung_offset + 5, "grey") #top rung
    canvas.create_rectangle(left_rack, CANVAS_HEIGHT - top_rung_offset - 10, left_rack + 10, CANVAS_HEIGHT - bottom_rung_offset + 10, "grey") #left post
    canvas.create_rectangle(right_rack - 10, CANVAS_HEIGHT - top_rung_offset - 10, right_rack, CANVAS_HEIGHT - bottom_rung_offset + 10, "grey") #right post
    #bottom balls
    ball_bottom_1 = canvas.create_oval(left_rack + 10, CANVAS_HEIGHT - 85 - (ball_size - 10), left_rack + 10 + (ball_size - 10), CANVAS_HEIGHT - 85, "orange", "black")
    ball_bottom_2 = canvas.create_oval(left_rack + 10 + ball_size - 9, CANVAS_HEIGHT - 85 - (ball_size - 10), left_rack + 10 + 2*(ball_size - 9), CANVAS_HEIGHT - 85, "orange", "black")
    #canvas.create_oval(left_rack + 10 + 2*(ball_size - 9), CANVAS_HEIGHT - 85 - (ball_size - 10), left_rack + 10 + 3*(ball_size - 9), CANVAS_HEIGHT - 85, "orange", "black")  
    #top balls
    ball_top_1 = canvas.create_oval(left_rack + 10, CANVAS_HEIGHT - 145 - (ball_size - 10), left_rack + 10 + (ball_size - 10), CANVAS_HEIGHT - 145, "orange", "black")
    ball_top_2 = canvas.create_oval(left_rack + 10 + ball_size - 9, CANVAS_HEIGHT - 145 - (ball_size - 10), left_rack + 10 + 2*(ball_size - 9), CANVAS_HEIGHT - 145, "orange", "black")
    balls = [ball_top_1, ball_top_2, ball_bottom_1, ball_bottom_2]
    #print(f"balls remaining = {balls}")
    return balls

def draw_room(canvas):
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, "tan")
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT - 100, "beige")
   
def draw_backboard(canvas):   
    fill = '#ADD8E6'
    outline = "black"
    canvas.create_rectangle(
        left_x,
        top_y,
        right_x,
        bottom_y, 
        fill,
        outline
    )
    #draws post
    canvas.create_rectangle(
        midpoint - 5,
        bottom_y,
        midpoint + 5,
        CANVAS_HEIGHT - 50,
        "brown")

def draw_hoop(canvas, hoop_size):
    hoop = canvas.create_oval(
        midpoint - hoop_size/2,
        bottom_y - 5,
        midpoint + hoop_size/2,
        bottom_y + 5,
        'white',
        "black"
    )
def draw_post(canvas):
        canvas.create_rectangle(
        midpoint - 5,
        bottom_y - 5,
        midpoint + 5,
        bottom_y + 5,
        "brown")

def draw_net(canvas, hoop_size, net_count):   
    for i in range (net_count - 1):
        canvas.create_line(
            midpoint - hoop_size/2 + ((i + 1) * hoop_size / net_count),
            bottom_y,
            midpoint - hoop_size/2 + ((i + 1) * hoop_size / net_count),
            bottom_y + 50,
        )
        net_left = canvas.create_line(
            midpoint - hoop_size/2,
            bottom_y,
            midpoint - hoop_size/2 + hoop_size / net_count,
            bottom_y + 50
        )
        canvas.create_line(
            midpoint + hoop_size/2,
            bottom_y,
            midpoint + hoop_size/2 - hoop_size / net_count,
            bottom_y + 50
        )        

def draw_shooter(canvas, shooter):
    if shooter == str("Larry") or shooter == str("larry"):
        skin_color = '#FBD99F'
        jersey_fill = "green"
        jersey_outline = "white"
    if shooter == str("Kareem") or shooter == str("kareem"):
        skin_color = '#B59050'
        jersey_fill = "yellow"
        jersey_outline = "purple"
    if shooter == str("Diana") or shooter == str("diana"):
        skin_color = '#D1AF73'
        jersey_fill = "purple"
        jersey_outline = "black"
    player_midpoint = 125
    head_size = 50
    torso_width = 40
    head_apex = 400
    waist_level = 530
#Head
    canvas.create_oval(
    player_midpoint - head_size/2, 
    head_apex, 
    player_midpoint + head_size/2, 
    head_apex + head_size, 
    skin_color
    )
#Body
#Shoulders
    canvas.create_oval(
        player_midpoint - torso_width/2, 
        head_apex + head_size,
        player_midpoint + torso_width/2, 
        head_apex + head_size * 2, 
        jersey_fill, 
        jersey_outline)
#Torso/Abdomen
    canvas.create_rectangle(
        player_midpoint - torso_width/2,
        head_apex + head_size * 1.5,
        player_midpoint + torso_width/2,
        waist_level,
        jersey_fill, 
        jersey_outline)
#Shorts
    canvas.create_rectangle(
        player_midpoint - torso_width/2,
        waist_level,
        player_midpoint + torso_width/2,
        waist_level + 25,
        jersey_fill,
        jersey_outline
    )
#Legs
    canvas.create_rectangle(
        player_midpoint - torso_width/2,
        waist_level + 25,
        player_midpoint - torso_width/6,
        CANVAS_HEIGHT,
        skin_color
    )
    canvas.create_rectangle(
        player_midpoint + torso_width/6,
        waist_level + 25,
        player_midpoint + torso_width/2,
        CANVAS_HEIGHT,
        skin_color
    )
#Arms
    humerus_length = 60
    forearm_length = humerus_length
    arm_width = 15
#Humerus
    canvas.create_rectangle(
        player_midpoint,
        head_apex + head_size + arm_width,
        player_midpoint + humerus_length,
        head_apex + head_size + arm_width * 2,
        skin_color
    )
 #Forearms
    canvas.create_rectangle(
        player_midpoint + humerus_length - 5,
        head_apex + head_size + arm_width - forearm_length,
        player_midpoint + humerus_length + arm_width - 5,
        head_apex + head_size + arm_width,
        skin_color
    )
#Hair (Diana only)
    if shooter == str("Diana") or shooter == str("diana"):
            canvas.create_oval(
            player_midpoint - head_size/1.6,
            head_apex,
            player_midpoint + head_size/4,
            head_apex + head_size/1.5,
            "brown"
        )
#Bun
            canvas.create_oval(
            player_midpoint - head_size/1.2,
            head_apex,
            player_midpoint - head_size/3.3,
            head_apex + head_size/2.3,
            "brown"
        )

if __name__ == '__main__':
    main()
    ```
