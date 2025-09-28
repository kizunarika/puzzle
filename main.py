from settings import *
from interface import Waiting_Interface


def find_path(grid, start, end):
    from collections import deque
    queue = deque()
    queue.append((start, [start]))
    visited = set()
    visited.add((int(start.x), int(start.y)))
    while queue:
        current, path = queue.popleft()
        if current == end:
            return path
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = int(current.x)+dx, int(current.y)+dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid) and not grid[ny][nx]:
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((vec(nx, ny), path+[vec(nx, ny)]))
    return None


class Cell:
    def __init__(self, x, y):
        self.pos = vec(x, y)  # Coordinates
        self.next: Cell = None
        self.prev: Cell = None
        self.point_end: vec = None  # If this cell is a point, the position of the other point
        self.state = None  # Active state

    def reset(self):
        self.state = None
        self.next = None
        self.prev = None

    def reset_all(self):
        self.state = None
        self.next = None
        if self.prev is not None:
            self.prev.reset_all()
        self.prev = None

    def is_empty(self):
        return self.state is None

    def set_next(self, next_cell):
        if next_cell is self or next_cell.prev is self or next_cell.prev is not None:
            return
        self.next = next_cell
        self.next.prev = self
        self.next.state = False

    def set_active(self):
        cell = self
        while cell is not None:
            cell.state = True
            cell = cell.prev

    def draw(self, surface, images: dict = None):
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        pygame.draw.rect(surface, (70, 70, 70),
                         (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, (50, 50, 50),
                         (x + 5, y + 5, CELL_SIZE - 10, CELL_SIZE - 10))
        if self.state is not None:
            # Draw line head
            if not self.state and self.prev is not None and self.next is None:
                direction = self.prev.pos - self.pos
                if direction.x == 1 and direction.y == 0:
                    surface.blit(pygame.transform.rotate(
                        images['head'], 270), (x, y))
                elif direction.x == -1 and direction.y == 0:
                    surface.blit(pygame.transform.rotate(
                        images['head'], 90), (x, y))
                elif direction.x == 0 and direction.y == 1:
                    surface.blit(pygame.transform.rotate(
                        images['head'], 180), (x, y))
                elif direction.x == 0 and direction.y == -1:
                    surface.blit(pygame.transform.rotate(
                        images['head'], 0), (x, y))

            elif self.prev is not None and self.next is not None:
                # Draw vertical line
                if self.prev.pos.x == self.next.pos.x:
                    surface.blit(pygame.transform.rotate(
                        images[('active ' if self.state else '')+'line'], 90), (x, y))
                # Draw horizontal line
                elif self.prev.pos.y == self.next.pos.y:
                    surface.blit(
                        images[('active ' if self.state else '')+'line'], (x, y))
                # Draw corner
                else:
                    dir_prev = self.prev.pos - self.pos
                    dir_next = self.next.pos - self.pos
                    if (dir_prev.x == 1 and dir_next.y == 1) or (dir_prev.y == 1 and dir_next.x == 1):
                        surface.blit(pygame.transform.rotate(
                            images[('active ' if self.state else '')+'corner'], 180), (x, y))
                    elif (dir_prev.x == -1 and dir_next.y == 1) or (dir_prev.y == 1 and dir_next.x == -1):
                        surface.blit(pygame.transform.rotate(
                            images[('active ' if self.state else '')+'corner'], 90), (x, y))
                    elif (dir_prev.x == -1 and dir_next.y == -1) or (dir_prev.y == -1 and dir_next.x == -1):
                        surface.blit(
                            images[('active ' if self.state else '')+'corner'], (x, y))
                    elif (dir_prev.x == 1 and dir_next.y == -1) or (dir_prev.y == -1 and dir_next.x == 1):
                        surface.blit(pygame.transform.rotate(
                            images[('active ' if self.state else '')+'corner'], 270), (x, y))


class Point(Cell):
    def __init__(self, x, y, image):
        super().__init__(x, y)
        self.image_point = image

    def draw(self, surface, images: dict = None):
        super().draw(surface, images)
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        surface.blit(self.image_point, (x, y))
        if self.state is not None:
            if self.prev is None and self.next is None:
                surface.blit(images['point'], (x, y))
            else:
                if self.prev is None:
                    direction = self.next.pos - self.pos
                elif self.next is None:
                    direction = self.prev.pos - self.pos

                if direction.x == 1:
                    surface.blit(pygame.transform.rotate(
                        images[('active point' if self.state else 'point line')], 270), (x, y))
                elif direction.x == -1:
                    surface.blit(pygame.transform.rotate(
                        images[('active point' if self.state else 'point line')], 90), (x, y))
                elif direction.y == 1:
                    surface.blit(pygame.transform.rotate(
                        images[('active point' if self.state else 'point line')], 180), (x, y))
                elif direction.y == -1:
                    surface.blit(
                        images[('active point' if self.state else 'point line')], (x, y))


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
        pygame.display.set_caption("Puzzle Game")
        self.clock = pygame.time.Clock()
        self.font_28 = pygame.font.Font("MinecraftRegular-Bmg3.otf", 28)
        self.font_40 = pygame.font.Font("MinecraftRegular-Bmg3.otf", 40)

        self.images = {
            'line': pygame.image.load("Graphics/line.png").convert_alpha(),
            'active line': pygame.image.load("Graphics/active line.png").convert_alpha(),
            'head': pygame.image.load("Graphics/head.png").convert_alpha(),
            'active head': pygame.image.load("Graphics/active head.png").convert_alpha(),
            # lt
            'corner': pygame.image.load("Graphics/corner.png").convert_alpha(),
            'active corner': pygame.image.load("Graphics/active corner.png").convert_alpha(),
            'point': pygame.image.load("Graphics/point.png").convert_alpha(),
            'point line': pygame.image.load("Graphics/point top.png").convert_alpha(),
            'active point': pygame.image.load("Graphics/active point.png").convert_alpha(),
            'yellow point': pygame.image.load("Graphics/yellow point.png").convert_alpha(),
            'green point': pygame.image.load("Graphics/green point.png").convert_alpha(),
            'white point': pygame.image.load("Graphics/white point.png").convert_alpha(),
            'purple point': pygame.image.load("Graphics/purple point.png").convert_alpha(),
            'blue point': pygame.image.load("Graphics/blue point.png").convert_alpha(),

            "square button": {
                "normal": pygame.image.load("Graphics/square btn/normal.png").convert_alpha(),
                "hover": pygame.image.load("Graphics/square btn/hover.png").convert_alpha(),
                "click": pygame.image.load("Graphics/square btn/click.png").convert_alpha()
            },
        }
        # Create the grid of cells
        self.cells: list[list[Cell]] = [[None for _ in range(CELL_NUMBER)]
                                        for _ in range(CELL_NUMBER)]
        self.import_puzzle(PUZZLE_DATA)

        # surface
        self.main_surface = pygame.Surface(
            (CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))

        # waiting interface
        self.waiting_interface = Waiting_Interface(
            images=self.images["square button"],
            font=self.font_28
        )
        self.waiting_interface.buttons[2].callback = lambda: (
            self.reset_grid(),
            self.reset_status(),
        )
        self.waiting_interface.buttons[1].callback = lambda: (
            self.status.update({"waiting": False, "playing": True}),
        )
        self.waiting_interface.buttons[0].callback = lambda: (
            self.import_puzzle(self.randomize_puzzle()))

    def import_puzzle(self, puzzle_data):
        self.puzzle_data = puzzle_data
        for i in range(CELL_NUMBER):
            for j in range(CELL_NUMBER):
                self.cells[i][j] = Cell(j, i)

        for color, positions in puzzle_data.items():
            for i in [0, 1]:
                x = int(positions[i].x)
                y = int(positions[i].y)
                self.cells[y][x] = Point(
                    x, y, self.images[f'{color} point'])
                self.cells[y][x].point_end = positions[1-i]

        self.point_select = None
        self.current_cell = None

        # status
        self.reset_status()

    def randomize_puzzle(self):
        grid = [[False for _ in range(CELL_NUMBER)]
                for _ in range(CELL_NUMBER)]
        all_positions = [(x, y) for x in range(CELL_NUMBER)
                         for y in range(CELL_NUMBER)]
        random.shuffle(all_positions)
        colors = ['yellow', 'green', 'purple', 'blue', 'white']
        puzzle_data = {}
        used = set()
        for i in range(random.randint(3, 5)):
            while True:
                if len(all_positions) < 2:
                    break
                p1 = all_positions.pop()
                p2 = all_positions.pop()
                if p1 != p2 and p1 not in used and p2 not in used:
                    start, end = vec(*p1), vec(*p2)
                    path = find_path(grid, start, end)
                    if path:
                        for pos in path:
                            grid[int(pos.y)][int(pos.x)] = True
                            used.add((int(pos.x), int(pos.y)))
                        puzzle_data[colors[i]] = [start, end]
                        break
                    else:
                        all_positions.insert(0, p1)
                        all_positions.insert(0, p2)
        return puzzle_data

    def check_win(self):
        for _, positions in self.puzzle_data.items():
            x, y = int(positions[0].x), int(positions[0].y)

            if self.cells[y][x].prev is None:
                while self.cells[y][x].next is not None:
                    # self.cells[y][x].print()
                    next_cell = self.cells[y][x].next
                    if next_cell is None:
                        break  # Ngắt nếu chuỗi bị đứt
                    x = int(next_cell.pos.x)
                    y = int(next_cell.pos.y)
            else:
                while self.cells[y][x].prev is not None:
                    next_cell = self.cells[y][x].prev
                    if next_cell is None:
                        break
                    x = int(next_cell.pos.x)
                    y = int(next_cell.pos.y)

            if (y, x) != (int(positions[-1].y), int(positions[-1].x)):
                print("Lose")
                return False
        self.status["Win"] = True
        self.status["playing"] = False
        self.status["waiting"] = True
        print("Win")
        return True

    def draw(self):
        # if self.status["playing"]:
        for row in self.cells:
            for cell in row:
                cell.draw(self.main_surface, self.images)
        self.screen.blit(self.main_surface, (0, 0))
        if self.status["waiting"]:
            self.waiting_interface.draw(
                self.screen, self.status["Win"], self.font_40)
            self.screen.blit(self.screen, (0, 0))
            for button in self.waiting_interface.buttons:
                button.update()

    def reset_grid(self):
        # Reset all cells
        for row in self.cells:
            for cell in row:
                cell.reset()

    def reset_status(self):
        self.status = {
            "playing": True,
            "waiting": False,
            'Win': False
        }

    def update(self):
        pygame.display.flip()
        self.clock.tick(30)

    def run(self):
        while True:
            self.event()
            self.draw()
            self.update()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if self.status["playing"]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.status["waiting"] = not self.status["waiting"]
                        self.status["playing"] = not self.status["waiting"]

                # Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    x = mouse_x // CELL_SIZE
                    y = mouse_y // CELL_SIZE
                    if 0 <= x < CELL_NUMBER and 0 <= y < CELL_NUMBER:
                        if (self.cells[y][x].next is None and self.cells[y][x].prev is None
                                and self.cells[y][x].point_end is not None):
                            self.point_select = self.cells[y][x]
                            self.current_cell = self.cells[y][x]
                            self.point_select.state = False
                # Release
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    x = mouse_x // CELL_SIZE
                    y = mouse_y // CELL_SIZE
                    if self.point_select and self.point_select.point_end == vec(x, y):
                        self.current_cell.set_active()
                    elif self.current_cell:
                        self.current_cell.reset_all()
                    self.point_select = None
                    self.current_cell = None
                    self.check_win()
                # Move
                if event.type == pygame.MOUSEMOTION and self.point_select is not None:
                    mouse_x, mouse_y = event.pos
                    x = mouse_x // CELL_SIZE
                    y = mouse_y // CELL_SIZE
                    if 0 <= x < CELL_NUMBER and 0 <= y < CELL_NUMBER:
                        if self.cells[y][x].is_empty() and (self.cells[y][x].point_end is None or self.point_select.point_end == vec(x, y)):
                            # Cross the endpoint
                            if self.point_select.point_end == self.current_cell.pos:
                                self.current_cell.set_active()
                                self.point_select = None
                                self.current_cell = None
                                self.check_win()
                            else:
                                self.current_cell.set_next(self.cells[y][x])
                                self.current_cell = self.cells[y][x]
                        # Back
                        elif self.cells[y][x] is self.current_cell.prev:
                            self.current_cell.reset()
                            self.current_cell = self.cells[y][x]
                            self.current_cell.next = None
            if self.status["waiting"]:
                self.waiting_interface.handle_event(event)


if __name__ == "__main__":
    main = Main()
    main.run()
