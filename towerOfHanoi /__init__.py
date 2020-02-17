def move(from_position, target_position):
    print(f'Move disk from {from_position} to {target_position}')


def hanoi(disk_count, from_position, helper_position, target_position):
    if not disk_count:
        return
    hanoi(disk_count - 1, from_position, helper_position, target_position)
    move(from_position, target_position)
    hanoi(disk_count - 1, helper_position, from_position, target_position)


if __name__ == '__main__':
    hanoi(4, "A", "B", "C")
