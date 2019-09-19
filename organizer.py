import json
import sys

x = 0
y = 1


def tolerant_x_sort(points, error_margin):
    less = []
    equal = []
    greater = []

    if len(points) > 1:
        pivot = points[0][x]

        for element in points:
            if element[x] - error_margin < pivot < element[x] + error_margin:
                equal.append(element)
            elif element[x] < pivot:
                less.append(element)
            elif element[x] > pivot:
                greater.append(element)
        return tolerant_x_sort(less, error_margin) + equal + tolerant_x_sort(greater, error_margin)  # Just use the + operator to join lists
    else:
        return points


def sort_points(unsorted_points):
    half_sorted_points = sorted(unsorted_points, key=lambda a: a[y])
    x_list = [dot[x] for dot in unsorted_points]
    lower_bound = min(x_list)
    upper_bound = max(x_list)
    width = upper_bound - lower_bound
    error_margin = width / 256
    sorted_points = tolerant_x_sort(half_sorted_points, error_margin)
    return sorted_points


class Organizer:
    def __init__(self, template_points_path):
        with open(template_points_path) as f:
            unsorted_points = json.load(f)['corners']
            self.template_points = sort_points(unsorted_points)
        out = {'corners': self.template_points}
        with open(template_points_path, 'w+') as f:
            f.write(json.dumps(out))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: python organizer.py [template_points_path]')
        exit()
    template_points = sys.argv[1]
    Organizer(template_points)

