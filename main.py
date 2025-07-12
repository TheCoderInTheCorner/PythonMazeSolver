def parse_maze(file: str):
    maze_file = open(file)
    lines = maze_file.readlines()
    maze = []

    # Populating the maze list so that the maze renders as a
    # 2d array (easier to visualize)
    for line in lines:
        maze.append([])  # creating each row
        for character in line:
            if character != '\n':
                maze[lines.index(line)].append(character)  # Adding characters
    maze_file.close()
    return maze


class Node:
    def __init__(self, id_, state, ):
        self.id_ = id_
        self.state = state
        self.parent = None


def nodify_maze(maze):
    node_maze = []
    id_ = 0
    for row in maze:
        node_maze.append([])
        for character in row:
            if character == '#':
                node_maze[maze.index(row)].append(Node(id_, 'wall'))
            elif character == ' ':
                node_maze[maze.index(row)].append(Node(id_, 'space'))
            elif character == 'B':
                node_maze[maze.index(row)].append(Node(id_, 'goal'))
            elif character == 'A':
                node_maze[maze.index(row)].append(Node(id_, 'start'))
            id_ += 1
    return node_maze


def solve_maze(file: str):
    parsed_maze = parse_maze(file)
    node_maze = nodify_maze(parsed_maze)
    frontier = []
    current_location = []
    explored_places = []
    path = []
    maze_completed = False
    for i in range(len(parsed_maze)):
        for a in range(len(parsed_maze[i])):
            if node_maze[i][a].state == 'start':
                current_location.append(i)
                current_location.append(a)
    frontier.append(current_location)

    while not maze_completed:

        if len(frontier) == 0:
            raise Exception('Cannot Solve Maze')
        current_location = frontier[0]
        current_node = node_maze[current_location[0]][current_location[1]]

        if current_node.state == 'goal':
            maze_completed = True
            start_reached = False
            goal_node = node_maze[current_location[0]][current_location[1]]
            path.append(goal_node.parent)
            current_parent = goal_node.parent
            while not start_reached:
                if node_maze[current_parent[0]][current_parent[1]].state == 'start':
                    start_reached = True
                    break

                current_parent = node_maze[current_parent[0]][current_parent[1]].parent
                path.append(current_parent)

        can_check_top = current_location[0] > 0
        can_check_bottom = current_location[0] < len(node_maze)-1
        can_check_left = current_location[1] > 0
        can_check_right = current_location[1] < len(node_maze[1])-1

        if can_check_top:
            top_node_coord = [current_location[0]-1, current_location[1]]
            top_node = node_maze[top_node_coord[0]][top_node_coord[1]]
            if top_node.state != 'wall' and top_node_coord not in explored_places:
                frontier.append(top_node_coord)
                top_node.parent = current_location

        if can_check_bottom:
            bottom_node_coord = [current_location[0]+1, current_location[1]]
            bottom_node = node_maze[bottom_node_coord[0]][bottom_node_coord[1]]
            if bottom_node.state != 'wall' and bottom_node_coord not in explored_places:
                frontier.append(bottom_node_coord)
                bottom_node.parent = current_location

        if can_check_left:
            left_node_coord = [current_location[0], current_location[1]-1]
            left_node = node_maze[left_node_coord[0]][left_node_coord[1]]
            if left_node.state != 'wall' and left_node_coord not in explored_places:
                frontier.append(left_node_coord)
                left_node.parent = current_location

        if can_check_right:
            right_node_coord = [current_location[0], current_location[1]+1]
            right_node = node_maze[right_node_coord[0]][right_node_coord[1]]
            if right_node.state != 'wall' and right_node_coord not in explored_places:
                frontier.append(right_node_coord)
                right_node.parent = current_location

        explored_places.append(current_location)

        frontier.pop(0)
    return path


def render_path(file, path_list):
    parsed_maze = parse_maze(file)
    node_maze = nodify_maze(parsed_maze)
    maze_with_path = []
    for row in range(len(parsed_maze)):
        maze_with_path.append("")
        for character in range(len(parsed_maze[0])):
            if [row, character] not in path_list:
                maze_with_path[row] += parsed_maze[row][character]

            else:
                maze_with_path[row] += "."

    for i in maze_with_path:
        print(i)


solution = solve_maze('maze1.txt')
render_path('maze1.txt', solution)
