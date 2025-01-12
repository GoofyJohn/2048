import random

"""
A python version of 2048, a puzzle game where you attempt to make the number 2048 by sliding
powers of 2 around on a 4x4 grid.
This project is meant to show my ability to work with class structures, queues, linked list, 2D arrays
and a little bit of exceptions.
"""


class QueueException(Exception):
    # Custom exception for any errors that could arise from improper use of a queue
    pass


class Node:
    # Basic implementation of a singly-linked node

    def __init__(self, data, next):
        self.data = data  # Value contained in the node (will always be an int for this program)
        self.next = next  # Variable for pointing to the next node of the list

    # Getters and setters

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def get_next(self):
        return self.next

    def set_next(self, next):
        self.next = next


class Queue:
    # Linked list implementation of a queue

    def __init__(self):
        self.head = Node(
            None, None
        )  # Dummy node containing no data for the start of the queue
        self.ptr = self.head  # pointer that points to the end of the queue
        self.size = 0  # Integer to keep track of the size. Size of the queue will never exceed 4 since it never needs to be bigger than that

    def enqueue(self, obj):
        if self.size >= 4:
            # Throws an exception if the max size of the queue is exceeded
            raise QueueException("Queue Overflow: Max size exceeded")
        elif obj is None:
            # Also throws an exception if NoneType data gets added to the queue
            raise QueueException("Data Error: Cannot queue None data")
        else:
            # Adds data to the end of the linked list, updates ptr to point to this new node, and increments the size
            self.ptr.set_next(Node(obj, None))
            self.ptr = self.ptr.get_next()
            self.size += 1

    def dequeue(self):
        if self.size == 0:
            # Throws an exception if the queue is empty
            raise QueueException(
                "Queue Underflow: No items currently in queue"
            )
        else:
            # returnNode points to the first real node of the queue
            returnNode = self.head.get_next()
            if returnNode is None:
                # If there is somehow a case where the size is not 0 but there is not a real node at the start then an exception is thrown
                raise QueueException(
                    "Data Error: Unexpected None node in queue"
                )
            # Data from the start of the queue is found, and the list is updated for it's size to decrease and the all elements of the queue to move up
            returnData = returnNode.get_data()
            self.head.set_next(returnNode.get_next())
            self.size -= 1
            # ptr is also updated if the last element was dequeued
            if self.size == 0:
                self.ptr = self.head
            return returnData

    def combine(self):
        # Method to combine elements to mimic them sliding into to each other to combine
        # Doing combining in the queue saved a lot of headache than doing it directly through the board
        trailer = self.head.get_next()  # Pointer to first element in queue
        if trailer is None:
            # Method will only attempt to run if there are elements in the queue
            return
        while trailer is not None:
            # An additional pointer to the element after the trailer is initialized at each loop
            combine_ptr = trailer.get_next()
            if combine_ptr is None:
                # If the combine_ptr is None than the loop breaks to prevent AttributeErrors
                break
            elif trailer.get_data() == combine_ptr.get_data():
                # If two nodes right next to each other contain the same element, the data in the trailer is doubled
                # and the combine_ptr node is skipped over in the newly adjusted queue
                trailer.set_data(trailer.get_data() * 2)
                trailer.set_next(combine_ptr.get_next())
                trailer = trailer.get_next()
                self.size -= 1
                # Combining is set-up this way to more closely follow 2048. In the game if you have (2, 2, 4) in a row and combine them
                # it won't just go to (8). Rather it will go to (4, 4) and you need to combine again to make (8).
            else:
                # If the two elements are different the trailer iterates to the next element
                trailer = trailer.get_next()
        reset_ptr = self.head.get_next()
        # The ptr member variable is also reset to make sure it is in the proper place for dequeueing and enqueueing
        while reset_ptr.get_next() is not None:
            reset_ptr = reset_ptr.get_next()
        self.ptr = reset_ptr

    def __str__(self):
        # Basic str method set up for debugging purposes
        buildStr = ""
        printPtr = self.head.get_next()
        while printPtr is not None:
            buildStr += (
                str(printPtr.get_data()) + "\n"
            )  # each element of the queue is just added to its own line
            printPtr = printPtr.get_next()
        return buildStr

    def is_empty(self):
        # Boolean method to check if the queue has any elements
        return self.size == 0

    def peek(self):
        # Method that returns the first element of the queue without dequeueing it
        # Never used only implemented to make a fuller queue class
        if self.size == 0:
            # Throws an exception if there are no elements to peek at
            raise QueueException("Queue Undeflow: No items currently in queue")
        else:
            return self.head.get_next().get_data()


class Board:
    # Class for 2048 to be played

    def __init__(self):
        self.board = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
        ]  # 2D List that represents the board the game is played
        self.win_flag = False  # Flag that will get set to true if 2048 is found on the board
        self.lose_flag = False  # Flag that will get set to true if all tiles on the board are filled

    def initialize_board(self):
        # Method for the start of the game that will add two 2s randomly to the board
        two_counter = 0
        while two_counter < 2:
            row_gen = random.randint(0, 3)
            col_gen = random.randint(0, 3)
            if self.board[row_gen][col_gen] != 2:
                # Will only add a 2 to the board if the location is unfilled
                self.board[row_gen][col_gen] = 2
                two_counter += 1

    def add_num(self):
        # Method for adding a number to a number to a random space on the board after each player input
        num_counter = 0
        while num_counter < 1:
            row_gen = random.randint(0, 3)
            col_gen = random.randint(0, 3)
            # Check to make sure location is unfilled
            if self.board[row_gen][col_gen] is None:
                # There is a 1/10 chance of a 4 being added to the board
                num_gen = random.randint(0, 9)
                if num_gen == 9:
                    self.board[row_gen][col_gen] = 4
                    num_counter += 1
                else:
                    self.board[row_gen][col_gen] = 2
                    num_counter += 1

    # Movement methods
    # All push methods are relatively similar they just iterate through the rows and columns in different ways

    def push_up(self):
        for i in range(len(self.board[0])):
            # Outer for loop iterates through each column
            row_counter = 0
            queue = Queue()
            while row_counter < 4:
                # While loop iterates through rows from the top down
                if self.board[row_counter][i] is None:
                    row_counter += 1
                else:
                    # All numbers are added to the queue and removed from the board
                    queue.enqueue(self.board[row_counter][i])
                    self.board[row_counter][i] = None
                    row_counter += 1
            # All elements that can be combined are
            queue.combine()
            row_placer = 0
            while not queue.is_empty():
                # Newly combined elements are added back to the board from the top down
                self.board[row_placer][i] = queue.dequeue()
                row_placer += 1

    def push_down(self):
        for i in range(len(self.board[0])):
            # Same as the push up function but iterates from the bottom row to the top
            row_counter = 3
            queue = Queue()
            while row_counter > -1:
                if self.board[row_counter][i] is None:
                    row_counter -= 1
                else:
                    queue.enqueue(self.board[row_counter][i])
                    self.board[row_counter][i] = None
                    row_counter -= 1
            queue.combine()
            row_placer = 3
            while not queue.is_empty():
                self.board[row_placer][i] = queue.dequeue()
                row_placer -= 1

    def push_left(self):
        # Outer for loop will iterate through each row
        for i in range(len(self.board)):
            col_counter = 0
            queue = Queue()
            while col_counter < 4:
                # While loop iterates through columns
                if self.board[i][col_counter] is None:
                    col_counter += 1
                else:
                    # Numbers are added to the queue and removed from the board
                    queue.enqueue(self.board[i][col_counter])
                    self.board[i][col_counter] = None
                    col_counter += 1
            # Elements are combined
            queue.combine()
            col_placer = 0
            while not queue.is_empty():
                # Newly combined elements are added from left to right in each row
                self.board[i][col_placer] = queue.dequeue()
                col_placer += 1

    def push_right(self):
        # Same as the push up function but ierates from right to left
        for i in range(len(self.board)):
            col_counter = 3
            queue = Queue()
            while col_counter > -1:
                if self.board[i][col_counter] is None:
                    col_counter -= 1
                else:
                    queue.enqueue(self.board[i][col_counter])
                    self.board[i][col_counter] = None
                    col_counter -= 1
            queue.combine()
            col_placer = 3
            while not queue.is_empty():
                self.board[i][col_placer] = queue.dequeue()
                col_placer -= 1

    def __str__(self):
        # The string method for the board object makes the 4x4 array but represents each number in a different color
        buildString = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                value = self.board[i][j]
                if value is None:
                    buildString += "  -  "
                elif value == 2:
                    buildString += "\033[0;31m" + "  2  " + "\033[0m"
                elif value == 4:
                    buildString += "\033[0;32m" + "  4  " + "\033[0m"
                elif value == 8:
                    buildString += "\033[0;34m" + "  8  " + "\033[0m"
                elif value == 16:
                    buildString += "\033[0;35m" + " 16  " + "\033[0m"
                elif value == 32:
                    buildString += "\033[0;36m" + " 32  " + "\033[0m"
                elif value == 64:
                    buildString += "\033[1;31m" + " 64  " + "\033[0m"
                elif value == 128:
                    buildString += "\033[1;32m" + " 128 " + "\033[0m"
                elif value == 256:
                    buildString += " 256 "
                elif value == 512:
                    buildString += "\033[1;34m" + " 512 " + "\033[0m"
                elif value == 1024:
                    buildString += "\033[1;35m" + "1024 " + "\033[0m"
                elif value == 2048:
                    buildString += "\033[1;33m" + "2048 " + "\033[0m"
            buildString += "\n\n"
        return buildString

    def game_over(self):
        # Iterates through each element of the 2D array to look for how many spaces are occupied or 2048
        num_counter = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 2048:
                    # If 2048 is found then the player won the game
                    self.win_flag = True
                elif self.board[i][j] is not None and self.board[i][j] != 2048:
                    num_counter += 1
        if num_counter == 16:
            # If there are 16 occupied spaces on the board then the player lost
            self.lose_flag = True
        return self.win_flag or self.lose_flag

    # Getters to find if the player won or lost the game
    
    def get_lose_flag(self):
        return self.lose_flag

    def get_win_flag(self):
        return self.win_flag


if __name__ == "__main__":
    # Board and turn counter are instantiated
    board = Board()
    turn_counter = 1
    print("Welcome to 2048!")
    print(
        "The goal of this game is to combine numbers to make 2048 by sliding tiles on the board."
    )
    board.initialize_board()
    # Loop will only iterate until the player wins or loses
    while not board.game_over():
        print()
        print(f"Turn {turn_counter}")
        print(board)
        # Player gives a direction of left, right, up or down
        print("Choose a direction (U, D, L, or R).")
        direction = input()
        direction.strip()
        # If the direction the player input does not properly match one of those, then they re-enter a direction
        # until it is correct
        while (
            direction != "U"
            and direction != "D"
            and direction != "L"
            and direction != "R"
        ):
            print("Invalid direction typed. Please try again (U, D, L, or R).")
            direction = input()
            direction.strip()
        # The numbers on the board will then be pushed the selected direction using the push methods
        if direction == "U":
            board.push_up()
        elif direction == "D":
            board.push_down()
        elif direction == "L":
            board.push_left()
        else:
            board.push_right()
        board.add_num()
        turn_counter += 1
    print(board)
    # A message is given corresponding to if the player won or lost
    if board.get_lose_flag():
        print("You lose!")
    elif board.get_win_flag():
        print("You win!")
